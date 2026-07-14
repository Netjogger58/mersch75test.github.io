# YouTube-Video-Script: Mersch75.lu – Websäit fir Dummies

Dëst Script passt zum [Dummies-Guide](website-arbeiten-fuer-dummies.md). Jiddwer Szene huet **Sprechtext** an **Screenshot-/Video-Hinweiser**. D'Video kannst du an **einem Stéck ophuelen** oder an 3 Deeler schneiden (Virbereedung, Éischt Schrëtt, Erweidert).

---

## Video-Metadaten (virgeschloen)

- **Titel:** Mersch75.lu Websäit – An 20 Minuten vun 0 op Online
- **Ënnertitel:** Fir nei Mataarbechter: GitHub, HTML, Biller, Git-Push a vill Tipps.
- **Thumbnail-Idee:** Säin eegene Computerbildschierm mam Mersch75-Logo + groussen Text "Websäit einfach änneren".
- **Beschreiwung:** Link op d'Dokumenter:
  - Dummies-Guide: `docs/website-arbeiten-fuer-dummies.md`
  - PDF: `docs/website-arbeiten-fuer-dummies.pdf`
  - Repository: `https://github.com/Netjogger58/mersch75test.github.io`

---

## Szene 1: Intro (0:00–0:45)

**Sprechtext:**

> Salut! An dësem Video weisen ech dir, wéi s de un der Mersch75-Websäit (mersch75.lu) schaffe kanns – och wann s de nach ni ee Code gesinn hues. Mir ginn Schrëtt fir Schrëtt duerch: wat s de brauchs, wou d'Fichiere sinn, wéi s de Text a Biller änners, a wéi däi Ännerungen online goen. All Wierder aus dësem Video stinn och an engem PDF-Guide, dee ech an der Beschreiwung verlinken.

**Bild/Screenshot:**

- Screen Recording: Startbild vum `mersch75.lu` am Browser.
- Kurz d'Repo op GitHub uschneiden (just d'Haaptseit, 2 Sekonnen).

---

## Szene 2: Wat brauchs de? (0:45–3:00)

### 2.1 GitHub-Kont (0:45–1:30)

**Sprechtext:**

> Éischtens brauchs de e GitHub-Kont, well d'ganz Websäit do läit. Falls s de nach kee hues, gees de op github.com a mells de de gratis un. Duerno muss den ECG oder Netjogger58 dech als sougenannte "Collaborator" an d'Repo aerlaben. ouni dat kanns de keng Ännerungen eroplueden.

**Bild/Screenshot:**

- Screen Recording: GitHub-Registratiounssäit (kannst du och mat engem Demo-Kont weisen).
- Screenshot: GitHub-Repository `Netjogger58/mersch75test.github.io` → Tab "Settings → Collaborators".

### 2.2 Programmer installéieren (1:30–2:30)

**Sprechtext:**

> Du brauchs dräi Saachen: Git, e Code-Editor an Node.js. Fir normal Texter reicht en Editor. Node.js brauchs de nëmmen, wann s de Biller konvertéiere wëlls.

**Bild/Screenshot:**

- Screenshot oder Screen Recording: Downloadsäite vu `git-scm.com`, `code.visualstudio.com` a `nodejs.org`.
- B-roll: Installatioun vu VS Code starten (keng komplett Installatioun néideg, just den Ufank).

### 2.3 Zwei-Faktor-Authentifikatioun (2:30–3:00)

**Sprechtext:**

> Fir däi GitHub-Kont ze schützen, schalt 2FA an. Dat geet mat enger Authenticator-App oder enger SMS. Heiansdo verlaangt GitHub dat souwisou fir Collaborateure.

**Bild/Screenshot:**

- Screen Recording: GitHub → Settings → Password and authentication → Enable two-factor authentication.

---

## Szene 3: D'Websäit op däi Computer lueden (3:00–5:00)

**Sprechtext:**

> Elo klone mir d'Websäit. Dat heescht, mir lueden all Fichieren op däi Computer erof. Du oppechs d'Terminal a tipps: `git clone https://github.com/Netjogger58/mersch75test.github.io.git`. Duerno gees de mat `cd mersch75test.github.io` an den neie Dossier. Fäerdeg.

**Bild/Screenshot:**

- Screen Recording: Terminal opmachen.
- Tippen vum `git clone` an `cd` Kommando (kann och kopéiert ginn).
- Screenshot: De geklonten Dossier am Finder/Explorer mat den Haaptfichieren (`index.html`, `styles.css`, `script.js`).

---

## Szene 4: Websäit-Struktur erklären (5:00–7:30)

**Sprechtext:**

> Gucken mir kuerz d'Struktur un. D'Websäit ass statesch – dat heescht keng Datenbank, keen Server. Et sinn einfach HTML-Fichieren, CSS fir d'Gestaltung a JavaScript fir dynamesch Saachen. De wichtegsten Dossier ass `assets` – do sinn all Biller a PDFen dran. `tools` ass fir Hëllefsprogrammer, an `data` ass fir lokale Archiver.

**Bild/Screenshot:**

- Screen Recording: VS Code opmaachen mam geklonten Projet.
- D'Haaptverzeichniss erklären: `index.html`, `styles.css`, `script.js`, `assets/`, `tools/`, `data/`.
- Zoom op `assets/shared/media/` an `assets/pages/comite/media/`.

---

## Szene 5: Einfach Text änneren (7:30–10:00)

**Sprechtext:**

> Loosse mer eppes änneren. Mir sichen an `index.html` no engem Text, z. B. eng Iwwerschrëft am Footer. Ech ännere "Handball" an "Handball Mersch75", späicheren a lueden d'Säit am Browser nei. Soubal d'Säit nei gelueden ass, gesinn mir d'Ännerung.

**Bild/Screenshot:**

- Screen Recording: `index.html` an VS Code opmaachen, `Cmd + F` fir ze sichen.
- Tippen vun enger klenger Textännerung.
- Browser: `Cmd + Shift + R` fir Cache ze läschen a Säit nei ze lueden.
- Split-Screen: VS Code (lénks) a Browser (riets).

> **Wichteg:** Sot am Video, datt ech d'Ännerung net pushen, well dat just e Beispill ass.

---

## Szene 6: Biller derbäisetzen an konvertéieren (10:00–13:30)

### 6.1 Bild addéieren (10:00–11:00)

**Sprechtext:**

> Biller gehéieren an `assets/`. Am beschten organiséiers de se no Säiten, z. B. `assets/pages/index/media/`. De Fichier-Numm sollt keng Leerzeechen hunn, wann méiglech. Ech kopéieren e Beispill-Bild an den Dossier.

**Bild/Screenshot:**

- Screen Recording: Finder/Explorer – Bild an den richtegen `assets` Dossier zéien.
- Screenshot: Deen neie Fichier am VS Code Explorer.

### 6.2 `convert-images.mjs` ausféieren (11:00–12:30)

**Sprechtext:**

> Nodefir d'Websäit modern Biller a WebP a AVIF Formater ze liwweren, hunn mir e Script. Ech ginn an den `tools`-Dossier a lafe `node convert-images.mjs`. Dat generéiert automatesch d'Varianten a baut d'`<picture>`-Elementer an d'HTML.

**Bild/Screenshot:**

- Screen Recording: Terminal → `cd tools` → `node convert-images.mjs`.
- D'Ausgab vum Script weisen: "Found images", "Converted/generated variants".
- Screenshot vum generéierte `.webp` an `.avif` Fichier nieweben dem Original.

### 6.3 HTML no der Konversioun kontrolléieren (12:30–13:30)

**Sprechtext:**

> Kucken mir d'HTML un. Hei gesinn mir elo `<picture>` mat `<source>` fir AVIF a WebP, an d'Original-`<img>` als Fallback. D'Websäit wielt automatesch de beschte Format.

**Bild/Screenshot:**

- Screenshot: Quellcode vun engem `<picture>`-Element an `index.html`.
- Browser: Netzwerkinspetion opmaachen (F12) a weisen, datt d'WebP/AVIF geluede ginn.

---

## Szene 7: Ännerungen online bréngen – Git-Workflow (13:30–16:30)

**Sprechtext:**

> Elo mussen mir d'Ännerungen op GitHub pushen. Ech tipps am Terminal: `git status` fir ze kucken, wat geännert ginn ass. Da `git add .` fir all Ännerungen ze markéieren. Duerno `git commit -m "keng Text"` an `git push`. No e puer Minuten ass d'Websäit op mersch75.lu aktualiséiert.

**Bild/Screenshot:**

- Screen Recording: Terminal mam komplette Git-Workflow.
- Screenshot: GitHub-Repository nodeems de Commit ukomm ass.
- Browser: `mersch75.lu` nei lueden a weisen, datt d'Ännerung live ass.

> **Tipp am Video:** Weist och `git pull` ier een ufänkt, fir déi lescht Versioun ze hunn.

---

## Szene 8: Heefeg Feeler a Backup (16:30–18:30)

**Sprechtext:**

> Hei sinn déi heefegst Feeler. Éischtens: d'Websäit weist nach déi al Versioun – da läsch de Cache mat `Cmd + Shift + R`. Zweetens: e Bild ass ze grouss, well den CSS-Selektor ëmmer nach op `> img` zielt, mä elo ass e Bild an `<picture>` – do muss een `> picture > img` huelen. Drëttens: ëmmer regelméisseg commiten a pushen, dat ass däin Backup.

**Bild/Screenshot:**

- Split-Screen: Falsch CSS vs. korrekten CSS.
- Browser: Cache läschen (`Cmd + Shift + R`).
- Git-Commit-History op GitHub weisen.

---

## Szene 9: Outro a Ressourcen (18:30–20:00)

**Sprechtext:**

> Dat war schonn alles, wat s de brauchs fir unzefänken. Denks drun: éischt froen, dann änneren. All Detailer, Links an d'Checkliste stinn am Dummies-Guide – de Link ass an der Beschreiwung. Abonnéiert de Kanal, wann dir méi Tutorials wëllt, a bis geschwënn!

**Bild/Screenshot:**

- Screen Recording: Endbild vun `mersch75.lu`.
- Endscreen mat Link op den Dummies-Guide-PDF an op d'GitHub-Repo.

---

## Checkliste fir d'Ophonen

- [ ] GitHub-Kont a Collaborator-Zougang klären.
- [ ] Git, VS Code a Node.js installéiert.
- [ ] Websäit geklont.
- [ ] Screen-Recording-Software bereet (z. B. QuickTime, OBS, Camtasia).
- [ ] Dëst Script ausgedréckt oder op engem zweete Bildschierm.
- [ ] Mikro getest (oder KI-Voiceover bereet).
- [ ] Thumbnail-Template bereet.

---

## Zousatz: Wou KI am Video hëllefe kann

| Aufgab | Gratis KI-Tool | Hinweis |
|---|---|---|
| Skript optiméieren | ChatGPT / Claude | Dëst Script kanns du als Basis benotzen |
| Voiceover | CapCut TTS / ElevenLabs free | Stëmm iwwer d'Screen-Recording leeën |
| Ënnertitel | YouTube Studio auto-captions / CapCut | Aus der Stëmm generéieren |
| Thumbnail | Canva free / Microsoft Designer | Mersch75-Farwen: Blau (#0d2f8f) |
| Screencast-B-Roll | – | Muss selwer ophuelen |
