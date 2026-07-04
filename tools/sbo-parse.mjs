#!/usr/bin/env node
// sbo-parse.mjs — Archivéiert SBO-PDFen zu Text maachen an d'Spillerstatistik erausléisen.
//
// Viraussetzung: `pdftotext` (Poppler).  macOS:  brew install poppler
//
// Notzung:
//   node tools/sbo-parse.mjs                 # all PDFen aus dem Index parsen
//   node tools/sbo-parse.mjs --season 2627
//   node tools/sbo-parse.mjs --sgid 3488556  # nëmmen een
//
// Effekt:
//   - Rohtext:  sbo-archiv/<season>/txt/<sGID>.txt   (fir manuell Kontroll!)
//   - Stats:    data/sbo-stats-<season>.json         (pro sGID: heuristesch Spiller-Reyen)
//
// WICHTEG: D'SBO-Layouten variéieren — d'heuristesch Extraktioun MUSS manuell
// kontrolléiert ginn ier se an d'Statistik-Säiten iwwerholl gëtt.

import { readFile, writeFile, mkdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');

function parseArgs(argv) {
    const opts = { season: '2627', sgid: null };
    for (let i = 0; i < argv.length; i++) {
        const a = argv[i];
        if (a === '--season') opts.season = argv[++i];
        else if (a === '--sgid') opts.sgid = argv[++i];
    }
    return opts;
}

function hasPdftotext() {
    try { execFileSync('pdftotext', ['-v'], { stdio: 'ignore' }); return true; }
    catch { return false; }
}

function pdfToText(pdfPath) {
    return execFileSync('pdftotext', ['-layout', '-enc', 'UTF-8', pdfPath, '-'], { encoding: 'utf8' });
}

// Heuristik: Zeile mat engem Numm (Buschtawen) gefollegt vu Prisзапisitiounen wéi
// "Nummer  Numm, Virnumm  ... Tore  7m".  Mir zéien Numm + éischt eenzel Zuelegruppen.
// Bewosst konservativ: gëtt éischter roh Kandidat-Reyen zréck fir manuell Kontroll.
function extractPlayers(text) {
    const players = [];
    const lines = text.split(/\r?\n/);
    for (const line of lines) {
        const l = line.trim();
        // Numm-Muster: "Nolauer, Charel" oder "Charel Nolauer" mat mindestens engem Komma/Buschtaf
        const nameMatch = l.match(/^(\d{1,3}\s+)?([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ.\-']+(?:[ ,]+[A-Za-zÀ-ÿ.\-']+)+)\s+(.*\d.*)$/);
        if (!nameMatch) continue;
        const name = nameMatch[2].replace(/\s+/g, ' ').trim();
        const nums = (nameMatch[3].match(/\d+/g) || []).map(Number);
        if (!nums.length) continue;
        // Filter offensichtlech Net-Spiller-Zeilen (z.B. Dates, Uhrzäiten)
        if (/\d{2}[:.]\d{2}/.test(l) || /\d{2}\.\d{2}\.\d{2,4}/.test(l)) continue;
        players.push({ name, numbers: nums, raw: l });
    }
    return players;
}

async function main() {
    const opts = parseArgs(process.argv.slice(2));
    if (!hasPdftotext()) {
        console.error('! `pdftotext` net fonnt. Installéieren:  brew install poppler');
        process.exit(2);
    }

    const indexPath = path.resolve(ROOT, 'data', `sbo-index-${opts.season}.json`);
    if (!existsSync(indexPath)) { console.error(`! Index net fonnt: ${path.relative(ROOT, indexPath)}`); process.exit(1); }
    const index = JSON.parse(await readFile(indexPath, 'utf8'));

    const txtDir = path.resolve(ROOT, 'sbo-archiv', opts.season, 'txt');
    await mkdir(txtDir, { recursive: true });
    const statsPath = path.resolve(ROOT, 'data', `sbo-stats-${opts.season}.json`);
    const stats = existsSync(statsPath) ? JSON.parse(await readFile(statsPath, 'utf8')) : {};

    const sgids = opts.sgid ? [opts.sgid] : Object.keys(index);
    let done = 0, failed = 0;
    for (const sgid of sgids) {
        const entry = index[sgid];
        if (!entry) { console.warn(`  ? ${sgid}: net am Index`); continue; }
        const pdfPath = path.resolve(ROOT, entry.file);
        if (!existsSync(pdfPath)) { console.warn(`  ✗ ${sgid}: PDF feelt (${entry.file})`); failed++; continue; }
        try {
            const text = pdfToText(pdfPath);
            await writeFile(path.join(txtDir, `${sgid}.txt`), text, 'utf8');
            const players = extractPlayers(text);
            stats[sgid] = { file: entry.file, parsedAt: new Date().toISOString(), needsReview: true, players };
            done++;
            console.log(`  ✓ ${sgid}: ${players.length} Kandidat-Reyen`);
        } catch (err) {
            failed++;
            console.warn(`  ✗ ${sgid}: ${err.message}`);
        }
    }

    await writeFile(statsPath, JSON.stringify(stats, null, 2) + '\n', 'utf8');
    console.log(`> Fäerdeg: ${done} geparst, ${failed} Feeler.`);
    console.log(`> Rohtext: ${path.relative(ROOT, txtDir)}/  ·  Stats: ${path.relative(ROOT, statsPath)}`);
    console.log('> ⚠ Manuell kontrolléieren ier an d\'Statistik iwwerholl gëtt (needsReview:true).');
}

main().catch((e) => { console.error('FATAL:', e); process.exit(1); });
