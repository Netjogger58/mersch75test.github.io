#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const root = path.resolve(__dirname, '..');
const htmlFiles = fs.readdirSync(root).filter((file) => file.endsWith('.html'));
const attrRe = /\b(?:src|href)\s*=\s*(?:"([^"]+)"|'([^']+)')/g;

function isExternal(ref) {
    return /^(https?:|mailto:|tel:|#|data:|javascript:)/i.test(ref);
}

const missing = [];

for (const file of htmlFiles) {
    const abs = path.join(root, file);
    const text = fs.readFileSync(abs, 'utf8');
    let match;

    while ((match = attrRe.exec(text)) !== null) {
        const raw = match[1] || match[2] || '';
        if (!raw || raw.includes('${') || raw.includes("' +") || raw.includes('" +') || isExternal(raw)) {
            continue;
        }

        let rel = raw.split('#')[0].split('?')[0];
        if (!rel) continue;

        try {
            rel = decodeURIComponent(rel);
        } catch {
            // keep original value if decoding fails
        }

        const target = path.resolve(path.dirname(abs), rel);
        if (!fs.existsSync(target)) {
            missing.push(`${file}: ${raw}`);
        }
    }
}

if (missing.length > 0) {
    console.error('Broken local references found:');
    missing.forEach((entry) => console.error(`- ${entry}`));
    process.exit(1);
}

console.log('OK: no broken local href/src references.');
