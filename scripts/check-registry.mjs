#!/usr/bin/env node
// Resolve every path in registry.json against this repo and its sibling clones.
//
//   node scripts/check-registry.mjs            # report
//   node scripts/check-registry.mjs --strict   # also fail when a sibling repo isn't cloned
//
// Paths are relative: `characters/...` lives here; `socials/content/...` means a `socials` clone next to this repo.
// Placeholders (<user>, <brand>, <Name>, <id>) check the folder they sit in; `{bot}` expands to _meta.bots;
// `{a|b}` checks each alternative; `file.json#a.b` checks that key path; `file.md#id` checks the id appears.
// A sibling repo you haven't cloned is reported as skipped, not broken, so a fresh public clone passes.
// Repos cloned elsewhere: list their parent folders in private/sibling-roots.txt (gitignored).
// Zero dependencies (Node 18+). Exit 1 = at least one broken path.

import { existsSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const siblings = dirname(here);
// Extra folders to look in for sibling repos (one per line) — gitignored, machine-specific.
const rootsFile = join(here, "private", "sibling-roots.txt");
const searchRoots = [siblings, ...(existsSync(rootsFile)
  ? readFileSync(rootsFile, "utf8").split(/\r?\n/).map((l) => l.trim()).filter((l) => l && !l.startsWith("#"))
  : [])];
const findRepo = (name) => searchRoots.map((r) => join(r, name)).find((p) => existsSync(p));
const strict = process.argv.includes("--strict");
const registry = JSON.parse(readFileSync(join(here, "registry.json"), "utf8"));
const bots = registry._meta?.bots ?? ["jenni-bot", "martian-bot"];
// private/ is the studio overlay: checked when present, skipped in a public clone.
const LOCAL = ["characters", "docs", "templates", "scripts", ...(existsSync(join(here, "private")) ? ["private"] : [])];
const PATHLIKE = /^[\w .{}<>|/@-]+\.(md|json|ya?ml)(#[\w.-]+)?$/;

const results = { ok: 0, broken: [], skipped: new Map() };

function expand(path) {
  let out = [path];
  for (const [, alts] of path.matchAll(/\{([^}]+)\}/g)) {
    const options = alts === "bot" ? bots : alts.split("|");
    out = out.flatMap((p) => options.map((o) => p.replace(`{${alts}}`, o)));
  }
  return out;
}

function hasJsonKey(file, keyPath) {
  let node = JSON.parse(readFileSync(file, "utf8"));
  for (const k of keyPath.split(".")) {
    if (node == null || typeof node !== "object" || !(k in node)) return false;
    node = node[k];
  }
  return true;
}

function check(where, raw) {
  const [pathPart, anchor] = raw.split("#");
  for (const path of expand(pathPart)) {
    const repo = path.split("/")[0];
    const repoDir = LOCAL.includes(repo) ? null : findRepo(repo);
    if (!LOCAL.includes(repo) && !repoDir) {
      results.skipped.set(repo, (results.skipped.get(repo) ?? 0) + 1);
      continue;
    }
    const base = repoDir ? dirname(repoDir) : here;
    const placeholder = path.search(/<[^>]+>/);
    const target = join(base, placeholder >= 0 ? path.slice(0, path.lastIndexOf("/", placeholder)) : path);
    let problem = null;
    if (!existsSync(target)) problem = "missing";
    else if (placeholder < 0 && anchor && statSync(target).isFile()) {
      if (target.endsWith(".json")) problem = hasJsonKey(target, anchor) ? null : `no key "${anchor}"`;
      else if (!readFileSync(target, "utf8").toLowerCase().includes(anchor.toLowerCase())) problem = `no "${anchor}"`;
    }
    if (problem) results.broken.push(`${where}: ${path}${anchor ? "#" + anchor : ""}  (${problem})`);
    else results.ok++;
  }
}

function walk(node, where) {
  if (Array.isArray(node)) node.forEach((v, i) => walk(v, `${where}[${i}]`));
  else if (node && typeof node === "object") for (const [k, v] of Object.entries(node)) walk(v, where ? `${where}.${k}` : k);
  else if (typeof node === "string") {
    // "a.md + resources/x.json": the second path lives in the first path's repo.
    const parts = node.split(" + ").map((s) => s.trim());
    const repoPrefix = parts[0].includes("/") ? parts[0].split("/")[0] + "/" : "";
    parts.forEach((p, i) => {
      const path = i > 0 && !LOCAL.includes(p.split("/")[0]) && repoPrefix && !p.startsWith(repoPrefix) ? repoPrefix + p : p;
      if (PATHLIKE.test(path)) check(where, path);
    });
  }
}

walk(registry, "");
for (const b of results.broken) console.log(`BROKEN   ${b}`);
for (const [repo, n] of results.skipped) console.log(`skipped  ${repo}/ not cloned beside voice-seed (${n} path${n > 1 ? "s" : ""})`);
console.log(`\n${results.ok} ok · ${results.broken.length} broken · ${[...results.skipped.values()].reduce((a, b) => a + b, 0)} skipped`);
process.exit(results.broken.length || (strict && results.skipped.size) ? 1 : 0);
