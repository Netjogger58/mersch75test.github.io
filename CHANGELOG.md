# Changelog — mersch75.lu

Kurze, chronologische Liste aller Änderungen. Neueste zuerst.
Format: `Datum · Commit · was & warum`. Details stehen in der jeweiligen Git-Commit-Message.

> Zweck: Dritte (und andere KI) sollen den Stand sofort verstehen und nahtlos weiterarbeiten können.
> Pflege: Bei jeder Änderung **eine Zeile** oben ergänzen. Für den aktuellen Gesamtzustand siehe `Webseiten-Statusbericht.md`.

---

## 2026-07-27
- **Cleanup & Saison-Update.** Al Backups geläscht: `joinx.html`, `generatorold.html`, `generator.html.bak-logofix`. `generator.html` Saison-Referenze vun 2025/26 op 2026/27 aktualiséiert. `kees-scanner.html` erkennt elo och "COTISATIOUN 2026-2027" nieft der aler 2025-2026.
- **Vereins-OS-App (interna) — Sprooch, Sortéierung & Data Hygiene.** Sprooch-Ableedung aus Nationalitéit (LU→lb, DE→de, FR→fr, EN→en, Default→fr) bei Member-Créierung + Nightly Auto-Fix (547 Memberen fixt). Wöchentlechen Data Hygiene Report per E-Mail un Admins all Samschdes. Alphabetesch Sortéierung als Default am Secretariat. Default Saison am Matches-Page op 2026-2027 aktualiséiert.

## 2026-07-15
- **Vereins-OS-App (umgesetzt) – Vereinfachten Prouftraining-Input in der Anwesenheit.**
  - Statt einer langen Dropdown-Liste aller Mitglieder bekommt der Trainer ein einheitliches Formular mit: Vorname, Nachname, Geburtsdatum, Handynummer (optional) und den letzten 5 Ziffern der KV-Karte (optional).
  - Bei bekanntem Namen + Geburtsdatum wird der existente Member sofort als Prouftraining für den aktuellen Tag/Team eingetragen (funktioniert für alle Aufsteiger-Kombinationen: U7↔U9, U13↔U15, Jugend↔Senioren, Frauen↔Männer).
  - Falls der Spieler nicht in der Datenbank ist, kann der Trainer wählen:
    - als **neuen Member mit Status `pending`** anlegen (wird vom Sekretariat validiert), oder
    - nur als **temporären Training-Gast** für den aktuellen Tag erfassen.
  - Spieler, die regulär in einer höheren Kategorie trainieren (`extraTeamIds`), erscheinen automatisch in der Suche.
  - Ziel: Trainer müssen nicht mehr auf KI warten, um neue oder spontane Spieler in eine Trainingseinheit einzutragen.

## 2026-07-15
- **Vereins-OS-App (intern) – Nominatiounen, Aufsteiger-Teams & Prouftraining.**
  - **Nominatiounen / Teams / Anwesenheet:** Memberer ginn iwwerall (Teams, Anwesenheet, Nominéierungen) no deem selwechte System sortéiert: Médico-Problemer (`inapte`, `overdue`, `keen Médico`) no ënnen, Alter (Jugend alt→jung, Senioren jung→alt), alphabetesch als Fallback.
  - **Aufsteiger-Teams (extraTeamIds):** Jugend-Spiller kënnen elo zu méi héije Kategorien agesat ginn. An der Team-Détail-Lëscht gëtt et fir all Jugend-Spiller 1–2 Checkboxen (z.B. U7→U9, U9→U11, U11 Espoir→U11 Elite a U13, U13→U15). Wann ugewielt, kënnt de Spiller och an där héijerer Ekipp nominéiert ginn. Gilt och an der Anwesenheet.
  - **Nominatioun-Boost:** Memberer, déi fir e kommende Match schonn nominéiert sinn, ruckelen an Teams/Anwesenheet automatesch no uewen.
  - **Prouftraining (isTrial):** An der Anwesenheet kann een elo manuell neie Spiller anerakommen (z.B. Jugend-Spiller déi eng Kategorie méi héich trainéieren). Si kréien de Status „Prouftraining". Soubal se eng Lizenz hunn, gëtt den Haken ewechgeholl a d'Trainingszählung gët normal gezielt.
  - Member-Detail krut eng nei Käerzeg „Zousätzlech Teams"; Backend krut nei Endpunkten (`/api/nominations/team/:id`) an nei Datenbankspalten (`extra_team_ids`, `attendance.is_trial`).

## 2026-07-14
- **Image-Optimierung: WebP/AVIF + Lazy-Loading + `<picture>`-Fallback.** Node-Skript `tools/convert-images.mjs` konvertéiert all PNG/JPEG/WebP/AVIF-Originaler (ausser `.git`, `node_modules`, `sbo-archiv`, `tools`) an WebP- an AVIF-Varianten, generéiert `<picture>`-Elementer mat `<source srcset>` fir AVIF/WebP a setzt `loading="lazy"` (Hero-Biller op `index.html` kréien `loading="eager"`). 974 Biller veraarbecht, 26 HTML-Säiten aktualiséiert, korrupte `Yamas.png` geläscht. Dokumentatioun: `docs/image-optimization.md`.
- **Inside-Seite (`inside.html`): Statuten-Badge Layout gefléckt.** CSS-Selektoren `> img` op `> picture > img` erweidert, nodeems d'Konvertéierungs-Script d'Biller an `<picture>`-Wrapper gesat huet – d'Statuten-Logo iwwerdeckt net méi dat drënnerläit Comité-Logo.
- **FLH Statistik-Archiv.** FLH-Donnéeën (Spillplang + Tabellen) an `data/flh-archive-2627.json` an `data/flh-archive-2526.json` exportéiert, esou datt si lokal verfügbar bleiwen, och wann d'FLH hir Donnéeën ewechhëlt. Neit Node-Skript `tools/flh-archive.mjs` fir den Export. SBO-PDFen an `sbo-archiv/2627/` a `sbo-archiv/2526/` erofgelueden (137 Stéck pro Saison) mat Index an `data/sbo-index-2627.json` / `data/sbo-index-2526.json`. `js/flh-live-sync.js` erweidert: `loadArchive(season)`, `loadSboIndex(season)` a `resolveSboLink()`. `live-center.html` a `live-center-25-26.html` lueden d'Archiv am Hannergrond, benotzen et als Fallback, a leeden SBO-Linken op lokal PDFen ëm. Cache-Bust `flh-live-sync.js?v=20260714a`.

## 2026-07-13
- **Training (`script.js` / `training.html`): Hotspots + Trainingsplan v130726.** Trainingsplan-Bild elo **`assets/Entrainements-2026-2027-130726.png`** (näischten Upload, 13.07.2026). Hotspots nees an d'nei Biller ugepasst: **U13F Méindes 17:30–19:00** (korrigéiert Zäit), U7 Fréng 16:30–17:00, U11 Freides 17:00–18:30, U13G Méindes 17:30–18:30 / Mëttwoch 19:00–20:00, U15 Méindes/Freides 19:00–20:00, Filles Fréng 16:30–17:00, Hommes Box-Breeten a Positiounen ugepasst. Duplizéiert Fichier `assets/Entraînements2026:2027 13072026.png` mat Doppelpunkt geläscht. Cache-Bust op **alle Säiten** op `script.js?v=20260713sched4` synchroniséiert.
- **News & Startseit (`news.html` + `index.html`): Save-the-Date-Slide 20.09.2026** synchroniséiert.

## 2026-07-12
- **Training (`script.js` / `training.html`): Hotspot-Boxen fein justéiert + Text-Fix.** Boxen pro Kolonn (lénks→riets) ëm **1 Zell (30 Min = 3.77 %)** no uewen/ënnen verréckelt: Kol. A U13G↑/Hommes↓, Kol. B U9↑, Kol. C U7↑, Kol. D U11↑/U13G↑, Kol. E U9↑, Kol. F Filles-Box no uewe **vergréissert**, Kol. G U7↑/U11↑/U15↑/Hommes↓, Kol. H U4↑. **„Probetraining ufroen" → „Prouftraining ufroen"** (lb-Iwwersetzung + HTML-Fallback; däitsch bleift „Probetraining anfragen"). Cache-Bust op alle Säiten: `script.js?v=20260712sched2` (spéider op `20260713sched4` aktualiséiert).
- **Training (`training.html`): Trainingsplan-Bild `Entraînements 2026_2027.png` mam korrigéierten Inhalt ersat** (selwechten Dateinumm, keng URL-Ännerung); onbenotzt Backup `...2026_2027old.png` aus dem Repo geläscht.
- **Inside (`inside.html`): Follow-up.** M75-CA-Icon op déi nei Versioun **`Logo-Menu-Mersch75-M75-CA-2026.png`** (den ale 2025 war gecacht). Armand **komplett aus dem Lobby-Beräich** vum Zielorganigramm eraus (Lobby Politik, Lobby Sport a Kolonn-Iwwerschrëft „Strat. / Lobby / Aussendarst." = elo nëmmen Jeff); bleift bei Akquise/Spenden.
- **Inside (`inside.html`): Header ëmgebaut + neie passwuert-geschützten „Projet Comité an Helperteams" (Zielorganigramm).** Inside-Icon elo eleng/gréisser (`min(320px,78vw)` wéi JoinUs-Hero); M75-CA-Icon méi kleng (220px) + lénks vertikal zentréiert zur Iwwerschrëft „Executive & Organisatioun" via `.exec-band`, Statuten-Badge onverännert. Nei klickbar Dept-Box **„Projet Comité an Helperteams / Divers"** (Icon `Projekt-Neie-Comite.png`) nieft Trainer & Supervisors → freet Passwuert **„M75"** (sessionStorage) a weist dann d'**Zielorganigramm** (Matrix aus `assets/Zielorganigramm.rtf`, `zo-`-scoped CSS). Korrekturen am Chart: Armand **net** méi Vize-Präsident (bleift bei Akquise/Spenden), Sportl. Leitung HERREN = **Charly (Charles Epps)**, nei **Teamchef Senioren = Sacha Marzadori**, GT Comm. & Sponsoring = **Max Blanc**, Xavier Maquil bei Wechsel/Leihe. Hiweis: client-säiteg Passwuert, net wierklech sécher.
- **Trainerstaff erweidert + Grégory/U4 korrigéiert.** Grégory Redavid ass **net méi U4**, mä **Teambegleeder U11** (mam Laurent Metzler) — Kaart + Tooltip ugepasst. **U4 = Gina Dimola & Kevin Wolmering** (Tooltip u4 ugepasst). Nei Bio-Boxen (Numm + Roll, Beschreiwung follegt): **Gina Dimola, Kevin Wolmering, Kim Eich, Jo-Anne Leisen, Tim Beneke, Wendy Skovgaard (Golkiipertrainer), Sacha Marzadori**.
- **Training-Plan Hotspots + Trainerstaff korrigéiert.** Boxen nei berechent, datt se **iwwer den Teamnimm-Text** vun de faarwege Bléck leien (U13F/U11M-brong Bléck ufänken elo richteg um 17:00/16:30, U15G/HO/HOMMES-Bléck ënnen ugepasst, Filles nëmmen 16:30-17:00). Laurent Metzler ass **net méi Teamchef 1. Härenekipp** (= Sacha Marzadori) → Bio-Kaart elo „Teambegleeder U11". Christophe Kremer (Foto + Text) komplett aus `trainerstaff.html` an aus den U4-Traineren am `script.js` ewech. École-Hal Tooltip = „Schoulsporthal Lintgen". Cache-Bust `script.js?v=20260712box`.
- **Training-Logo aktualisiert** auf `Logo-Mersch75-TeamTraining-12072026.png` (fehlerbereinigte Version): Hero-Logo in `training.html` **und** Menü-Icon in `wellkomm-mapp.html` (p8-Liste). Altes `-26092025.png` wird nicht mehr referenziert.
- **Bewäertung/Feedback-Widget komplett entfernt.** Das dezente, lokal gespeicherte Bewertungs-Widget wird nicht mehr geladen: `initializeFeedbackSystem()` (Funktion + Aufruf) aus `script.js` entfernt → auf allen öffentlichen Seiten weg. `feedback.js`/`feedback-config.js` bleiben nur für die interne Auswertung `feedback-intern.html` erhalten. Cache-Bust: alle Seiten auf `script.js?v=20260712nofb`.
- **Training (`script.js`): Interaktive Hotspots komplett auf 2026-2027 neu aufgebaut.** 11 Teams (U4M, U7M, U9M, U11M, U13F, U13G, U15, Filles, Femmes, Hommes, Loisir) mit korrekten Tagen/Zeiten/Hallen (Tooltip) in 5 Sprachen. Box-Positionen aus dem neuen Bild per Gitter-Vermessung exakt gesetzt (Spalten 7.34-99.44%, Zeitraster ab 09:00=23.92%, 30min=3.77%). Hallen sauber getrennt: Gare (50 rue de la Gare) vs. École/Schoulsportshal (4 rue de l'Ecole). Laurent Metzler nicht mehr Trainer (jetzt Spieler) → aus Hommes entfernt; Trainer-Zeile im Tooltip nur noch bei vorhandenem Namen. `script.js?v=20260712sched`.
- **Training (`training.html`): Trainingsplan-Bild ersetzt** durch `assets/Entraînements 2026_2027.png` (Alt-Text „Trainingsplan 2026-2027"; altes Bild entfernt).
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
