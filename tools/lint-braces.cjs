#!/usr/bin/env node
// Schneller Brace-Balance-Check für inline <script> Blöcke in HTML-Dateien.
// Fängt verwaiste Klammern BEVOR sie als Syntaxfehler enden.
// Ergänzt lint-js.cjs (das erst nach node --check fehlschlägt).

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const root = path.resolve(__dirname, '..');
const htmlFiles = execSync(
    `find "${root}" -maxdepth 3 -name "*.html" -not -path "*/node_modules/*" -not -path "*/.git/*" -not -path "*/dist/*"`,
    { encoding: 'utf-8' }
).trim().split('\n').filter(Boolean);

let errors = 0;

function stripStringsAndComments(code) {
    let out = '';
    let i = 0;
    while (i < code.length) {
        const c = code[i];
        const n = code[i + 1];
        // Line comment
        if (c === '/' && n === '/') {
            while (i < code.length && code[i] !== '\n') i++;
            continue;
        }
        // Block comment
        if (c === '/' && n === '*') {
            i += 2;
            while (i < code.length && !(code[i] === '*' && code[i + 1] === '/')) i++;
            i += 2;
            continue;
        }
        // Strings
        if (c === '"' || c === "'" || c === '`') {
            const quote = c;
            i++;
            while (i < code.length && code[i] !== quote) {
                if (code[i] === '\\') i++;
                i++;
            }
            i++;
            continue;
        }
        out += c;
        i++;
    }
    return out;
}

for (const file of htmlFiles) {
    const html = fs.readFileSync(file, 'utf-8');
    const matches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
    if (matches.length === 0) continue;

    matches.forEach((m, i) => {
        const stripped = stripStringsAndComments(m[1]);
        const openB = (stripped.match(/\{/g) || []).length;
        const closeB = (stripped.match(/\}/g) || []).length;
        const openP = (stripped.match(/\(/g) || []).length;
        const closeP = (stripped.match(/\)/g) || []).length;
        const openS = (stripped.match(/\[/g) || []).length;
        const closeS = (stripped.match(/\]/g) || []).length;

        const issues = [];
        if (openB !== closeB) issues.push(`{} ${openB}/${closeB}`);
        if (openP !== closeP) issues.push(`() ${openP}/${closeP}`);
        if (openS !== closeS) issues.push(`[] ${openS}/${closeS}`);

        if (issues.length > 0) {
            errors++;
            console.error(`FAIL  ${path.relative(root, file)} (block ${i+1}): ${issues.join(', ')}`);
        } else {
            console.log(`  OK  ${path.relative(root, file)} (block ${i+1})`);
        }
    });
}

if (errors > 0) {
    console.error(`\n${errors} Klammern-Imbalance gefunden. Push abgebrochen.`);
    process.exit(1);
}
console.log('\nAlle Klammern balanciert.');
