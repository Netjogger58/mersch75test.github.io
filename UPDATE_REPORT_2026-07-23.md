# Mersch75 — Update-Bericht fir de Comité
## Datum: 23. Juli 2026

---

## 1. Vereins-OS (manager.mersch75.lu) — Member-Datenbank

### 1.1 Member-Reconciliatioun mat Excel-Lëscht
- D'aktiv Memberen an der Vereins-OS Datebank goufen mat der offizieller Excel-Lëscht vum Sekretär (Adrien M75_membres_2026_2027_Codes_alt_neu_210726.xlsx) ofgeglach.
- **Resultat**: Genee **564 aktiv Memberen** an der Datebank — identesch mat der Excel-Lëscht.
- Memberen déi net an der Excel-Lëscht stinn goufen als `ehemalig` (archivéiert) markéiert — keng Date goufe geläscht.
- All 564 Memberen kruten hir Card-ID vun der Excel-Lëscht synchroniséiert.

### 1.2 Excel-Datei — Sexe (M/F) derbäigesat
- An der Spalt C (Sexe) goufen fir all 564 Memberen M oder F agesat, baséiert op der Datebank.
- 3 Memberen ouni Gender-Eintrag an der DB kruten F no hiren Nimm (all weiblech).

### 1.3 Excel-Datei — Fixéiert Kolonnen
- D'Kolonnen A (Nom) a B (Prénom) souwéi d'Kappzeil sinn elo fixéiert — se bleiwen ugewisen beim Scrollen.

### 1.4 Secretariat UI — nei Buttons
- **Import**-Button am Secretariat derbäigesat (linkt op d'Excel-Import-Säit).
- **+Mitglied**-Button am Secretariat derbäigesat (linkt op d'Member-Säit mat Formulaire fir neie Member).
- Nom Beaarbechten oder Creéieren vun engem Member gëtt een elo zeréck op d'Secretariat-Lëscht geleet (net méi op d'allgemeng Member-Säit).

### 1.5 Server — JoinUs Endpoint
- De `/api/joinus` Endpoint acceptéiert elo en optionalen `FamilyCode` Parameter.
- De `familyCode` gëtt an der Äntwert zeréckginn, soudass Familljememberen de selwechte Code kréien.
- Dës erlaabt datt Familljen-Umeldunge mat méi Persounen all an d'Datebank agedro ginn.

---

## 2. mersch75test.github.io — Join Us Säit

### 2.1 Familljen-Umeldung — Familljememberen an Datebank
- Wa eng Famill-Umeldung gemaach gëtt (Famill-Memberskaart 2+ Persounen), ginn elo **all Persounen** separat an d'Vereins-OS Datebank geschéckt.
- All Persoun krut:
  - Eegee Card-ID
  - De selwechte Family Code (Verknépplung an der Datebank)
  - Gemeinsam Adress, E-Mail, GSM vum Haaptformulaire
  - Eegene Numm, Geburtsdatum, CNS, Nationalitéit, Ale Veräin
  - Roll automatesch baséiert op Relatioun (Kand = Spiller, Elterendeel = Bénévole oder Spiller)
  - Status `pending` (muss vum Sekretariat validéiert ginn)

### 2.2 5-Sproochen Iwwersetzungen fir Familljen-Felder
- All Familljen-Felder sinn elo iwwersat an **5 Sproochen** (Lëtzebuergesch, Franséisch, Däitsch, Englesch, Portugisesch):
  - Famill-Memberskaart Label
  - Persounenzuel Fro
  - Hint-Text
  - "Persoun X" Titel
  - Numm a Virnumm
  - Roll / Relatioun (Elterendeel, Kand, Partner, Familljemember)
  - Bénévole Fro
  - Lizenz Fro
  - Geburtsdatum, CNS, Nationalitéit, Ale Veräin
- Beim Wiesselen vun der Sprooch ginn d'Familljen-Felder automatesch re-rendered.

### 2.3 CNS Matricule Hint
- Beim CNS Matricule Feld gëtt elo ugewisen: "Just déi läscht 5 Zifferen" — iwwersat an all 5 Sproochen.

---

## 3. Technesch Detailer

### Server
- **Server IP**: 178.105.40.239
- **App URL**: https://manager.mersch75.lu
- **Datebank**: SQLite, 564 aktiv Memberen, 461 archivéiert (ehemalig)
- **Node.js/Express** Backend, **React** Frontend

### GitHub Repos
- **mersch75test.github.io**: Join Us Säit + Website
- **Vereins-OS**: Member-Management App (server + client)

### Datéierungen
- Excel-Reconciliatioun: Juli 2026
- UI Verbesserungen (Secretariat Buttons, Redirect): 22. Juli 2026
- Familljen-Umeldung + Iwwersetzungen: 23. Juli 2026

---

## 4. Wat nach open ass

- **Family Tarif Marking** am Secretariat: Visuell Markéierung vun Familljen (2+ Persounen) am Secretariat — nach ze implementéieren.
- **4 geläscht Memberen**: Waarden op explizit Uweisung vum Comité fir erëm ze restauréieren.

---

*Bericht erstallt duerch Cascade AI Assistant — 23. Juli 2026*
