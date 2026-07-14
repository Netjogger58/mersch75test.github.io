# FLH Statistik-Archiv (mersch75.lu)

> D'Dokument beschreift, wéi d'FLH-Donnéeën (Spillplang, Resultater, Tabellen an SBO-PDFen) lokal archivéiert ginn, fir datt si och verfügbar bleiwen, wann d'FLH (handball4all.de) hir Inhalter ewechhëlt oder ännert.

## Ziel

- Onofhängeg vun der FLH-Websäit bleiwen **Spillplang, Resultater, Tabellen** an **SBO-PDFen** op `mersch75.lu` verfügbar.
- D'Live-Center Säiten (`live-center.html`, `live-center-25-26.html`) lueden d'Archiv am Hannergrond a fudderen d'Live-Donnéeën nëmmen nach, fir z'aktualiséieren.

## Dateistruktur

| Pad | Beschreiwung |
|-----|--------------|
| `data/flh-archive-2627.json` | FLH Spillplang + Tabellen fir d'Saison 2026/2027 |
| `data/flh-archive-2526.json` | FLH Spillplang + Tabellen fir d'Saison 2025/2026 |
| `data/sbo-index-2627.json` | Index: `sGID` → lokal PDF, Original-URL, Gréisst, Datum |
| `data/sbo-index-2526.json` | Index fir 2025/2026 |
| `sbo-archiv/2627/<sGID>.pdf` | Archivéiert SBO-PDFen 2026/2027 |
| `sbo-archiv/2526/<sGID>.pdf` | Archivéiert SBO-PDFen 2025/2026 |
| `tools/flh-archive.mjs` | Node-Skript fir den JSON-Archiv-Export |
| `tools/sbo-archive.mjs` | Node-Skript fir den SBO-PDF-Download |
| `js/flh-live-sync.js` | Browser-Skript, bitt `loadArchive`, `loadSboIndex`, `resolveSboLink` |

## Aktualiséieren vum Archiv

### 1. FLH JSON-Archiv

```bash
# Aktuell Saison (2026/2027)
node tools/flh-archive.mjs --season 2627 --force

# Vrgaang Saison (2025/2026)
node tools/flh-archive.mjs --season 2526 --force
```

Auswäertung: `data/flh-archive-<season>.json` mat `games`, `standingsByLabel`, `fetchedAt`, `source`.

### 2. SBO-PDFen

```bash
# 2026/2027: scannt live-center.html a live-center-25-26.html
node tools/sbo-archive.mjs live-center.html live-center-25-26.html --season 2627

# 2025/2026: scannt d'Archiv-Säit
node tools/sbo-archive.mjs live-center-25-26.html --season 2526
```

## Wéi d'Websäit d'Archiv benotzt

1. `live-center.html` (bzw. `live-center-25-26.html`) lueden `js/flh-live-sync.js`.
2. Beim Start gëtt `loadArchive(season)` opgeruff.
3. D'archivéiert Donnéeën gi mat deenen am Säit-Code vermëscht (`mergeLiveSeasonGames`).
4. Nofolgend gëtt `fetchAllGames()` ausgefouert, fir Live-Ännerungen z'iwwerhuelen.
5. `sboCell()` resolvéiert SBO-Links iwwer `resolveSboLink()` op lokal `sbo-archiv/<season>/<sGID>.pdf` wann d'PDF existéiert.

## Cache-Bust

Wann `js/flh-live-sync.js` geännert gëtt, muss de Cache-Bust an de Säiten aktualiséiert ginn:

```html
<script src="js/flh-live-sync.js?v=20260714a"></script>
```

## Technesch Notizen

- Quell: `https://spo.handball4all.de/service/if_g_json.php` (`og=95`)
- `flh-live-sync.js` ass pur Vanilla-JS, IIFE, browsersäitig. `fetch` gëtt fir Archiv an SBO-Index benotzt.
- D'Archivéierung ass momentan **manuell**: `flh-archive.mjs` a `sbo-archive.mjs` musse periodesch ausgefouert ginn.

## Open Punkten

- Automatiséierung via GitHub Action oder Cron.
- Rechtlech: SBO-PDFen (Spillernimm) sinn ëffentlech op handball4all.de, mee kënne rechtlech Froen opwerfen wann se lokal duergestallt ginn.
