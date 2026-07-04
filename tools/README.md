# SBO-Archiv-Tools

Hält eng eege Kopie vun de Handball4All-SBO-Berichter (PDF), well d'FLH se net méi
zouverlässeg uweist. Plang: `../.windsurf/plans/sbo-archiv-hetzner-7c1e4a.md`.

Viraussetzung: **Node 18+** (built-in `fetch`). Fir d'Parsen: **Poppler** (`brew install poppler`).

## Workflow (pro Spilldag, manuell)

```bash
# 1) SBO-PDFen zéien + Index aktualiséieren  (scannt live-center.html)
node tools/sbo-archive.mjs

# 2) Kucken wat géif ëmgesat ginn (Dry-Run), dann applizéieren
node tools/sbo-rewrite.mjs live-center.html
node tools/sbo-rewrite.mjs live-center.html --write

# 3) PDFen zu Text/Stats maachen (manuell kontrolléieren!)
node tools/sbo-parse.mjs

# 4) Committen + op Hetzner deployéieren (sbo-archiv/ muss mat!)
git add sbo-archiv data live-center.html && git commit -m "SBO-Archiv aktualiséiert" && git push
```

## Wat wou landet

| Pad | Inhalt |
|-----|--------|
| `sbo-archiv/2627/<sGID>.pdf` | Archivéiert PDFen (mat op Hetzner deployéieren) |
| `sbo-archiv/2627/txt/<sGID>.txt` | Rohtext fir manuell Kontroll |
| `data/sbo-index-2627.json` | sGID → {file, url, savedAt, bytes} |
| `data/sbo-stats-2627.json` | Heuristesch Spiller-Reyen (`needsReview:true`) |

## Datamodell am Live Center

`sboCell(row)` (`live-center.html`) hëlt:
- `row.sbo` = eis lokal/Hetzner-Kopie (prioritär) → Label **📄 SBO**
- `row.sboLive` = Handball4All-Original (Fallback) → Label **📄 SBO (FLH)**

`js/flh-live-sync.js` iwwerschreift eng existent `sbo` (lokal Kopie) **net** méi mat
Live-Donnéeën a match Spiller iwwer d'`sGID` (aus `sbo` oder `sboLive`).

## Oppen Entscheedungen (kuck Plang, Kap. 13)

- **Hetzner-Deploy vun `sbo-archiv/`**: via GitHub-Deploy oder direkt SFTP/WebDAV?
- **Rechtlech**: SBO-PDFen (mat Spillernimm) selwer archivéieren/uweisen — mat FLH ofklären.
- **Automatiséierung**: manuell (aktuell) oder spéider GitHub Action / Cron.
