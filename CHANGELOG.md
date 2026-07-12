# Changelog — mersch75.lu

Kurze, chronologische Liste aller Änderungen. Neueste zuerst.
Format: `Datum · Commit · was & warum`. Details stehen in der jeweiligen Git-Commit-Message.

> Zweck: Dritte (und andere KI) sollen den Stand sofort verstehen und nahtlos weiterarbeiten können.
> Pflege: Bei jeder Änderung **eine Zeile** oben ergänzen. Für den aktuellen Gesamtzustand siehe `Webseiten-Statusbericht.md`.

---

## 2026-07-12
- **Join Us (`join.html`): Officiels-Regel + Alterskategorien geklärt.** Officiels (mat/ouni Lizenz) zahlen **keine Cotisation**, aber **min. 50€ für Stimmrecht auf der AG** (lt. Statuten) — Modal-Liste, Dropdown & `suggestTarif` angepasst. Alterskategorien (Männer, vom Comité bestätigt): U11=2016-2017, U9=2018-2019, **U7=2020-2022** (jüngste offizielle FLH-Kategorie), **U4=2023/2024** (M75-intern, keine FLH-Kategorie, nicht jünger als 2024) = Kidssport; darüber U13=2014-2015, U15=2012-2013, U17=2010-2011, U21=2006-2009, Seniors 1992-2005, Veterans ≤1991. Damen-Bänder parallel gesetzt (FLH-Bestätigung ausstehend). Spiegel-Doku Vereins-OS aktualisiert.
- **Join Us (`join.html`): Tarife 2026-2027 korrigiert.** Neue/korrigierte Werte: Adulte €300, Youth (≤25) €210, Officiels €50, **Kidssport & Loisirs = €10 par unité ou Family Tarif** (auto für U4), **Family Tarif = fix €384**. Aktualisiert in Modal-Liste, Dropdown, `suggestTarif`. FLH-Alterskategorien um +1 Jahr auf 2026-2027 verschoben + U4 (Jg. 2022+) ergänzt. Spiegel-Doku Vereins-OS `docs/join-to-sheet-automation-f4cdcc.md` angepasst.

## 2026-07-11
- **Join Us (`join.html`): Cotisatioun 2026-2027 komplett umgestellt.** Tarif-Liste im Modal + Formular-Dropdown + Auto-Logik (`suggestTarif`) + Family-Label + Saison-Labels/Karten-Texte (alle „2025-2026" → „2026-2027"). Neue Tarife: Adulte €300, Youth (≤25) €210, Kidssport & Loisirs €50, Officiels €50, Family Tarif (Formel). Auto-Vorschlag: >25 = Adulte, ≤25 = Youth, Officiel/Arbitter/Bénévole+Lizenz = €50, Family-Flag = Family; Kidssport & Loisirs nur manuell. Alte Optionen (€100/€200/€250, honoraire, Donateur) entfernt. Spiegel-Doku in Vereins-OS `docs/join-to-sheet-automation-f4cdcc.md` mit angepasst. (Fee-Rules-DB im M75-Manager ist leer → dort nichts zu ändern.)
- **Comité (`inside.html`) aktualisiert:** Armand Kremer & Philippe Kremer entfernt; Vizepräsident = „(nach net besat)"; Buvette-Rollen Koordinatioun/Entréeskeess = „(net besat)"; Festivitéiten nur noch Jeff Schuster; Sponsoring ohne Armand. Neu: Charles Epps (1. Ekipp Männer) & Xavier Maquil unter „Weider Memberen".
- **Trainerstaff: Team-Übersicht Saison 2026-2027** oben auf `trainerstaff.html` ergänzt (Team → Trainer, inkl. Golkiipertrainer). Bio-Karten darunter unverändert. CSS-Block „Trainerteams-Iwwersiicht" + `styles.css?v=20260711trainers`.

## 2026-07-08
- `6f08f9d` **AG-Slide: 2 Boxen statt einem Bild-Link.** Banner bleibt als Bild; darunter Box 1 „Umellen" (öffnet Anmelde-Popup) + Box 2 „Procuration ausdrécken" (öffnet PDF). PDF nach `assets/shared/media/Hauptseite/Procuration-AG-2026.pdf` verschoben (ASCII-Name gegen URL-Encoding-Probleme). CSS `styles.css?v=20260708box1`.

## 2026-07-06
- `654fd0f` **Deploy-Retrigger** (leerer Commit) — Pages-Build hing.
- `0b94d9e` **AG-Banner aktualisiert** auf `AG Mersch75 10072026.png` (neues 50-Joer-3D-Logo, Datum 10.07.2026).
- `d4e18f6` **`.nojekyll` hinzugefügt** → zuverlässigerer statischer Deploy + Build-Retrigger.
- `ef0d108` **AG-Mailbutton mit Kopier-Fallback** — `mailto` funktioniert nicht ohne Standard-Mailprogramm; jetzt wird der komplette E-Mail-Text in die Zwischenablage kopiert + Hinweis. `script.js?v=20260706ag2`.
- `70046fb` **AG-Umeldung als Popup/Modal** (`#agModal`) mit sichtbarer Adresse `info@mersch75.lu`, Kopier-Button + „Per E-Mail umellen".
- `582d5fc` **AG-Banner 2026 ins News-Carousel** + `mailto`-Umeldung.

---

## AG-Feature (aktueller Stand & Wo weiterarbeiten)

**Betroffene Dateien** (Änderungen sind in `index.html` UND `news.html` identisch zu halten):
- `index.html` / `news.html` → AG-Slide: `<article class="news-slide-ag">` mit blauer Textbox (`events-copy`) + `div.news-ag-media` (Banner + 2 Boxen).
- `script.js` → `initializeAgModal()` (Popup öffnen, Adresse/Text kopieren mit `execCommand`-Fallback). Trigger = Elemente mit Klasse `.news-ag-link`.
- `styles.css` → Blöcke „AG-Umeldung Modal" und „AG-Slide: Banner + zwee Aktioun-Boxen" (am Dateiende).

**Automatisches Ablaufen:** `data-news-expires="2026-07-10T23:59"` sitzt auf `div.news-ag-media`. Nach dem 10.07.2026 entfernt das Carousel-JS nur diesen Block (Banner + beide Boxen); die blaue Textbox + Hintergrundbild bleiben (gewünschtes Verhalten).

## Wichtige Hinweise für den nächsten Bearbeiter / KI
- **Hosting:** GitHub Pages, Branch-Deploy (kein Actions-Workflow), Custom-Domain `mersch75.lu` (`CNAME`).
- **Deploy hängt gelegentlich:** Wenn eine Änderung nach ein paar Minuten nicht live ist, mit einem leeren Commit neu anstoßen: `git commit --allow-empty -m "chore(pages): retrigger" && git push`.
- **Cache-Busting:** `styles.css`/`script.js` werden in HTML mit `?v=JJJJMMTTkennung` referenziert. Bei CSS/JS-Änderungen die Version in `index.html` **und** `news.html` erhöhen.
- **Live-Check (Beispiel):** `curl -s -o /dev/null -w "%{http_code}" "https://mersch75.lu/<pfad>"`.
