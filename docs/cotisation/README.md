# Cotisation-Formel (Spalte L) – Bausatz

Berechnet die Mitgliedsbeiträge in **Spalte L** der Mitgliederliste
(Blatt `Membres 2026_2027`) automatisch. Die Logik ist in **Python nachgebaut**
(`pruef_cotisation.py`) und gegen die bestehende Datei geprüft.

## Ausgangslage (geprüfte Fakten)

* Datei: `Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv`, 771 Datenzeilen → Excel-Zeilen 2–772
* Spalten: `J` Naissance · `K` Alterskategorie (SEN/U25/?) · `L` Cotisatioun (Ziel) ·
  `M` Spielen J/R/N · `N` code courrier (alt) · `O` Code Courrier neu (**Familien-ID**) ·
  `AG` Spielerlizenz · `AH/AI/AJ` Offizier-/ZS-/Schiri-Lizenz · `BB` Officiel
* Spalte L enthält 233 Werte der **Saison 2025/26** (alte Handeingabe)
* **Achtung:** Es gibt **keine Excel-Tabelle (ListObject)** in der Datei, daher normale Bereichsverweise.
* **Achtung:** Die .xlsm-Version hat ein anderes Layout (dort: C=Alterskategorie, D=Cotisatioun,
  M=Code Courrier neu, AE=Spielerlizenz, AF/AG/AH=Offizier, AO=Geburtsdatum) und **keine Spalte
  „Spielen J/R/N"**. Vor dem Einfügen prüfen, welches Layout offen ist.

## Trefferquote der Logik

| Variante | Übereinstimmung mit Spalte L |
|---|---|
| Rechnungsträger = **erste Zeile des Familienblocks** | **747/771 = 96,9 %** |
| Rechnungsträger = ältestes Geburtsdatum | 632/771 = 82,0 % |

Von den 24 verbleibenden Abweichungen sind **18 „bisher leer"** (die Datei hat noch nichts
eingetragen) – das ist Vervollständigung, kein Fehler. Die 5 Fälle `210 (+0+50)` sind
**freiwillige Beiträge** (Offizielle zahlen 0 oder 50 € für das Stimmrecht an der AG) und
lassen sich aus keiner Spalte ableiten → dafür ist die Spalte `Manuell` gedacht.

## Schritt 1 – Blatt `Cotisation` anlegen

| A1 Tarif | B1 Wert | C1 Bedeutung | F1 Nom | G1 Prénom | H1 Ausgabe |
|---|---|---|---|---|---|
| SEN | 300 | Einzelner Senior | Bourg | Jeannot | Don?+0+50 |
| U25 | 210 | Einzelner U25-Jugendspieler | Bourg-Thielen | Gaby | Don?+0+50 |
| Familie | 384 | ab 2 Spielern oder SEN+U25 | | | |
| Zusatz | 50 | Offizielle, freiwillig (Stimmrecht AG) | | | |
| XSEUL | 300 | Fixbetrag, pro Zeile | | | |
| GAJGL | 0 | Fixbetrag, pro Zeile | | | |
| ZusatzBeiFamilie | NEIN | 384 ist das Maximum → kein +50 auf 384 | | | |
| TraegerRegel | Erste | Erste = erste Zeile · Aelteste = ältestes Geburtsdatum | | | |
| ZusatzAuchOfficiel | NEIN | Offiziersrolle auch in Spalte BB werten | | | |

B7/B8/B9 als **Text** eingeben (`NEIN`, `Erste`) – die Formel vergleicht mit `=`.

## Schritt 2 – Helfer-Spalten BN:BV

Überschriften in **BN1:BV1**, Formeln in Zeile 2, dann nach unten ausfüllen.
Bereiche `$2:$772` anpassen, wenn die Liste wächst.

```
BN2  =WENN($O2="";"@"&ZEILE();$O2)
BO2  =WENN(ISTZAHL($J2);$J2;WENNFEHLER(DATUMWERT($J2;"DD.MM.YYYY");73415))-ZEILE()/1000000
BP2  =MINWENNS($BO$2:$BO$772;$BN$2:$BN$772;$BN2)
BQ2  =ZÄHLENWENNS($BN$2:$BN$772;$BN2;$M$2:$M$772;"J";$AG$2:$AG$772;"<>")
BR2  =ZÄHLENWENNS($BN$2:$BN$772;$BN2;$M$2:$M$772;"J";$AG$2:$AG$772;"<>";$K$2:$K$772;"SEN")
BS2  =ZÄHLENWENNS($BN$2:$BN$772;$BN2;$M$2:$M$772;"J";$AG$2:$AG$772;"<>";$K$2:$K$772;"U25")
BT2  =ZÄHLENWENNS($BN$2:$BN$772;$BN2;$AG$2:$AG$772;"";$AH$2:$AH$772;"<>")
     +ZÄHLENWENNS($BN$2:$BN$772;$BN2;$AG$2:$AG$772;"";$AI$2:$AI$772;"<>")
     +ZÄHLENWENNS($BN$2:$BN$772;$BN2;$AG$2:$AG$772;"";$AJ$2:$AJ$772;"<>")
     +ZÄHLENWENNS($BN$2:$BN$772;$BN2;$AG$2:$AG$772;"<>";$M$2:$M$772;"N")
     +ZÄHLENWENNS($BN$2:$BN$772;$BN2;$AG$2:$AG$772;"<>";$M$2:$M$772;"R")
BU2  =WENN(Cotisation!$B$8="Aelteste";$BO2=$BP2;ZÄHLENWENNS($BN$2:$BN2;$BN2)=ZÄHLENWENNS($BN$2:$BN$772;$BN2))
```

* **BN** Familien-ID – Zeilen ohne Code werden zu einer eigenen Familie (`@ZEILE`), sonst
  würden 166 Mitglieder mit Spielstatus `J` gar nicht kotiert.
* **BO** Sortierschlüssel – `Datum − ZEILE()/1000000`: ältestes Mitglied = kleinster Wert, bei
  **Gleichstand gewinnt die kleinere Zeilennummer** (deterministisch). `73415` (31.12.2100)
  fängt `///` und Leerwerte ab, damit keine Familie ohne Ergebnis bleibt.
* **BU** Rechnungsträger – Standard „Erste“ (zählt die Familienzeilen bis hierher). Steht in
  `Cotisation!B8` auf `Aelteste`, vergleibt die Formel stattdessen `BO` mit `BP`.
* **BV** `Manuell` (optional) – hier eingetragene Werte gewinnen immer, z. B. für freiwillige
  50-€-Beiträge von Offiziellen.

## Schritt 3 – Spalte L

> Vorher den alten Inhalt von L sichern (Werte 2025/26) oder die Formel in eine leere Spalte
> setzen – in der Liste existiert bereits **BM „Cotisatioun 2026-27"** (leer).

```excel
=LET(
 Tar;WENN(ODER($BQ2>=2;UND($BR2>=1;$BS2>=1));Cotisation!$B$3;
      WENN($BR2>=1;Cotisation!$B$1;WENN($BS2>=1;Cotisation!$B$2;0)));
 Zus;WENN(UND($BT2>=1;ODER(Cotisation!$B$7="JA";Tar<>Cotisation!$B$3));Cotisation!$B$4;0);
 Aus;XVERWEIS($A2&"|"&$B2;Cotisation!$F$2:$G$200;Cotisation!$H$2:$H$200;"");
 WENN(UND($O2="";$M2="");"";
  WENN($O2="XSEUL";TEXT(Cotisation!$B$5;"0");
   WENN($O2="GAJGL";TEXT(Cotisation!$B$6;"0");
    WENN(ISTZAHL($BU2);"";
     WENN(ISTZAHL($BV2);TEXT($BV2;"0");
      WENN(Aus<>"";Aus;
       WENN(UND(Tar=0;Zus=0);"";
        WENN(Tar=0;"(0+"&TEXT(Zus,"0")&")";
         TEXT(Tar,"0")&WENN(Zus>0;" (+0+"&TEXT(Zus,"0")&")";""))))))))))
```

## Reihenfolge der Prüfungen

1. `O` **und** `M` leer → leer
2. `O` = XSEUL → 300 · `O` = GAJGL → 0 – **je Zeile, ohne Familiengruppierung**
   (belegt: ANSAY Luka (SEN) und Mathis (U25) haben beide 300 unter demselben Code)
3. `BV` (Manuell) ausgefüllt → dieser Wert
4. nicht Rechnungsträger → leer
5. Name in der Ausnahmentabelle → fester Wert (z. B. `Don?+0+50`)
6. Tarif: 384 bei ≥2 Spielern oder SEN+U25, sonst 300 (SEN) bzw. 210 (U25)
7. Zusatz `+50` **pauschal pro Familie** bei Offizier ohne Spielerlizenz oder Status N/R –
   **nicht** bei Tarif 384 (Maximum) und **nicht** pro Person
   (CLEMENT/METZLER: zwei Offizielle → trotzdem `(0+50)`)

## Behobene Fehler der alten Formel

| vorher | jetzt |
|---|---|
| Zirkelbezug `B_E;$M$2:$M$5000` (las die eigene Spalte) | getrennte Helfer, kein Zirkelbezug |
| `UND(A4="Bourg";B5="Jeannot")` – Zeilenversatz 4/5 | Lookup über A und B derselben Zeile |
| `J5=Aeltester` **und** `ZÄHLENWENNS($O$2:$O5)=1` – bei Gleichstand **keine** Ausgabe | Schlüssel `J − ZEILE()/1e6` löst den Konflikt |
| `ODER(NICHT(ISTZAHL(J5));…)` – Doppelrechnung ohne Geburtsdatum | `73415`-Fallback, genau ein Träger je Familie |
| `MINWENNS` über Textdaten `///` → 0 → Spalte bleibt leer | `ISTZAHL`/`DATUMWERT` mit Fallback |
| 4 × `SUMMENPRODUKT` über 5 Arrays × 4999 Zeilen | 7 × `ZÄHLENWENNS` auf 772 Zeilen, keine Array-Formel |
| Tarife, Codes und Namen fest im Formeltext | alles in Zellen bzw. Tabellen |

## Prüfen

```bash
python3 docs/cotisation/pruef_cotisation.py --bericht /tmp/abweichungen.csv
```

Das Skript bildet dieselbe Logik in Python nach und listet alle Abweichungen mit Begründung.
Es liest `tarife-cotisation.csv` und `ausnahmen-cotisation.csv` – dieselben Werte, die später
im Blatt `Cotisation` stehen.

