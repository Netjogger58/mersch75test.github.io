#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
function collectFiles(dir) {
    const out = [];
    const entries = fs.readdirSync(dir, { withFileTypes: true });
    for (const entry of entries) {
        const abs = path.join(dir, entry.name);
        if (entry.isDirectory()) {
            if (entry.name === '.git') continue;
            out.push(...collectFiles(abs));
            continue;
        }
        if (entry.name.endsWith('.html') || entry.name.endsWith('.css')) {
            out.push(abs);
        }
    }
    return out;
}

const files = collectFiles(root);
const attrRe = /\b(?:src|href)\s*=\s*(?:"([^"]+)"|'([^']+)')/g;
const cssRe = /url\(\s*(?:"([^"]+)"|'([^']+)'|([^'")\s]+))\s*\)/g;

function normalize(ref) {
    return ref.trim().replace(/^\.\//, '').replace(/^\//, '');
}

const violations = [];

for (const abs of files) {
    const text = fs.readFileSync(abs, 'utf8');
    const relFile = path.relative(root, abs).replace(/\\/g, '/');
    let match;

    while ((match = attrRe.exec(text)) !== null) {
        const ref = normalize(match[1] || match[2] || '');
        if (ref.startsWith('Media/')) {
            violations.push(`${relFile}: ${ref}`);
        }
    }

    while ((match = cssRe.exec(text)) !== null) {
        const ref = normalize(match[1] || match[2] || match[3] || '');
        if (ref.startsWith('Media/')) {
            violations.push(`${relFile}: ${ref}`);
        }
    }
}

if (violations.length > 0) {
    console.error('Asset policy violation: Media/ references found in live page source.');
    violations.forEach((entry) => console.error(`- ${entry}`));
    process.exit(1);
}

console.log('OK: no Media/ references in HTML src/href/url().');
