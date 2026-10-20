#!/usr/bin/env python3
"""Restore a spoken-voice clip: de-click, de-plosive, de-noise, de-ess, level.

Pure numpy (no scipy). Decodes any ffmpeg-readable input to 48 kHz mono float,
runs a staged DSP chain, writes 24-bit WAV, and optionally finalises loudness
with ffmpeg's two-pass loudnorm.

Why this exists: OmniVoice / VoxCPM2 are synthesis + cloning engines. They
cannot repair a recording. A clone reference that still contains plosives and
mouth sounds teaches the model those artifacts, so the reference must be
cleaned *before* it is cloned. This tool produces that reference.

Chain (each stage can be switched off):

  hp         DC removal + 70 Hz high-pass (handling rumble)
  declick    strict sample-level removal of isolated ticks
  transient  spectral transient suppressor:
               - plosive bursts  (P / B / T / K): low-band dominant transients
               - mouth sounds    (lip smacks): noise-like transients below
                                  the speech level
  denoise    spectral gating against a noise profile estimated from the
             quietest frames (the gaps), which is where the room noise and
             the mouth sounds actually live
  deess      dynamic gain reduction in the sibilance band
  comp       gentle level control
  norm       loudness normalisation (ffmpeg loudnorm, two-pass)

Usage
-----
  python restore-voice-clip.py IN.m4a -o OUT.wav
  python restore-voice-clip.py IN.m4a --analyze
  python restore-voice-clip.py IN.m4a -o OUT.wav --lufs -16 --mp3
  python restore-voice-clip.py IN.m4a -o OUT.wav --stages hp,denoise
  python restore-voice-clip.py IN.m4a --spectrogram spec.png
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

SR = 48000
N_FFT = 2048
HOP = 512
T_NFFT = 1024      # transient stage: short window, fine time resolution
T_HOP = 128


# --------------------------------------------------------------------------
# io
# --------------------------------------------------------------------------
def decode(path: Path, sr: int = SR) -> np.ndarray:
    """Decode any input to mono float32 at `sr` via ffmpeg."""
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error",
        "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(sr), "-",
    ]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg decode failed: {res.stderr.decode(errors='replace')}")
    x = np.frombuffer(res.stdout, dtype=np.float32).astype(np.float64)
    if x.size == 0:
        raise RuntimeError("decoded 0 samples")
    return x


def _u32(v: int) -> bytes:
    return int(v).to_bytes(4, "little", signed=False)


def _u16(v: int) -> bytes:
    return int(v).to_bytes(2, "little", signed=False)


def write_wav(path: Path, x: np.ndarray, sr: int = SR, bits: int = 24) -> None:
    """Write mono PCM WAV (16 or 24 bit)."""
    payload = np.clip(x, -1.0, 1.0)
    if bits == 16:
        data = (payload * 32767.0).astype("<i2").tobytes()
        bitsval = 16
    elif bits == 24:
        ints = np.round(payload * 8388607.0).astype(np.int32)
        buf = bytearray(3 * len(ints))
        for i in range(len(ints)):
            v = ints[i]
            buf[i * 3] = v & 0xFF
            buf[i * 3 + 1] = (v >> 8) & 0xFF
            buf[i * 3 + 2] = (v >> 16) & 0xFF
        data = bytes(buf)
        bitsval = 24
    else:
        raise ValueError("bits must be 16 or 24")
    block = bitsval // 8
    hdr = b"RIFF" + _u32(36 + len(data)) + b"WAVEfmt "
    hdr += _u32(16) + _u16(1) + _u16(1) + _u32(sr)
    hdr += _u32(sr * block) + _u16(block) + _u16(bitsval)
    hdr += b"data" + _u32(len(data))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(hdr + data)


def write_mp3(path: Path, wav: Path, bitrate: str = "192k") -> None:
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav),
        "-codec:a", "libmp3lame", "-b:a", bitrate, str(path),
    ]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0:
        raise RuntimeError(f"mp3 encode failed: {res.stderr.decode(errors='replace')}")


def ffmpeg_loudness(path: Path) -> dict:
    """Integrated LUFS / true peak / LRA via ffmpeg ebur128."""
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-filter_complex", "ebur128=peak=true", "-f", "null", "-",
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="replace")
    summary = res.stderr.split("Summary:")[-1]
    vals = {}
    for key, name in (
        ("I:", "integrated_lufs"),
        ("LRA:", "lra"),
        ("Peak:", "true_peak_dbfs"),
    ):
        for line in summary.splitlines():
            if key in line:
                try:
                    vals[name] = float(line.split(key)[1].split()[0])
                except (IndexError, ValueError):
                    pass
    return vals


# --------------------------------------------------------------------------
# dsp helpers
# --------------------------------------------------------------------------
def stft(x: np.ndarray, n_fft: int = N_FFT, hop: int = HOP):
    win = np.hanning(n_fft + 1)[:-1]
    pad = n_fft
    xp = np.pad(x, (pad, pad), mode="reflect")
    n_frames = 1 + (len(xp) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + hop * np.arange(n_frames)[:, None]
    frames = xp[idx] * win
    return np.fft.rfft(frames, axis=1), win, n_fft, hop


def istft(X: np.ndarray, win: np.ndarray, n_fft: int, hop: int, length: int) -> np.ndarray:
    frames = np.fft.irfft(X, n=n_fft, axis=1)
    n_frames = frames.shape[0]
    out = np.zeros((n_frames - 1) * hop + n_fft)
    wsum = np.zeros_like(out)
    w2 = win ** 2
    for i in range(n_frames):
        s = i * hop
        out[s:s + n_fft] += frames[i] * win
        wsum[s:s + n_fft] += w2
    out = out / np.maximum(wsum, 1e-8)
    pad = n_fft
    return out[pad:pad + length]


def sliding_median(x: np.ndarray, w: int) -> np.ndarray:
    if w < 3:
        return x.copy()
    pad = w // 2
    xp = np.pad(x, (pad, pad), mode="reflect")
    view = np.lib.stride_tricks.sliding_window_view(xp, w)
    return np.median(view, axis=1)


def median_filter_1d(x: np.ndarray, w: int) -> np.ndarray:
    """Median filter with edge padding (w in samples)."""
    if w < 3:
        return x.copy()
    pad = w // 2
    xp = np.pad(x, (pad, pad), mode="edge")
    view = np.lib.stride_tricks.sliding_window_view(xp, w)
    return np.median(view, axis=1)


def moving_average(x: np.ndarray, w: int) -> np.ndarray:
    if w < 2:
        return x.copy()
    return np.convolve(x, np.ones(w) / w, mode="same")


def smooth_envelope(e: np.ndarray, win: int) -> np.ndarray:
    return moving_average(e, win) if win >= 2 else e


def rms_db(x: np.ndarray) -> float:
    if x.size == 0:
        return -120.0
    r = float(np.sqrt(np.mean(x ** 2)))
    return 20 * math.log10(r) if r > 1e-12 else -120.0


def count_runs(mask: np.ndarray, hop: int = 1, sr: int = SR,
               min_ms: float = 0.0) -> int:
    """Count contiguous True runs (events), not frames."""
    idx = np.flatnonzero(mask)
    if idx.size == 0:
        return 0
    breaks = int(np.sum(np.diff(idx) > 1))
    min_gap = max(1, int(min_ms / 1000.0 * sr / hop))
    if min_gap > 1:
        # merge runs separated by less than min_gap
        merged = 1
        prev_end = idx[0]
        for i in idx[1:]:
            if i - prev_end > min_gap:
                merged += 1
            prev_end = i
        return merged
    return breaks + 1


def time_smooth_gain(g: np.ndarray, sr: int, attack_ms: float,
                     release_ms: float) -> np.ndarray:
    """Smooth a gain curve with an asymmetric attack/release envelope."""
    a = math.exp(-1.0 / max(1.0, sr * attack_ms / 1000.0))
    r = math.exp(-1.0 / max(1.0, sr * release_ms / 1000.0))
    out = np.empty_like(g)
    prev = 1.0
    for i, v in enumerate(g):
        if v < prev:
            prev = a * prev + (1 - a) * v
        else:
            prev = r * prev + (1 - r) * v
        out[i] = prev
    return out


# --------------------------------------------------------------------------
# stages
# --------------------------------------------------------------------------
def stage_hp(x: np.ndarray, sr: int, hz: float = 70.0, q: float = 0.707) -> np.ndarray:
    """DC removal + 2nd-order high-pass (RBJ biquad)."""
    x = x - float(np.mean(x))
    w0 = 2 * math.pi * hz / sr
    alpha = math.sin(w0) / (2 * q)
    b0 = (1 + math.cos(w0)) / 2
    b1 = -(1 + math.cos(w0))
    b2 = (1 + math.cos(w0)) / 2
    a0 = 1 + alpha
    a1 = -2 * math.cos(w0)
    a2 = 1 - alpha
    b = np.array([b0, b1, b2]) / a0
    a1n, a2n = a1 / a0, a2 / a0
    y = np.empty_like(x)
    x1 = x2 = y1 = y2 = 0.0
    for i, xn in enumerate(x):
        yn = b[0] * xn + b[1] * x1 + b[2] * x2 - a1n * y1 - a2n * y2
        y[i] = yn
        x2, x1 = x1, xn
        y2, y1 = y1, yn
    return y


def stage_declick(x: np.ndarray, sr: int, k: float = 12.0, w: int = 5,
                  min_rel: float = 0.02) -> tuple[np.ndarray, int]:
    """Strict removal of isolated impulsive ticks.

    A sample is only a tick when it deviates from the local median by more
    than `k` times the *local* residual scale AND by more than `min_rel` of
    the signal peak. The relative floor is what keeps this from firing on
    ordinary consonants, which also spike away from their local median.
    """
    med = sliding_median(x, w)
    r = x - med
    absr = np.abs(r)
    scale_win = max(3, int(sr * 0.030))
    local = np.maximum(smooth_envelope(absr, scale_win), 1e-5)
    peak = float(np.max(np.abs(x))) if x.size else 1.0
    flags = (absr > k * local) & (absr > min_rel * peak)
    if not flags.any():
        return x, 0
    out = x.copy()
    idx = np.flatnonzero(flags)
    spans = []
    start = prev = idx[0]
    for i in idx[1:]:
        if i == prev + 1:
            prev = i
            continue
        spans.append((start, prev))
        start = prev = i
    spans.append((start, prev))
    for (s, e) in spans:
        out[s:e + 1] = med[s:e + 1]
        a, b = max(0, s - 4), min(len(x) - 1, e + 4)
        if a > 0 and b < len(x) - 1:
            n = e - s + 1
            t = (np.arange(n) + 1) / (n + 1)
            ramp = x[a - 1] + (x[b + 1] - x[a - 1]) * t
            out[s:e + 1] = out[s:e + 1] * (1 - t) + ramp * t
    return out, int(flags.sum())


def stage_transient(x: np.ndarray, sr: int,
                    plosive_db: float = -11.0, plosive_high_db: float = -5.0,
                    mouth_db: float = -16.0,
                    plosive_over: float = 7.0, mouth_over: float = 4.0,
                    quiet_under: float = 6.0) -> tuple[np.ndarray, dict]:
    """Spectral transient suppressor.

    Two different artefacts share the word "pop" and need different treatment:

    * **Plosive bursts** (P / B / T / K) are loud, short and low-band dominant
      (the lip blast is a 60-300 Hz thump). They are tamed with a deep gain
      cut in the low band and a light one above it, so the consonant survives.
    * **Mouth sounds** (lip smacks, wet clicks) are quiet, short and noise-like.
      They sit *below* the speech level, so restricting the detector to that
      region removes them without touching real consonants, which are loud.

    Both are found by comparing each frame's energy with the local median
    energy around it, which is what distinguishes a transient from a vowel.
    """
    X, win, n_fft, hop = stft(x, T_NFFT, T_HOP)
    mag = np.abs(X)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    n_frames = mag.shape[0]
    if n_frames < 8:
        return x, {"plosive_frames": 0, "mouth_frames": 0}

    energy = np.sum(mag ** 2, axis=1)
    energy_db = 10 * np.log10(energy + 1e-12)
    # local median energy (+/- 250 ms) -> the sustained-speech reference
    w_local = max(3, int(0.25 * sr / hop))
    local_med = median_filter_1d(energy_db, w_local)
    # 90th percentile frame energy ~ the level of loud speech
    speech_db = float(np.percentile(energy_db, 90))

    # spectral flatness: 1.0 = white noise, low = tonal
    logm = np.log(mag + 1e-10)
    flatness = np.exp(np.mean(logm, axis=1)) / (np.mean(mag, axis=1) + 1e-12)

    low_mask = freqs < 500
    tot = np.sum(mag ** 2, axis=1) + 1e-12
    low_ratio = np.sum(mag[:, low_mask] ** 2, axis=1) / tot

    over = energy_db - local_med
    is_transient = over > 3.0

    plosive = is_transient & (over > plosive_over) & (low_ratio > 0.45) & (energy_db > speech_db - 3.0)
    mouth = is_transient & (over > mouth_over) & (flatness > 0.12) & (energy_db < speech_db - quiet_under)

    # build the gain curve per band
    g_low = np.ones(n_frames)
    g_high = np.ones(n_frames)
    if plosive.any():
        g_low[plosive] = 10 ** (plosive_db / 20.0)
        g_high[plosive] = 10 ** (plosive_high_db / 20.0)
    if mouth.any():
        g_low[mouth] = np.minimum(g_low[mouth], 10 ** (mouth_db / 20.0))
        g_high[mouth] = np.minimum(g_high[mouth], 10 ** (mouth_db / 20.0))

    # smooth in time so gain changes never click (fast attack, slower release)
    sr_frame = sr / hop
    g_low = time_smooth_gain(g_low, sr_frame, 1.0, 25.0)
    g_high = time_smooth_gain(g_high, sr_frame, 1.0, 25.0)

    Y = X.copy()
    Y[:, low_mask] = X[:, low_mask] * g_low[:, None]
    Y[:, ~low_mask] = X[:, ~low_mask] * g_high[:, None]
    out = istft(Y, win, n_fft, hop, len(x))
    stats = {
        "plosive_frames": int(plosive.sum()),
        "mouth_frames": int(mouth.sum()),
        "plosive_low_cut_db": plosive_db,
        "mouth_cut_db": mouth_db,
    }
    return out, stats


def estimate_noise_profile(mag: np.ndarray, energy_db: np.ndarray,
                           pct: float = 15.0) -> np.ndarray:
    """Per-bin noise magnitude taken from the quietest frames.

    Taking a percentile across *all* frames conflates speech with noise; the
    room noise and the mouth sounds are best seen in the gaps, so the profile
    comes from the quietest `pct` of frames.
    """
    quiet = energy_db <= np.percentile(energy_db, pct)
    if quiet.sum() < 2:
        quiet = energy_db <= np.percentile(energy_db, 50)
    return np.sqrt(np.mean(mag[quiet] ** 2, axis=0)) + 1e-8


def stage_denoise(x: np.ndarray, sr: int, strength: float = 1.0,
                  floor_db: float = -72.0, quiet_pct: float = 15.0,
                  expander_db: float = -9.0) -> tuple[np.ndarray, dict]:
    """Spectral gating against a gap-derived noise profile, plus a soft
    expander so the gaps go quiet instead of hissing."""
    X, win, n_fft, hop = stft(x)
    mag = np.abs(X)
    energy_db = 10 * np.log10(np.sum(mag ** 2, axis=1) + 1e-12)
    noise = estimate_noise_profile(mag, energy_db, quiet_pct)
    snr = mag / noise
    floor_lin = 10 ** (floor_db / 20.0)
    gain = np.clip((snr ** 2 - 1.0) / np.maximum(snr ** 2, 1e-9), 0.0, 1.0)
    gain = gain * (1.0 - floor_lin) + floor_lin
    gain = np.clip(gain, floor_lin, 1.0)
    # widen the gain over time so it does not chatter
    k = 5
    pad = k // 2
    gp = np.pad(gain, ((pad, pad), (0, 0)), mode="edge")
    gain_s = np.apply_along_axis(lambda v: np.convolve(v, np.ones(k) / k, mode="valid"), 0, gp)
    gain_s = np.clip(gain_s, floor_lin, 1.0)
    strength = float(np.clip(strength, 0, 1))
    gain_mix = 1.0 - strength + strength * gain_s

    # soft expander on the frame level: quiet frames get pushed further down
    speech_db = float(np.percentile(energy_db, 90))
    below = energy_db < (speech_db - 28.0)
    if below.any() and expander_db < 0:
        extra = np.ones(len(gain_mix))
        extra[below] = 10 ** (expander_db / 20.0)
        # taper the extra gain in over ~30 ms
        extra = time_smooth_gain(extra, sr / hop, 1.0, 30.0)
        gain_mix = gain_mix * extra[:, None]

    out = istft(X * gain_mix, win, n_fft, hop, len(x))
    stats = {
        "noise_profile_db": round(float(20 * math.log10(np.median(noise) + 1e-12)), 2),
        "mean_gain_db": round(float(20 * math.log10(np.mean(gain_mix) + 1e-12)), 2),
        "attenuated_frames": int((gain_mix < 0.7).sum()),
        "total_frames": int(len(gain_mix)),
    }
    return out, stats


def stage_deess(x: np.ndarray, sr: int, lo: float = 3800.0, hi: float = 9000.0,
                thresh_db: float = -24.0, amount_db: float = -7.0) -> tuple[np.ndarray, int]:
    """Dynamic gain reduction in the sibilance band."""
    X, win, n_fft, hop = stft(x)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    mag = np.abs(X)
    band = (freqs >= lo) & (freqs <= hi)
    out_band = mag * band
    broad = np.sqrt(np.sum(mag ** 2, axis=1)) + 1e-12
    band_level = np.sqrt(np.sum(out_band ** 2, axis=1))
    rel = 20 * np.log10(band_level / broad)
    over = rel - thresh_db
    red = np.zeros_like(rel)
    active = over > 0
    red[active] = -amount_db * np.clip(over[active] / 6.0, 0, 1)
    red = moving_average(red, 7)
    gain = 10 ** (red / 20.0)
    Y = X.copy()
    Y[:, band] = X[:, band] * gain[:, None]
    out = istft(Y, win, n_fft, hop, len(x))
    return out, int(active.sum())


def stage_comp(x: np.ndarray, sr: int, threshold_db: float = -20.0,
               ratio: float = 3.0, attack: float = 0.005, release: float = 0.120) -> np.ndarray:
    """Soft-knee compressor on the broadband envelope."""
    env = smooth_envelope(np.abs(x), int(sr * 0.010))
    th = 10 ** (threshold_db / 20.0)
    gain = np.ones_like(env)
    over = env > th
    gain[over] = (th / env[over]) ** (1.0 - 1.0 / ratio)
    g = time_smooth_gain(gain, sr, attack * 1000, release * 1000)
    return x * g


def trim_silence(x: np.ndarray, sr: int, thresh_db: float = -45.0,
                 pad_ms: int = 60) -> tuple[np.ndarray, int, int]:
    """Trim leading/trailing silence, keeping a small pad."""
    env = smooth_envelope(np.abs(x), int(sr * 0.010))
    thr = 10 ** (thresh_db / 20.0)
    voiced = np.flatnonzero(env > thr)
    if voiced.size == 0:
        return x, 0, len(x)
    pad = int(sr * pad_ms / 1000)
    s = max(0, int(voiced[0]) - pad)
    e = min(len(x), int(voiced[-1]) + pad)
    return x[s:e], s, e


# --------------------------------------------------------------------------
# metrics
# --------------------------------------------------------------------------
def measure(x: np.ndarray, sr: int = SR) -> dict:
    """Objective measures used to prove the chain did something."""
    peak = float(np.max(np.abs(x))) if x.size else 0.0
    peak_db = 20 * math.log10(peak) if peak > 1e-9 else -120.0
    win = int(sr * 0.3)
    best = 999.0
    if len(x) > win:
        step = max(1, win // 4)
        for s in range(0, len(x) - win, step):
            r = rms_db(x[s:s + win])
            if r < best:
                best = r
    noise_db = best if best > -900 else -120.0

    X, win2, n_fft, hop = stft(x)
    mag = np.abs(X)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    energy_db = 10 * np.log10(np.sum(mag ** 2, axis=1) + 1e-12)
    w_local = max(3, int(0.25 * sr / hop))
    local_med = median_filter_1d(energy_db, w_local)
    speech_db = float(np.percentile(energy_db, 90))
    low_mask = freqs < 500
    tot = np.sum(mag ** 2, axis=1) + 1e-12
    low_ratio = np.sum(mag[:, low_mask] ** 2, axis=1) / tot
    over = energy_db - local_med
    plosive = (over > 7.0) & (low_ratio > 0.45) & (energy_db > speech_db - 3.0)
    logm = np.log(mag + 1e-10)
    flatness = np.exp(np.mean(logm, axis=1)) / (np.mean(mag, axis=1) + 1e-12)
    mouth = (over > 4.0) & (flatness > 0.12) & (energy_db < speech_db - 6.0)
    hiss_e = float(np.sum(mag[:, freqs >= 8000] ** 2))
    all_e = float(np.sum(mag ** 2))
    return {
        "duration_s": round(len(x) / sr, 3),
        "peak_dbfs": round(peak_db, 2),
        "rms_dbfs": round(rms_db(x), 2),
        "noise_floor_dbfs": round(noise_db, 2),
        "snr_db": round(rms_db(x) - noise_db, 2),
        "plosive_events": count_runs(plosive, hop, sr, 30.0),
        "plosive_frames": int(plosive.sum()),
        "mouth_events": count_runs(mouth, hop, sr, 30.0),
        "mouth_frames": int(mouth.sum()),
        "hiss_pct_over_8k": round(100.0 * hiss_e / max(all_e, 1e-12), 2),
    }


def analyze(path: Path) -> dict:
    x = decode(path)
    m = measure(x)
    m["file"] = str(path)
    m["dc_offset"] = round(float(np.mean(x)), 6)
    m["clipped_samples"] = int(np.sum(np.abs(x) > 0.999))
    m.update(ffmpeg_loudness(path))
    return m


def spectrogram(path: Path, out_png: Path, sr: int = SR) -> Path:
    """Render a dB spectrogram so pops and noise bands are visible, not guessed."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    x = decode(path, sr)
    X, win, n_fft, hop = stft(x)
    mag = np.abs(X)
    db = 20 * np.log10(mag + 1e-10)
    freqs = np.fft.rfftfreq(n_fft, 1.0 / sr)
    times = np.arange(mag.shape[0]) * hop / sr
    top = min(8000, sr / 2)
    sel = freqs <= top
    fig, ax = plt.subplots(figsize=(14, 5))
    im = ax.pcolormesh(times, freqs[sel], db[:, sel].T, shading="auto",
                        cmap="magma", vmin=np.percentile(db, 5), vmax=np.percentile(db, 99.5))
    ax.set_ylim(0, top)
    ax.set_xlabel("seconds")
    ax.set_ylabel("Hz")
    ax.set_title(f"{path.name} — spectral content (dB)")
    fig.colorbar(im, ax=ax, label="dB")
    fig.tight_layout()
    out_png.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_png, dpi=110)
    plt.close(fig)
    return out_png


# --------------------------------------------------------------------------
# driver
# --------------------------------------------------------------------------
def normalize_static(wav: Path, target_lufs: float, tp_db: float = -1.5) -> dict:
    """Loudness-normalise with a static gain plus a look-ahead limiter.

    ffmpeg's `loudnorm` is the obvious tool, but in dynamic mode it resamples
    to 192 kHz and adds a 3-second look-ahead delay, which inflates the file
    and shifts every clip. These clips have a low loudness range already, so a
    measured static gain plus a limiter is both exact and delay-free.
    """
    before = ffmpeg_loudness(wav)
    measured = before.get("integrated_lufs")
    if measured is None or measured < -70:
        return {"normalised": False, "reason": "no measurable loudness"}
    gain = target_lufs - measured
    tmp = wav.with_suffix(".norm.wav")
    cmd = [
        "ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav),
        "-af", f"volume={gain:.3f}dB,alimiter=limit={tp_db}dB:attack=5:release=50:level=disabled",
        "-ar", str(SR), "-c:a", "pcm_s24le", str(tmp),
    ]
    res = subprocess.run(cmd, capture_output=True)
    if res.returncode != 0 or not tmp.exists() or tmp.stat().st_size == 0:
        return {"normalised": False, "reason": res.stderr.decode(errors="replace")[:200]}
    tmp.replace(wav)
    return {
        "normalised": True,
        "gain_db": round(gain, 2),
        "measured_lufs": measured,
        "target_lufs": target_lufs,
        "true_peak_dbfs": ffmpeg_loudness(wav).get("true_peak_dbfs"),
    }


def restore(path: Path, out: Path, *, stages: list[str], lufs: float | None,
            strength: float = 1.0, deess_db: float = -7.0, mp3: bool = False,
            trim: bool = True, bits: int = 24, floor_db: float = -72.0,
            expander_db: float = -9.0,
            out_spectrogram: Path | None = None) -> dict:
    x = decode(path)
    report = {"input": str(path), "stages": stages, "before": measure(x)}
    if "hp" in stages:
        x = stage_hp(x, SR, hz=70.0)
    if "declick" in stages:
        x, n = stage_declick(x, SR)
        report["declick_samples"] = n
    if "transient" in stages:
        x, st = stage_transient(x, SR)
        report.update(st)
    if "denoise" in stages:
        x, st = stage_denoise(x, SR, strength=strength, floor_db=floor_db,
                               expander_db=expander_db)
        report.update(st)
    if "deess" in stages:
        x, hits = stage_deess(x, SR, amount_db=deess_db)
        report["deess_frames"] = hits
    if "comp" in stages:
        x = stage_comp(x, SR)
    if trim:
        x, s, e = trim_silence(x, SR)
        report["trim_s"] = round(s / SR, 3)
        report["trim_e_s"] = round(e / SR, 3)

    out.parent.mkdir(parents=True, exist_ok=True)
    write_wav(out, x, bits=bits)

    if lufs is not None and lufs > -70:
        report.update(normalize_static(out, lufs))

    report["after"] = measure(decode(out))
    report["final_loudness"] = ffmpeg_loudness(out)
    if mp3:
        write_mp3(out.with_suffix(".mp3"), out)
        report["mp3"] = str(out.with_suffix(".mp3"))
    if out_spectrogram:
        spectrogram(out, out_spectrogram)
        report["out_spectrogram"] = str(out_spectrogram)
    return report


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", type=Path)
    ap.add_argument("-o", "--output", type=Path)
    ap.add_argument("--analyze", action="store_true")
    ap.add_argument("--lufs", type=float, default=-16.0, help="target integrated LUFS (use -100 to skip)")
    ap.add_argument("--stages", default="hp,declick,transient,denoise,deess,comp")
    ap.add_argument("--denoise-strength", type=float, default=1.0)
    ap.add_argument("--floor-db", type=float, default=-72.0,
                    help="spectral gate floor (dB) - lower = more aggressive")
    ap.add_argument("--expander-db", type=float, default=-9.0,
                    help="extra gain applied to frames below the speech floor")
    ap.add_argument("--deess-db", type=float, default=-7.0)
    ap.add_argument("--mp3", action="store_true")
    ap.add_argument("--no-trim", action="store_true")
    ap.add_argument("--bits", type=int, default=24, choices=[16, 24])
    ap.add_argument("--spectrogram", type=Path, help="also write a dB spectrogram PNG of the INPUT")
    ap.add_argument("--out-spectrogram", type=Path, help="write a dB spectrogram PNG of the OUTPUT")
    args = ap.parse_args(argv)

    if args.spectrogram:
        spectrogram(args.input, args.spectrogram)
        print(f"spectrogram: {args.spectrogram}")
    if args.analyze:
        print(json.dumps(analyze(args.input), indent=2))
        return 0
    if args.output is None:
        ap.error("--output is required unless --analyze")
    stages = [s.strip() for s in args.stages.split(",") if s.strip()]
    rep = restore(args.input, args.output,
                  stages=stages,
                  lufs=args.lufs if args.lufs > -70 else None,
                  strength=args.denoise_strength,
                  deess_db=args.deess_db,
                  floor_db=args.floor_db,
                  expander_db=args.expander_db,
                  mp3=args.mp3,
                  trim=not args.no_trim,
                  bits=args.bits,
                  out_spectrogram=args.out_spectrogram)
    print(json.dumps(rep, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
