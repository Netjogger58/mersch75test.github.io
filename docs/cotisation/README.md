# Cotisation-Formel (Spalte L) – Bausatz

Berechnet die Mitgliedsbeiträge in **Spalte L** der Mitgliederliste
(Blatt `Membres 2026_2027`).

## Fertige Datei

```bash
python3 docs/cotisation/baut_arbeitsmappe.py
```

erzeugt **`Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm`**
– eine Kopie der Mitgliederliste mit allen Formeln. **Das Original wird nicht
angefasst** (SHA-256 wird vorher/nachher verglichen). Eingebaut werden:

* Blatt **`Cotisation`** (vorne eingefügt) – alle Tarife, Schalter und Ausnahmen in Zellen
* Blatt **`Membres 2026_2027`**
  * Spalte **L** – die Ausgabeformel (772 Zeilen)
  * Spalten **BN:BZ** – 11 Helferformeln (772 Zeilen)
  * Spalte **BW** – Sicherung der bisherigen Ergebnisse aus L (233 Werte, Saison 2025/26)

Die Logik ist in `pruef_cotisation.py` in Python nachgebaut und gegen die Datei geprüft.

## Warum ohne LET / XLOOKUP / MINIFS

Das XLSX-Format speichert Funktionen neuerer Excel-Versionen mit Sonderpräfix
(`_xlfn.LET`, `_xlfn.XLOOKUP`, `_xlfn.MINIFS`). Die alte Formel in L war genau so
gespeichert. Ohne das Präfix zeigt Excel `#NAME?`. Der Bausatz nutzt deshalb
ausschließlich klassische Funktionen – `IF`, `AND`, `OR`, `NOT`, `COUNTIFS`,
`IFERROR`, `INDEX`, `MATCH`, `SUMPRODUCT`, `MIN`, `TEXT`, `ROW`, `DATEVALUE`,
`ISNUMBER`. Damit läuft die Datei in jeder Excel-Version, in LibreOffice und in
Google Sheets. In einem deutschen Excel erscheinen die Formeln automatisch
übersetzt (`IF` → `WENN`, `COUNTIFS` → `ZÄHLENWENNS`, `INDEX/MATCH` → `INDEX/VERGLEICH`).

## Ausgangslage (geprüfte Fakten)

* Blatt `Membres 2026_2027`, 772 Datenzeilen (Zeile 2–773), 65 Spalten plus Helfer ab BN
* `J` Naissance · `K` Alterskategorie (SEN/U25/?) · `L` Cotisatioun (Ziel) ·
  `M` Spielen J/R/N · `N` code courrier (alt) · `O` Code Courrier neu (**Familien-ID**) ·
  `AG` Spielerlizenz · `AH/AI/AJ` Offizielle-/ZS-/SR-Lizenz · `BB` Officiel
* `BN` bis `BO` waren in der Datei frei
* Die Datei enthält keine Excel-Tabelle (ListObject), daher normale Bereichsverweise
* **Hinweis:** Es gibt ein zweites Blatt `Cotisations` mit **anderem** Layout
  (C=Alterskategorie, D=Cotisatioun, M=Code Courrier neu, AE=Spielerlizenz,
  AF/AG/AH=Offizielle, AO=Geburtsdatum, keine Spalte „Spielen J/R/N").
  Die Formeln gehören in `Membres 2026_2027`, **nicht** in `Cotisations`.

## Blatt `Cotisation`

Tarife in A/B ab Zeile 1, Ausnahmen in D/F, Schlüsselspalte G (automatisch):

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| SEN | 300 | Einzelner Senior | Nom | Prénom | Ausgabe | Schlüssel |
| U25 | 210 | Einzelner U25-Jugendspieler | Bourg | Jeannot | Don?+0+50 | `Bourg\|Jeannot` |
| Familie | 384 | ab 2 Spielern oder SEN+U25 | Bourg-Thielen | Gaby | Don?+0+50 | `Bourg-Thielen\|Gaby` |
| Zusatz | 50 | Offizielle (AH/AI/AJ) oder Status N/R, freiwillig (Stimmrecht AG) | | | | |
| XSEUL | 300 | Fixbetrag, pro Zeile | | | | |
| GAJGL | 0 | Fixbetrag, pro Zeile | | | | |
| ZusatzBeiFamilie | NEIN | 384 ist das Maximum → kein +50 auf 384 | | | | |
| TraegerRegel | Erste | `Erste` = erste Zeile des Blocks · `Aelteste` = ältestes Geburtsdatum | | | | |
| ZusatzAuchOfficiel | NEIN | Rolle als Offizieller auch in Spalte BB werten | | | | |
| ReservistenWert | (0+50) | Wert für Spieler mit Status **R** oder Code **GAJGL** | | | | |
| SaisonStichtag | 01.08.2026 | Saisonbeginn – das Alter wird an diesem Tag gemessen | | | | |
| U25MaxAlter | 25 | Wer am Stichtag noch keine 25 Jahre alt ist, bleibt die ganze Saison U25 | | | | |

B7/B8/B9 als **Text** eingeben (`NEIN`, `Erste`). Neue Ausnahme: Zeile in D/E/F
eintragen, G ergänzt sich selbst – Zeile 200 der Schlüsselspalte ist vorbereitet.

## Helfer-Spalten BN:CA

| Spalte | Titel | Aufgabe |
|---|---|---|
| BN | FamID | Familien-ID; Zeilen ohne Code werden zu `@ZEILE`, sonst würden 166 Mitglieder mit Status `J` nie kotiert |
| BO | Schluessel | `Datum − ZEILE()/1000000`; `73415` fängt `///` und Leerwerte ab |
| BP | Aeltester | kleinster Schlüssel der Familie (`SUMPRODUCT(MIN(...))`) |
| BQ | SpielerGes | Spieler mit Lizenz in der Familie |
| BR | SpielerSEN | davon Alterskategorie SEN |
| BS | SpielerU25 | davon Alterskategorie U25 |
| BT | Zusatz | Personen mit Offizielle-/ZS-/SR-Lizenz ohne Spielerlizenz **oder** Status N/R |
| BU | Traeger | `TRUE`, wenn die Zeile der Rechnungsträger ist |
| BV | Manuell | Freie Eingabe; gewinnt immer (z. B. freiwillige 50 € eines Offiziellen) |
| BW | L_alt_2025-26 | Sicherung der bisherigen Ergebnisse |
| BX | Tarif | 384 / 300 / 210 / 0 |
| BY | AusnahmeNr | ZeilenNr der Ausnahme oder 0 |
| BZ | Zuschlag | 50 oder 0 |
| CA | Personenwert | Wert, der **auf dieser Zeile** steht: Ausnahme (z. B. Bourg) oder Spieler mit Status R / Code GAJGL |
| CB | Altersprüfung | `PRUEFEN`, wenn Spalte K vom Geburtsdatum abweicht – siehe unten |

## Die Formeln (deutsche Schreibweise, wie sie in Excel erscheinen)

```
BN2  =WENN($O2="";"@"&ZEILE();$O2)
BO2  =WENN(ISTZAHL($J2);$J2;WENNFEHLER(DATUMWERT($J2;"DD.MM.YYYY");73415))-ZEILE()/1000000
BP2  =SUMPRODUCT(MIN(($BN$2:$BN$773=$BN2)*$BO$2:$BO$773+($BN$2:$BN$773<>$BN2)*10^15))
BQ2  =ZÄHLENWENNS($BN$2:$BN$773;$BN2;$M$2:$M$773;"J";$AG$2:$AG$773;"<>")
BR2  =ZÄHLENWENNS($BN$2:$BN$773;$BN2;$M$2:$M$773;"J";$AG$2:$AG$773;"<>";$K$2:$K$773;"SEN")
BS2  =ZÄHLENWENNS($BN$2:$BN$773;$BN2;$M$2:$M$773;"J";$AG$2:$AG$773;"<>";$K$2:$K$773;"U25")
BT2  =ZÄHLENWENNS($BN$2:$BN$773;$BN2;$AG$2:$AG$773;"";$AH$2:$AH$773;"<>")
     +ZÄHLENWENNS($BN$2:$BN$773;$BN2;$AG$2:$AG$773;"";$AI$2:$AI$773;"<>")
     +ZÄHLENWENNS($BN$2:$BN$773;$BN2;$AG$2:$AG$773;"";$AJ$2:$AJ$773;"<>")
     +ZÄHLENWENNS($BN$2:$BN$773;$BN2;$AG$2:$AG$773;"<>";$M$2:$M$773;"N")
     +ZÄHLENWENNS($BN$2:$BN$773;$BN2;$AG$2:$AG$773;"<>";$M$2:$M$773;"R")
BU2  =WENN(Cotisation!$B$8="Aelteste";$BO2=$BP2;ZÄHLENWENNS($BN$2:$BN2;$BN2)=1)
BX2  =WENN(ODER($BQ2>=2;UND($BR2>=1;$BS2>=1));Cotisation!$B$3;
      WENN($BR2>=1;Cotisation!$B$1;WENN($BS2>=1;Cotisation!$B$2;0)))
BY2  =WENNFEHLER(VERGLEICH($A2&"|"&$B2;Cotisation!$G$2:$G$200;0);0)
BZ2  =WENN(UND($BT2>=1;ODER(Cotisation!$B$7="JA";$BX2<>Cotisation!$B$3));Cotisation!$B$4;0)
CA2  =WENN($BY2>0;INDEX(Cotisation!$F$2:$F$200;$BY2);
      WENN(UND($AG2<>"";ODER($M2="R";$O2="GAJGL"));Cotisation!$B$10;""))
```

Spalte **L** – reine Anzeige, alle Werte kommen aus den Helfern:

```excel
=WENN(UND($O2="";$M2="");"";WENN($BV2<>"";$BV2&"";WENN($CA2<>"";$CA2;WENN($O2="XSEUL";TEXT(Cotisation!$B$5;"0");WENN($O2="GAJGL";TEXT(Cotisation!$B$6;"0");WENN(NICHT($BU2);"";WENN($BX2+$BZ2=0;"";WENN($BX2=0;"(0+"&TEXT($BZ2;"0")&")";TEXT($BX2;"0")&WENN($BZ2>0;" (+0+"&TEXT($BZ2;"0")&")";"")))))))))
```

## Reihenfolge der Prüfungen

1. `O` **und** `M` leer → leer
2. `BV Manuell` ausgefüllt → dieser Wert (gilt immer und zuerst)
3. **Personenwert `CA`** → gilt auf **dieser Zeile**, unabhängig vom Rechnungsträger:
   * Name in der Ausnahmentabelle → fester Wert (Bourg/Jeannot **und**
     Bourg-Thielen/Gaby → beide `Don ? +(0 +50)`)
   * Spieler mit Spielerlizenz und Status **R** (Reserve) oder Code **GAJGL** → `(0+50)`
4. `O` = XSEUL → 300 (je Zeile; ANSAY Luka und Mathis haben beide 300 unter demselben Code)
5. `O` = GAJGL ohne Spielerlizenz → 0
6. nicht Rechnungsträger (`BU` = falsch) → leer
7. Tarif: 384 bei ≥2 Spielern oder SEN+U25, sonst 300 (SEN) bzw. 210 (U25)
8. Zuschlag `+50` **pauschal pro Familie** bei einem Offiziellen ohne Spielerlizenz oder
   Status N/R – **nicht** bei Tarif 384 (Maximum) und **nicht** pro Person
   (CLEMENT/METZLER: zwei Offizielle → trotzdem `(0+50)`)

Spieler mit Antwort **N**, die freiwillig (0+50) zahlen wollen, kommen in Spalte **BV
Manuell** – 50 € sind ein freiwilliger Beitrag mit Stimmrecht an der AG und stehen in
keiner Spalte der Liste.

## Selbsttest nach dem Öffnen

In der erzeugten Datei müssen diese Zellen so aussehen:

| Zeile | Person | M | Erwartet in L |
|---|---|---|---|
| 2 | AAMODT Astrid (F0096) | N | `210` |
| 5 | AKIKAWA Marie (F0103, 2 Spieler) | J | `384` |
| 11 | AMADOR FORTES Fabio Daniel (XSEUL) | J | `300` |
| 27 | ASSEL Leo (GAJGL) | N | `(0+50)` |
| 57 | BINGEN Fränk (F0015) | **R** | `(0+50)` |
| 64 | BISENIUS Ben (F0059) | **R** | `(0+50)` |
| 72 | BOURG Jeannot (F0006) | N | `Don ? +(0 +50)` |
| 73 | BOURG-THIELEN Gaby (F0006) | N | `Don ? +(0 +50)` |
| 134 | DIEDENHOFEN Alex (F0013) | J | `210 (+0+50)` |

Spalte **BW** daneben zeigt, was die alte Formel geliefert hat.

## Auswirkung der neuen Regeln auf die Saison 2025/26

Gegenüber den 233 bisherigen Werten ändern sich 66 Zeilen – davon **43 gewollt**:

| Änderung | Zeilen | Grund |
|---|---|---|
| `300` → `(0+50)` | 23 | Spieler mit Status R unter Code XSEUL |
| `0` → `(0+50)` | 15 | Spieler mit Code GAJGL |
| `210 (+0+50)` → `(0+50)` | 1 | BINGEN Fränk |
| `(0+50)` → `Don ? +(0 +50)` | 1 | BOURG Jeannot |
| leer → `Don ? +(0 +50)` | 1 | BOURG-THIELEN Gaby (zweite Ausnahme) |
| leer → `(0+50)` | 2 | BISENIUS Ben, SERRES Sven (Status R) |
| **Rest** | 23 | Tarife, die die Liste 2025/26 noch nicht enthielt |

Die 23 XSEUL-Reservisten sind der einzige Punkt mit echter finanzieller Wirkung: sie
fallen von 300 auf 50 €. Falls das **nicht** gewollt ist, in `Cotisation!B10` einen
anderen Wert eintragen.

## Die U25-Regel (Alter)

**U25 heißt: am Saisonbeginn noch keine 25 Jahre alt sein.** Wer zu Beginn der Saison
24 ist und im Laufe des Jahres 25 wird, bleibt die ganze Saison U25 und zahlt 210 €.
Wer am Saisonbeginn **schon 25** ist, zahlt ab sofort 300 € – auch wenn er erst im
Februar 25 wurde.

Die Spalte **K** (`Alterskategorie`) im Blatt ist genau das: die einmal pro Saison
festgelegte Einstufung des Sekretariats. Belegt in den Daten – die Regel
„Alter am Stichtag 01.08.2026 < 25 = U25" passt auf **alle 329** Mitglieder mit
SEN oder U25, ohne eine einzige Abweichung:

| Stichtag | Abweichungen |
|---|---|
| 01.07.2026 | 0 |
| **01.08.2026** | **0** |
| 01.09.2026 | 0 |
| 01.01.2026 | 2 |

Die Grenzfälle zeigen, warum ein **Geburtsjahr** als Kriterium nicht taugt – zwei
Personen aus demselben Jahr landen in verschiedenen Kategorien:

| Geburtstag | K | Alter am 01.08.2026 |
|---|---|---|
| 2001-05-12 ANSAY Luka | SEN | 25 |
| 2001-06-16 SYLVESTER Destiny | SEN | 25 |
| 2001-10-04 AMADOR FORTES Fabio Daniel | U25 | 24 |
| 2001-12-04 VAN DER WEKEN Louis | U25 | 24 |

Damit gilt: **25 Jahre oder jünger am Saisonbeginn = U25**, älter = SEN. Stichtag und
Grenzalter stehen in `Cotisation!B11` und `B12` – für die nächste Saison wird nur der
Stichtag weitergerückt, die Logik bleibt.

Spalte **CB** (`Altersprüfung`) rechnet das Alter am Stichtag nach und schreibt
`PRUEFEN`, wenn Spalte K und Geburtsdatum auseinanderlaufen. Nachgerechnet über alle
329 Zeilen: **0 Treffer** – die Einstufung im Blatt ist also vollständig konsistent.

> In der App (`Vereins-OS`) wird das Alter am **Stichtag 1. August** gerechnet
> (`SAISON_STICH_TAG`) statt am laufenden Datum, und der Vergleich lautet
> `alter < 25` (nicht `> 25`). Vorher wäre ein Spieler mitten in der Saison von 210
> auf 300 € gesprungen.

## Abgleich mit App und Join-Formular

Die Regeln werden an drei Stellen gepflegt. Die Widersprüche, der Abgleich und der
Vorschlag für eine gemeinsame Quelle stehen in
[`vereins-os-abgleich.md`](vereins-os-abgleich.md).
## Trefferquote der Logik

| Variante | Übereinstimmung mit den 233 Werten der Saison 2025/26 |
|---|---|
| Rechnungsträger = **erste Zeile des Familienblocks** | 705/771 = 91,4 % |
| Rechnungsträger = ältestes Geburtsdatum | 591/771 = 76,7 % |

Die 66 Abweichungen bestehen aus **43 gewollten Änderungen** (siehe Tabelle oben) und
**23 Tarifen, die die Liste 2025/26 noch nicht enthielt** – also Vervollständigung,
kein Fehler. Die 5 Fälle `210 (+0+50)` sind **freiwillige Beiträge** (Offizielle zahlen
0 oder 50 € für das Stimmrecht an der AG) und lassen sich aus keiner Spalte ableiten →
Spalte `BV Manuell`.

## Behobene Fehler der alten Formel

| vorher | jetzt |
|---|---|
| Array-Formel mit `_xlfn.LET` – 9 Variablen, über 2500 Zeichen | 11 Helferzellen + schlanke Anzeigeformel |
| `A4="Bourg"` mit `B5="Jeannot"` – Zeilenversatz 4/5 | Treffer über A und B derselben Zeile |
| `J5=Aeltester` **und** `ZÄHLENWENNS($O$2:$O5)=1` – bei Gleichstand **keine** Ausgabe | Schlüssel `J − ZEILE()/1e6` löst den Konflikt |
| `ODER(NICHT(ISTZAHL(J5));…)` – Doppelrechnung ohne Geburtsdatum | `73415`-Fallback, genau ein Träger je Familie |
| `MINWENNS` über Textdaten `///` → 0 | `ISTZAHL`/`DATUMWERT` mit Fallback |
| 4 × `SUMMENPRODUKT` über 5 Arrays × 4999 Zeilen | `ZÄHLENWENNS` auf 772 Zeilen, keine Array-Formel |
| Tarife, Codes und Namen fest im Formeltext | alles in Zellen bzw. Tabellen |

## Prüfen ohne Excel

```bash
python3 docs/cotisation/pruef_cotisation.py --bericht /tmp/abweichungen.csv
```

Das Skript bildet dieselbe Logik in Python nach und listet alle Abweichungen mit
Begründung. Es liest `tarife-cotisation.csv` und `ausnahmen-cotisation.csv` –
dieselben Werte, die im Blatt `Cotisation` stehen.
