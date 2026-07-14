#!/usr/bin/env node
// Konvertéiert all PNG/JPEG/WebP/AVIF-Biller an WebP/AVIF-Varianten a past <picture> + lazy-loading an HTML.

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import sharp from 'sharp';
import { parse } from 'node-html-parser';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');

const IMAGE_EXT = /\.(png|jpg|jpeg|webp|avif|gif)$/i;
const SOURCE_EXT = /\.(png|jpg|jpeg|webp|avif|gif)(?:\?[^\s"<>]*)?/i;
const SKIP_DIRS = new Set(['.git', 'node_modules', 'sbo-archiv', 'tools']);

let heroCounts = new Map();

function isImageFile(file) {
    return IMAGE_EXT.test(file);
}

function listImageFiles(dir) {
    const out = [];
    function walk(d) {
        for (const entry of fs.readdirSync(d, { withFileTypes: true })) {
            const full = path.join(d, entry.name);
            if (entry.isDirectory()) {
                if (!SKIP_DIRS.has(entry.name) && !entry.name.startsWith('.')) walk(full);
            } else if (isImageFile(entry.name)) {
                out.push(full);
            }
        }
    }
    walk(dir);
    return out;
}

function relativeToRoot(abs) {
    return path.relative(ROOT, abs).replace(/\\/g, '/');
}

function decodedRel(rel) {
    try { return decodeURIComponent(rel); } catch (e) { return rel; }
}

function stripQuery(src) {
    return String(src).split('?')[0];
}

function pathFromSrc(src, htmlDir) {
    if (!src) return null;
    if (src.startsWith('http') || src.startsWith('data:') || src.startsWith('#')) return null;
    const rel = decodedRel(stripQuery(src));
    if (rel.startsWith('/')) return path.join(ROOT, rel);
    return path.resolve(htmlDir, rel);
}

async function convertImage(filePath, { qualityWebp = 82, qualityAvif = 70, effort = 4 } = {}) {
    const rel = relativeToRoot(filePath);
    const ext = path.extname(filePath).toLowerCase().replace('.', '');
    if (ext === 'gif') {
        return { rel, webp: false, avif: false, meta: null };
    }
    const base = filePath.replace(IMAGE_EXT, '');
    const webpPath = base + '.webp';
    const avifPath = base + '.avif';
    let meta;
    try {
        meta = await sharp(filePath).metadata();
    } catch (e) {
        console.error('Metadata fail:', rel, e.message);
        return { rel, webp: false, avif: false, meta: null };
    }
    const results = { rel, webp: false, avif: false, meta };

    if (!fs.existsSync(webpPath)) {
        try {
            await sharp(filePath)
                .webp({ quality: qualityWebp, effort: 6 })
                .toFile(webpPath);
            results.webp = relativeToRoot(webpPath);
        } catch (e) {
            console.error('WebP fail:', rel, e.message);
        }
    } else {
        results.webp = relativeToRoot(webpPath);
    }

    if (!fs.existsSync(avifPath)) {
        try {
            await sharp(filePath)
                .avif({ quality: qualityAvif, effort })
                .toFile(avifPath);
            results.avif = relativeToRoot(avifPath);
        } catch (e) {
            console.error('AVIF fail:', rel, e.message);
        }
    } else {
        results.avif = relativeToRoot(avifPath);
    }

    return results;
}

function listHtmlFiles() {
    return fs.readdirSync(ROOT)
        .filter(f => f.endsWith('.html'))
        .map(f => path.join(ROOT, f));
}

function buildSourceForType(src, type, media) {
    const mediaAttr = media ? ` media="${media}"` : '';
    return `    <source srcset="${src}" type="${type}"${mediaAttr}>`;
}

function swapExt(src, ext) {
    return stripQuery(src).replace(SOURCE_EXT, '.' + ext.toLowerCase());
}

function computeTypeFromSrc(src) {
    const ext = path.extname(stripQuery(src)).replace('.', '').toLowerCase();
    if (ext === 'jpg') return 'image/jpeg';
    if (['png', 'webp', 'avif', 'gif'].includes(ext)) return 'image/' + ext;
    return '';
}

function variantExists(src, htmlDir) {
    const p = pathFromSrc(src, htmlDir);
    return p && fs.existsSync(p);
}

function hasSource(parent, srcset, type, media) {
    return parent.querySelectorAll('source').some(s =>
        s.getAttribute('srcset') === srcset &&
        s.getAttribute('type') === type &&
        (s.getAttribute('media') || '') === (media || '')
    );
}

function getAllClasses(imgNode) {
    const classes = (imgNode.getAttribute('class') || '').split(/\s+/).filter(Boolean);
    let parent = imgNode.parentNode;
    while (parent) {
        if (parent.tagName) {
            const cls = parent.getAttribute('class') || '';
            classes.push(...cls.split(/\s+/).filter(Boolean));
        }
        parent = parent.parentNode;
    }
    return classes;
}

function shouldBeHero(htmlFile, imgNode) {
    if (!htmlFile.endsWith('index.html')) return false;
    const allClasses = getAllClasses(imgNode);
    const heroClasses = ['news-u13-background', 'news-men-background', 'news-women-background', 'news-u11-background', 'poster-visual-hero', 'events-background'];
    const matched = heroClasses.find(c => allClasses.includes(c));
    if (!matched) return false;
    const count = (heroCounts.get(matched) || 0) + 1;
    heroCounts.set(matched, count);
    return count <= 2;
}

function processImgNode(imgNode, htmlDir, htmlFile, idx) {
    const src = imgNode.getAttribute('src');
    if (!src) return;
    if (src.startsWith('http') || src.startsWith('data:') || src.startsWith('#')) return;
    const filePath = pathFromSrc(src, htmlDir);
    if (!filePath || !fs.existsSync(filePath)) {
        console.warn('Image not found:', src, 'in', htmlFile);
        return;
    }
    const rel = relativeToRoot(filePath);
    if (!isImageFile(rel)) return;

    const isHero = shouldBeHero(htmlFile, imgNode);
    const loading = isHero ? 'eager' : (imgNode.getAttribute('loading') || 'lazy');
    imgNode.setAttribute('loading', loading);

    const webpSrc = swapExt(src, 'webp');
    const avifSrc = swapExt(src, 'avif');
    const hasWebp = variantExists(webpSrc, htmlDir);
    const hasAvif = variantExists(avifSrc, htmlDir);
    const parent = imgNode.parentNode;
    const isInsidePicture = parent && parent.tagName && parent.tagName.toLowerCase() === 'picture';

    if (isInsidePicture) {
        const sources = parent.querySelectorAll('source');
        if (sources.length === 0) {
            if (hasAvif && !hasSource(parent, avifSrc, 'image/avif', '')) {
                imgNode.insertAdjacentHTML('beforebegin', buildSourceForType(avifSrc, 'image/avif', ''));
            }
            if (hasWebp && !hasSource(parent, webpSrc, 'image/webp', '')) {
                imgNode.insertAdjacentHTML('beforebegin', buildSourceForType(webpSrc, 'image/webp', ''));
            }
        } else {
            sources.forEach((source) => {
                const srcset = source.getAttribute('srcset') || '';
                if (!srcset) return;
                const media = source.getAttribute('media') || '';
                const ext = path.extname(stripQuery(srcset)).replace('.', '').toLowerCase();
                const type = computeTypeFromSrc(srcset);
                const currentType = source.getAttribute('type') || '';
                if (type && !currentType) {
                    source.setAttribute('type', type);
                }
                if (ext !== 'avif') {
                    const avif = swapExt(srcset, 'avif');
                    if (variantExists(avif, htmlDir) && !hasSource(parent, avif, 'image/avif', media)) {
                        source.insertAdjacentHTML('beforebegin', buildSourceForType(avif, 'image/avif', media));
                    }
                }
                if (ext !== 'webp' && ext !== 'avif') {
                    const webp = swapExt(srcset, 'webp');
                    if (variantExists(webp, htmlDir) && !hasSource(parent, webp, 'image/webp', media)) {
                        source.insertAdjacentHTML('beforebegin', buildSourceForType(webp, 'image/webp', media));
                    }
                }
            });
        }
    } else {
        const width = imgNode.getAttribute('width');
        const height = imgNode.getAttribute('height');
        const widthAttr = width ? ` width="${width}"` : '';
        const heightAttr = height ? ` height="${height}"` : '';
        const alt = imgNode.getAttribute('alt') || '';
        const altAttr = alt ? ` alt="${alt.replace(/"/g, '&quot;')}"` : '';
        const cls = imgNode.getAttribute('class');
        const classAttr = cls ? ` class="${cls}"` : '';
        const i18n = imgNode.getAttribute('data-i18n-attr');
        const i18nAttr = i18n ? ` data-i18n-attr="${i18n}"` : '';
        const i18n2 = imgNode.getAttribute('data-i18n');
        const i18nAttr2 = i18n2 ? ` data-i18n="${i18n2}"` : '';
        const style = imgNode.getAttribute('style');
        const styleAttr = style ? ` style="${style}"` : '';
        const id = imgNode.getAttribute('id');
        const idAttr = id ? ` id="${id}"` : '';
        const loadingAttr = ` loading="${loading}"`;

        const sources = [];
        if (hasAvif) sources.push(`    <source srcset="${avifSrc}" type="image/avif">`);
        if (hasWebp) sources.push(`    <source srcset="${webpSrc}" type="image/webp">`);
        if (sources.length === 0) return;

        const newHtml = `<picture>
${sources.join('\n')}
    <img src="${src}"${altAttr}${classAttr}${idAttr}${styleAttr}${widthAttr}${heightAttr}${i18nAttr}${i18nAttr2}${loadingAttr}>
</picture>`;
        const replacement = parse(newHtml).firstChild;
        imgNode.replaceWith(replacement);
    }
}

async function main() {
    const images = listImageFiles(ROOT);
    console.log('Found images:', images.length);

    // 1. Biller konvertéieren
    let converted = 0;
    for (const file of images) {
        const res = await convertImage(file);
        if (res.webp || res.avif) converted++;
        if (converted % 25 === 0) console.log('  processed', converted);
    }
    console.log('Converted/generated variants:', converted);

    // 2. HTML updaten
    const htmlFiles = listHtmlFiles();
    let updatedHtml = 0;
    for (const htmlFile of htmlFiles) {
        heroCounts = new Map();
        const htmlDir = path.dirname(htmlFile);
        const original = fs.readFileSync(htmlFile, 'utf8');
        const root = parse(original, { comment: true, blockTextElements: { script: true, style: true } });
        const imgs = root.querySelectorAll('img');
        let changed = false;

        imgs.forEach((img, idx) => {
            const src = img.getAttribute('src');
            if (!src || src.startsWith('http') || src.startsWith('data:') || src.startsWith('#')) return;
            processImgNode(img, htmlDir, htmlFile, idx);
            changed = true;
        });

        if (changed) {
            fs.writeFileSync(htmlFile, root.toString(), 'utf8');
            updatedHtml++;
        }
    }
    console.log('Updated HTML files:', updatedHtml);
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
