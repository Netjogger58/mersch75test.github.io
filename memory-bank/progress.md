## Carousel-Skript + 3-Slides-Verifikation – 2026-09-25

### Befund
- `_carousel_clean.py` läuft **fehlerfrei** (`Keeping: 3 / Removing: 0`, exit 0); der gemeldete Bug (nicht definierte `track_content_start`/`track_end_pos`) ist **nicht mehr vorhanden** – auch `_clean_v2.py` enthält diese Variablen nicht (grep: 0 Treffer). Beide Skripte sind zeilenweise + idempotent umgesetzt, Guard `kept != 3` vorhanden.
- `index.html`: genau **3 `<article>`** (`news-slide-floumaart`, `news-slide-coupe-fe`, `news-slide-ag`), Datei endet mit `</html>`; kein Bezug mehr auf entfernte Slides (z. B. `news-slide-luxqf3`).
- `hallo_agent2.txt` = `Cline ist startklar!` ✓
- Live-Check lief bereits idempotent (`diff` nach Skriptlauf: identisch) → keine Änderung, **kein Commit/Push nötig**; HEAD == origin/main (`5426786`). Einzig untracked: `assets/Unbenannt-1.psd` (nicht Teil der Aufgabe, liegen gelassen).

---

## Live-Center: Alte Resultate (vor 15.08.2026) entfernt – 2026-09-24

### Problem
Live-Center zeigte wieder Resultate aus der Vorsaison (25/26, Spiele Feb–Mai 2026), obwohl nur 2 Spiele (20.09.26) gespielt waren.

### Root Cause (in `js/flh-live-sync.js`)
1. `CURRENT_PERIOD_ID = '137'` = **Saison 25/26**; laut FLH-`po`-Menü ist die aktuelle Periode **142** (26/27).
2. `REQUESTS` nutzten noch die **alten `cl`-Klassen-IDs** der Saison 25/26 (153713, 152653, …).
3. Folge: `fetchAllGames()` holte 70 Alt-Spiele (mit Resultaten) und `mergeLiveSeasonGames()` mischte sie in `allGamesData` → Anzeige vor dem Saisonstart.
4. Zusätzlich: falsche `sGID`-Werte bei den 2 gespielten Spielen (3276105/3357291 = Vorsaison-Spiele) → Merge über sGID schlug fehl bzw. verlinkte falsche SBO-Berichte.

### Fix (neue `cl`-IDs via FLH-API verifiziert; 5 Kategorien)
| Kategorie | alt `cl` | **neu `cl`** |
|---|---|---|
| Männer (H-PRO) | 153713 | **167931** |
| Frauen (D-PRO) | 152653 | **168031** |
| U15G | 156341 | **168871** |
| U13M-P1 | 152106 (PE) | **168526** |
| U13M-P2 | – | **168531** |
- `CURRENT_PERIOD_ID` `'137'` → `'142'`.
- Turnier-Requests (u15fin, u11el, u11elpf, u11es, u9, u7) entfernt – Tournoi hat keine Resultate/Tabellen (Aussage Nutzer).
- **Saison-Guard** `SEASON_START = 15.08.2026` in `fetchCompetitionGames`: Live-Spiele davor werden verworfen (unparsebare Daten bleiben erhalten).
- `buildMergeKey` → `buildMergeKeys` (Mehrfach-Schlüssel `nr|` **und** `sbo|sGID`) + `mergeLiveSeasonGames` merged über beliebigen Treffer.
- Neu exportiert: `MerschFlhSync.dedupeByGameNumber()` (führt statisch/Live über `gNo` zusammen, behält Eintrag mit Resultat) – aufgerufen in `live-center.html` (`applyLiveCenterCorrections`) und `generator.html` (`applyGeneratorLiveGames`).
- `live-center.html`: sGID der 2 gespielten Spiele korrigiert → `3504081` (Frauen) / `3504641` (Männer).
- `renderStandingsPanel()` nutzt jetzt die **Live-Tabellen** (`window.__liveStandings`) statt nur der statischen Null-Astellung; Fallback bleibt.
- Cache-Bust: `flh-live-sync.js?v=20260714a` → `?v=20260924a` (live-center.html, generator.html).

### Verifikation (Node-Tests gegen echte FLH-API)
- Live-Payload: **47 Spiele, 0 vor 15.08.2026, 0 Fehler**; 5 Tabellen (Männer/Frauen/U15G/U13-P1/U13-P2).
- Merge+Saisonfilter Live-Center: **50 Einträge, 0 Duplikate, 0 Alt-Spiele**; Resultate: Frauen 25:22, Männer 29:27 (20.09.26).
- Generator: **47 Einträge, 0 Duplikate, 0 Alt-Spiele**.
- Archiv (`live-center-25-26.html` + `data/flh-archive-2526.json`): Merge-Ausgabe **identisch zu vorher** (148 Einträge) – **Archiv unberührt** (`git status` sauber für `data/`, `sbo-archiv/`, `live-center-25-26.html`).
- `node --check js/flh-live-sync.js` OK; alle Inline-Scripts in `live-center.html`/`generator.html` syntaktisch OK.

### Nicht angefasst (Anweisung Nutzer)
- `data/flh-archive-*.json`, `data/sbo-index-*.json`, `sbo-archiv/**`, `live-center-25-26.html` (Archiv).

---

## News-Carousel Cleanup (index.html) – 2026-09-23

### Goal
News-Carousel in `index.html` auf genau 3 Slides kürzen: `news-slide-floumaart`, `news-slide-coupe-fe`, `news-slide-ag`.

### Critical Incident
- Ein früherer Bereinigungslauf hat `index.html` auf **155 Zeilen abgeschnitten** (alles nach dem Track-Schluss: news-arrow-Buttons, news-dots, Footer, alle `<script>`s, `</body></html>`).
- Dieser kaputte Stand wurde versehentlich in Commit `37d172a` mitgecommitted und gepusht → Live-Seite war betroffen.
- **Reparatur:** Vollständige Datei aus `HEAD~1` (714 Zeilen, 12 Slides) wiederhergestellt, dann Cleanup erneut sauber ausgeführt → 531 Zeilen.

### Root Cause (Skript-Bugs)
1. Ältere Versionen: inkonsistente Variablennamen (`content_start` vs. `track_content_start`) und `rfind('<div', …)`, das das innere statt das Track-Div traf.
2. `_clean_v2.py` (1. Fassung): `in_track` wurde nie auf `False` gesetzt → nach dem Track-Div wurde **alle restlichen Zeilen bis EOF verworfen** (dieser Abbruch verursachte die 155-Zeilen-Datei).

### Solution (jetzt in `_carousel_clean.py` und `_clean_v2.py`)
- **Zeilenweise** Verarbeitung statt Region-Slicing: nur `<article …news-slide…>`-Blöcke (bis `</article>`) werden gefiltert, **alle anderen Zeilen laufen unverändert durch** → Track/Viewport-Divs, Buttons, Scripts, Footer bleiben garantiert intakt.
- Guard: `kept != 3` → Fehlermeldung und **kein Schreiben** der Datei.
- Idempotent: 2. Lauf ergibt `Keeping: 3 / Removing: 0`.

### Verification
- 531 Zeilen, genau 3 `<article>`, Klassen: `news-slide-ag`, `news-slide-coupe-fe`, `news-slide-floumaart`
- Tag-Balance: 37/37 `div`, 3/3 `article`, 5/5 `section`, 1× `</body></html>`
- `news-arrow-prev/next` (Zeile ~170) und `news-dots` vorhanden; kein JS/HTML-Bezug auf entfernte Slide-Klassen (nur Cache-Buster `script.js?v=…luxqf3`, der ist unrelated)
- `hallo_agent2.txt` = `Cline ist startklar!`

### Nachtrag (gleicher Tag): Poster-Pfad-Fix
- `37d172a` hatte `Matchday 260926 LSP.webp` und `Portrait 26092026.webp` nach `Media/` (ohne Unterordner) gelegt, aber `index.html` referenziert beide unter `Media/Hauptseite/` (11 Stellen: srcset, Poster-Download-Links, Cache-Busting-JS).
- **Fix (Commit `0738124`):** `git mv` beider Dateien nach `Media/Hauptseite/` (dort lagen auch die Vorgänger `current-matchposter.*`). Pfade `Media/…` ohne `Hauptseite/` wurden nirgends referenziert.
- Verifiziert: alle 11 Referenzen + Stichproben (`inside.html`, Logos) lösen auf Disk auf.

---

## Generator.html - Saison 2026/27 Fixes

### Issues Fixed:
1. **Portrait-Poster Hintergrundbild** - Das alte `portrait-poster-neu.png` (enthält bereits alte Spiele) wird **nicht mehr** als CSS-Hintergrund verwendet. Stattdessen: fester dunkler Hintergrund `#0d1b2a`. Das Portrait wird komplett dynamisch gerendert (alte Spiele können nicht mehr "doppelt" erscheinen).
2. **Tournoi-Slot-Anzeige** - Wenn kein Turnier aktiv ist, wird ein "Kein Turnier aktiv" Platzhalter angezeigt, sodass Jugend-Teams nicht falsch zusammenrutschen
3. **Jugend-Abstände** - Jugend-Teams haben jetzt besseren Abstand zwischen sich und den Männer-Teams durch erweiterte `youthCols`-Liste und optimierte Top-Positionen
4. **Youth-Modus Toggle** - Der Jugend-Modus funktioniert jetzt korrekt mit sauberer Trennung zwischen Turnier-, Jugend- und Männer-Slots
5. **Layout-Logik** - Turnier-Slot (`l-dynamic-tournoi`), Jugend-Slots (`youth3col` mit getrennten Spalten) und Männer-Slots (`l-dynamic-main`) sind jetzt sauber getrennt
6. **Einzelnes Portrait-Spiel** - Bei genau einem ausgewählten Spiel wird der Block auf 50% Breite gesetzt und horizontal mittig angezeigt
7. **`renderPortraitDataUrl()`** - Wartet nicht mehr auf ein Hintergrundbild, das bereits veraltete Spiele enthielt. Nur Fonts und dynamische Bilder werden gewartet.

### Root Cause:
Das Bild `assets/portrait-poster-neu.png` war **kein leeres Hintergrundbild**, sondern ein bereits gerendertes Poster mit alten Spielen. Als es als CSS-Background genutzt wurde, wurden alte Spiele fest ins Bild gebacken und die neuen nur darübergelegt → sichtbare "alt + neu"-Doppelung.

### Technical Changes:
- **CSS** (line 159): `#poster-portrait` background changed from `url("assets/portrait-poster-neu.png")` → `#0d1b2a` (einfarbig dunkel)
- **JS** `renderPortraitDataUrl()`: Removed background image load wait; only waits for fonts and `<img>` elements
- **JS** `updatePortraitPreview()`: Single portrait game → 50% width + centered via flex container
- **Landscape Layout**: youthCols `[40, 500, 800, 1200]`, youth top 600/660, clear tournoi/youth/senior separation

### Verification:
- Generator im Browser öffnen → alle Teams durchklicken → Landscape + Portrait prüfen
- Portrait zeigt NUR dynamische Inhalte (neue Spiele), kein altes Hintergrundbild mehr
- Bei genau einem Spiel → Block 50% Breite, zentriert
- "Poster herunterladen" → sauberes Portrait ohne alte Spiele darunter

---

## 2026-09-23: Homepage-Poster + Menü-Diagnose

### 1) Poster: Landscape statt Portrait auf index.html
- **Wunsch:** Die erste Seite soll das Landscape-Poster zeigen, nicht das Portrait.
- **Änderung:** `<picture id="landscape-poster-pic">` vereinacht zu einer einzigen WebP-Quelle + `<img>`-Fallback, beide = `Media/Hauptseite/Matchday 260926 LSP.webp`. Portrait-`<source>` (Mobil-Hochkant) und Portrait-Fallback entfernt. **Download-Buttons (Landscape/Portrait) unverändert.**
- **Hinweis:** Auf dem Handy (Hochkant) wird das Landscape-Poster jetzt ebenfalls angezeigt (hochkant gedreht), statt des Portrait-Posters.

#### Korrektur (gleicher Tag, finale Variante)
- **User-Klärung:** gewünscht ist das responsive Original-Verhalten:
  - Handy **Hochkant** (≤900px + portrait) → **Portrait**-Poster
  - Handy **Querformat** → **Landscape**-Poster
  - **PC** (jede Orientierung) → **nur Landscape**-Poster
- **Finale Struktur:** Portrait-`<source>` mit `media="(max-width: 900px) and (orientation: portrait)"` zurück, Landscape als `<source>` (ohne media) und als `<img>`-Fallback (statt früher Portrait-Fallback). Der wirkungslose `type="image/avif"`-Source (zeigte auf .webp) entfällt.

### 2) Menü "geht nicht mehr auf" – Diagnose: Live funktioniert es
- Headless-Chrome-Test von `https://mersch75.lu/`: **kein JS-Fehler**, `script.js` lädt, DOM enthält `site-menu-shell`/`site-menu-primary`/`site-menu-close` → `initializeSiteMenu()` läuft komplett durch; beide Poster-Pfade liefern HTTP 200.
- Wahrscheinlichste Ursache beim Reporter: **Browser-Cache des defekten Zwischenstands `37d172a`** (index.html auf 155 Zeilen beschnitten, ohne `<script src="script.js">` → Menü konnte gar nicht funktionieren). Abhilfe: **hart neu laden** (Cmd+Shift+R / Safari: Website neu laden), HTML-Cache auf GitHub Pages läuft nach ≤10 min aus.
- Reihenfolge in script.js geprüft: `initializeMobileMenu` (Z89) und `initializeSiteMenu` (Z2714) laufen **vor** `initializeNewsCarousel` (Z2718) – ein Carousel-Fehler könnte das Menü nicht brechen (und es gibt keinen).

### Verification
- `index.html`: 3 Artikel, 37/37 div, 5/5 section, endet `</html>`, 530 Zeilen.
- Referenzen des geänderten picture-Blocks prüfen: `Matchday 260926 LSP.webp` → 200 live.
## 2026-09-23 – Alte Portrait-Bilder endgültig entfernt
- `assets/Portrait Poster hellerer Hintergrund.png`, `assets/portrait-poster-neu.png`, `assets/assets/portrait-poster-neu.png` gelöscht (git rm), verschachtelter `assets/assets/`-Ordner entfernt.
- Repo-weit (ohne .kilo/.git) null Referenzen auf alte Bilder; einzige Quellen: CSS Zeile 159 + Export `renderPortraitDataUrl()` Zeile 2462 → `assets/PortraitBild mit hellem Hintergrund23092026.webp`.
- Achtung: Browser-Cache – Seite mit Hard-Reload (Strg/Cmd+Shift+R) neu laden.
