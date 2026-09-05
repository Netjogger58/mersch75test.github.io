# mersch75.lu – To-Do-Liste Homepage

> **Erstellt:** 2026-09-05
> **Status:** Audit abgeschlossen, Fixes noch offen
> **Quellen:** Manueller Audit aller 38 HTML-Seiten + CSS (`styles.css`, 5.913 Zeilen, 29 Media-Queries)

---

## 🔴 P0 – Sofort (Live-Site funktioniert, aber Risk)

| # | Seite | Problem | Aufwand | Priorität |
|---|-------|---------|---------|-----------|
| 1 | `contact.html` | 2 tote Links in Navigation: `matchcenter.html` und `matchday.html` existieren nicht auf Disk | 5 Min | 🔴 |
| 2 | `generator.html` | **Kein `<meta name="viewport">`** → auf Mobile komplett kaputt (Zoom auf 1600px) | 5 Min | 🔴 |
| 3 | `index.html` | News-Karussell `min-height: 380px` fix → auf Mobile und großen Monitoren gleiche Höhe, keine Skalierung | 30 Min | 🟡 |
| 4 | `inside.html` | `.weider-box { min-width: 620px; }` außerhalb Media-Query → horizontaler Scroll auf Tablets (620–900px Breite) | 10 Min | 🟡 |
| 5 | `hallenkarte-editor.html` | Sidebar `width: 360px; flex-shrink: 0;` **null Media-Queries** → auf Phone komplett unbenutzbar | 1 Std | 🟡 |

---

## 🟠 P1 – Bald (sichtbare UX-Probleme auf Mobile/Pad)

| # | Seite | Problem | Aufwand | Priorität |
|---|-------|---------|---------|-----------|
| 6 | `contact.html` | `.contact-title { font-size: 52px; }` hardcoded → nur 1 Breakpoint bei 768px. Besser: `clamp(2rem, 5vw, 3.25rem)` | 10 Min | 🟠 |
| 7 | `contact.html` | 17× `font-size: 12–24px` hardcoded (Labels, Body, Buttons) | 30 Min | 🟠 |
| 8 | `live-center.html` + `live-center-25-26.html` | `#flhIframe { width: 1360px; }` → Landscape auf Mobile bricht aus | 1 Std | 🟠 |
| 9 | `kees-scanner.html` | `.kees-table { min-width: 860px }` erzwingt horizontalen Scroll auf Phone (akzeptabel, aber UX) | 30 Min | 🟠 |
| 10 | `wellkomm-mapp.html` | Print-orientiert (`width: 210mm`) → Mobile nur via `transform:scale`, fragil | 2 Std | 🟠 |

---

## 🟡 P2 – Mittel (Konsistenz, Polish)

### A) Navigation: `events.html` fehlt in den meisten Menüs
Nur `events.html` selbst hat den vollständigen Header. Folgende Seiten verlinken **events.html nicht** in der Top-Nav:
- `index.html`
- `contact.html`
- `news.html`
- `training.html`
- `trainerstaff.html`
- `gallery.html`
- `memories.html`

→ Einheitliche Nav über alle Seiten einbauen.

### B) Redirect-Stubs ohne Nav/Footer
- `history.html` → nur `<meta http-equiv="refresh">` zu `inside.html#history`
- `comite.html` → nur Redirect zu `inside.html#comite`

Beide sind technisch ok, aber Google findet hier "Thin Content". Entweder echte Mini-Pages bauen oder `<meta name="robots" content="noindex">` hinzufügen.

### C) Font-Sizes hardcoded in 11 HTML-Dateien
Insgesamt 17 Vorkommen in `contact.html` + weitere in:
- `hallenkarte.html` / `hallenkarte-editor.html`
- `inside.html`
- `generator.html`
- `live-center.html` / `live-center-25-26.html`

**Ziel:** Alles auf `clamp()` umstellen für flüssige Skalierung.

### D) Karussell (News) responsive machen
Datei: `index.html` Zeile 106–112, `styles.css` Zeile 840–910
- Aktuell: `min-height: 380px` fest, Headlines fix-positioniert
- **Soll:** Höhe relativ zur Viewport-Breite (`aspect-ratio: 16/9` o.ä.), Text-Layer mit `clamp()` für Schriftgrößen, kleinere Bilder-Padding auf Mobile

### E) Hero-Texte (Desktop-Fluid)
Die Hero-Sektionen (z.B. `inside.html`, `index.html`) nutzen teils `font-size: 52px` und ähnliches. Wenn das Browserfenster verkleinert/vergrößert wird, springen die Texte abrupt an den Media-Query-Breakpoints.

**Soll:** `clamp(min, fluid, max)` für:
- H1 / H2 / H3
- Container-Padding
- Button-Größen
- Logo-Größen im Footer

---

## 🟢 P3 – Nice-to-have (langfristig)

| # | Thema | Idee |
|---|-------|------|
| 11 | Container-Querformat | Ein `clamp(1rem, 4vw, 2rem)` Standard-Padding-System für alle Container |
| 12 | Bilder | `loading="lazy"` ist gesetzt, aber `width`/`height` Attribute fehlen → CLS-Probleme |
| 13 | Touch-Targets | Buttons auf Mobile mind. 44×44px (Apple HIG) – aktuell nicht überall erfüllt |
| 14 | Print-CSS | `@media print {}` für `terms.html`, `dataprotection.html`, `impressum.html` |
| 15 | Dark-Mode | `prefers-color-scheme: dark` für die Hauptseiten (Logo, Textfarben) |

---

## 📋 Konkrete Schritte (nächste 1–2 Tage)

### Schritt 1: Schnelle Quick-Fixes (30 Min)
- [ ] `contact.html` Nav: tote Links `matchcenter.html`, `matchday.html` entfernen oder auf echte Seiten umleiten
- [ ] `generator.html`: Viewport-Meta hinzufügen
- [ ] `inside.html`: `min-width: 620px` aus `.weider-box` raus, in Media-Query verschieben

### Schritt 2: CSS-Fluid-System aufbauen (2 Std)
- [ ] CSS-Variablen für Schriftgrößen-Tokens anlegen:
  ```css
  :root {
      --fs-h1: clamp(2rem, 5vw, 3.5rem);
      --fs-h2: clamp(1.5rem, 3.5vw, 2.5rem);
      --fs-body: clamp(0.95rem, 1.5vw, 1.125rem);
      --fs-small: clamp(0.8rem, 1.2vw, 0.95rem);
  }
  ```
- [ ] `contact.html` `font-size: 52px` → `var(--fs-h1)`
- [ ] Andere 16 hardcoded Sizes ersetzen

### Schritt 3: News-Karussell responsive (1 Std)
- [ ] `min-height: 380px` → `aspect-ratio: 16/9` oder `padding-bottom: 50%`
- [ ] Text-Overlay mit `clamp()` für Schriftgrößen
- [ ] Swipe-Geste auf Mobile hinzufügen (falls noch nicht da)

### Schritt 4: hallenkarte-editor Mobile-tauglich (2 Std)
- [ ] Media-Query `@media (max-width: 768px)`: Sidebar als Bottom-Drawer / Toggle-Button
- [ ] `flex-direction: column` auf Mobile

### Schritt 5: Nav-Konsistenz (1 Std)
- [ ] Eine einheitliche Nav-Komponente (Snippet / Server-Side-Include oder Build-Step) für alle Seiten
- [ ] Mindestens `events.html` überall hinzufügen wo es fehlt

---

## 🛠️ Vorschlag: Reihenfolge der Umsetzung

| Woche | Aufgabe | Geschätzter Aufwand |
|-------|---------|---------------------|
| Diese Woche | Schritt 1 + Schritt 2 | 2,5 Std |
| Nächste Woche | Schritt 3 (Karussell) + Schritt 5 (Nav) | 2 Std |
| Danach | Schritt 4 (hallenkarte-editor) | 2 Std |
| Backlog | P2 + P3 | nach Bedarf |

---

## 📊 Audit-Zusammenfassung

- **38 HTML-Seiten** geprüft
- **32/33** haben korrekten Viewport-Meta-Tag (nur `generator.html` fehlt)
- **29 Media-Queries** in `styles.css` (gut ausgebaut)
- **41 `clamp()`-Aufrufe** in CSS (gute Basis, aber ausbaufähig)
- **3 Seiten mit echten Mobile-Problemen** (generator, hallenkarte-editor, inside)
- **0 tote Asset-Referenzen** (alle Bilder/JS/CSS existieren)
- **2 tote Seiten-Links** (matchcenter.html, matchday.html)
- **2 Redirect-Stubs** ohne Nav/Footer (history.html, comite.html)
