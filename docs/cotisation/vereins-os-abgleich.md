# Abgleich Cotisation: Excel, Vereins-OS-App und join.html

> Stand 2026-09-26. Vergleicht die Beitraglogik an allen bekannten Stellen und benennt
> die Widersprüche. Bezug: `docs/cotisation/README.md` (Excel-Formel).

## Kurzfassung

Die Beitraglogik existiert **an drei Stellen unabhängig voneinander**, die C-Code-Liste
an **drei weiteren**. Zwei Befunde sind echte Fehler, einer ist eine Fehlentscheidung
in der Modellierung:

1. **Die App wendet den Familientarif nie an.** `getCotisation()` bekommt
   `playerCount` als Parameter – und benutzt ihn nicht. Zwei Geschwister werden in
   der App je 210 € angezeigt, in der Excel-Rechnung 384 €.
2. **`join.html` zeigt Jugendlichen 200 €**, während App und Excel 210 € berechnen.
   Das ist für Neumitglieder sichtbar falsch.
3. **AC-Codes und C-Codes sind nicht doppelt, nur missverständlich benannt.**
   AC-Codes beantworten *„welche Berechtigung hat die Person"* (Zugriff auf die App),
   C-Codes *„welche Beitragspflicht und welcher Tarif"*. Sie gehören **nicht**
   zusammengelegt, sondern in zwei klar benannte, verknüpfte Listen.

## Inventar: wo die Regeln stehen

| # | Ort | Datei | Art | Aktuell |
|---|---|---|---|---|
| A | Excel Blatt `Membres 2026_2027`, Spalte L | `GC 2026-09-24 …_mit-Cotisation.xlsm` | Berechnung, familienbezogen | Tarife in Zellen (Blatt `Cotisation`) |
| B | App, Registrierungsassistent | `Vereins-OS/client/src/lib/registrationLogic.ts` (`getCotisation`) | Berechnung, personenbezogen | **384 fehlt** |
| C | App, Rollen/Berechtigungen | `Vereins-OS/shared/registrationRules.ts` | AC-Codes (Zugriff) | 9 AC-Codes |
| D | Join-Formular, Tarif-Anzeige | `join.html` (`lookupDefinitionCode`) | Anzeige | **200 € statt 210 €** |
| E | Join-Formular, C-Codes | `join.html` (`MERSCH75_DEFINITION_CODES`) | C0001–C0040 **mit Tarifen** | abweichende Tarife |
| F | Vereins-OS, C-Code-Berechnung | `scripts/update_definitioun_2026_2027.py` | 13 Prioritätsregeln | keine Tarife |
| G | Vereins-OS, Doku | `docs/definitioun-coden-workflow.md` | Beschreibung C-Codes | **andere Tarife als E** |

Die Vereins-OS-Aufgabenliste (`docs/code-list-improvement-plan.csv`) benennt das
Problem bereits: CL-02 *„Eng zentral Source of Truth … keng duebel Lëschte méi"*,
CL-05 *„C0001–C0017 an enger eenheetlecher Lëscht zesummebréngen"*, CL-10 *„Tarif-/
Definitioun-Coden net separat drifte loossen"*.

## Widersprüche (alle belegt)

| # | Thema | Excel (A) | App (B) | join.html (D/E) | Vereins-OS (G) |
|---|---|---|---|---|---|
| 1 | **Familientarif** | 384 ab 2 Spielern | **fehlt** (`playerCount` ungenutzt) | 384 (Anzeige) | nicht erwähnt |
| 2 | **Jugendtarif** | 210 | 210 | **200** (C0007, C0008, C0010) | nicht erwähnt |
| 3 | **Senior** | 300 (K = SEN) | 300 (`age > 25`) | 300 (C0009) | C0009 |
| 4 | **Offizielle** | `(+0+50)`, freiwillig | *„min. €50"* | 50 (C0012) | C0012 |
| 5 | **Alter statt Kategorie** | Spalte K (SEN/U25, Grenzjahr 2001) | Alter am Stichtag 1.8. (`age > 25`) | `age < 12 / < 18` | CAT-Codes |
| 6 | **Reserve (M=R) / GAJGL** | `(0+50)` | fehlt | fehlt | fehlt |
| 7 | **U4 / Kidssport** | fehlt | 10 € pro Einheit | C0006 *„Pro Training"* | C0006 |
| 8 | **Trainer** | fehlt | 0 € (Comité 50) | 7 Codes *„individuell ausgehandelt"* (C0015–21) | C0015–21 |
| 9 | **Bourg-Ausnahme** | Tabelle | fehlt | fehlt | fehlt |

Punkt 5 ist nicht nur eine Doppelung, sondern eine **inhaltliche Abweichung**: Ein
26-jähriger Spieler mit `K = U25` bekommt in Excel 210 €, in der App 300 €.
Punkt 8 zeigt die Überkomplexität: **sieben** Trainer-Codes für denselben Fall
(0 €, individuell ausgehandelt). `registrationRules.ts` kennt nur **fünf**
Trainer-Arten (coach, coach_backup, teamchef, teambegleeder, supervisor) – die
einzige Stelle, die sauber differenziert.

## Nicht doppelt: AC-Codes vs. C-Codes

`definitioun-coden-workflow.md` behandelt AC-Codes, C-Codes und CAT-Codes in einer
einzigen Liste („Definitioun-Coden aktualiséieren"). Dadurch wirkt es, als gäbe es
drei Codesysteme für dieselbe Sache. Tatsächlich:

| System | Frage | Beispiele | Wo gespeichert |
|---|---|---|---|
| **AC-Code** | Welche **Berechtigung** in der App? | AC300 Spieler, AC102 Arbitre/Officiel, AC400 Contact Famille, AC401 Bénévole, AC200–204 Trainer | `registrationRules.ts` → `accessProfiles` |
| **CAT-Code** | Welche **FLH-Kategorie**? | 11 = Senior H, 15 = U13 H, 31 = Senior F … | `registrationRules.ts` → `catCode` |
| **C-Code** | Welche **Beitragspflicht / welcher Tarif**? | C0007 Jugendlicher mit Lizenz, C0012 Offizieller | `join.html`, Doku, Python-Skript |

**Empfehlung: nicht zusammenlegen.** Sie beantworten verschiedene Fragen. Stattdessen
umbenennen (AC → *Rollenprofil*, C → *Tarifdefinition*) und eine **Zuordnungstabelle**
C-Code → AC-Code → CAT-Code anlegen. Damit verschwindet die Doppelung aus der
Wahrnehmung, ohne eine Migration von Datenbank und Excel zu riskieren.

## Empfehlung: eine Quelle der Wahrheit

```
shared/cotisationRules.ts          ← Tarife, Regeln, C-Code-Definitionen (Single Source)
        │
        ├── client/src/lib/registrationLogic.ts   importiert COTISATION_RATES
        ├── scripts/export_cotisation_config.py  erzeugt tarife-cotisation.csv
        │        └── docs/cotisation/...          → Excel-Blatt "Cotisation"
        └── scripts/sync_rates_to_join.mjs       erzeugt MERSCH75_DEFINITION_CODES
```

Reihenfolge der Umsetzung:

1. **Tarife zentralisieren** (SOFORT) – `COTISATION_RATES` in `registrationLogic.ts`
   ist der Anker; Excel-CSV und `join.html` werden daraus generiert.
   *Werte erledigt, Generierungsschritt offen.*
2. **C-Code-Liste an einem Ort** (CL-05) – `join.html` und `definitioun-coden-workflow.md`
   führen heute unterschiedliche Tarife für dieselbe Code-Nummer. Eine Datei
   `shared/definitionCodes.ts` als Quelle, beide lesen sie daraus.
3. **C-/AC-Trennung dokumentieren** (CL-10) – Begriffsklärung statt Datenmigration.
4. **Alterslogik entscheiden** – entweder Kategorie (Spalte K) oder Alter (CNS).
   Empfehlung: **Kategorie**, weil sie die FLH-Lizenz abbildet und im Excel ohne
   Altersberechnung auskommt. Punkt 5 ist bis dahin in der App still falsch.
5. **Trainer-Codes** (C0015–21 → AC200/202/203/204) – sieben C-Codes auf die fünf
   AC-Rollen abbilden, Rest als „Trainer individuell" zusammenfassen.

## Umgesetzt in diesem Durchgang

| Änderung | Datei | Wirkung |
|---|---|---|
| Familientarif 384 fehlt → `playerCount >= 2` greift | `Vereins-OS/…/registrationLogic.ts` | zwei Spieler in einer Anmeldung zeigen jetzt 384 statt 210/300 |
| Tarife als `COTISATION_RATES` exportiert | `Vereins-OS/…/registrationLogic.ts` | eine Konstantenliste statt 7 fest verdrahteter Zahlen |
| Notation vereinheitlicht (`Arbitter` → `Arbitre`, `min. €50` → `0€ oder 50€`) | `Vereins-OS/…/registrationLogic.ts` | verständlicher fürs Sekretariat |
| Jugendtarif 200 → 210 (C0007, C0008, C0010 + Fallback-Strings) | `join.html` | Anzeige stimmt mit Rechnung überein |
| `tsc --noEmit` | Vereins-OS | fehlerfrei |

## Offene Entscheidungen

| Frage | Warum ich sie nicht entscheide |
|---|---|
| Alterslogik: Kategorie (K) oder Alter (CNS)? | Betrifft 26-jährige U25-Spieler – fachliche Festlegung |
| Trainer: 7 C-Codes oder 5 AC-Rollen? | Touché mit dem laufenden Betrieb auf Hetzner |
| U4/Kidssport 10 € in Excel aufnehmen? | Gibt es in der Mitgliederliste keine U4-Zeile – evtl. bewusst |
| Reservisten-Regel: gilt sie auch für XSEUL? | 23 Mitglieder wechseln damit von 300 auf `(0+50)` – siehe unten |
