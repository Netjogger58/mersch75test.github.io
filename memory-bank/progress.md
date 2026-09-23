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