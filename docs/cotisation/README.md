# Cotisation-Formel (Spalte M) – Bausatz

Berechnet die Mitgliedsbeiträge in **Spalte M** der Mitgliederliste
(Blatt `Membres 2026_2027`).

> **Stand 26.09.2026:** Die Spaltenordnung wurde vom Benutzer geändert –
> `Spielen J/R/N` wurde in `Spieler J/R/N` umbenannt und nach **L** verschoben,
> `Cotisatioun` liegt jetzt in **M**, davor kam die Eingabespalte
> `N BEZAHLT J/N` für den Kassierer. Alle Formeln und Helfer sind darauf
> umgestellt, `BN` ist die letzte Datenspalte, die Helfer beginnen bei `BP`.

## Fertige Datei

```bash
python3 docs/cotisation/baut_arbeitsmappe.py
```

Quelle ist die vom Benutzer bearbeitete Arbeitsfassung
**`TEST1_nur-calcchain.xlsm`**, erzeugt wird
**`Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm`**.
**Das Original vom 24.09. wird nicht angefasst.** Eingebaut werden:

* Blatt **`Cotisation`** (hinten angehängt) – alle Tarife, Schalter und Ausnahmen in Zellen
* Blatt **`Membres 2026_2027`**
  * Spalte **M** – die Ausgabeformel (772 Zeilen)
  * Spalten **BP:CD** – 14 Helferformeln, **BX** = Eingabefeld `Manuell`
  * Spalte **CE** – Sicherung der bisherigen Ergebnisse aus M (233 Werte, Saison 2025/26)

Die Logik ist in `pruef_cotisation.py` in Python nachgebaut, gegen die Datei
geprüft und **als `<v>`-Wert in jede M-Zelle geschrieben** – die Mappe zeigt also
schon vor der ersten Neuberechnung durch Excel das richtige Ergebnis.

## Prüfskripte

```bash
python3 docs/cotisation/pruefe_datei.py     # Struktur: XML, Spaltenfolge, Vollständigkeit
python3 docs/cotisation/pruefe_ausgabe.py   # Inhalt: Spalte M, Verteilung, Stichproben
python3 docs/cotisation/pruefe_abgleich.py  # Python-Referenz gegen Excel-Nachbau
python3 docs/cotisation/pruefe_faelle.py    # BOURG, ANSAY, QUINN, Offizielle, Phantomzeilen
python3 docs/cotisation/pruefe_spalten.py   # keine Spalte entfernt, keine Zelle verloren
python3 docs/cotisation/uebersicht.py       # Gesamtübersicht + Cotisation-UEBERSICHT.csv
python3 docs/cotisation/erkl_zeile.py 154  # Rechenweg einer Familie vollständig
```

## Übersicht (start hier)

`uebersicht.py` schreibt **`docs/cotisation/Cotisation-UEBERSICHT.csv`** – eine
Zeile pro Mitglied mit den Spalten `Zeile, Nom, Prénom, Kategorie, Spieler (L),
Spielerlizenz, Haushalt, Personen, Spieler mit Lizenz, Tarif, Rechnung traegt,
Ausgabe M, Begruendung`. Auf der Konsole zusätzlich:

1. **Spieler MIT Lizenz, aber nur Haushaltscode** – *kein* Fehler: die Rechnung
   trägt eine andere Person desselben Haushalts (z. B. BÜCHLER: Maxime Z155 = 384,
   Yannick Z154 = `F0054`; BRÜCK: Felix Z225 = 384, Oscar Z224 = `F0076`).
2. **Echte Lücken**: Haushalte, in denen jemand mit Lizenz spielt, aber
   *nirgends* ein Betrag steht – Prüfung, die alle Fehler dieser Art findet.
3. **Leere Zeilen**: 183 Phantomzeilen ohne Namen/Geburtsdatum/Lizenz.
4. **Haushalte ohne Spieler**: 23 von 181.

`erkl_zeile.py <ZeilenNr>` zeigt für eine Familie den kompletten Rechenweg
(Personen, Spieler, Tarif, wer trägt die Rechnung).

`pruefe_datei.py` ist der Gegenstück zur früheren Excel-Reparatur-Meldung und
prüft genau die Punkte, an denen Excel sonst „Problem bei einigen Inhalten“ meldet:
Wohlgeformtheit aller XML-Teile, **aufsteigende Spaltenfolge in jeder Zeile**,
**fremde Inhalte in `<row>`**, unveränderte Übernahme aller Originalzellen sowie
`app.xml`/`calcChain`. Er findet den alten Fehler zuverlässig – siehe
`regression_row1.py`, das die kaputte Fassung bewusst künstlich erzeugt.

## Abgleich Python ↔ Excel

`pruefe_abgleich.py` bildet die Excel-Formel **unabhängig** nach (eigene
Umsetzung von FamID, Schluessel, Traeger, Tarif, Zuschlag, XSEULwert und
Personenwert) und vergleicht sie Zeile für Zeile mit dem Python-Referenzmodell.
Der Abgleich hat drei echte Fehler aufgedeckt, die sonst erst in Excel
aufgefallen wären:

1. **`parse_datum` kannte keine Excel-Serienzahlen.** Spalte J enthält fast nur
   Zahlen (`ANSAY Luka` = 37023), kein Textdatum. Dadurch bekamen alle
   numerischen Daten den Ersatzwert 73415 und „Rechnungsträger = Älteste“ wurde
   faktisch zu „letzte Zeile des Blocks“. `parse_datum` akzeptiert jetzt beide
   Formen; `12.05.2001` ergibt dieselbe Serienzahl.
2. **Vorzeichen im Gleichstandsausgleich.** `Schluessel − ZEILE()/1000000` lässt
   bei gleichem Geburtsdatum die *spätere* Zeile gewinnen. Richtig ist
   `+ ZEILE()/1000000`, damit die oberste Zeile gewinnt.
3. **Config-CSV mit und ohne Kopfzeile.** `tarife-cotisation.csv` hat eine
   Kopfzeile, `ausnahmen-` und `haushalte-cotisation.csv` ebenfalls – ein
   doppeltes `[1:]` ließ `BOURG Jeannot` und den einzigen Haushalt
   (`1, Medernacherstrooss`) verschwinden. Folge: BOURG zeigte `F0006` statt
   `Don ? +(0 +50)`, und die ANSAY-Brüder je 300 statt einmal 384.
   `pruef_cotisation.liese_config()` erkennt die Kopfzeile jetzt selbst.

Zusätzlich korrigiert: der Zweig „Tarif 0“ war beim Umbau verloren gegangen –
Offizielle ohne Spielertarif zeigten `0 (+0+50)` statt `(0+50)` und leere
Zeilen zeigten `0` statt nichts. Und `XSEUL` wirkt **pro Zeile** (Belege ANSAY),
darum steht der Zweig vor der Träger-Prüfung, nicht darin.

## Warum die Zeilen jetzt nur noch an einer Stelle angefasst werden

In der ersten Fassung wurden die Zellen jeder Zeile per Regex **neu ausgelesen und
zusammengesetzt**. Dabei gingen Details wie `t="array" ref="…"` und `cm="1"`
verloren – die Ursache der Reparatur-Meldung. Jetzt gilt:

* die vorhandene Zelle **M** wird an **genau ihrer Stelle** durch die neue ersetzt
  (reiner Textersatz, Stil `s="…"` bleibt erhalten),
* die Helferzellen werden **hinten angehängt** (alle hinter `BN`, also bereits in
  aufsteigender Folge) und sortiert,
* **keine** andere Zelle der Datei wird angefasst – Kommentare, `cm=`-Metadaten,
  Array-Formeln, Formatvorlagen, VBA und alle übrigen Blätter bleiben unverändert.

## Warum ohne LET / XLOOKUP / MINIFS

Das XLSX-Format speichert Funktionen neuerer Excel-Versionen mit Sonderpräfix
(`_xlfn.LET`, `_xlfn.XLOOKUP`, `_xlfn.MINIFS`). Die alte Formel in L war genau so
gespeichert. Ohne das Präfix zeigt Excel `#NAME?`. Der Bausatz nutzt deshalb
ausschließlich klassische Funktionen – `IF`, `AND`, `OR`, `NOT`, `COUNTIFS`,
`IFERROR`, `INDEX`, `MATCH`, `SUMPRODUCT`, `MIN`, `TEXT`, `ROW`, `DATEVALUE`,
`ISNUMBER`. Damit läuft die Datei in jeder Excel-Version, in LibreOffice und in
Google Sheets. In einem deutschen Excel erscheinen die Formeln automatisch
übersetzt (`IF` → `WENN`, `COUNTIFS` → `ZÄHLENWENNS`, `INDEX/MATCH` → `INDEX/VERGLEICH`).

## Spalte O – was die Werte J / R / N / X bedeuten (wichtig!)

`O` ist **kein Freitextfeld**. In keiner Formel steht ein `X`, `x`, `ja`,
`nein` oder `1` – solche Werte werden **stillschweigend ignoriert**. Es gibt
nur drei gültige Eingaben:

| Wert | Bedeutung | Wirkung auf `L` |
|---|---|---|
| `J` | Spieler/in mit Lizenz | 300 € (SEN) / 210 € (U25) / 384 € (Familie 2+ Spieler) |
| `R` | Reserve | `(0+50)` – 50 € Zuschlag auf der eigenen Zeile |
| `N` | spielt nicht | kein eigener Spielertarif, Zuschlag bleibt möglich |
| *(leer)* | unbekannt | wie `N`, aber ohne Zuschlag-Anteil |
| **alles andere, z. B. `X`** | **undefiniert** | **wird wie „leer" behandelt – die Person fällt komplett raus** |

**Was ein `X` konkret auslöst** (gemessen mit `test_spielt_x.py`, Ist 234
Rechnungen / 55 428 €):

1. **Ist noch ein lizenzierter Spieler im Haushalt:** der Familientarif 384 €
   fällt auf den Tarif des verbleibenden Spielers (210 € oder 300 €). Der
   Betrag wandert auf die **andere** Zeile, die eigene zeigt danach nur noch den
   Haushaltscode. Ein `X` ändert also den Betrag einer **anderen** Person –
   44 Haushalte sind so betroffen.
2. **Ist die Person der einzige lizenzierte Spieler:** Tarif 0 und Zuschlag 0 →
   `L` wird **leer** (nicht „0.–") → der Haushalt **verliert die Rechnung
   komplett** und erscheint weder im `Stripe_Export` noch als Stripe-Beleg.
   Beispiel Z12 ANDRADE SOUSA Matilde: 210 € → keine Rechnung.
3. Im Mittel kostet ein `X` rund **129 €** Rechnungssumme, im Extremfall 384 €.

**Deshalb ist Spalte O rot markiert**, sobald dort etwas anderes als `J`, `R`
oder `N` steht: `O2:O900`, Regel
`AND($O2<>"",$O2<>"J",$O2<>"R",$O2<>"N")`. Ein Tippfehler ist damit sofort
sichtbar, statt eine Rechnung still zu löschen.

**Wer einen Spieler ausschließen will, ohne den Satz zu verlieren, nimmt `R`
(0+50) oder trägt den Betrag in `BX` (Manuell) ein. Wer den Satz ganz
entfallen lassen will, nimmt `N`.** Beides ist dokumentiert und im
`Cotisation`-Blatt über die Parameter steuerbar.

### Neues Mitglied eintragen — was davon Pflicht ist

Ab Zeile 774 einfach in den normalen Spalten eintragen. **Pflichtfelder, sonst
gibt es keine Rechnung:**

| Spalte | Inhalt | Ohne sie |
|---|---|---|
| `A` `B` | Name, Vorname | keine Zuordnung |
| `G` | Adresse | Haushalt wird nicht erkannt |
| `J` | Geburtsdatum | Altersprüfung kann nicht rechnen |
| **`K`** | **Alterskategorie `SEN` oder `U25`** | **kein Tarif → L bleibt leer → keine Rechnung** |
| `O` | `J` (Spieler), `R` (Reserve), `N` (spielt nicht) | Person zählt nicht |
| `Q` | Haushaltscode (`F….`, `XSEUL`) | kein Haushalt, keine Rechnung |
| `AI` | Spielerlizenz-Nummer | kein Spielertarif |
| `AX` | E-Mail | Payment Link geht, Invoice nicht |

Nach dem Eintrag: `L` rechnet sofort, die Zelle `N` wird **hellblau**, das
Blatt `Stripe_Export` zeigt die Rechnung mit Betrag, und
`stripe_sync.py` nimmt sie beim nächsten Lauf mit. **Nichts kopieren, nichts
von Hand eintragen.**

Geprüft mit `test_neues_mitglied.py`: ein Testmitglied in Zeile 774 wird vom
Modell gesehen, ergibt 300 € (Tarif SEN) und ist rechnungsfähig.

⚠️ **Ein erneuter Build verwirft neue Mitglieder.** Der Build erzeugt die Mappe
aus dem **Original**, nicht aus der Arbeitsdatei. Neue Zeilen ab 774 stünden
dann nur noch in der Sicherung `….backup-<Zeitstempel>.xlsm`. **Deshalb: nach
Neuzugängen die Datei sichern und den Build erst wieder ausführen, wenn die
neuen Zeilen auch im Original stehen** – oder den Build gar nicht mehr
brauchen, weil Spalten L und `Stripe_Export` ohnehin live rechnen. Für die
laufende Saison ist **kein** Build nötig: eintragen, `N` = `J` setzen, fertig.

## Wenn die Datei in Google Drive liegt (Tresorier mit Zugriff)

Ausgangslage: Die Arbeitsmappe liegt beim Tresorier in **Google Drive**, er
kommt nicht an den Mac und hat **keinen** Stripe-Key. Die Werkzeuge hier
laufen dagegen auf einem Rechner mit der Datei. Also: **eine Datei, ein
Ablageort, klare Reihenfolge.**

### Was der Tresorier braucht

1. Die Datei **herunterladen** (in Drive: *Rechtsklick → Downloaden*).
2. **Mit Excel öffnen, nicht mit Google Sheets.** Eine `.xlsm` in Google
   Sheets zu öffnen zerstört den Aufbau: die bedingten Formatierungen
   (hellblau/grün/rot), die Helfer-Spalten `BP:CE`, die vorberechneten Werte in
   `L` und das Blatt `Stripe_Export` werden umgebaut oder gehen verloren. Die
   Datei lässt sich danach nicht mehr zuverlässig reparieren.
3. Eintragen, `N` = `J` setzen, speichern, **wieder in Drive hochladen**.

### Was du danach machst

```bash
# 1) die hochgeladene Datei herunterladen, dann:
python3 docs/cotisation/build_perfect_workbook.py --datei "/pfad/aus/Drive/…_mit-Cotisation.xlsm"
python3 docs/cotisation/stripe_sync.py       --datei "/pfad/aus/Drive/…_mit-Cotisation.xlsm"

# 2) Ergebnis (mit den erzeugten Links) wieder in Drive hochladen
```

`--datei` verarbeitet genau die genannte Datei, egal wo sie liegt — getestet
mit einer Kopie in einem fremden Ordner. Die Statusdatei mit den
Payment-Links entsteht **neben** der Arbeitsdatei, damit der Weg zwischen
den Rechnern nachvollziehbar bleibt.

### Wichtig: nur eine Datei

Es darf **nur eine** `…_mit-Cotisation.xlsm` in Bearitung sein. Sonst
entstehen zwei Stände, die auseinanderlaufen. Die Sicherungskopien
`….backup-<Zeitstempel>.xlsm` sind bewusst keine Mappen zum Bearbeiten.

Zusätzlich: Für den Tresorier ist Google Drive die Ablage, aber **Google
Sheets ist nicht die Arbeitsumgebung**. Wer im Browser arbeiten soll, braucht
den Google-Weg mit `syncStripe()` (dort ist Sheets das Werkzeug, die
`.xlsm` aber nicht).

## Arbeit mit einer Drittperson (Tresorier) – was geht und was nicht

Kurzantwort: **Ja, er kann mit der Datei arbeiten – aber er kann die
Stripe-Links nicht selbst erzeugen.** Die Rollen sind getrennt:

| Aufgabe | Wer | Wie |
|---|---|---|
| Mitglieder eintragen, Daten pflegen | **Tresorier** | Excel, Zeilen ab 774 frei |
| Bezahlt markieren (`N` → `J`) | **Tresorier** | Excel, Zelle wird grün |
| Offene Posten sehen, Beträge prüfen | **Tresorier** | Blatt `Stripe_Export` |
| Payment Links erzeugen | **du** | `stripe_sync.py` auf dem Mac |
| Stripe-Konto / API-Key | **du** | nie in die Datei, nie ins Repo |

### Drei Fallen, die man kennen muss

1. **Der Secret Key ist keine Sache zum Weitergeben.** Wer `sk_live_…` hat,
   kann über die API das **ganze** Konto: Kundendaten lesen, Rückerstattungen
   auslösen, Preise ändern. Gib dem Tresorier lieber einen eigenen
   Stripe-Zugang mit den Rollen, die er braucht – oder er arbeitet mit
   dieser Datei, **du** machst den Sync.
2. **Ein erneuter Build überschreibt seine Eingaben.** `build_perfect_workbook.py`
   erzeugt die Mappe immer neu aus dem **Original** – alle `J` und alle neu
   eingetragenen Mitglieder lägen nur in der bisherigen Datei. Deshalb legt
   der Build jetzt vorher eine Sicherung an:
   `…_mit-Cotisation.backup-<Jahr-MM-DD_hhmm>.xlsm`. **Vor jedem Build den
   aktuellen Stand sichern** und die Sicherungen gelegentlich aufräumen.
3. **Die Datei ist eine `.xlsm` und damit kein Blatt, das man gemeinsam
   bearbeitet.** Zwei Personen gleichzeitig daran arbeiten erzeugt
   Konflikte. Erst abschließen, dann weitergeben.

### Wenn der Tresorier ohne Mac arbeiten soll

Dann lohnt sich der Google-Weg (`scripts/google-apps-script-stripe-bridge.js`):
ein Google-Sheet als Spiegel, `syncStripe()` per Zeit-Trigger, der Tresorier
arbeitet im Browser. Dafür braucht **er** den `STRIPE_SECRET_KEY` als
Script-Eigenschaft – dieselbe Rechtefrage wie oben, also bewusst entscheiden.
**Nur einen der beiden Wege benutzen**, sonst entstehen doppelte Links.

Für die tägliche Arbeit mit dieser einen Datei reicht der Direktweg: Er
markiert, du erzeugst die Links.

## Stripe starten – ganz ohne Google (Stand 27.09.2026)

Der Weg braucht **kein Google-Sheet**. Der Plan mit dem Google-Spiegel ist
optional; der einfachste Weg ist Excel → lokales Skript → Stripe. Excel bleibt
die Wahrheit, es wird nichts zwischengespeichert.

```bash
# 1) Erst nur ansehen – ohne Key, ohne Aktion
python3 docs/cotisation/stripe_sync.py

# 2) Mit Test-Keys buchen (max. 5, echte Testkarten-Zahlung nötig)
STRIPE_SECRET_KEY=sk_test_… python3 docs/cotisation/stripe_sync.py --apply --limit 5

# 3) Produktiv – verlangt eine zweite Bestätigung
M75_LIVE_OK=1 STRIPE_SECRET_KEY=sk_live_… python3 docs/cotisation/stripe_sync.py --apply

# Was schon angelegt wurde:
python3 docs/cotisation/stripe_sync.py --status
```

**Stand heute (ohne Key):** 234 Rechnungen, 234 offen, Summe **56.828 €**,
davon 2 ohne E-Mail (Payment Link geht, Invoice nicht).

### Was das Skript macht

1. Rechnet die Rechnungen mit **derselben Logik wie die Excel-Formeln**
   (`pruef_cotisation`) – nicht mit den Formeln selbst, sondern mit dem
   nachgebauten Modell, das gegen die Mappe geprüft ist.
2. Legt pro offener Zeile einen Stripe **Payment Link** an, mit
   `metadata[famid]`, `metadata[excel_zeile]`, `metadata[saison]` – damit ist
   jeder Link später wiederzufinden und zu deaktivieren.
3. Schreibt nichts in die Arbeitsmappe, sondern in eine Statusdatei
   `…_mit-Cotisation.stripe-status.json` neben der Mappe. Bereits angelegte
   Zeilen werden **nicht** erneut gebucht – auch dann nicht, wenn in Spalte N
   noch kein `J` steht.
4. **Spalte N auf `J` setzen** markiert den Posten als bezahlt: die Zelle wird
   grün, und `syncStripe()` bzw. ein späterer Lauf überspringt die Zeile.

### Sicherheitsnetze (alle getestet)

| Situation | Verhalten |
|---|---|
| ohne `--apply` | zeigt nur die Vorschau, **kein** Stripe-Kontakt |
| `--apply` ohne Key | Abbruch, nichts gebucht |
| `sk_live_…` ohne `M75_LIVE_OK=1` | Abbruch, nichts gebucht |
| Key | kommt aus der Umgebungsvariable, **nie** aus dem Repo |

### Was nur du brauchst

* **Stripe-Konto** bei stripe.com, verifiziert (Vereinsname, Adresse, IBAN,
  RCS-Nummer, Ausweis eines Vertreters). Bis dahin alles im Testmodus.
* **Secret Key** unter *Entwickler → API-Schlüssel* – zuerst `sk_test_…`.
  **Nicht** ins Repo, **nicht** in die Excel-Datei, nur als Umgebungsvariable.
* **E-Mail-Sender** (`from_email` im Payment Link) braucht eine verifizierte
  Stripe-Domain, sonst nimmt Stripe eine Platzhalteradresse. Für den Start
  reicht die Stripe-Standardadresse.

### Optional: der Google-Weg

`scripts/google-apps-script-stripe-bridge.js` macht dasselbe über ein
Google-Sheet (`syncStripe()`, Zeit-Trigger, `STRIPE_MODE=payment_link|invoice`).
Das lohnt sich erst, wenn der Tresorier die Links **ohne den Mac** täglich
aktualisieren soll. Für beide Wege gilt: **einen von beiden benutzen**, nicht
beide – sonst entstehen doppelte Links.

## Welche Zeilen eine Rechnung erzeugen (Stripe_Export Spalte A)

**Tor:** `L<>""` **und** `Q<>"GAJGL"` **und** (`BW="TRAEGER"` **oder**
`BX<>""` oder `CB<>""` oder `CD<>""`)

| Helfer | Bedeutung | Rechnung? |
|---|---|---|
| `BW` | Rechnungsträger des Haushalts (älteste Person, `Cotisation!$B$8`) | ja, 1 pro Haushalt |
| `BX` | manuelle Vorgabe | ja |
| `CB` | Personenwert: namentliche Ausnahme, Spieler mit Status `R`, offene Frage | ja |
| `CD` | XSEUL-Sonderwert (300 €) | ja |

**Warum das zweite Tor (`BX`/`CB`/`CD`) nötig ist:** `XSEUL` ist **kein
Haushaltscode**, sondern ein Status für Einzelpersonen — 74 Zeilen teilen sich
denselben `BP`-Wert `"XSEUL"` und haben damit nur **einen** Träger. Mit der
reinen `BW`-Bedingung wären **71 von 73** XSEUL-Rechnungen (je 300 €) nie im
Export gelandet, obwohl in `L` ein Betrag stand.

Gemessen mit `pruefe_stripe_export.py`:

| | Anzahl |
|---|---|
| Zeilen mit echtem Betrag (ohne GAJGL) — **Soll** | **234** |
| nur `BW="TRAEGER"` — vorher im Export | 163 |
| mit `BX`/`CB`/`CD` — jetzt im Export | **234** |
| Differenz | **+71** (49 × 300 €, 23 × `(0+50)`) |

Die 15 `GAJGL`-Zeilen bleiben draußen (reine Info, nie berechnet). Familien-
angehörige mit `Fxxxx` in `L` bleiben draußen (zeigen nur den Haushaltscode,
der Träger trägt die Rechnung) — korrekt, denn `L` ist dort kein Betrag.

**Spalte C ist der zu zahlende Betrag** – und er ist **immer eine Zahl**, auch
wenn in `L` Text steht. Ein reines `VALUE(L)` reicht nicht, `VALUE` scheiterte
an Texten:

| `L` (Spalte D zeigt den Rohtext) | `C` Betrag | Bedeutung |
|---|---|---|
| `384`, `300`, `210` | `384` / `300` / `210` | Regeltarif |
| `(0+50)` | **`50`** | 0 € Basis + 50 € Zuschlag = 50 € zu zahlen |
| `210 (+0+50)` | **`210`** | die +50 sind **Bestandteil** von 210, nicht zusätzlich |
| `Don ? +(0 +50)` | *(leer)* | Betrag steht nicht fest → nicht im Export |

Damit sind **234 von 234** Rechnungen mit Betrag befüllt (Summe **56.828 €**);
vorher waren es nur 200, weil 34 Zeilen mit Textbetrag in Stripe **ohne
Betrag** ankamen und `syncStripe()` sie deshalb übersprang. Die beiden
`Don ?`-Ausnahmen (BOURG) bleiben bewusst draußen — der Betrag ist offen.

Parser getestet mit `test_betrag_parse.py`, Soll/Ist-Abdeckung mit
`pruefe_stripe_export.py`.

Prüfen:
```bash
python3 docs/cotisation/pruefe_stripe_export.py   # Soll/Ist + Betragsabdeckung
python3 docs/cotisation/pruefe_stripe_tor.py      # Tor in der gebauten Datei
python3 docs/cotisation/test_betrag_parse.py      # Betragsparser
```

## Blatt umbenannt / neue Mitglieder (Stand 27.09.2026)

Die Mappe ist auf **Dauerbetrieb** ausgelegt, nicht auf eine einmalige
Berechnung. Zwei Regeln genügen:

### 1. Datenblatt in Excel umbenennen

| Schritt | Warum |
|---|---|
| Blatt in Excel **umbenennen** (Rechtsklick → Umbenennen) | Excel aktualisiert **alle** Formelverweise selbst – auch im Blatt `Stripe_Export` und in den bedingten Formatierungen. |
| danach `python3 docs/cotisation/build_perfect_workbook.py` laufen lassen | Der Build liest den Blattnamen **aus der Quell-Mappe** (`blattname_lesen()`) und baut alle Formeln auf den neuen Namen. Kein Suchen/Ersetzen nötig. |
| `docs/cotisation/README.md` nicht nötig anpassen | Nur `BLATT_ERWARTET` in `build_perfect_workbook.py` ist ein Default; weicht er ab, gibt das Skript eine Warnung aus. |

Ein Blattname **mit Leerzeichen** wird automatisch korrekt quotiert
(`'Neuer Name'!$A2`). Wird das Blatt **gelöscht oder verschoben**, sind die
Formeln kaputt – dann die Datei neu bauen.

**Nicht** umbenannt werden darf `Cotisation` (Parameterblatt) und
`Stripe_Export` (Spiegel für Google/Stripe) – beide werden fest im Skript und
im Apps-Script referenziert.

### 2. Laufend neue Mitglieder eintragen

Alles ist bis **Zeile 900** vorbereitet (`KAPAZITAET` in
`build_perfect_workbook.py`):

* **Datenblatt** Zeilen 774–900 enthalten bereits L-Formel, `N` = `N` und alle
  Helfer `BP:CE`.
* **`Stripe_Export`** führt die Zeilen 1:1 mit (Spalte J = `N` aus dem
  Datenblatt, Spalten K–M für Status/Link).
* Alle Haushaltszählungen (`COUNTIFS`, `SUMPRODUCT`) rechnen bis Zeile 900 –
  ein neues Familienmitglied zählt **sofort** bei seinem Haushalt mit.
* AutoFilter und Sortierzustand decken ebenfalls A1:BO900 ab.
* Bedingte Formatierung: `N2:N900` bzw. `J2:J900`.

**Neues Mitglied eintragen:** einfach die nächste freie Zeile ab 774 in den
normalen Spalten ausfüllen (Name, Vorname, Geburtsdatum `J`, Spieler `O`,
Haushaltscode `Q`, Adresse, E-Mail `AX`). `L`, die Helfer, die Farbe und
`Stripe_Export` folgen automatisch. **Keine Formel kopieren, nichts neu
eintragen.** Reicht der Platz nicht, `KAPAZITAET` erhöhen und neu bauen.

**Wichtig:** leere Zeilen bleiben restlos stumm. `BP` (FamID) liefert bei
leerem Haushaltscode `""` – dadurch entstehen **keine** Phantom-Positionen
(kein `TRAEGER`, kein Text `@774` in `L`, keine Stripe-Zeile).

### Grenze

`KAPAZITAET = 900` heißt: 127 Plätze über den heutigen 772 Datenzeilen. Reicht
das nicht, `KAPAZITAET` im Skript auf z. B. 1000 setzen und neu bauen – alles
andere skaliert automatisch mit.

### 3. Datei umbenannt (Datum im Namen)

Der Tresorier benennt die fertige Datei gelegentlich um (z. B. neues Datum).
Der Pfad ist dafür **nicht** hart kodiert, sondern liegt in
`docs/cotisation/mappe.py`:

1. Standardname `GC 2026-09-26 …_mit-Cotisation.xlsm`, falls vorhanden
2. sonst die neueste `*_mit-Cotisation*.xlsm` im Ordner (Rename erkannt,
   Meldung wird ausgegeben)
3. sonst Abbruch mit klarer Meldung

Damit darf die Datei beliebig umbenannt werden — `build_perfect_workbook.py`,
`pruefe_formeln.py` und `pruefe_alle_blaetter.py` finden sie automatisch.
Excel-Sperrdateien (`~$…`) werden ignoriert. **Wichtig:** Es darf nur **eine**
solche Datei im Ordner liegen, sonst ist „die neueste“ mehrdeutig.

Das **Original** `GC 2026-09-24 …xlsm` wird nie angefasst – es ist die Quelle
für jeden Build.

## Ausgangslage (geprüfte Fakten)

* Blatt `Membres 2026_2027`, 772 Datenzeilen (Zeile 2–773), 66 Spalten (A–BN)
* `J` Naissance · `K` Alterskategorie (SEN/U25/?) · **`L` Spieler J/R/N** ·
  **`M` Cotisatioun (Ziel)** · **`N` BEZAHLT J/N (Eingabe Kassierer)** ·
  `O` code courrier (alt) · `P` Code Courrier neu (**Familien-ID**) ·
  `AH` Spielerlizenz · `AI/AJ/AK` Offizielle-/ZS-/SR-Lizenz · `BC` Officiel
* `BP` bis `CE` sind im Blatt frei und werden für die Helfer benutzt
* Die Datei enthält keine Excel-Tabelle (ListObject), daher normale Bereichsverweise
* **Hinweis:** Es gibt ein zweites Blatt `Cotisations` mit **anderem** Layout
  (C=Alterskategorie, D=Cotisatioun, M=Code Courrier neu, AE=Spielerlizenz,
  AF/AG/AH=Offizielle, AO=Geburtsdatum, keine Spalte „Spieler J/R/N").
  Die Formeln gehören in `Membres 2026_2027`, **nicht** in `Cotisations`.
* Die Zeilen im Blatt sind vom Benutzer in Excel umsortiert worden – der alte
  CSV-Export `GC 2026-09-24 …csv` hat deshalb eine **andere Zeilenreihenfolge**.
  Die Werte werden daher direkt aus dem Blatt gelesen, nicht aus dem CSV.

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
| TraegerRegel | Aelteste | `Aelteste` = ältestes Familienmitglied nach Geburtsdatum (Gleichstand/kein Datum = oberste Zeile) · `Erste` = erste Zeile des Blocks | | | | |
| ZusatzAuchOfficiel | NEIN | Rolle als Offizieller auch in Spalte BB werten | | | | |
| ReservistenWert | (0+50) | Wert für Spieler mit Status **R** oder Code **GAJGL** | | | | |
| SaisonStichtag | 01.08.2026 | Saisonbeginn – das Alter wird an diesem Tag gemessen | | | | |
| U25MaxAlter | 25 | Wer am Stichtag noch keine 25 Jahre alt ist, bleibt die ganze Saison U25 | | | | |

B7/B8/B9 als **Text** eingeben (`NEIN`, `Aelteste`). Neue Ausnahme: Zeile in D/E/F
eintragen, G ergänzt sich selbst – Zeile 200 der Schlüsselspalte ist vorbereitet.

| D | Adresse gleicher Haushalt | J | Bemerkung |
|---|---|---|---|
| 1, Medernacherstrooss | | | ANSAY Luka + Mathis – gleiche Adresse, 2 Spieler, 1× 384, Rechnung an den Ältesten |

Weitere Zeilen in I/J = weitere Haushalte, die trotz verschiedener Familiencodes als
Einheit kotiert werden (z. B. Geschwister, die beide `XSEUL` haben).

**Warum eine Liste statt automatischer Adress-Gruppierung?** Die Daten sind für eine
automatische Zusammenfassung nicht geeignet:

* **187 von 771 Zeilen** haben gar keine Adresse
* **10 Familiencodes** sind über mehrere Adressen verteilt (getrennte Eltern,
  Pension, Ferienwohnung)
* Adressen sind uneinheitlich geschrieben (`22, RUE DE COLMAR-BERG` und
  `22,RUE DE COLMAR-BERG` sind dieselbe)
* `34, RUE PRINCIPALE` existiert in **zwei verschiedenen Orten** (Bigonville und
  Schrondweiler) – ein Schreibfehler, der beim Gruppieren falsche Verwandte
  zusammengezogen hätte

Die Liste entscheidet also bewusst, nicht die Formel. Für die ANSAYs gilt: Luka ist
sowohl der Älteste (12.05.2001) als auch die erste Zeile des Haushalts – beide
Trägerregenzen kommen dort zum selben Ergebnis.

## Helfer-Spalten BP:CE

> **Achtung:** Die Tabelle unten beschrieb noch die alte Belegung `BN:CC`
> (vor dem Spaltenumbau vom 26.09.2026). Aktuell gilt:
> `BP` FamID · `BQ` Schluessel · `BR` Aeltester · `BS` SpielerGes · `BT` SpielerSEN ·
> `BU` SpielerU25 · `BV` Zusatz · `BW` Traeger · `BX` Manuell · `BY` Tarif ·
> `BZ` AusnahmeNr · `CA` Zuschlag · `CB` Personenwert · `CC` Altersprüfung ·
> `CD` XSEULwert · `CE` Sicherung.

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
| CC | XSEULwert | 300 für `XSEUL`, außer der Haushalt aus Spalte I hat 2+ Spieler |

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

Spalte **M** – reine Anzeige, alle Werte kommen aus den Helfern:

```excel
=WENN($BP2="";"";WENN($BX2<>"";$BX2&"";
 WENN($CB2<>"";$CB2&"";
 WENN($BW2="TRAEGER";
  WENN($CD2<>"";$CD2&"";$BY2&WENN($CA2>0;" (+0+50)";""))&"";
  WENN(LINKS($BP2;4)="ADR:";$P2&"";$BP2&"")))))
```

## Reihenfolge der Prüfungen

1. kein Haushaltscode (`BP` = `@ZEILE`, Zeile ohne alles) → leer
2. `BX Manuell` ausgefüllt → dieser Wert (gilt immer und zuerst)
3. **Personenwert `CB`** → gilt auf **dieser Zeile**, unabhängig vom Rechnungsträger:
   * Name in der Ausnahmentabelle → fester Wert (Bourg/Jeannot **und**
     Bourg-Thielen/Gaby → beide `Don ? +(0 +50)`)
   * Spieler mit Spielerlizenz und Status **R** (Reserve) oder Code **GAJGL** → `(0+50)`
   * Spieler mit Lizenz und `FRAGEN` in `AW:AZ` → `(0+50)`
4. Rechnungsträger (`BW` = `TRAEGER`):
   * `P` = XSEUL → 300 (je Zeile)
   * sonst Tarif: 384 bei ≥2 Spielern oder SEN+U25, sonst 300 (SEN) bzw. 210 (U25)
   * Zuschlag `+50` **pauschal pro Familie** bei einem Offiziellen ohne Spielerlizenz
     oder Status N/R – **nicht** bei Tarif 384 (Maximum) und **nicht** pro Person
     (CLEMENT/METZLER: zwei Offizielle → trotzdem `(0+50)`)
5. **kein** Rechnungsträger → es steht der **Haushaltscode `Fxxxx`** in der Zelle.
   Damit ist auf einen Blick sichtbar, zu welchem Haushalt die Person gehört,
   und die Zeile wirkt nicht leer.

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

**Jahrgang 2002 = U25, und zwar bis zum Ende der Saison.** Alle drei Mitglieder aus
diesem Jahrgang stehen im Blatt auf U25, auch die beiden, die im Februar bzw. März
2027 **25 Jahre alt werden**:

| Geburtstag | Alter am 01.08.2026 | Alter am 31.05.2027 | K |
|---|---|---|---|
| 2002-02-21 PIRES MARTINS Jordan | 24 | 25 | U25 |
| 2002-03-06 DIEDENHOFEN Alex | 24 | 25 | U25 |
| 2002-12-18 FORTES Florian | 23 | 24 | U25 |

Das funktioniert, weil das Alter **nur** vom Geburtsdatum und dem Stichtag abhängt –
nicht vom heutigen Tag. Die Einstufung kann sich mitten in der Saison gar nicht ändern.
Eine Berechnung „Alter heute" würde genau diese beiden im Februar/März auf Senior
umstellen.

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
