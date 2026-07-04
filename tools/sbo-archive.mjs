#!/usr/bin/env node
// sbo-archive.mjs — SBO-PDFen vun Handball4All eroflueden a lokal sécheren.
//
// Notzung:
//   node tools/sbo-archive.mjs                     # scannt live-center.html no SBO-Linken
//   node tools/sbo-archive.mjs live-center.html live-center-25-26.html
//   node tools/sbo-archive.mjs --url "https://spo.handball4all.de/misc/sboPublicReports.php?sGID=3488556"
//   node tools/sbo-archive.mjs --season 2627       # Zil-Ordner sbo-archiv/<season>/
//
// Effekt:
//   - Zitt all PDF (validéiert %PDF-Header), späichert sbo-archiv/<season>/<sGID>.pdf
//   - Aktualiséiert data/sbo-index-<season>.json  (sGID -> {file,url,savedAt,bytes})
//   - Idempotent: scho archivéiert sGIDs ginn iwwersprongen (ausser --force)

import { readFile, writeFile, mkdir, stat } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const SBO_RE = /https?:\/\/spo\.handball4all\.de\/misc\/sboPublicReports\.php\?sGID=(\d+)/g;

function parseArgs(argv) {
    const opts = { season: '2627', force: false, files: [], urls: [] };
    for (let i = 0; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--season') opts.season = argv[++i];
        else if (a === '--force') opts.force = true;
        else if (a === '--url') opts.urls.push(argv[++i]);
        else opts.files.push(a);
    }
    if (!opts.files.length && !opts.urls.length) opts.files = ['live-center.html'];
    return opts;
}

async function collectSgids(opts) {
    const map = new Map(); // sGID -> full url
    for (const u of opts.urls) {
        const m = u.match(/sGID=(\d+)/);
        if (m) map.set(m[1], u);
    }
    for (const rel of opts.files) {
        const file = path.resolve(ROOT, rel);
        if (!existsSync(file)) { console.warn(`! Datei net fonnt: ${rel}`); continue; }
        const html = await readFile(file, 'utf8');
        let m;
        while ((m = SBO_RE.exec(html)) !== null) map.set(m[1], m[0]);
    }
    return map;
}

async function loadIndex(indexPath) {
    if (!existsSync(indexPath)) return {};
    try { return JSON.parse(await readFile(indexPath, 'utf8')); }
    catch { return {}; }
}

async function fetchPdf(url) {
    const res = await fetch(url, { redirect: 'follow' });
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const buf = Buffer.from(await res.arrayBuffer());
    const head = buf.subarray(0, 5).toString('latin1');
    if (!head.startsWith('%PDF')) throw new Error(`kee valabelt PDF (Header: "${head.replace(/[^\x20-\x7e]/g, '.')}")`);
    if (buf.length < 1000) throw new Error(`ze kleng (${buf.length} B)`);
    return buf;
}

async function main() {
    const opts = parseArgs(process.argv.slice(2));
    const outDir = path.resolve(ROOT, 'sbo-archiv', opts.season);
    const indexPath = path.resolve(ROOT, 'data', `sbo-index-${opts.season}.json`);
    await mkdir(outDir, { recursive: true });
    await mkdir(path.dirname(indexPath), { recursive: true });

    const sgids = await collectSgids(opts);
    const index = await loadIndex(indexPath);
    console.log(`> ${sgids.size} SBO-Link(en) fonnt · Saison ${opts.season}`);

    let saved = 0, skipped = 0, failed = 0;
    for (const [sgid, url] of sgids) {
        const rel = `sbo-archiv/${opts.season}/${sgid}.pdf`;
        const dest = path.resolve(ROOT, rel);
        if (!opts.force && index[sgid] && existsSync(dest)) { skipped++; continue; }
        try {
            const buf = await fetchPdf(url);
            await writeFile(dest, buf);
            index[sgid] = { file: rel, url, savedAt: new Date().toISOString(), bytes: buf.length };
            saved++;
            console.log(`  ✓ ${sgid} (${buf.length} B)`);
        } catch (err) {
            failed++;
            console.warn(`  ✗ ${sgid}: ${err.message}`);
        }
    }

    await writeFile(indexPath, JSON.stringify(index, null, 2) + '\n', 'utf8');
    console.log(`> Fäerdeg: ${saved} nei, ${skipped} iwwersprongen, ${failed} Feeler.`);
    console.log(`> Index: ${path.relative(ROOT, indexPath)}`);
    if (failed) process.exitCode = 1;
}

main().catch((e) => { console.error('FATAL:', e); process.exit(1); });
