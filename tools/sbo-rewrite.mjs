#!/usr/bin/env node
// sbo-rewrite.mjs — SBO-Linken an engem HTML-Fichier op déi lokal Kopie ëmsetzen.
//
// Fir all Spill dat schonn archivéiert ass (steet an data/sbo-index-<season>.json),
// gëtt:   sbo: "https://spo.handball4all.de/...sGID=<id>"
// zu:     sbo: "sbo-archiv/<season>/<id>.pdf", sboLive: "https://...sGID=<id>"
//
// Notzung:
//   node tools/sbo-rewrite.mjs live-center.html            # DRY-RUN (weist just wat geännert géif)
//   node tools/sbo-rewrite.mjs live-center.html --write     # schreift d'Ännerungen
//   node tools/sbo-rewrite.mjs live-center.html --season 2627

import { readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function parseArgs(argv) {
    const opts = { season: '2627', write: false, file: null };
    for (let i = 0; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--season') opts.season = argv[++i];
        else if (a === '--write') opts.write = true;
        else opts.file = a;
    }
    return opts;
}

async function main() {
    const opts = parseArgs(process.argv.slice(2));
    if (!opts.file) { console.error('Notzung: node tools/sbo-rewrite.mjs <file.html> [--write] [--season 2627]'); process.exit(1); }

    const filePath = path.resolve(ROOT, opts.file);
    const indexPath = path.resolve(ROOT, 'data', `sbo-index-${opts.season}.json`);
    if (!existsSync(filePath)) { console.error(`! Datei net fonnt: ${opts.file}`); process.exit(1); }
    if (!existsSync(indexPath)) { console.error(`! Index net fonnt: ${path.relative(ROOT, indexPath)} — als éischt sbo-archive.mjs lafen.`); process.exit(1); }

    const index = JSON.parse(await readFile(indexPath, 'utf8'));
    let html = await readFile(filePath, 'utf8');

    // Match: sbo: "https://...sGID=<id>..."  (nach net op eng lokal Kopie ëmgesat)
    const re = /sbo:\s*"(https?:\/\/spo\.handball4all\.de\/misc\/sboPublicReports\.php\?sGID=(\d+)[^"]*)"/g;
    const changes = [];
    html = html.replace(re, (full, url, sgid) => {
        if (!index[sgid]) return full; // nach net archivéiert -> onverännert loossen
        const local = `sbo-archiv/${opts.season}/${sgid}.pdf`;
        changes.push(sgid);
        return `sbo: "${local}", sboLive: "${url}"`;
    });

    console.log(`> ${changes.length} Link(en) ze ëmsetzen an ${opts.file}${changes.length ? ': ' + changes.join(', ') : ''}`);
    if (!changes.length) return;

    if (opts.write) {
        await writeFile(filePath, html, 'utf8');
        console.log('> Geschriwwen. (Denk drun: sbo-archiv/ mat op Hetzner deployéieren!)');
    } else {
        console.log('> DRY-RUN — mat --write applizéieren.');
    }
}

main().catch((e) => { console.error('FATAL:', e); process.exit(1); });
