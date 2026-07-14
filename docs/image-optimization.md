# Image-Optimierung (WebP / AVIF + Lazy Loading)

Dës Dokument beschreift de Batch-Prozess fir all Biller vun `mersch75.lu` an modern Formater ze konvertéieren an d'HTML-Säiten optiméiert auszeliwweren.

## Zweck

- **Klénger Dateigréissten** duerch WebP a AVIF.
- **Besser Ladeverhalen** duerch `loading="lazy"`.
- **Breite Browser-Ënnerstëtzung** duerch `<picture>` mat original Fichier als Fallback.

## Tools

- [`tools/convert-images.mjs`](../tools/convert-images.mjs)
- [`tools/package.json`](../tools/package.json)
- Node.js + `sharp` + `node-html-parser`

## Installatioun

```bash
cd tools
npm install
```

## Ablaf

```bash
node convert-images.mjs
```

1. **Inventarisatioun**: sicht all Biller a `.png`, `.jpg`, `.jpeg`, `.webp`, `.avif` (ausser `.git`, `node_modules`, `sbo-archiv`, `tools`).
2. **Konversioun**: generéiert `*.webp` (Qualitéit 82) a `*.avif` (Qualitéit 70) nieweben dem Original.
3. **HTML-Update**: fir all `<img>` an den HTML-Säiten:
   - Huet seng Original-Datei WebP/AVIF-Varianten, gëtt dat `<img>` an en `<picture>`-Wrapper gesat.
   - `<source srcset>` fir AVIF an WebP ginn agesat, d'Original-`<img>` bleiwt als Fallback.
   - `loading="lazy"` gëtt bäigesaat, wann net laanscht – Hero-Biller op `index.html` bleiwen `eager`.
   - Eloen `<picture>` ginn ergänzt, wann Source-Typen feelen.
4. **Validatioun**: Script nees starten ass **idempotent** (keng duplizéiert Quellen).

## Hero-Biller

Op `index.html` bleiwen de poster-Bild an déi éischt News-Slide-Biller `loading="eager"`:

- `.poster-visual-hero` (Parent vum éischte `<img>`)
- éischt `.events-background`
- éischt `news-u13-background`, `news-men-background`, `news-women-background`, `news-u11-background`

## Käschten

- `archive/media-legacy-2026-06-20/Sponsoring/Yamas.png` war korrupt an huet `sharp`-Feler ("libspng read error") produzéiert, dofir geläscht.
- Biller an externen URLen (`http://`, `data:`) ginn iwwersprongen.

## Maintenance

Nom Konvertéieren kënnt CSS-Selektoren déi nëmmen `> img` matchen net méi gëllen, well d'Biller elo an `<picture>` stinn. Beispill-Fix: `inside.html` `.statuten-side-badge > img` → `.statuten-side-badge > picture > img`.

## Verwandelt Dokumenter

- [`CHANGELOG.md`](../CHANGELOG.md) — lafend Ännerungen.
- [`Webseiten-Statusbericht.md`](../Webseiten-Statusbericht.md) — Gesamtzoustand.
