# Mersch75 Website Structure

Die Website wird direkt aus dem Repository-Root auf GitHub Pages ausgeliefert. Aktive Root-Dateien bleiben deshalb an ihrem bestehenden Ort; eine Migration würde die öffentlichen URLs brechen.

## Homepage-Navigation

- Home: `index.html`
- Live-Center: `live-center.html`, `live-center-25-26.html`
- Training: `training.html`, `trainerstaff.html`, `probetraining.html`
- Club: `inside.html`, `comite.html`, `history.html`
- News: `news.html`
- Community: `community.html`, `nextgen.html`, `join.html`
- Media: `gallery.html`, `memories.html`
- Kontakt/Service: `contact.html`, `hallenkarte.html`, `links.html`, `qr.html`
- Rechtliches: `impressum.html`, `terms.html`, `dataprotection.html`
- Verwaltung: `generator.html`, `feedback-intern.html`, `hallenkarte-editor.html`, `kees-scanner.html`

Neue Seiten-Assets gehören nach `assets/pages/<seite>/`, gemeinsame Assets nach `assets/shared/`. `Media/` bleibt als Legacy-Eingangsbereich erhalten, bis alle aktiven Referenzen atomar migriert wurden.
