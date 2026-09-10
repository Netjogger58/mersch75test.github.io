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

function stripStringsCommentsAndRegexes(code) {
    let out = '';
    let i = 0;
    let previous = 'START';
    const regexStarters = new Set([
        'START', '(', '{', '[', ',', ';', ':', '=', '?', '!', '~', '+', '-', '*', '/', '%', '^', '&', '|',
        '=>', 'return', 'case', 'throw', 'delete', 'void', 'typeof', 'instanceof', 'in', 'of', 'yield', 'await', 'else', 'do'
    ]);

    function skipQuotedString() {
        const quote = code[i];
        i++;
        while (i < code.length) {
            if (code[i] === '\\') {
                i += 2;
                continue;
            }
            if (code[i] === quote) {
                i++;
                return;
            }
            i++;
        }
    }

    function readRegexLiteral() {
        let end = i + 1;
        let inCharacterClass = false;
        while (end < code.length) {
            const character = code[end];
            if (character === '\n' || character === '\r') return -1;
            if (character === '\\') {
                end += 2;
                continue;
            }
            if (character === '[') inCharacterClass = true;
            else if (character === ']') inCharacterClass = false;
            else if (character === '/' && !inCharacterClass) {
                end++;
                while (end < code.length && /[gimsuy]/.test(code[end])) end++;
                return end;
            }
            end++;
        }
        return -1;
    }

    while (i < code.length) {
        const character = code[i];
        const next = code[i + 1];

        if (/\s/.test(character)) {
            i++;
            continue;
        }
        if (character === '/' && next === '/') {
            while (i < code.length && code[i] !== '\n') i++;
            continue;
        }
        if (character === '/' && next === '*') {
            i += 2;
            while (i < code.length && !(code[i] === '*' && code[i + 1] === '/')) i++;
            i += 2;
            continue;
        }
        if (character === '"' || character === "'" || character === '`') {
            skipQuotedString();
            previous = 'literal';
            continue;
        }
        if (character === '/' && regexStarters.has(previous)) {
            const end = readRegexLiteral();
            if (end !== -1) {
                i = end;
                previous = 'regex';
                continue;
            }
        }
        if (/[A-Za-z_$]/.test(character)) {
            let end = i + 1;
            while (end < code.length && /[A-Za-z0-9_$]/.test(code[end])) end++;
            previous = code.slice(i, end);
            i = end;
            continue;
        }
        if (/[0-9]/.test(character) || (character === '.' && /[0-9]/.test(next || ''))) {
            let end = i + 1;
            while (end < code.length && /[A-Za-z0-9_.]/.test(code[end])) end++;
            previous = 'number';
            i = end;
            continue;
        }

        const operator = code.slice(i, i + 2);
        const token = ['===', '!==', '>>>', '<<=', '>>=', '=>', '==', '!=', '<=', '>=', '++', '--', '&&', '||', '??', '?.', '**', '<<', '>>', '+=', '-=', '*=', '/=', '%=', '&=', '|=', '^=', '...'].includes(operator)
            ? operator
            : character;
        out += token;
        previous = token;
        i += token.length;
    }
    return out;
}

for (const file of htmlFiles) {
    const html = fs.readFileSync(file, 'utf-8');
    const matches = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
    if (matches.length === 0) continue;

    matches.forEach((m, i) => {
        const stripped = stripStringsCommentsAndRegexes(m[1]);
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
