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