#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const root = path.resolve(__dirname, '..');

function sh(cmd) {
  return execSync(cmd, { cwd: root, encoding: 'utf8' }).trim();
}

function encodeUrlPath(p) {
  return p
    .split('/')
    .map((seg) => encodeURIComponent(seg))
    .join('/');
}

function decodeMaybe(p) {
  try {
    return decodeURIComponent(p);
  } catch {
    return p;
  }
}

function normalizeExtracted(ref) {
  let out = ref.trim();
  out = out.replace(/^\.\//, '');
  out = out.replace(/^\//, '');
  return out;
}

function pageNameFromFile(relPath) {
  const base = path.basename(relPath);
  if (!base.endsWith('.html')) return null;
  return base.replace(/\.html$/i, '').toLowerCase();
}

const files = sh("rg --files --glob '*.html' --glob '*.css' --glob '*.js'")
  .split('\n')
  .filter(Boolean)
  .filter((p) => !p.startsWith('assets/'))
  .filter((p) => !p.startsWith('scripts/'));

const extractRe = /(["'(])((?:\.?\/?Media\/)[^"')]*?)(["')])/g;

const usages = new Map();
const fileContents = new Map();

for (const rel of files) {
  const abs = path.join(root, rel);
  const text = fs.readFileSync(abs, 'utf8');
  fileContents.set(rel, text);
  let m;
  while ((m = extractRe.exec(text)) !== null) {
    const raw = normalizeExtracted(m[2]);
    if (!raw.startsWith('Media/')) continue;
    if (!usages.has(raw)) usages.set(raw, new Set());
    usages.get(raw).add(rel);
  }
}

const mapping = new Map();
const unresolved = [];
const copied = [];

for (const [rawRef, usedIn] of usages.entries()) {
  const decodedRef = decodeMaybe(rawRef);
  const srcAbs = path.join(root, decodedRef);

  if (!fs.existsSync(srcAbs)) {
    unresolved.push({ ref: rawRef, decoded: decodedRef, usedIn: Array.from(usedIn) });
    continue;
  }

  let destRel;
  if (usedIn.size === 1) {
    const only = Array.from(usedIn)[0];
    const page = pageNameFromFile(only);
    if (page) {
      destRel = path.posix.join('assets/pages', page, 'media', decodedRef.replace(/^Media\//, ''));
    } else {
      destRel = path.posix.join('assets/shared/media', decodedRef.replace(/^Media\//, ''));
    }
  } else {
    destRel = path.posix.join('assets/shared/media', decodedRef.replace(/^Media\//, ''));
  }

  const destAbs = path.join(root, destRel);
  fs.mkdirSync(path.dirname(destAbs), { recursive: true });
  fs.copyFileSync(srcAbs, destAbs);
  mapping.set(rawRef, encodeUrlPath(destRel));
  copied.push({ from: decodedRef, to: destRel, count: usedIn.size });
}

for (const rel of files) {
  const oldText = fileContents.get(rel);
  const newText = oldText.replace(extractRe, (full, left, inner, right) => {
    const norm = normalizeExtracted(inner);
    if (!norm.startsWith('Media/')) return full;
    const repl = mapping.get(norm);
    if (!repl) return full;
    return `${left}${repl}${right}`;
  });

  if (newText !== oldText) {
    fs.writeFileSync(path.join(root, rel), newText, 'utf8');
  }
}

const report = {
  filesScanned: files.length,
  refsFound: usages.size,
  mapped: mapping.size,
  unresolved,
  copiedCount: copied.length,
};

const reportPath = path.join(root, 'data', 'asset-migration-report.json');
fs.mkdirSync(path.dirname(reportPath), { recursive: true });
fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));

console.log(`Scanned files: ${report.filesScanned}`);
console.log(`Found refs: ${report.refsFound}`);
console.log(`Mapped refs: ${report.mapped}`);
console.log(`Copied assets: ${report.copiedCount}`);
console.log(`Unresolved refs: ${report.unresolved.length}`);
console.log(`Report: data/asset-migration-report.json`);
