## Generator – Coupe als eigener Postermodus – 2026-09-25
- Coupe-Spiele werden im Landscape-Poster nicht mehr zusammen mit Meisterschafts-/Season-Games gerendert; sobald mindestens ein sichtbares Coupe-Spiel vorhanden ist, gilt der separate Coupe-Zweig.
- Reihenfolge im Coupe-Zweig bleibt Frauen – Männer – U15; die Spielart-Checkbox „Coupe“ gilt weiterhin für beide Vorschau- und Exportlogik.
- Der Pokal ist kein globales, absolut positioniertes Element mehr, sondern wird relativ im blauen U15-Coupe-Block mittig über dessen Badge/Titel erzeugt und verkleinert dargestellt.
- Entfernt wurde die alte globale Trophy-Positionierung; das bestehende Coupe-Asset bleibt `assets/Coupe de Luxembourg2026.webp`.


## Agent 11 – Strukturierung & Cleanup – 2026-09-25
## Generator – Coupe-Spiele integriert – 2026-09-25

- `generator.html`: Separate Schaltfläche „Coupe dieses Wochenende laden“ ergänzt.
- `js/flh-live-sync.js`: Coupe-Kategorien (`H-C-LN`, `D-C-LN`, `H-C-FLH`, `U15G-C`, `U13M-C`) liefern gemeinsam `COUPE:`-markierte Spiele an den Generator.
- Generator trennt Coupe- und Championship-Spiele beim Wochenende-Laden; Coupe-Spiele werden in den magischen Scanner mit Kategorie `Coupe` und passender Mannschafts-ID (`s1`, `fe`, `u15`, `u13p1`) übergeben.
- Bestehende Championship-/M75-Daten bleiben unverändert und werden nicht ersetzt.
- Syntaxprüfung für `js/flh-live-sync.js` und alle Inline-Skripte in `generator.html` sowie `git diff --check` erfolgreich.


## Generator – Sichtbarkeit der Posterbereiche – 2026-09-25

- Checkboxen im LS-/Landscape- und Portrait-Poster ermöglichen, einzelne Mannschaften/Spielblöcke ein- oder auszublenden.
- Auswahl wird unter `mersch75-generator-poster-visibility-v1` im Local Storage gespeichert und beim Neuladen wiederhergestellt.
- Landscape-Rendering berücksichtigt die Checkboxen auch im Coupe-Zweig; die feste Reihenfolge Frauen – Männer – U15 bleibt erhalten.
- Portrait-Haupt- und Zusatzspiele verwenden dieselbe Checkbox-Auswahl; Vorschau und Export folgen der Auswahl.
- Syntaxprüfung aller Inline-Skripte, FLH-Sync-Prüfung und `git diff --check` erfolgreich.


## Generator – Pokalposition LS-Poster – 2026-09-25
- Coupe-Pokal im LS-/Landscape-Poster aus der mittigen Position entfernt.
- Rechts mittig über dem U15-Spiel platziert und von 230×290 px auf 300×375 px vergrößert.
- Asset-Pfad `assets/Coupe de Luxembourg2026.webp` geprüft; Vorschau-/Export-Logik unverändert.
- `node --check` für FLH-Sync und Inline-Skripte sowie `git diff --check` erfolgreich.


- Homepage-Navigation inventarisiert und eine rückwärtskompatible Zielstruktur unter `docs/structure/pages/` dokumentiert.
- Kategorien für Home, Live-Center, Training, Club, News, Community, Media, Kontakt/Service, Rechtliches, Verwaltung und Shared angelegt.
- Aktive Root-Dateien nicht verschoben: GitHub Pages liefert aus dem Root aus und die bestehenden URLs/Referenzen wären sonst gebrochen.
- `hallo_agent11.txt` erstellt; Struktur-Dokumentation und Verzeichnisse validiert.

## Agent 10 – i18n & Mehrsprachigkeit – 2026-09-25

- Sprachmatrix für LB/FR/DE/EN/PT geprüft; `misc-i18n.js` enthält die neuen Galerie-, Memories- und Legal-Schlüssel in allen fünf Sprachen.
- `script.js` um `navMemories` in allen fünf Sprachpaketen ergänzt; dynamisches Agent-4-Menü enthält jetzt `memories.html` neben `gallery.html` und aktualisiert Labels beim Sprachwechsel.
- Fallback-Kette in `script.js` implementiert: gewählte Sprache → LB → FR → EN → DE → PT; unbekannte Sprachwerte werden auf LB normalisiert.
- `gallery.html` und `memories.html` starten mit korrektem `lang="lb-LU"`; Sprachwechsler aktualisiert das `html.lang` zur Laufzeit.
- `hallo_agent10.txt` erstellt; i18n-Syntax- und Diff-Prüfung erfolgreich.


## Agent 9 – Performance & Asset-Optimierung – 2026-09-25

### 1. Bild-Optimierung (LCP/CLS)
- Bestand: 232× WebP + 207× AVIF bereits modern; 131× PNG / 66× JPG bleiben nur dort, wo sie aktiv referenziert sind (keine Duplikate angelegt, keine Dateien umbenannt — AGENTS.md-konform).
- `picture`-Elemente mit AVIF→WebP→PNG-Fallback existieren bereits (z. B. Ball, Teamfotos, Zesumme-Staark-Logo in `news.html`).
- LCP (Hero-Poster `index.html`): `fetchpriority="high"` + `decoding="async"` auf Hero-`<img>` (statisch + dynamisch via `setPoster()` neu erzeugtes Bild) + `<link rel="preload" as="image">` für `Matchday 260926 LSP.webp`.
- `loading="lazy"` nachgerüstet: `join.html` (2× unterhalb Viewport: Memberskaart-Modal, Footer-Logo; Hero-Logo bewusst `eager`), `statistics-25-26.html` (4× JS-generierte Kids-Teamfotos), `news.html` (alle Feed-Cards unterhalb der ersten auf `lazy` + `decoding="async"`; nur NEXTGEN-Hero bleibt `eager`).
- CLS: neue Regel `.news-card-bg, .news-card-poster { aspect-ratio: 16/9 }` in `styles.css` reserviert Bildplatz vor dem Laden. Hero-`.news-card-hero` hatte bereits `aspect-ratio: 16/9`.
- Korrigiert: falscher MIME-Typ `type="image/avif"` auf einer `.webp`-Source im dynamischen `setPoster()` entfernt (verhinderte ggf. Preload-Miss).
- `generator.html`-Canvas-Bilder bewusst ohne `loading` (Export-Logik, `crossorigin` nötig) — nicht angefasst.

### 2. DOM-Reduzierung (konservativ, kein Risiko)
- CSS-Klassen-Scan (449 definierte Klassen): 69 nur 1× gefunden — fast alle sind JS-Toggles (`is-open`, `menu-open`), seitenweite Klassen oder i18n-Ziele → **keine Klasse gelöscht** (Löschen wäre DRY-Verstoß-Risiko ohne RUM-Daten).
- Stattdessen: 1 toter HTML-Kommentar (zeitgesteuerte Slide-Vorlage in `index.html`, historisch überholt) — bewusst BEHALTEN, da aktive Dokumentation für Redakteure. Keine auskommentierten Legacy-Blöcke in `styles.css` (nur 1-zeilige Sektions-Header).
- Echte Redundanz entfernt: doppelte AVIF-`<source>`-Zeile auf `.webp`-Datei im `setPoster()`-JS (siehe oben).

### 3. Caching-Logik
- `generator.html` Portrait-Hintergrund: CSS-`background:url(...)` + JS-Preload `bg.src` bekamen Cache-Buster `?v=20260925a9` → neue Hintergrunddatei erscheint ohne Hard-Reload; Version bumpbar pro Poster-Update.
- `index.html` Poster-Refresh (`#poster-set-btn`): nutzt bereits `?t=Date.now()`-Buster auf beiden Orientierungen (Portrait + Landscape) — verifiziert, unverändert korrekt.
- JS/CSS-Buster (`script.js?v=...`, `styles.css?v=...`) seitenweit vorhanden — unverändert.

### Verification
- `git diff --check` sauber; `loading=`-Counts: index 16 / news 16 / join 5 / stats 3→7; alle geänderten `src` lösen auf Disk auf.
- `hallo_agent9.txt` = `Cline ist startklar!` ✓
- Commits: `perf(...)` (Bilder/LCP/CLS) — PSD `assets/Unbenannt-1.psd` (13 MB) bewusst NICHT committet.

---

## Agent 8 – Git-Management & Konfliktauflösung – 2026-09-25

### Konfliktanalyse
- `git status`: uncommittet waren `gallery.html`, `misc-i18n.js`, `memory-bank/progress.md` (Agent-6-Arbeit) + untracked `assets/Unbenannt-1.psd` (13 MB, NICHT committet), `hallo_agent6.txt`.
- Konfliktmarker-Scan (`<<<<<<<`/`>>>>>>>`/`=======`) in `generator.html`, `index.html`, `script.js`, `styles.css`: **0 Treffer — keine Merge-Konflikte**.
- `git diff --check`: sauber (keine Whitespace-Fehler). Keine unmerged Pfade (`git ls-files -u` leer), kein Stash, Branch `main` synchron mit `origin/main`.
- Code-Zusammenführung: nichts zusammenzuführen nötig — `generator.html`/`index.html`/`script.js`/`styles.css` sind unverändert gegenüber HEAD (`a445abc`); parallele Agenten-Änderungen (Galerie/i18n) überschneiden sich nicht mit Generator/Carousel/Live-Center/Menü.

### Commit-Struktur (atomar)
- `ffb583b feat(gallery): Mannschaftsbilder-Bereich Saison 25/26 + i18n (Agent 6)` — `gallery.html`, `misc-i18n.js`, `hallo_agent6.txt`.
- Folgend: `chore(agent8): Git-Status verifiziert + hallo_agent8.txt` — dieser Eintrag + `hallo_agent8.txt`.
- Bewusst NICHT committet: `assets/Unbenannt-1.psd` (13 MB Arbeitsdatei, kein Deployment-Asset).

### Deployment-Check (GitHub Pages)
- `CNAME` = `mersch75.lu` ✓, `.nojekyll` vorhanden ✓, `index.html` im Root ✓.
- Kein `.github/workflows/` nötig (Pages via Branch-Deploy); kein Buildschritt (statisches HTML/CSS/JS).
- `index.html`-Referenzen: lokale `src`/`href` lösen auf (`?v=`-Query ausgenommen, ok); externe Links (flh.lu, Social, ehftv) unverändert.
- Validierung: `node --check misc-i18n.js` OK, `gallery.html` HTML-Parse OK, alle 14 `src` auf Disk (2× `?v=`-Cache-Buster ausgenommen = erwartet).
- `hallo_agent8.txt` = `Cline ist startklar!` ✓

---

## Agent 6 – Galerie-Ordner + Mannschaftsbilder – 2026-09-25

### Aufgabe
1. Auf `gallery.html` einen Folder/Bereich für Mannschaftsbilder anlegen (Bilder der Equippen einsetzen können).
2. Zusatz: `hallo_agent6.txt` im Root mit Inhalt `Cline ist startklar!`.
3. NICHT anfassen: `generator.html`, `live-center.html`, `_carousel_clean.py`, `js/flh-live-sync.js` (Generator-Bildkoordination daher bewusst NICHT umgesetzt — Eingriff wäre gegen die Vorgabe).

### Umsetzung
- Neuer Ordner `assets/pages/gallery/` (Repo-Konvention: page-spezifische Assets; keine Duplikate — Teamfotos bleiben Single-Source in `assets/shared/media/Ekippe Fotoen Saison 25-26/`, Galerie referenziert sie nur).
- `gallery.html`: neue responsive Sektion `gallery-teams` (Badge/Titel/Beschreibung + 9 Karten FE/H1/U15/U13/U11/U11-Espoir/U9/U7/U4, `loading="lazy"`, Grid 3→2→1 Spalten). Bestehende Coming-soon-Karte bleibt erhalten.
- `misc-i18n.js`: neue Keys `galleryTeamsBadge/Title/Desc` in allen 5 Sprachen (lb/fr/de/en/pt), an bestehende `galleryBadge/Title/Desc` angehängt.

### Verification
- `node --check misc-i18n.js` + `node --check script.js` OK; HTML-Parse OK.
- Alle 14 `src`-Referenzen in `gallery.html` lösen URL-dekodiert auf Disk auf (0 missing).
- `hallo_agent6.txt` = `Cline ist startklar!` ✓
- `git status`: nur `gallery.html`, `misc-i18n.js` modifiziert + `assets/pages/gallery/`, `hallo_agent6.txt` neu; Generator/Live-Dateien unberührt.

---

## NEXTGEN-Slide + Menü-Fix – 2026-09-25

### Aufgabe
1. `Media/Hauptseite/Nextgen Poster.webp` (3548×1787, Landscape) als neuen Carousel-Slide in `index.html` **und** als Karte in `news.html` einbauen, Klick → `nextgen.html`. Poster an Carousel-Dimensionen anpassen, nicht umgekehrt.
2. Menü-Button („Menü" klick → nichts geschieht) reparieren.

### Umsetzung
- Poster-Datei als Repo-Asset aufgenommen: `Media/Hauptseite/Nextgen Poster.webp` (`git add`), referenziert als `Media/Hauptseite/Nextgen%20Poster.webp`.
- `index.html`: neuer erster Slide `news-slide-nextgen` mit `<a class="news-slide-link" href="nextgen.html">` um das Poster-Bild. Bild nutzt bestehende Carousel-Geometrie (`flex: 0 0 100%`, `min-height: clamp(240px, 36vw, 390px)`) + neu `object-fit: contain` (Klassen `.events-background-contain`/`.news-nextgen-image`, Link-Block `.news-slide-link`) → Poster passt sich der Box an.
- `news.html`: neue Karte `<a class="news-card news-card-link news-slide-nextgen" href="nextgen.html">` vor der Hero-Karte, mit `.news-card-link` (Block, ohne Deko) + `.news-card-bg-contain` (`object-fit: contain`) in `styles.css`.
- `KEEP` in `_carousel_clean.py`/`_clean_v2.py` um `news-slide-nextgen` ergänzt → Skript: `Keeping: 3 / Removing: 0`, exit 0.
- Menü-Root-Cause: **2 konkurrierende Click-Handler** auf `.nav-toggle` – `initializeMobileMenu()` (Zeile 89, toggelt nur `.site-nav.is-open`) und `initializeSiteMenu()` (Zeile 2714, toggelt `.site-nav.is-open` + `.site-menu-backdrop.is-open` + `body.menu-open`) hoben sich gegenseitig auf → Klick = No-Op. **Fix:** doppelten Toggle-Handler aus `initializeMobileMenu()` entfernt (nur ESC-Schließlogik bleibt); Öffnen/Schließen läuft ausschließlich über `initializeSiteMenu()`.

### Verification
- `node --check script.js` OK; lokaler Server + headless Chrome: `site-menu-shell/-primary/-secondary/-close/-backdrop` vorhanden, simulierter Menü-Klick → `CLICKRESULT:OPEN-OK|aria=true|backdrop=1|body=true`, keine JS-Fehler.
- `index.html`: 3 `<article>` (nextgen/coupe-fe/ag), divs 35/35, endet `</html>`; `nextgen.html` live HTTP 200.

---

## Floumaart-Slide entfernt (index.html) – 2026-09-25

### Aufgabe
Slide mit Floumaart-zu-Schous-Poster (blauer Kasten, „Mir sinn dobäi!!") aus dem News-Carousel entfernen.

### Umsetzung
- `<article class="… news-slide-floumaart …">`-Block (inkl. Bild `assets/shared/media/Floumaart zu Schous.webp`) aus `index.html` entfernt → Carousel hat jetzt **2 Slides** (`news-slide-coupe-fe`, `news-slide-ag`). Datei-Bild bleibt auf Disk erhalten; `news.html` nutzt es weiterhin (5 Treffer dort, bewusst nicht angefasst).
- Zugehörige, nun verwaiste CSS-Regeln in `styles.css` entfernt (7 Block-Regeln: Desktop-Block + Mobile-Media-Query) → 0 Treffer `news-slide-floumaart` in `index.html`/`styles.css`.
- `KEEP`-Listen in `_carousel_clean.py` und `_clean_v2.py` auf `{'news-slide-coupe-fe', 'news-slide-ag'}` aktualisiert (Guard bleibt konsistent: Skriptlauf = `Keeping: 2 / Removing: 0`, exit 0).

### Verification
- `index.html`: 2 `<article>`, divs 35/35, sections 5/5, endet mit `</html>`.

---

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

## FLH-Cup-Synchronisierung (Agent 13)
- `js/flh-live-sync.js` lädt zusätzlich die aktuellen Coupe-Klassen der FLH: H-C-LN, D-C-LN, H-C-FLH, U15G-C und U13M-C.
- Coupe-Spiele werden als markierte Datensätze in den bestehenden Live-Sync aufgenommen; der Bereich „Coupe“ in `live-center.html` ersetzt seine bisherigen statischen Platzhalter durch die aktuellen FLH-Daten, sofern welche geliefert werden.
- Bestehende statische Coupe-Einträge bleiben als Fallback erhalten, wenn die FLH-Schnittstelle nicht erreichbar ist.
- Validiert mit `node --check` und `git diff --check`.



## 2026-09-25: Coupe-Poster und LS-Poster
- Drei Coupe-/Senior-Spiele werden im Landscape-Poster nebeneinander in drei gleich breiten Spalten dargestellt.
- Das Desktop-Asset `Coupe de Luxembourg2026.png` wurde als optimiertes WebP nach `assets/Coupe de Luxembourg2026.webp` übernommen.
- Der Pokal ist im Landscape-/LS-Poster zentriert über dem Spielbereich eingebunden und für den Canvas-Export mit `crossorigin="anonymous"` markiert.
- Bestehende Ein-Spiel-Zentrierung und Spiellogik bleiben erhalten.
