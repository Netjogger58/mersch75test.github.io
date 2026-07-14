# Websäit Mersch75 – Dummies-Guide

Dës Dokument ass fir jiddereen, déi éischt Kéier un der Mersch75-Websäit (mersch75.lu) schafft. Et erkläert, wéi d'Websäit opgebaut ass, wou d'wichtegst Fichieren sinn a wéi een Inhalt ännert, ouni datt een alles kaputt mécht.

> **Wichteg:** Falls s dech net sécher fillss, nemmmer eng Kopiéierung vum Fichier, ier s de eppes änners. Oder fro den ECG / Netjogger58.

---

## 1. Wat brauchs de fir unzefänken (Virbedéngungen)

Ier s de un der Websäit schaffe kanns, brauchs de e puer Saachen. Hei alles Schrëtt fir Schrëtt.

### 1.1 E GitHub-Kont

- **Jo, du brauchs onbedéngt e GitHub-Kont.** D'Websäit läit an engem GitHub-Repository (`Netjogger58/mersch75test.github.io`).
- Falls s de nach kee Kont hues: op [github.com](https://github.com) goen a gratis registréieren (E-Mail, Benotzernumm, Passwuert).
- **Duerno muss s de vum Proprietär (Netjogger58 / ECG) als "Collaborator" agelueden ginn**, soss kanns de keng Ännerungen späicheren (pushen). Schéck däi GitHub-Benotzernumm un Netjogger58, du kriss dann eng Invitatioun per E-Mail, déi s de unhëlls.
- Ouni Collaborator-Zougang kanns de d'Fichiere just **liesen**, awer net änneren.

### 1.2 Programmer déi s de installéiere muss

| Programm | Wofir | Wou erofgelueden |
|----------|-------|------------------|
| **Git** | Fir Ännerungen erofzelueden a pushen | [git-scm.com](https://git-scm.com) |
| **Code-Editor** | Fir d'Fichieren ze änneren (empfeelen: VS Code) | [code.visualstudio.com](https://code.visualstudio.com) |
| **Node.js** | Fir d'Hëllefs-Scripten (Biller, FLH-Archiv) | [nodejs.org](https://nodejs.org) (LTS-Versioun) |
| **Webbrowser** | Fir ze testen (Chrome, Safari, Firefox) | scho do |

> **Hiweis:** Node.js brauchs de nëmmen, wann s de Biller konvertéiere oder d'FLH-Daten aktualiséiere wëlls. Fir einfachen Text ze änneren duer e Code-Editor.

> **Video-Tutorial:** E YouTube-Video fir déi éischt Schrëtt ass **an der Maach** an gëtt hei verlinkt, soubal et fäerdeg ass.

### 1.3 Zwei-Faktor-Authentifikatioun (2FA) – staark empfohlen

- Fir däi GitHub-Kont ze sécheren, ass et **staark empfohlen** 2FA anzeschalten (SMS, Authenticator-App oder Passkeys).
- D'Websäit selwer brauch keng 2FA, mä den Zougang zum Repo ass wichteg.
- Heiansdo verlaangt GitHub fir Collaborateure 2FA. Wann dat de Fall ass, kritt s de eng Notifikatioun wann s de derbäikomm.

Hëllef: [GitHub 2FA anstiellen](https://docs.github.com/de/authentication/securing-your-account-with-two-factor-authentication-2fa)

### 1.4 Grondwëssen dat hëllefräich ass

- **Ganz roueg:** du muss kee Programméierer sinn fir Text oder Biller z'änneren.
- Hëllefräich ass e bësse Grondwëssen iwwer:
  - **HTML** (wéi eng Säit opgebaut ass – Tags wéi `<p>`, `<img>`, `<div>`).
  - **Git** (späicheren = commit, eroplueden = push). Kuck Kapitel 5.
  - **Terminal / Kommandozeil** (fir d'Scripten). Nëmmen néideg fir Biller/FLH.
- Wann eppes onkloer ass: **éischt froen, dann änneren.**

### 1.5 D'Websäit op däi Computer lueden (klonen)

Eng eemoleg Aktioun um Ufank. Terminal opmaachen an:

```bash
git clone https://github.com/Netjogger58/mersch75test.github.io.git
cd mersch75test.github.io
```

Dosdno hues de all d'Fichiere lokal a kanns lassleeën.

### 1.6 Backup-Strategie

Du brauchs keng komplizéiert Backup-Routine, just dës 3 Regelen:

1. **Nie eppes ouni Commit änneren.** Soubal eppes fäerdeg ass: `git commit` + `git push`. Dann ass d'Versioun sécher op GitHub.
2. **Regeleméisseg Pullen.** Ier s de ufänks, `git pull` ausféieren – sou huet s de déi lescht Versioun.
3. **Lokal Kopiéien.** Fir riskant Ännerunge kanns de e Fichier manuell an en aneren Dossier kopéieren, ier s de dréi gezunn gezunn.

### 1.7 Ier s de ufänks – Checkliste

1. GitHub-Kont erstallt.
2. Als Collaborator agelueden (Invitatioun ugeholl).
3. Git installéiert (`git --version` am Terminal fir ze préiwen).
4. Code-Editor installéiert (VS Code).
5. (Optional) Node.js installéiert (`node --version`).
6. 2FA fir GitHub-Kont ageschalt (empfohlen, Kapitel 1.3).
7. Backup-Regelen verstanen (Kapitel 1.6).
8. Repository geklont (Kapitel 1.5).

Wann all Punkten ✅ sinn, kanns de mat Kapitel 2 weiderfueren.

---

## 2. Grouss Iwwersiicht

- D'Websäit ass **statesch**: just HTML, CSS a JavaScript. Keng WordPress, keng React-Build.
- Se gëtt op **GitHub Pages** gehost.
- Déi Haaptdatebank ass **kee Server**: Säiten sinn einfach `.html`-Fichieren.
- Vill Inhalt läit an `script.js` oder JSON-Fichieren a gëtt vum Browser generéiert.

---

## 3. Wichteg Verzeichnisser a Fichieren

### 3.1 Haaptverzeichnis

- `index.html` – Start- a News-Säit.
- `*.html` – Eng Datei pro Säit (`inside.html`, `training.html`, `join.html`, ...).
- `styles.css` – All d'Gestaltung (Farwen, Layout, Schrëften).
- `script.js` – JavaScript fir d'News, Navigation, i18n, Formularen, asw.
- `CNAME` – Definéiert d'Domain `mersch75.lu` (net änneren!).

### 3.2 `assets/`

Hei sinn all Biller, Logoen, PDFen an aner Dateien.

- `assets/shared/media/` – Biller déi op méiere Säite benotzt ginn.
- `assets/pages/<säit>/media/` – Biller, déi nëmmen op enger bestëmmter Säit gebraucht ginn.
- `assets/pages/comite/media/` – Comité, Organigramm, Statuten.

### 3.3 `tools/`

Automatesch Hëllefs-Scripten (Node.js):

- `convert-images.mjs` – Konvertéiert Biller an WebP/AVIF a baut `<picture>`-Elementer.
- `flh-archive.mjs` – Lued FLH-Spillplang, Tabellen an SBO-PDFen erof.
- `package.json` – Huet d'Ofhängegkeeten (z. B. `sharp`).

### 3.4 `data/`

JSON-Fichieren a lokal Archiver:

- `data/flh-archive-2627.json` – FLH-Daten fir 2026/27.
- `data/flh-archive-2526.json` – FLH-Daten fir 2025/26.
- `data/sbo-index-*.json` – Index vun de lokalen SBO-PDFen.

### 3.5 `sbo-archiv/`

Hei gi SBO-PDFen (Spillberichter) vun der FLH geséchert.

---

## 4. Ännerunge maachen

### 4.1 Text an enger Säit

1. `.html`-Fichier an engem Texteditor opmaachen.
2. Nom Text sichen (`Cmd + F`).
3. Text änneren, Fichier späicheren.
4. Am Browser d'Säit aktualiséieren (`Cmd + Shift + R` fir Cache ze läschen).

> **Opgepasst:** Text, deen op 5 Sproochen iwwersat gëtt, steet am `script.js` an engem I18n-Objet (z. B. `window.i18n`). Direkt an HTML geschriwwene Text gëtt nëmmen op där Säit ugewisen.

### 4.2 Biller derbäisetzen ersetzen

1. Bild an den richtegen Dossier kopéieren (z. B. `assets/pages/index/media/Hauptseite/`).
2. Fichier-Numm ouni Sonnerzeechen a Leerzeechen halen, wann méiglech (oder `%20` an HTML benotzen).
3. Node-Script ausféieren, fir WebP/AVIF ze generéieren:
   ```bash
   cd tools
   npm install
   node convert-images.mjs
   ```
4. D'Script aktualiséiert d'HTML automatesch a setzt `<picture>` mat Lazy-Loading.
5. Ännerunge committen a pushen.

### 4.3 News-Slide änneren

- De News-Carousel ass an `index.html` an `news.html` (muss identesch sinn).
- Jiddwer Slide ass en `<article class="news-slide ...">` Block.
- Den Text kann direkt an HTML geännert ginn.
- Bilder duerch d'Script konvertéieren (siëhe 4.2).

### 4.4 Trainingplang aktualiséieren

- De Trainingplang ass en Bild, z. B. `assets/Entrainements-2026-2027-130726.png`.
- Hotspots (klickbar Boxen) si an `script.js` ageschriwwen.
- Wann den Plan nei ass:
  1. Neit Bild an `assets/` setzen.
  2. `script.js` sichen nom ale Bildnumm.
  3. Hotspot-Positionen an `script.js` upassen (Prozentwäerter).

### 4.5 Comité / Organigramm

- `inside.html` huet den Header-Beräich mam Comité-Logo an Organigramm.
- Comité-Fotoen an `assets/pages/comite/media/`.
- Passwuert-geschützten Deel: d'Passwuert ass nëmmen client-säiteg (`M75`) – net wierklech sécher, just fir Léit ze verhënneren, déi net vum Comité sinn.

### 4.6 FLH-Daten a Live-Center

- `live-center.html` a `live-center-25-26.html` hun engem "Lokal Archiv".
- Node-Script `tools/flh-archive.mjs` aktualiséiert d'Archiver:
  ```bash
  cd tools
  node flh-archive.mjs --season=2627 --force
  ```
- SBO-PDFen ginn iwwer `tools/flh-archive.mjs` erofgelueden.

---

## 5. Git-Workflow

### 5.1 Lokal testen

D'Websäit brauch kënne Server. Du kanns d'HTML-Fichieren direkt am Browser opmaachen:

```bash
open index.html
```

Fir méi realistesch Testen:

```bash
python3 -m http.server 8000
```

Dann am Browser `http://localhost:8000` opmaachen.

### 5.2 Ännerungen publizéieren

```bash
git status          # kucken wat geännert ginn ass
git add <fichier>   # oder git add . fir alles
git commit -m "beschreiwung vun der ännerung"
git push
```

No e puer Minuten ass d'Websäit op `mersch75.lu` aktualiséiert (GitHub Pages baut automatesch).

---

## 6. Wichteg Tools

### 6.1 Biller konvertéieren

```bash
cd tools
node convert-images.mjs
```

- Generéiert WebP/AVIF.
- Schreift `<picture>`-Markup an all `.html`.
- Setzt `loading="lazy"`.

### 6.2 FLH-Archiv aktualiséieren

```bash
cd tools
node flh-archive.mjs --season=2627
```

### 6.3 Cache-Bust-Parametern

CSS a JS ginn oft mat `?v=20260713a` gelueden. Nodeems s de `script.js` oder `styles.css` geännert hues, muss deen Parameter an den HTML-Fichieren aktualiséiert ginn, soss kucken d'Besicheren nach déi al Versioun:

```html
<script src="script.js?v=20260714a"></script>
```

### 6.4 `push_updates.sh`

Klenge Helper, deen eng Séier vun Ännerunge pusht. Kuck dran, ier s de en ausféiers.

---

## 7. Heefeg Feeler a Piège

| Problem | Méiglech Ursaach | Léisung |
|---------|------------------|---------|
| Bild ass rieseg / iwwerdeckt anert | CSS mat `> img` statt `> picture > img` | Selektor u `<picture>` upassen |
| Biller lueden net | Falsch Pad oder Leerzeechen net URL-encodéiert | `%20` benotzen oder Pads korrigéieren |
| Ännerunge si net online | Browser-Cache | `Cmd + Shift + R` |
| JavaScript ass al | Cache-Bust-Parameter feelt | `?v=...` an HTML aktualiséieren |
| `node convert-images.mjs` huet Feeler | `Yamas.png`-ähnlecht korrupt Bild | Bild entfernen oder mat enger Bildveraarbeitung reparéieren |
| SBO-Link funktionéiert net | Erofluede feelt | `flh-archive.mjs` nees lafen |

---

## 8. Wéini soll een hëllefen froen?

- Wann s de nët weess, wou een Text steet.
- Wann een JavaScript-Logik geännert soll ginn (Tariffer, Hotspots, i18n).
- Wann d'Websäit ganz komisch ausgesäit (wahrscheinlech CSS).
- Ier s de eng nei Säit oder eng nei Fonktioun duerchfeiers.

---

## 9. Zesummefaassung fir den Ufank

1. **GitHub-Kont** maachen + als Collaborator agelueden ginn (Kapitel 1).
2. **Git + Code-Editor** (+ Node.js) installéieren; 2FA fir GitHub aschalten.
3. **Repository klonen** an d'Backup-Regelen kennen (commit → push, reegelméisseg pullen).
4. Websäit ass **statesch HTML/CSS/JS** (keng WordPress, kee Server).
5. Biller an `assets/`, generéiert Varianten duerch `tools/convert-images.mjs`.
6. Text direkt an `.html` oder an `script.js` (i18n).
7. Lokal testen, dann `git add / commit / push`.
8. GitHub Pages deployt automatesch op `mersch75.lu`.
9. Bei Zweiwel: Backup maachen an froen.

**Video-Tutorial:** Follegt (aktuell an der Maach).

**Gutt ze wëssen:** Den Haapt-Kontakt / Proprietär vun der Websäit ass Netjogger58 / ECG. Bei groussen Ännerunge soll ëmmer ofgestëmmt ginn.
