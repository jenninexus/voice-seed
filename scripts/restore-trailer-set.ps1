param(
  [string]$SourceDir = "C:\Github\game-dev\games\Dress-Up\Jenni-Styles\Art\audio\trailer",
  [string]$OutDir   = "C:\Github\game-dev\games\Dress-Up\Jenni-Styles\Art\audio\omni",
  [string]$Tool     = "C:\Github\voice-seed\scripts\restore-voice-clip.py",
  [string]$Levels   = "popfix,clean,studio",
  [string]$Only     = ""
)

$ErrorActionPreference = "Continue"
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

# Three levels of processing. The point is that "cleaned" is a dial, not a
# switch: the owner picks the amount that sounds right, and that choice is
# what the clone reference is built from.
$recipes = @{
  "raw" = @{
    # Level-matched but otherwise untouched: the honest baseline, because it
    # isolates what the processing did from the loudness change.
    stages = ""
    extra  = @("--denoise-strength", "0")
  }
  "popfix" = @{
    stages = "hp,declick,transient,deess,comp"
    extra  = @("--denoise-strength", "0")
  }
  "clean" = @{
    stages = "hp,declick,transient,denoise,deess,comp"
    extra  = @("--denoise-strength", "0.85", "--floor-db", "-72", "--expander-db", "-9")
  }
  "studio" = @{
    stages = "hp,declick,transient,denoise,deess,comp"
    extra  = @("--denoise-strength", "1", "--floor-db", "-78", "--expander-db", "-14")
  }
}

$files = Get-ChildItem -LiteralPath $SourceDir -Filter *.m4a | Sort-Object Name
if ($Only) { $files = $files | Where-Object { $Only -split ',' -contains $_.BaseName } }

$summary = @()
foreach ($f in $files) {
  # The untouched original, transcoded only, so the page can play it and the
  # first thing the listener hears is exactly what was recorded.
  & ffmpeg -hide_banner -loglevel error -y -i $f.FullName -codec:a libmp3lame -b:a 192k (Join-Path $OutDir ("{0}.original.mp3" -f $f.BaseName))
  foreach ($lvl in $Levels -split ',') {
    if (-not $recipes.ContainsKey($lvl)) { continue }
    $r = $recipes[$lvl]
    $wav = Join-Path $OutDir ("{0}.{1}.wav" -f $f.BaseName, $lvl)
    $args = @($Tool, $f.FullName, "-o", $wav, "--stages", $r.stages, "--lufs", "-16") + $r.extra
    $json = & python @args 2>$null | Out-String
    try {
        $rep = $json | ConvertFrom-Json
        $summary += [pscustomobject]@{
          Clip   = $f.BaseName
          Level  = $lvl
          SNRbefore = $rep.before.snr_db
          SNRafter  = $rep.after.snr_db
          FloorBefore = $rep.before.noise_floor_dbfs
          FloorAfter  = $rep.after.noise_floor_dbfs
          Plosives    = "$($rep.before.plosive_events) -> $($rep.after.plosive_events)"
          LUFS   = $rep.final_loudness.integrated_lufs
          TP     = $rep.final_loudness.true_peak_dbfs
          Dur    = $rep.after.duration_s
        }
    } catch {
      Write-Warning ("FAILED {0} {1}: {2}" -f $f.BaseName, $lvl, $json)
    }
  }
}

# mp3 mirrors for the preview page (small, and every browser plays them)
Get-ChildItem -LiteralPath $OutDir -Filter *.wav | ForEach-Object {
  $mp3 = [IO.Path]::ChangeExtension($_.FullName, ".mp3")
  & ffmpeg -hide_banner -loglevel error -y -i $_.FullName -codec:a libmp3lame -b:a 192k $mp3
}

$summary | Format-Table -AutoSize | Out-String -Width 200
$summary | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $OutDir "restoration-report.json") -Encoding utf8
Write-Host "report: $(Join-Path $OutDir 'restoration-report.json')"
