#!/usr/bin/env node
// Lint alle inline <script> Blöcke in HTML-Dateien und script.js auf Syntaxfehler.
// Bricht ab mit Exit-Code 1 wenn ein Fehler gefunden wird.

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const htmlFiles = execSync(`find "${root}" -maxdepth 3 -name "*.html" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*"`, { encoding: 'utf-8' }).trim().split('\n').filter(Boolean);
const jsFiles = execSync(`find "${root}" -maxdepth 3 -name "*.js" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*" -not -name "*-min.js"`, { encoding: 'utf-8' }).trim().split('\n').filter(Boolean);

let errors = 0;

for (const file of jsFiles) {
    try {
        execSync(`node --check "${file}"`, { stdio: 'pipe' });
        console.log(`  OK  ${path.relative(root, file)}`);
    } catch (e) {
        errors++;
        console.error(`FAIL  ${path.relative(root, file)}\n  ${e.stderr ? e.stderr.toString().trim() : e.message}`);
    }
}

for (const file of htmlFiles) {
    const html = fs.readFileSync(file, 'utf-8');
    const matches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
    if (matches.length === 0) continue;
    matches.forEach((m, i) => {
        const code = m[1];
        const tmp = `/tmp/lint-${Date.now()}-${i}.js`;
        fs.writeFileSync(tmp, code);
        try {
            execSync(`node --check "${tmp}"`, { stdio: 'pipe' });
            console.log(`  OK  ${path.relative(root, file)} (inline block ${i+1})`);
        } catch (e) {
            errors++;
            console.error(`FAIL  ${path.relative(root, file)} (inline block ${i+1})\n  ${e.stderr ? e.stderr.toString().trim() : e.message}`);
        }
        fs.unlinkSync(tmp);
    });
}

if (errors > 0) {
    console.error(`\n${errors} Syntaxfehler gefunden. Push abgebrochen.`);
    process.exit(1);
}
console.log('\nAlle JS-Syntax-Checks OK.');
