# Plang: SBO-Berichter archivéieren op Hetzner (Live Center, Saison 26/27)

> Status: **ENTWURF / zur Ofstëmmung** — nach net implementéiert.
> Ausgeléist duerch: Handball4All weist d'SBO-Berichter (PDF) net méi zouverlässeg un;
> Donnéeën "verschwannen". Zil: eng eege Kopie hale fir Uweisung **an** Auswäertung.

---

## 1. Ausgangslag

- **Live Center** (`live-center.html`) benotzt pro Match e Feld `sbo` = voll URL op
  `https://spo.handball4all.de/misc/sboPublicReports.php?sGID=<ID>`.
- Gerendert gëtt de Link an `sboCell(v)` (`@live-center.html:1178`) als
  `<a href="${v}">📄 SBO</a>`.
- D'SBO-Berichter si **binär PDFen** — net direkt parsebar an ëmmer méi dacks fort.
- **Hosting:** D'Säit gëtt **statesch iwwer Hetzner** ausgeliwwert (`@impressum.html:86`),
  GitHub ass d'Quell/Backup. → Eng eege Kopie kann iwwer déiselwecht Domain
  (z.B. `https://mersch75.lu/sbo-archiv/...`) ausgeliwwert ginn.

## 2. Zil

1. **Archivéieren:** Vun all SBO-Link automatesch eng **PDF-Kopie** zéien a sécheren.
2. **Ëmschalten:** De Link am Live Center op **eis Kopie** (Hetzner) setzen — mat
   Fallback op den originalen Handball4All-Link.
3. **Auswäerten:** Aus de PDFen d'**Spillerdonnéeën** (Nimm, Goaler, 7m) extrahéieren,
   fir d'Statistik-Säiten (wéi bei U13) automatesch ze fëllen.
4. **Sécheren op GitHub:** Konfiguratioun, Scripten a Metadonnéeën am Repo versionéieren.

## 3. Nei "Regel" fir de Live Center (Kär vun der Ufro)

Pro Match, soubal en SBO-Link do ass:

```
1. sbo-Link liesen  →  2. PDF eroflueden (Kopie)  →  3. op Hetzner sécheren
                                                     →  4. sbo-Link op Hetzner-Kopie ëmsetzen
                                                     →  5. PDF parsen → Spiller-Stats
```

Dat gëtt **net am Browser** gemaach (statesch Säit, CORS/binär), mä vun engem
**Archiv-Script** dat lokal oder als Automatisatioun leeft an d'Resultat commit't.

## 4. Architektur-Iwwersiicht

```
Handball4All (SBO PDF)
        │  (Archiv-Script: fetch)
        ▼
  sbo-archiv/<saison>/<gNo>.pdf   ──commit──► GitHub ──deploy──► Hetzner (mersch75.lu/sbo-archiv/…)
        │  (Parser: pdftotext)
        ▼
  data/sbo-stats-<saison>.json  (Spiller: Goaler, 7m pro Team)
        │
        ▼
  Statistics *.html  +  live-center.html (sboCell → Hetzner-Kopie)
```

## 5. Datei-Layout (nei)

| Pad | Inhalt |
|-----|--------|
| `sbo-archiv/2627/<gNo>.pdf` | Archivéiert SBO-PDFen (pro Saison-Ordner) |
| `data/sbo-index-2627.json` | Mapping `gNo`/`sGID` → lokale Datei + Original-URL + Datum |
| `data/sbo-stats-2627.json` | Extrahéiert Spiller-Stats (pro Team: Numm, Goaler, 7m G/V, Presenz) |
| `tools/sbo-archive.mjs` | Node-Script: fetch → sécheren → Index/Links aktualiséieren |
| `tools/sbo-parse.mjs` | Node-Script: PDF → Text → Stats-JSON |

**Benennung:** `gNo` (offiziell Spillnummer, schonn am Datmodell) als stabilen Dateinumm,
z.B. `sbo-archiv/2627/29154014.pdf`. `sGID` als Alternativ wann `gNo` feelt.

## 6. Datastruktur-Ännerung (Live Center)

Nei/gepasst Felder pro Spill:

```js
{
  ...,
  sbo:      "sbo-archiv/2627/29154014.pdf",   // NEI: eis Kopie (relativ, Hetzner-Domain)
  sboLive:  "https://spo.handball4all.de/misc/sboPublicReports.php?sGID=3488556" // Original als Fallback
}
```

`sboCell(v)` gëtt esou ugepasst (Fallback-Logik):

```js
function sboCell(row) {
  const local = row.sbo, live = row.sboLive;
  if (local) return linkTo(local, "📄 SBO");            // eis Kopie prioritär
  if (live)  return linkTo(live,  "📄 SBO (FLH)");        // Fallback
  return '<span class="link-fehlt">🔗 fehlt</span>';
}
```

> Wichteg: `sboCell` kritt aktuell just `r.sbo` (String). Dësen Ëmbau op `row` muss un
> alle 3 Opruffplazen (`@live-center.html:642,740,1011`) ugepasst ginn.

## 7. Storage-Optiounen (ENTSCHEEDUNG NÉIDEG)

**A) Am Git-Repo (empfohlen fir den Ufank)**
- PDFen an `sbo-archiv/` commit'en → automatesch mat op Hetzner deployéiert.
- ✅ Einfach, versionéiert, ee Workflow. ❌ Repo gëtt méi grouss (PDFen sinn ~50–200 KB/Match).
- Bei ~150 Matcher/Saison × ~100 KB ≈ **15–30 MB/Saison** — nach OK fir Git.

**B) Direkt op Hetzner (SFTP/WebDAV), net am Git**
- Script lueden d'PDFen direkt an d'Hetzner-Webspace.
- ✅ Repo bleift schlank. ❌ Zousätzlech Credentials/Deploy-Wee, net am Git versionéiert.

→ **Empfehlung:** Start mat **A** (einfach), spéider op **B** wiesselen wann d'Gréisst stéiert.

## 8. Archiv-Script (`tools/sbo-archive.mjs`) — Oflaf

1. All Spiller aus dem Live-Datmodell liesen (oder aus `flh-live-sync` Live-Payload).
2. Fir all Spill mat `sboLive` (Handball4All-URL) an nach **ouni** lokal Kopie:
   - PDF eroflueden (`fetch`, `Content-Type: application/pdf` checken).
   - Nëmme sécheren wann Gréisst > X KB a valabelt PDF (`%PDF`-Header).
   - Späicheren als `sbo-archiv/2627/<gNo>.pdf`.
   - `data/sbo-index-2627.json` aktualiséieren.
   - Am Live-Datmodell `sbo` op lokale Pad setzen (Original an `sboLive` behalen).
3. Idempotent: scho archivéiert Matcher iwwersprangen.
4. Ausgab: Log wéivill nei archivéiert, wéivill Feeler.

## 9. Parser (`tools/sbo-parse.mjs`) — Oflaf

- `pdftotext -layout` (Poppler) oder `pdf-parse` (Node) fir Text ze kréien.
- Text vun der SBO-Spillerstatistik-Tabell parsen: Numm, Rëckennummer, **Goaler**,
  **7m (G/V)**, Karten.
- Pro Team iwwer d'Saison aggregéieren → `data/sbo-stats-2627.json`.
- **Manuell Kontroll** virum Publizéieren (OCR/Layout kann Feeler maachen).
- Format vum JSON kompatibel mat der U13-Torschützelëscht, fir 1:1 an d'Statistik-Säiten
  ze fëllen.

## 10. Automatiséierung (ENTSCHEEDUNG NÉIDEG)

| Optioun | Wéi | Notiz |
|---------|-----|-------|
| **Manuell** | `node tools/sbo-archive.mjs` no de Spilldeeg lafen | Am einfachsten, voll Kontroll |
| **GitHub Action** | Cron (z.B. Méindes) → archivéiert → PR/commit | Automatesch, brauch Setup + evtl. Secrets |
| **Lokalen Cron** | Op engem Rechner/Server | Ofhängeg vun engem Apparat |

→ **Empfehlung:** Start **manuell** (no de Weekend-Spiller), spéider GitHub Action.

## 11. Fallback & Feelerfäll

- Kee `sbo` an `sboLive`? → "🔗 fehlt" (wéi haut).
- Lokal Kopie feelt, awer `sboLive` do? → Link op Handball4All (bis archivéiert).
- Handball4All liwwert kee valabelt PDF? → net sécheren, spéider erëm probéieren.
- **Rechtlech:** Kopie fir eegen Uweisung/Archiv — mat der FLH ofklären ob OK
  (Berichter enthalen Spillernimm; DSGVO/FLH-Reglement beuechten).

## 12. Rollout-Phasen

1. **Phase 0 (elo):** Dëse Plang ofstëmmen + Entscheedungen (Kap. 7, 10, +Hetzner-Zougang).
2. **Phase 1:** `tools/sbo-archive.mjs` + `sbo-archiv/` + Index-JSON. Manuell testen mat
   e puer 26/27-Matcher soubal SBO-Linken do sinn.
3. **Phase 2:** `sboCell`-Fallback-Logik am Live Center abauen (`sbo` + `sboLive`).
4. **Phase 3:** `tools/sbo-parse.mjs` + `sbo-stats`-JSON + Statistik-Säiten fëllen.
5. **Phase 4:** Evtl. GitHub Action / Cron fir Automatiséierung.

## 13. Oppen Entscheedungen (brauch Input vun dir)

- [ ] **Hetzner-Zougang:** Wéi kommen d'Fichieren op Hetzner? (a) via GitHub-Deploy
      (schonn de Wee?), oder (b) direkt SFTP/WebDAV — an ënnert wéi engem Pad/URL
      (`mersch75.lu/sbo-archiv/`?).
- [ ] **Storage:** Optioun A (am Git) oder B (Hetzner direkt)?
- [ ] **Automatiséierung:** Manuell fir den Ufank, oder direkt GitHub Action?
- [ ] **Rechtlech:** Dierfe mir d'SBO-PDFen (mat Spillernimm) selwer archivéieren an
      op eiser Domain uweisen? (mat FLH ofklären)
- [ ] **Retention:** All Saison an engem eegenen Ordner behalen? (jo empfohlen)

---

*Dëse Plang ass just d'Virbereedung. Implementéierung fänkt eréischt un no denger
Ofstëmmung vun de Punkten a Kapitel 13.*
