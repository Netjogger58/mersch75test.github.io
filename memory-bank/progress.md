## Zweite Ursache gefunden: eine Klammer zu viel in BV – 2026-09-30

- **Symptom:** Der Reparatur-Dialog blieb trotz behobener Entities und trotz `t="str"`. Meine Prüfungen meldeten alles grün.
- **Ursache:** Ich hatte die BV-Formel beim Neuaufbau **neu konstruiert** statt zu ändern. Dabei ist an Zeichen 189 eine Klammer dazugekommen: `..."'",""))))>0,"ADR:"&` (funktionierend) wurde zu `..."'",""))))>0),"ADR:"&`. Beide sind für sich **ausgeglichen** – deshalb haben Klammerprüfung, XML-Prüfung und Entity-Prüfung alle nichts gemeldet. Excel lehnt die Datei aber ab.
- **Merksatz:** Klammerbalance beweist nur, dass die Gesamtzahl stimmt. Sie sagt nichts darüber, ob die Formel **dieselbe** ist. Erst der zeichengenaue Vergleich mit dem Original hat es aufgedeckt.
- **Lösung:** BV wird nicht mehr neu gebaut, sondern **aus der Originalformel abgeleitet**: die XSEUL-Verzweigung wird als reine Einfügung vor `,$Q{r}))` eingesetzt, ohne eine einzige Klammer zu berühren. Formel steht jetzt als **eine einzige** Python-Zeile in FORMELN – als verkettete Literale hatte Python hier schon zweimal still ein Tupel aufgesplittet (4 statt 3 Elemente), wodurch nur der letzte Teil als Formel galt.
- **Neu: `formeln_gegen_datei_pruefen.py`** vergleicht FORMELN zeichengenau mit dem, was tatsächlich in der Mappe steht, und gibt den Abstand zum Original aus. Gegen die kaputte Fassung meldet es Zeichen 189 – also genau die Stelle, an der Excel gescheitert ist.
- **Zwischenlösung:** Weil die Ursache nicht sicher war, wurde die Mappe zwischenzeitlich auf den **byte-identischen** Sicherungsstand zurückgesetzt (byteweise per `cmp` geprüft). Die E7/E8-Fassung liegt als `…mit-E7E8-2026-09-30.xlsm` daneben.
- **Verifikation:** `mappe_pruefen.py` grün, `formeln_gegen_datei_pruefen.py` grün (10/10 Spalten identisch, Abstand zum Original wie erwartet), `pruefe_formeln.py` 0 Fehler, `spec_pruefen.py` 19/19, `pruefe_stripe_tor.py` grün.
- **Lehre für die weitere Arbeit:** Vor jedem Schreibvorgang in eine `.xlsm` muss ein Test laufen, der die **geschriebene Datei** gegen die **bekannt gute Vorlage** stellt – nicht gegen die eigenen Prüfkriterien. Drei Fehler in Folge (Entities, Zelltyp, Klammerlage) waren alle nur so auffindbar.


## Excel-Reparatur-Dialog: doppelt escapte Entities in BV und CJ – 2026-09-30

- **Symptom:** Excel öffnet die Arbeitsmappe nicht mehr, sondern fragt „Wir haben ein Problem bei einigen Inhalten … Sollen wir so viel wie möglich wiederherstellen?"
- **Ursache:** In `FORMELN` standen in **BV** und **CJ** bereits die XML-Entities `&gt;` und `&amp;`. Beim Schreiben wandert jede Formel durch `esc()`, das `&`, `<`, `>` **noch einmal** escapt. Im File stand dadurch `&amp;gt;` statt `&gt;`. Excel liest das als **Text** statt als Operator, die Formel ist syntaktisch kaputt → Reparatur-Dialog. Betroffen waren ausschließlich die zwei gestern neu geschriebenen Spalten; CL, BY, BZ, CA, CE, CC, CH und L waren nie betroffen.
- **Fix:** Entities in `FORMELN` durch rohe Zeichen ersetzt. `esc()` bleibt unverändert – es ist korrekt, es darf nur keine Entities in den Quelltext bekommen.
- **Dauerhafte Absicherung:** Neue Funktion `pruefe_keine_entities()` bricht **vor** jedem Schreibvorgang ab, wenn eine Formel `&amp;`, `&gt;`, `&lt;` oder `&quot;` enthält. Aufruf als erstes in `main()`.
- **Mappe wiederhergestellt:** Aus der Sicherung `…_vor-E7E8.xlsm` (Zustand, den der User erfolgreich geöffnet hatte), danach die korrigierten Formeln neu eingespielt: 8.997 Zellen in CL, BY, BZ, CA, CE, CC, CH, BV, CJ, L. Die kaputte Fassung liegt als `…_KAPUTT-2026-09-30.xlsm` zur Analyse daneben.
- **Neu: `mappe_pruefen.py`** prüft die Mappe auf alles, woran Excel beim Öffnen scheitert: ZIP-Integrität, Wohlgeformtheit aller 38 XML-Teile, doppelt escapte Entities in der **ganzen** Mappe und Klammerbalance aller 27.486 Formelzellen in Blatt 1.
- **Verifikation:** `mappe_pruefen.py` grün (0 doppelte Entities, 0 unbalancierte Formeln, ZIP ok, Makro erhalten), `pruefe_formeln.py` 47.407 Zellen / 45 Muster / 0 Fehler, `spec_pruefen.py` 19/19, `pruefe_stripe_tor.py` und `pruefe_stripe_export.py` grün, `fullCalcOnLoad="1"` gesetzt.
- **Eigener Fehler unterwegs:** Beim Versuch, BV und CJ per Zeilenersetzung zu reparieren, wurde die BV-Formel zerstückelt und in CJ ging `$O{r}="R"` verloren. Die Datei wurde aus Git zurückgesetzt und die Korrektur minimal und maschinell vorgenommen. Lehre: Textersetzung in Formelstrings ist fehleranfällig – die Klammerbilanz muss **programmatisch** geprüft werden, was inzwischen in `pruefe_keine_entities()` und `mappe_pruefen.py` passiert.


## Turniere im Generator waren unerreichbar, magicScan stuerzte ab – 2026-09-30

- **Symptom:** Im Generator war kein einziges Turnier zu finden.
- **Ursache 1 – kein Knopf passte:** `loadWeekendSchedule` lädt nur **Freitag bis Sonntag** eines Wochenendes. Die Turniertermine liegen über die ganze Saison verteilt (11.10. bis 29.11.). Am 30.09. erreicht keiner der Knöpfe ("dieses"/"nächstes Wochenende") einen einzigen Termin.
- **Neu: Knopf „Alle Turniere laden"** lädt alle **kommenden** Turniertermine auf einmal, sortiert nach Datum, mit Datumsliste in der Statuszeile. Beschränkung auf kommende Termine ist Absicht: sonst würden beim nächsten Aufruf alte Einträge die Felder überschreiben.
- **Ursache 2 – magicScan stürzte ab (schwerwiegender):** In der Typ-Erkennung stand ein Ausdruck mit `game.halle` und der erst 40 Zeilen später per `let` deklarierten Variablen `parsedLocationValue`. Im Zeilen-Loop gibt es **keine Variable `game`**, `parsedLocationValue` liegt in der TDZ. Sobald eine Turnierzeile gelesen wurde, warf die Funktion einen **ReferenceError** – es landete überhaupt nichts in den Feldern. Zusätzlich hätte das `else` jedem Turnier **ohne Halle** den Typ „Season Games" gegeben. Zeile entfernt; der Ort wird weiter unten korrekt aus `hallCodes` aufgelöst.
- **Neu: `generator_magicscan_pruefen.py`** führt magicScan mit den echten Turnierdaten aus und prüft Typ-Erkennung, Reichweite der Oberfläche und Abdeckung durch den neuen Knopf. Der Test reproduziert die alte Zeile und belegt den ReferenceError.
- **Entfernt: U9-Turnier am 11.10.2026 (Mersch75)** auf Wunsch des Users, in `generator.html` und `live-center.html`. Das U11-Turnier am selben Tag (HB Esch) bleibt. Stand: 6 Turniere im Generator, 8 im Live Center (davon 2 ältere aus der Vorsaison: 10.11. und 22.11.).
- **Eigener Testfehler unterwegs:** Der Datums-Parser im Test (`split(".").reverse().join("-")`) erzeugte ein ungültiges Datum, der Test meldete deshalb „0 Turniere". Durch echtes Zerlegen von Tag/Monat/Jahr ersetzt.
- **Verifikation:** `generator_tour_pruefen.py` grün, `tourer_sichtbarkeit_pruefen.py` grün, `generator_magicscan_pruefen.py` grün, beide JS-Blöcke mit `node --check` gültig.


## U11-Turniere waren unsichtbar – Phantom-Filter gefunden und entschärft – 2026-09-30

- **Symptom:** Im Live Center waren **5 U9-Turniere und 0 U11-Turniere** sichtbar, obwohl 4 U11-Termine korrekt in den Daten standen. Die Rohdaten waren zu jedem Zeitpunkt richtig – der Fehler lag **ausschließlich in der Anzeige**.
- **Ursache:** In `renderAllGames` unterdrückte ein alter Phantom-Zeilen-Filter jede Zeile, auf die `/Turn.?ier\s*U11/i` auf **`heim` UND `gast`** passte. Er war für eine alte Platzhalter-Zeile gedacht, hat aber jede echte U11-Turnierzeile (`gast: "Turnier U11"`) mit weggenommen. U9 war nicht betroffen, weil das Muster nur „U11" kennt – daher genau „5 U9, 0 U11".
- **Fix:** Der Filter unterdrückt jetzt nur noch Zeilen **ohne Team UND ohne Ergebnis**. Die 4 U11-Turniere erscheinen wieder.
- **Der eigentliche Fehler war meiner:** Ich hatte die Turnierdaten korrekt eingetragen, `node --check` war grün und mein Sichtbarkeitstest war ebenfalls grün – weil er nur die **Daten** prüfte, nicht den **Anzeigefilter**. Die Prüfung muss die Seite nachbilden, nicht nur die Daten lesen.
- **Test erweitert:** `tourer_sichtbarkeit_pruefen.py` sucht jetzt **alle** Zeilen-Unterdrücker der Form `if (…) return;` im `renderAllGames`-Block, wertet jeden gegen die echten Turnierdaten aus und meldet jeden, der ein Turnier verschluckt. Er verdrahtet **keinen** aktuellen Filter fest, sondern findet neue automatisch. Optionaler Pfad-Parameter erlaubt den Lauf gegen einen alten Stand.
- **Wirksamkeitsbeweis:** Gegen den gepushten Commit `d5f8b83` (mit dem Fehler) meldet der Test **4 unterdrückte Turniere** namentlich: 10.11., 11.10., 18.10. und 25.10.26. Gegen den aktuellen Stand: grün. Erst dieser Vergleich macht den Test glaubwürdig.
- **Generator geprüft:** dort tritt der Fehler nicht auf – es gibt keinen solchen Filter, und die 7 Zeilen bleiben nach der Deduplizierung erhalten (`generator_tour_pruefen.py` grün).
- **Verifikation:** `live-center.html` mit `node --check` gültig, beide Turnier-Tests grün, Debug-Skript entfernt.


## Anleitung, Stripe-Test und Live-Center-Turniere – 2026-09-30

- **`ANLEITUNG-Cotisation-Tresorier.md` überarbeitet** (829 Zeilen, 6.113 Wörter, 19 Kapitel): neues Kapitel **19 „Die Prüfskripte"**, neuer Rubrik-Abschnitt **„Ein Haushalt, eine Rechnung"** (E7), Checkliste um „kein Haushalt hat zwei Posten" ergänzt, Kapitel 11 um `XS:<Card-ID>` erweitert, Kapitel 12 an E7 angepasst, Kapitel 7 stellt klar dass das Stripe-Tor auf **`$CC`** beruht (nicht `$BW`).
- **Stripe: ja, aktuell – aber ein Test war tot.** `pruefe_stripe_tor.py` suchte `</f></c>`, Excel schreibt aber `</f><v/>`: **0 Treffer**, `IndexError`. Das Skript lief nie. Erster Fehler gefunden: der Regex. Zweiter: es erwartete noch `$BW` statt `$CC` und meldete „Tor FEHLT", obwohl das Tor korrekt ist. **Beides behoben**, jetzt `ERGEBNIS: Tor im File korrekt verbaut`. `pruefe_stripe_export.py`: 180/180, 39.168 €.
- **Zwei Fehler im eigenen Prüftool gefunden und behoben:** GitHub wandelt **jedes** Leerzeichen in einen Bindestrich um (nicht nur Folgen), und Anker müssen URL-dekodiert verglichen werden. Ohne das hätte der Prüfer 2 korrekte Links als tot gemeldet. Beim Reparaturversuch hat ein Skript versehentlich den Link von Kapitel 6 überschrieben – **wiederhergestellt und geprüft**.
- **`live-center.html`: 7 Turniere eingetragen** (U11: 11.10. HB Esch, 18.10. + 25.10. Mersch75 · U9: 11.10. + 25.10. Mersch75, 25.10. HB Pétange, 15.11. HB Dudelange, 29.11. HB Museldall).
- **Dabei ein Duplikat gefunden und entfernt:** die drei Turnierzeilen standen **zweimal** im File – einmal in `tournamentData` (Z. 519) und einmal in einem zweiten `concat` (Z. 1070). Jedes Turnier erschien dadurch doppelt in „Alle Spiele". Die Daten liegen jetzt nur noch an einer Stelle.
- **`generator.html`: dieselben 7 Turniere** in der Spieldatenliste, mit eindeutiger `nr` nach dem Muster `<Team>T<Tag><Monat><Jahr>` (U11 nutzt dort `JUGEND: U11 Espoir` statt `U11M-1` wie im Live Center). `halle` leer bei Auswärtsturnieren – nur Mersch75 hat eine Halle (290101). U11 18.10.26 war bereits vorhanden.
- **Verifikation:** beide JS-Blöcke mit `node --check` syntaktisch geprüft (**beide OK**), Turnierzeilen gezählt (10 im Live Center ohne Duplikate, 7 im Generator, keine doppelte `nr`).


## E7 und E8 umgesetzt – 2026-09-30

- **E7 (ein Posten je Haushalt)** und **E8 (eigener Schlüssel je XSEUL-Mitglied)** sind jetzt in Python (`pruef_cotisation.py`) **und** in der Excel-Mappe (`cotisation_regeln_setzen.py`, Spalten **BV, CH, CJ, L**) umgesetzt. Freigabe des Users: „setze es um“.
- **Ergebnis: 196 → 195 Posten, 39.968 → 39.918 €** (Delta exakt −50 €). Der einzige betroffene Haushalt ist **F0026**: METZLER Bernard (Z377) ist Comité-Mitglied, aber nicht Rechnungsträger — er zeigt jetzt den Familiencode `F0026` statt einer eigenen 50-€-Rechnung. CLEMENT Liliane (Z96) rechnet den Haushalt mit `(0+50)` ab.
- **E8 in `BV`:** XSEUL bekommt jetzt `XS:<Card-ID>` statt des Sammelcodes. **XSEUL-Schlüssel 1 → 72**, Postenzahl der XSEUL-Mitglieder bleibt bei **61** (nur die Gruppierung ändert sich, nicht die Beträge). Die Adressprüfung steht bewusst **vor** der XSEUL-Prüfung, damit die ANSAY-Brüder als gelistetes Adress-Haushalt bei 1× 384 bleiben.
- **Wichtige Korrektur einer Fehlannahme:** XSEUL und GAJGL sind **keine Haushalte**, sondern Sondercodes, die pro Zeile gerechnet werden (Zweig 4, vor der Träger-Prüfung). Eine pauschale E7-Ausnahme für beide hätte 87 Zeilen / ~10.500 € ersatzlos gelöscht. Die E7-Bedingung in Python lautet deshalb `i == traeger[key] or fam == GAJGL_CODE`, in Excel `OR($CC="TRAEGER",$Q="GAJGL")`.
- **Weitere Korrektur:** Der erste Excel-Entwurf ließ die Comité-50-€-Regel in `CJ` **vor** der Spielberechtigkeit greifen. Damit wäre VAN DER WEKEN Louis (XSEUL, Comité, Status R) von 50 € auf `(0+50)` = 0 € gefallen. Die Reihenfolge ist jetzt `CL=1 → 300` **vor** `BI<>"" → 50`, deckt sich mit Python und mit der Aussage des Users zu seinem Beispiel.
- **Verifikation:** Der Excel-Zweig wurde durch einen **unabhängigen Nachbau der Formelkette** (nicht von `pruef_cotisation` abgeleitet) gegen das Python-Modell geprüft, jeweils alt gegen neu. **Excel-Delta = 1 Zeile (Z377), Python-Delta = dieselbe 1 Zeile, Schnittmenge identisch, „nur in Excel" = leer.** Die 25 weiteren Python-only-Zeilen sind die schon previously eingebaute P-Regel (leer → `0`), kein E7/E8-Effekt.
- **Datei geprüft:** ZIP intakt, 43 Teile, `vbaProject.bin` erhalten, `<calcPr fullCalcOnLoad="1"/>`, `pruefe_formeln.py` 47.407 Formelzellen / 45 Muster / **0 Fehler**, `spec_pruefen.py` **19/19**, `test_betrag_parse.py` grün, 8.997 Zellen geschrieben (Zeilen 2–901; BV fehlt in 583–585, das ist vorbestehend).
- **Sicherung:** `…_regeln-2026-09-29_vor-E7E8.xlsm` plus automatische `…_regeln-2026-09-30_0732.xlsm`.
- **Offen:** Die Mappe muss einmal in Excel geöffnet und gespeichert werden, damit die gecachten Werte neu berechnet werden — erst danach ist `pruefe_excel_gegen_python.py` aussagekräftig. **GAJGL bleibt die einzige Sammelcode-Ausnahme** (15 Mitglieder, 700 €, alle `(0+50)`); ob GAJGL ebenfalls einen eigenen Schlüssel je Person braucht (E6), ist nicht entschieden.


## E2 gestrichen: kein 350 €, und zwei Fehlbestände in der Mappe gefunden – 2026-09-29

- **Beschluss des Users:** „Ich habe 350 € als Vorschlag hinterlegt, braucht es nicht – da 300 für Erwachsenenbeitrag ja auch die 50 € inkludiert, wenn man im Comité ist oder andere Offizielle Funktionen hat wie Zeitnehmer oder Schiedsrichter (z. B. Louis Van der Weken).“ **E2 ist damit entschieden und gestrichen.**
- **Folge in der Spezifikation:** Der Zuschlag hängt jetzt **am Rechnungsträger**, nicht mehr am Haushalt. Neue Prüfkette in § 4/§ 7: `TARIF ∈ {300, 384}` → 0 · `TARIF = 210 und Träger ist Spieler` → 0 · sonst `Träger im Comité` oder `Träger opt_stimmrecht` → 50. **Es gibt keinen Pfad zu 350 € mehr**; das rechnerische Maximum ist 384.
- **Die einzige verbleibende Addition ist 210 + 50 = 260**, und zwar genau dann, wenn der Rechnungsträger **selbst kein Spieler** ist und den Haushalt allein mit einem Jugendbeitrag vertritt (SCHUSTER Jeff). Testfall **T18** sichert das ab.
- **Vier neue Testfälle T16–T19** ergänzt, darunter **T16/T17** als Prüfsteine: 300er-Haushalt mit Nichtspieler im Comité als Träger → **300**, nicht 350. **Verifikation: 19/19 bestanden.**
- **Zwei Fehlbestände in der Live-Mappe gemessen** (in § 10 dokumentiert):
  1. **300er-Haushalt kann 350 € ergeben** – der Träger bekommt 300 €, und ein Comité-Mitglied auf einer **anderen** Zeile desselben Haushalts bekommt eine **eigene 50-€-Rechnung**. Referenzfall ist genau VAN DER WEKEN Louis (Z537): Spielerpass + Zeitnehmer-Lizenz + Comité, nicht Träger, Ergebnis 50 € als **eigener** Posten.
  2. **Manche Haushalte bekommen mehr als eine Rechnung:** `F0026` = 2 Posten / **100 €** (CLEMENT `(0+50)` + METZLER `50`).
- **Zusätzlich aufgefallen: `XSEUL` ist ein Sammelcode, kein Haushalt.** 72 Mitglieder teilen sich denselben Haushaltsschlüssel, dadurch 61 Posten in einer Gruppe. Das ist ein Fehler der **Haushaltsbildung**, nicht der Beitragshöhe – XSEUL ist laut eigener Regel *kein* Familiencode. Als **E8** aufgenommen (Vorschlag: eigener Schlüssel `XS:<Card-ID>` je Person), **E7** fragt die Ein-Posten-Regel je Haushalt ab.
- **Nichts in der Excel-Mappe geändert** – beides ist erst nach Freigabe von E7/E8 sinnvoll umsetzbar, weil es die Postenzahl und damit echte Beträge verschiebt.

## Beitragsregeln als Spezifikation formalisiert – 2026-09-29

- **Vom User gelieferte 5 Regeln** (Haushalts-Obergrenze 384 · Doppelrolle Spieler+Offizieller zahlt nur den Höchstbetrag · fakultativer 50/0-Zuschlag für Offizielle · Comité-Mindestbeitrag 50 · Inklusion bei 384 bzw. 210+50=260 beim Jugendbeitrag) in **`docs/cotisation/beitragsregeln-spezifikation.md`** (315 Zeilen, 12 Kapitel) zu einer eindeutigen Berechnungsvorgabe ausformuliert: Begriffe, Eingangsdaten, drei Rechenschritte, Pseudocode, 15 Testfälle, System-Prompt, Abgleich mit der Ist-Mappe, offene Entscheidungen.
- **Kern der Logik:** Tarif ist eine reine Funktion der **Spielerzahl im Haushalt** (0/1/2+ sowie SEN+U25). Der 50er-Zuschlag ist **ein Betrag pro Haushalt** und wird nur nach der Prüfung `TARIF = 384 → 0` vergeben. Regel 2 folgt automatisch, weil Spieler nie in die Menge der zuschlagsauslösenden Personen aufgenommen werden. `min(tarif+zuschlag, 384)` ist als Schutzschranke eingebaut, rechnerisch aber redundant (Maximum real 350).
- **Die Tests haben zwei echte Fehler in meiner eigenen Spezifikation aufgedeckt** – Grund für den Mehraufwand, aber genau der Zweck: `STIMMTRECHTEN` prüfte zunächst `any(m.opt_stimmrecht)` **ohne** den Spielerausschluss. Dadurch hätte ein Spieler mit Stimmrecht-Opt-in trotz Regel 2 einen Zuschlag ausgelöst (T9 ergab 260 statt 210, T15 350 statt 300). Korrigiert auf `m.opt_stimmrecht and not m.ist_spieler`; die Warnung steht jetzt in § 4, § 7 und im System-Prompt, damit sie beim Vereinfachen nicht verlorengeht.
- **Verifikation:** `docs/cotisation/spec_pruefen.py` rechnet die 15 Testfälle gegen den Pseudocode aus § 7 → **15/15 bestanden**. T8 und T10 (Comité + zwei Spieler → 384, nicht 434) sind die Prüfsteine für die Inklusionsregel.
- **Abgleich mit der Ist-Mappe: 4 von 5 Regeln sind bereits umgesetzt.** Obergrenze, Doppelrolle, Comité-Mindestbeitrag und die Inklusionsregel funktionieren. **Einziger Fehlbestand ist Regel 3:** heute löst die Mappe 50 € automatisch aus, sobald eine Offiziellen-Lizenz existiert – die Wahl 50 **oder** 0 gibt es nicht. Dafür ist **ein neues Feld nötig** (Vorschlag `CN` `Stimmrecht (50/0)`); ohne dieses Feld wäre es eine andere Regel.
- **Sechs offene Entscheidungen dokumentiert (E1–E6),** davon zwei mit Geldwirkung: **E1** gilt Regel 2 auch für jemanden mit Spielerlizenz und Status `N`/`R`? **E2** bekommt ein Comité-Mitglied, das als Erwachsener 300 € als Träger zahlt, zusätzlich 50 € (→ 350 €)? Regel 5 nennt nur den Jugendfall.

## Rubrik ergänzt: „Das muss der Tresorier wissen" ganz oben – 2026-09-29

- **Auf Wunsch des Users die Anleitung geteilt** in einen Handlungsteil und einen Referenzteil. Datei jetzt **759 Zeilen / 5.508 Wörter**.
- **Rubrik (Zeile 18–134, H1 mit 🔴):** reine Praxis, kein Technik-Inhalt.
  - *Die fünf wichtigsten Regeln* (nur Excel · nie in L/N schreiben · Beträge nie von Hand korrigieren · `B13` am 1. Januar hochzählen · Geburtsdaten prüfen)
  - *„⚠️ Womit man am häufigsten auf die Nase fällt"* – 7 Fallen mit Ursache und Gegenmaßnahme, darunter die gefährlichste: **fehlende Alterskategorie in K erzeugt lautlos 0 €** ohne jede Fehlermeldung
  - *Die vier Beträge* (300 / 210 / 384 / 50) inklusive `(0+50)` als Schreibweise
  - *„Der Satz, der am häufigsten Rückfragen verursacht"*: **In L steht keine Zahl, sondern eine Anweisung** – `Betrag_EUR` in `Cotisatiounen` ist die Wahrheit
  - *Wer zahlt in einer Familie* mit den drei Kontrollfragen (volljährig? Geburtsdatum? Adresse identisch?)
  - *Checkliste vor dem Abschicken* (7 Punkte)
  - *Wo man Fragen stellt* (Adrien vs. Secrétariat) und *Wenn etwas schiefgeht* (6 Symptome mit erster Hilfe)
- **Referenzteil (ab Zeile 136, H1 mit 📘)** unverändert die 18 Kapitel, jetzt mit der Überschrift *„Inhalt des Referenzteils"*, damit klar ist, dass das Inhaltsverzeichnis nur diesen Teil abdeckt.
- **Prüfung:** Rubrik beginnt vor dem Referenzteil · 18 Kapitel = 18 TOC-Einträge, kein Verweis ohne Ziel · 0 unvollständige Tabellenzeilen · alle 8 Rubrik-Bausteine vorhanden.

## Anleitung für den Tresorierer vollständig neu geschrieben – 2026-09-29

- **`Vereins-OS/docs/ANLEITUNG-Cotisation-Tresorier.md` von 251 auf 630 Zeilen erweitert** (4.530 Wörter, 18 Kapitel, 19 Unterkapitel). Zuvor war die Datei an vielen Stellen veraltet.
- **Alte, jetzt falsche Angaben sind entfernt** (automatisch gegengeprüft): `Spielt J/R/N/X` → `J/R/N/P` · „Daten enden in Zeile 591“ → 901 · „Hilfsformeln bis 903“ → 901 · „235 Posten / 53.846 €“ → 181 Posten / 39.218 € · „Diese Regel ist bisher NICHT in die Berechnung eingebaut“ (Spielberechtigung **ist** inzwischen in `CL` eingebaut) · Hilfsspalten „BP bis CE“ → korrekt `BV` bis `CL`.
- **Neu und aus der Datei ausgelesen, nicht geraten:** alle 14 Blätter · die **90 Spalten A–CL** des Hauptblatts getrennt in Eingabe (mit Pflichtangabe) und berechnet · die **13 Konfigurationszellen** `Cotisation!B1:B13` mit Name, Wert und Wirkung · die Ausnahmen-Liste F/G und die Haushalts-Adressen I · die **17 Hilfsspalten BV–CL** mit dem, was sie rechnen · die Reihenfolge der 9 Prüfstufen in der L-Kette.
- **Blatt `Cotisatiounen` (A–AE) und `Stripe_Export` (A–M) sind erstmals dokumentiert.** Wichtig: dieses Blatt ist **nicht leer** (1,9 MB, 901 Zeilen) – meine erste Inventur am 29.09. hatte es noch vor dem Excel-Speichern der 18:25-Datei als leer gesehen. Es wandelt die Textausgabe aus L in eine echte Euro-Zahl (`Betrag_EUR`, Summe 39.218 €) und hält den Stripe-Stand (`AC`/`AD`, beide noch leer).
- **Zwei Kapitel aus den heutigen Ermittlungen:** Kapitel 10 dokumentiert die Schwäche beim Rechnungsträger (fehlende Geburtsdaten → Kind wird Träger, 122 Träger unter 18, 321 ohne Datum) mit Verweis auf `Jugend-Zahler.csv`; Kapitel 6 erklärt ausdrücklich, **warum** `P` nicht pauschal 0 ergibt (sonst verlören sechs Haushalte mit 1.434 € ihre Rechnung).
- **Kapitel 16 neu: „Was die Datei ausdrücklich nicht kann“** – damit klar ist, dass sie kein Mahnwesen, keine Dublettenprüfung und keine Vollständigkeitsprüfung hat (fehlende Alterskategorie erzeugt lautlos 0 €).
- **Bestandszahlen aktuell:** 590 Mitglieder · Status `N` 292 / `J` 204 / `P` 64 / `R` 30 · 503 in F-Haushalten, 72 XSEUL, 15 GAJGL.
- **Endprüfung:** 18 Kapitel = 18 TOC-Einträge, kein TOC-Eintrag ohne Ziel, 0 unvollständige Tabellenzeilen.
- **Merksatz:** Beim schrittweisen Einfügen mit `insert_line` haben sich Textblöcke verschoben (Abschnitt 14 landete am Dateiende, der Körper von Abschnitt 12 ebenfalls). Deshalb wurde das Dokument am Ende **mit einem Skript neu erzeugt** statt weitergepatcht. Bei Dateien dieser Größe: lieber Generator-Skript, Abschnitt für Abschnitt an `T` anhängen, am Ende einmal schreiben.

## Excel-Formel L angewendet: P→0 in der Live-Mappe (Datei 18:25) – 2026-09-29

- **Beschluss bestätigt vom User:** „Bei ‚P‘ als Erwachsener Elternteil von Jugendspieler bekommt die Rechnung des Jugendspielers geschickt – das gleiche wie bei N.“ In den Daten verifiziert: Z57 BINGEN Dani (J) zeigt `F0015`, Z58 BINGEN Fränk (P) trägt **210**; ebenso Z143/Z144, Z158/Z160, Z222/Z223, Z494/Z496 sowie Z351 MARCK Peter (P) mit **384** bei 3 Spielern im Haushalt. **Keine Code-Änderung nötig** – die bestehende Logik `P und BY=0 → 0` lässt genau diese 6 Haushaltsträger unberührt.
- **Medico-Regel bestätigt:** `int(AX) >= 2026` gilt unverändert, 2025 und früher = keine gültige Lizenz. RESSEL Z458 (2023) und ROCHA MAJERUS Z468 (2025) stehen dadurch auf 0.
- **Blocker `LETZTE` behoben:** `cotisation_regeln_setzen.py` hatte `ERSTE, LETZTE = 2, 902`, im Blatt existiert Zeile 902 aber nicht (Lücke 902–908, danach nur verwaiste BZ-Zellen 909–911). Die Vorpruefung brach mit „1 Zeilen fehlen im Blatt“ ab. → `LETZTE = 901` (letzte vollständige Zeile mit A..L und BV..CL).
- **`fullCalcOnLoad` ergänzt:** Das Skript ersetzt 8.100 Formelzellen und entfernt dabei die gecachten `<v>`-Werte. Ohne `<calcPr fullCalcOnLoad="1">` hätte die Mappe beim Öffnen überall leer ausgesehen, bis manuell Strg+Alt+F9 gedrückt würde. Der Baustein ist jetzt fester Bestandteil des Schreibabschnitts (Muster wie `build_perfect_workbook.py:203`) – inkl. Abbruch, falls `workbook.xml` kein `calcPr` enthält.
- **Geschrieben:** 8.100 Zellen in CL, BY, BZ, CA, CE, CC, CH, CJ, L, Zeilen 2–901. Sicherungen `…regeln-2026-09-29_1826.xlsm` und `…_1827.xlsm`.
- **Verifikation:** ZIP intakt (40 Teile, `vbaProject.bin` erhalten) · `<calcPr fullCalcOnLoad="1" calcId="191029"/>` · L458 enthält die P-Schranke · `pruefe_formeln.py` **38.417 Formelzellen, 45 Muster, 0 Fehler** · `test_betrag_parse.py` grün · **196 Stripe-Posten unverändert**.
- **Wichtiger Hinweis:** `pruefe_excel_gegen_python.py` meldet bis Excel die Datei **einmal geöffnet** hat alle 572 Zeilen als Abweichung – es liest die gecachten `<v>`-Werte, und die sind jetzt absichtlich leer. Nach dem Öffnen und Speichern in Excel stimmen sie wieder.

## Status P: „P mit Lizenz ist 0" eingebaut (Modell + Excel) – 2026-09-29

- **Beschluss des Users:** RESSEL Chloé (Medico 2023) und ROCHA MAJERUS Darius (Medico 2025) sind absichtlich auf **P** gesetzt und sollen **0** zahlen. Regel: **`P` + Lizenz = 0**.
- **Modell (`pruef_cotisation.py`):** neue Konstante `NICHT_SPIELER_CODE = "P"`. Im Zweig „kein Spielertarif, kein Zusatz“ gilt jetzt: `P` **und** kein spielberechtiger Haushaltsmitglied (`sp_gesamt == 0`) → `"0"` mit Grund „Status P, kein Spielertarif im Haushalt“; sonst unverändert leer. GAJGL/XSEUL-Zweige bleiben **vor** diesem Zweig unberührt.
- **Excel (`cotisation_regeln_setzen.py`, Spalte L):** neue Schranke `IF(AND($O{r}="P",$BY{r}=0),"0", …)` direkt nach der Leerzeilen-Prüfung, plus **eine** zusätzliche schließende Klammer am Kettenende. `BY` = SpielerGes (zählt nur spielberechtigte J-Mitglieder), deshalb greift die Schranke **nur** bei Haushalten ganz ohne Spieler.
- **Der entscheidende Sicherheitsnachweis:** 6 P-Mitglieder sind Rechnungsträger eines Haushalts **mit** spielberechtigtem Spieler und zahlen heute echte Beträge – BINGEN Fränk Z58 **210**, DOS SANTOS RIBEI Camila Z144 **210**, ELSEN Emily Z160 **210**, HAAS Tom Z223 **210**, MARCK Peter Z351 **384**, SCHMITZ Nathanaël Z496 **210** = **1.434 EUR**. Ohne die `BY`-Bedingung wären diese 6 ersatzlos auf 0 gefallen. **Sie bleiben unverändert** – genau deshalb ist die Formel nicht `O="P"→0`, sondern `O="P" UND BY=0 → 0`.
- **Bilanz unverändert:** Modellsumme **37.518 EUR / 196 Stripe-Posten** vor und nach der Änderung. Der P-Zweig erzeugt also **keine** neue Rechnung und nimmt **keine** weg – er schreibt nur „0“ statt eines leeren Feldes.
- **Excel-Formel noch nicht angewendet:** `cotisation_regeln_setzen.py --apply` bricht weiterhin ab (`1 Zeilen fehlen im Blatt, z. B. [902] – Zeilengrenze pruefen`, `LETZTE=902` vs. letzte Datenzeile 901). Das ist ein **vorbestehender Blattgrenzen-Zustand**, unabhängig von dieser Änderung, und wurde nicht eigenmächtig angefasst.
- **Verifikation:** alle 9 Formeln aus `FORMELN` klammerbalanciert (L: 23/23) · `pruefe_formeln.py` 19.387 Formelzellen, 45 Muster, **0 Fehler** · `test_betrag_parse.py` grün · `py_compile` grün.
- **Weiterhin offen:** GAJGL-Höhe (0 oder `(0+50)`) und die 25 P-Zeilen ohne Spieler im Haushalt, die Excel-seitig noch `(0+50)`/`''` zeigen – Update der Mappe steht aus.

## P-Status (vormals X), GAJGL und Bénévole-Spalte – Analyse + zwei Fixes – 2026-09-29

- **X → P:** Kopf der Spalte O heißt jetzt `'Spielt J/R/N/P'` (SharedString, geprüft). Der reine Texttausch reicht nicht: `pruef_cotisation.SPALTEN_ALT` kannte nur `"…/X"`, also wäre **jeder Modell-/Stripe-Lauf mit `FEHLENDE SPALTEN` abgebrochen**. → Alias `"Spielt J/R/N/P"` ergänzt (`pruef_cotisation.py:70`). Kein Logikumbau nötig: die Modell- und Excel-Logik prüft O nur auf `J`/`N`/`R`; `P` verhält sich automatisch wie das alte `X` = „kein Spieler“.
- **Bénévole-Spalte ist AN, nicht AI:** Layout hat sich verschoben – `AI` heißt jetzt `U9F` (Jugendlizenz), `AN` = `'Bénévole (B)'`. `benevole_setzen.py` schrieb bisher nach **AI** und hätte dort Lizenznummern mit „B“ überschrieben; außerdem war das Ziel AN in der Prüfmenge `AH..AN` enthalten (Ursache der falschen „253 Verletzungen“). → `ZIEL_SPALTE="AN"`, `PRUEF` auf die echten Lizenz-/Rollen-Spalten **AG–AM + AO–AS** gesetzt (Ziel aus Prüfung raus). Trockenlauf auf der Live-Mappe erkennt Kopf korrekt: 590 Zeilen mit Name, **275 Kandidaten** ohne Lizenz & ohne GAJGL. **Nicht `--apply`**: die Auto-Regel würde die Liste über die vorhandenen ~258 B hinaus VERGRÖßERN (sie erfasst auch Inaktive/Passive) – Ausdünnen bleibt Handarbeit über `Benevole-Durchsicht.csv`.
- **Blatt `Cotisatiounen` (sheet2.xml) ist leer** (`<sheetData/>`, 1189 B). Eine „Automatik Membres→Cotisatiounen“ existiert nicht und ist ein Irrglaube; gerechnet wird über die Helfer BV–CL in `Membres` und Ausgabespalte L.
- **Fehlende Helfer BV/BW/BX bei Neuzugängen (Z583–585 ZEBROWSKY/ZELLER):** dort fehlen die Zellen `BV`(FamID)/`BW`(Schlüssel)/`BX`(Ältester) (+ CF/CG). `cotisation_regeln_setzen.FORMELN` erzeugt sie **nicht** (nur CL,BY,BZ,CA,CE,CC,CH,CJ,L) → Excel-L bleibt leer. **Aber:** `pruefe_stripe_export` und `stripe_sync` rechnen über `pr.berechne()` (Python-Modell), lesen **nicht** Spalte L → **Stripe-Beträge sind davon nicht betroffen**, nur die Excel-Sicht. → Display-Problem, kein Rechnungsfehler.
- **GAJGL:** in `pruef_cotisation` bereits behandelt (`fam=="GAJGL"` → 0, bzw. Personenwert `(0+50)` wenn Spielerlizenz vorliegt, Zeile ~386/433). Excel-`CH` liefert für GAJGL `(0+50)` (Cotisation!B10=`(0+50)`). Beide stimmen für lizenzierte GAJGL überein. **Punkt „GAJGL = 0?“ bleibt Fachentscheidung**, nicht eigenmächtigt geändert.
- **Offene Fachentscheidungen (blockieren weitere Formel-/Semantik-Änderungen):**
  1. **P-Mitglied mit Lizenz / als Rechnungsträger:** Z458 RESSEL und Z468 ROCHA MAJERUS sind `O=P`, haben aber Spielerpass (AO) und hängen an Familien F0032/F0091. Excel zeigt `(0+50)`, Modell zeigt leer. Zahlt ein P-Mitglied den Haushalts-/Tarifbetrag, `(0+50)`, oder 0?
  2. **GAJGL-Höhe:** fester 0-Betrag oder `(0+50)` (Status quo)?
- **Verification:** `pruefe_excel_gegen_python.py` auf der 09-29-Mappe läuft jetzt durch (vorher Abbruch): 549 Zeilen, 5 echte Abweichungen – davon 3 = fehlende Helfer (Z583–585, Modell korrekt), 2 = P-Politik (RESSEL/ROCHA). Beide geänderten Skripte `py_compile`-grün.
- **Kratz-Skripte** (`_kopf.py`, `_kopf2.py`, `_abwe.py`, `_zell.py`, `_cot*.py`) nur zur Analyse, nicht Teil der Pipeline.

## Spielberechtigung (Pass + Medico) – Regel dokumentiert, Auswirkung gemessen – 2026-09-27

- **Vorgabe des Users:** Ohne Spielerpass darf niemand spielen. `XXX` im Spielerpass = Antrag an die FLH geschickt, **Lizenz existiert noch nicht**. Ein vorhandener Pass braucht ein vorhandenes Medico. Medico und Lizenz sind **jahres-, nicht saisonabhängig**: 2026/27 braucht AX ≥ **2026** (gültig bis 31.12.2026), ab 1.1.2027 muss **2027** stehen.
- **Wichtige Erkenntnis zur Spalte AX:** Sie enthält **2031, 2035, 2028 …** – also das **Jahr BIS WANN gültig**, nicht das Jahr der Untersuchung. Meine erste Prüfung suchte die Zeichenkette „2026“ und ergab deshalb 21 statt 193 Treffer. Richtig ist der **Vergleich `int(AX) >= 2026`**. In AX kommen auch Nicht-Jahre vor (`Apte`).
- **Bestand:** Von **417** Personen mit Status `J` sind nach dieser Regel nur **182** spielberecht. 180 haben weder Pass noch Medico (167 davon: beide Felder leer), 44 haben Pass aber abgelaufenes Medico (2021–2025), 11 haben Medico aber keinen Pass, 13 haben `XXX`.
- **Auswirkung, wenn eingebaut:** **52 von 181 Haushalten** wechseln den Tarif, zusammen **11.556 €**: 37 × 210 → 0, 9 × 384 → 210, 5 × 384 → 0, 1 × 300 → 0. Betroffen sind offenbar aktive Familien (ROLLINGER Medico 2023/2024, HERMES 2021, KASEL 2022) – die Daten wirken **veraltet gepflegt**, nicht wie eine bewusste Spielverbotsliste.
- **Entscheidung deshalb offen gelassen** und in `ANLEITUNG-Cotisation-Tresorier.md` unter „Offene Punkte“ vermerkt, mit dem ausdrücklichen Hinweis, dass die Regel **noch nicht eingebaut** ist. Nicht eigenmächtig umgesetzt – 11.500 € und 52 Familien sind keine Detailfrage.
- **Anleitung ergänzt** (246 Zeilen): neuer Abschnitt „Wer darf spielen“ (Pass, `XXX`, Medico als Gültigkeitsjahr, `///`, Wanderung der Jahresgrenze ab 1.1.2027) + Tabelle „Offene Punkte“ mit Spielberechtigung, Ehrenmitgliedern, Jahresgrenze und XSEUL-Reservisten.


## Anleitung für den Tresorierer aktualisiert – 2026-09-27

- `Vereins-OS/docs/ANLEITUNG-Cotisation-Tresorier.md` von 107 auf 206 Zeilen ergänzt. **Achtung: mehrere Angaben waren veraltet und sind jetzt korrigiert:**
  - **`X` war als Tippfehler dokumentiert** („löscht im Extremfall eine Rechnung über 384 €“). Tatsächlich ist `X` ein **gültiger Status** („ungeklärt“, ergibt 0 €). Text ersetzt, plus Hinweis dass `X` nirgends als Reserve gewertet wird.
  - **Spielerlizenz stand auf `AI`** – in der Mappe ist `AI` die Alterskategorie `U9F`; die Lizenz sitzt in **`AO`**. **E-Mail stand auf `AX`** – das ist inzwischen `Prochain Médico`; E-Mail ist **`BD`**. Warnhinweis ergänzt („im Zweifel die Kopfzeile prüfen, nicht dem Buchstaben trauen“).
  - **Hilfsspalten „BP bis CE“** → richtig ist **`BV` bis `CJ`**; `BP` ist die Quellspalte „Aktives Profil“. `CD (Manuell)` als einzige **Eingabe**-Spalte benannt (aktuell leer), `Z`–`AM` als Formelspalten.
  - **„Ab Zeile 774“** → Daten enden in **591**, Hilfsformeln laufen bis **903**.
  - **„Blatt Stripe_Export, 234 Posten“** → **235 Posten / 53.846 €**; ergänzt, dass das Skript **nur neue Links anlegt und bestehende nie aktualisiert** (Link bei Stripe muss bei Betragsänderung von Hand geändert werden).
- **Neuer Abschnitt „Die Regeln im Überblick“:** Tarife, Bedeutung der Notation `(0+50)`, 384 als Maximum, **XSEUL nach Spielstatus** (J=300, R/N=(0+50), X/leer=0) samt ADR-Ausnahme und „kein Spielerpass → kein 300“, **Comité-Mindestbetrag 50** mit den drei Ausnahmen (selbst spielen / Rechnungsträger mit Tarif / Zuschlag wird echt addiert → SCHUSTER Jeff 260), sowie **Ehrenmitglieder als offene Frage** (3 Personen mit `Membre honoraire`, bisher ohne eigene Regel).


## Cotisation – Zuschlag beim Comité-Mitglied wird real berechnet (SCHUSTER Jeff) – 2026-09-27

- **Regel:** Ein **Comité-Mitglied** zahlt den Zuschlag **echt**: 210 (Sohn Elie, U25) + 50 = **260**. Das Maximum 384 wird nicht erreicht, deshalb 260. Für **alle ohne Comité** bleibt die Notation „210 (+0+50)“ und der Stripe-Parser liest weiter nur die Zahl davor → **210**.
- **Fehler, den ich gemacht habe:** Ich hatte zuerst im **Parser** (`betrag_zahl`) generell „X (+0+Y) = X+Y“ eingebaut. Das traf **6 Posten** (DIEDENHOFEN, EYDT, QUINN, SCHILT, SCHUSTER, SKOVGAARD) statt nur einen – 300 € zu viel, davon 250 € bei fremden Mitgliedern. Zurückgenommen, Parser liest wieder nur die Zahl vor `(`.
- **Richtige Umsetzung an der Quelle, nicht im Parser:** In `pruef_cotisation` wird die Ausgabe für Comité-Mitglieder **selbst** zur Summe: `wert = "210 (+0+50)"` → `"260"`. Damit stimmen Beschriftung und Betrag überein und der Parser braucht keine Sonderlogik. Entsprechend in `pruefe_abgleich.py` und in der **Excel-Formel L** (`TEXT($CE+$CG)` im Träger-Zweig, Bedingung `$BI<>"" & $O<>"J" & $CE>0 & $CG>0`).
- **Kontrolle über den Stripe-Weg (235 Posten, 53.846,00 €):** SCHUSTER Jeff **260,00** (L=260) · DIEDENHOFEN 210 · EYDT 210 · QUINN 210 · SCHILT 210 · SKOVGAARD 210 (alle unverändert, L zeigt weiter „210 (+0+50)“) · BISENIUS Ben 384 · BLANC Max und DIDELOT-SCHOEN 50 (L=(0+50)).
- **Merksatz:** Eine Ausnahme ist keine Generalregel. Vor dem Umstellen einer Sonderregel auf „alle“ immer die betroffene Gruppe auflisten und rückfragen.
- **Verifikation:** `pruefe_abgleich.py` → 0 Abweichungen (772), `pruefe_formeln.py` → 0 Fehler, `test_betrag_parse.py` grün, Klammern L 20/20, 0 Zellen mit `=` im `<f>`, ZIP intakt. Sicherung `…regeln-2026-09-27_2323.xlsm`.


## Kopfzeile O1 = „Spielt J/R/N/X“ – 2026-09-27

- **Vorgabe:** Spalte 14 (O) soll im Titel **J/R/N/X** führen – **X** dokumentiert den Status „ungeklärt“, der unter XSEUL mit 0 € abrechnet.
- **Vorher:** `'Spielt            J/R/N'` – 12 Leerzeichen innen, dazu ohne X. Deshalb fand `berechne().spalte()` die Spalte nicht.
- **Zwei Stellen mussten angepasst werden, sonst wäre es zweimal kaputt gewesen:**
  1. **Titel in der Mappe** → `'Spielt J/R/N/X'` (Sicherheitsregel: der SharedString 7964 wird von **genau einer** Zelle benutzt – O1 – deshalb durfte er direkt geändert werden; das Skript prüft das und bricht sonst ab).
  2. **`SPALTEN_ALT`** in `pruef_cotisation.py` um `'Spielt J/R/N/X'` ergänzt. Ohne diesen Eintrag wäre die Auflösung wieder gescheitert und der Stripe-Lauf mit `FEHLENDE SPALTEN` abgebrochen – der Titel hätte den Fehler also nur verlagert.
- **Skript:** `kopf_setzen.py` (Sicherung, XML-Validierung, Referenzprüfung, Probelauf ohne `--apply`).
- **Verifikation:** Stripe läuft wieder (235 Posten, 53.796,00 €), `pruefe_abgleich.py` → 0 Abweichungen (772), `pruefe_formeln.py` → 0 Fehler, ZIP intakt, `vbaProject.bin` erhalten, 39 Teile. Sicherung `…kopf-2026-09-27_2306.xlsm`.


## Stripe – Lauf war blockiert, jetzt läuft er – 2026-09-27

- **Befund:** `stripe_sync.py` brach sofort ab: `FEHLENDE SPALTEN in der Quelldatei: Spieler J/R/N`. **Kein Stripe-Lauf möglich, also auch kein „auf dem letzten Stand“.**
- **Nicht selbst verursacht:** Der Fehler tritt identisch auf der unberührten Sicherung `…alterskat-2026-09-27_1852.xlsm` (18:50, vor allen heutigen Arbeiten) auf. Er bestand bereits.
- **Ursache:** Der Spaltenkopf im Blatt lautet `'Spielt            J/R/N'` (12 Leerzeichen), der Code erwartete exakt `'Spielt J/R/N'` bzw. den CSV-Namen `'Spielen J/R/N'`. `kopf.strip()` entfernt nur Randleerzeichen, nicht die inneren.
- **Fix:** In `berechne().spalte()` zusätzlich der Vergleich **ohne Leerraum** (`" ".join(s.split())`) über Name und alle `SPALTEN_ALT`-Varianten. Damit ist die Auflösung robust gegen Formatierungs-Abweichungen zwischen CSV und Blatt.
- **Zweiter, wichtiger Befund:** Es existiert **keine `.stripe-status.json`** – `mappe.datenquelle()` verweist auf die Arbeitsmappe, also wurde über dieses Skript **noch nie** ein Link erzeugt. Die im Stripe-Dashboard sichtbaren Posten stammen aus einem anderen Weg und tragen **alte Beträge**.
- **Verhalten des Skripts beachten:** Zeilen, die schon in der Statusdatei stehen, werden **übersprungen** – es aktualisiert bestehende Payment Links **nie**. Betroffene Links müssen in Stripe von Hand geändert oder gelöscht und neu erzeugt werden.
- **Kontrolle über den echten Stripe-Weg (`sammle_rechnungen`):** 235 Positionen, 53.796,00 € offen. BISENIUS Ben **384** · BLANC Max **50** · CASTELLANO **50** · DEISCHTER **50** · DIDELOT-SCHOEN **50** · METZLER Bernard **50** · VAN DER WEKEN **50** · CLEMENT Liliane **50** (`(0+50)`) · MAQUIL **384** · SCHUSTER **210** · DA CONCEICAO **384**. EPPS Charly erscheint **nicht** – er ist über F0039 abgedeckt und erzeugt bewusst keine eigene Rechnung.
- **Zeilennummern:** Die Arbeitsmappe ist gegenüber der CSV sortiert (BISENIUS Ben steht in der Mappe in **Z60**, in der CSV in Z64). Stripe rechnet auf der **Mappe**, `pruef_cotisation` beim Prüfen auf der **CSV** – bei Rückfragen immer die Quelle nennen.


## Cotisation – EPPS-Ausnahme: Comité-Mitglied, das selbst spielt – 2026-09-27

- **Befund:** `EPPS Charly` (Z163) war durch die Comité-Regel von `F0039` auf **50** gesetzt worden. Richtig ist **F0039** – er ist aktiver Spieler und über seinen Haushalt abgedeckt.
- **Haushalt F0039 („6, im Batz“):** EPPS Thomas (J, lizenziert, nicht Träger) → F0039 · **EPPS Charly (J, lizenziert, nicht Träger, Comité)** → F0039 · PIRSON Isabelle (Mutter, N, **Trägerin**) → **384**. Zwei aktive Spieler ⇒ Familientarif, die Mutter zahlt ihn.
- **Korrektur:** Die Comité-Mindestregel gilt nur, wenn die Person **nicht selbst spielt**. Bedingung: `ist_comite and spielt != "J" and (Wert ist "", "0", Haushaltscode oder "(0+50)")`. Damit bleibt EPPS bei F0039, METZLER Bernard (Status N) weiter bei 50.
- **Unterschied zu METZLER ist also genau der Status:** EPPS = **J** (Spieler, abgedeckt) gegenüber METZLER = **N** (spielt nicht, deshalb Mindestbetrag).
- **Endstand der 10 (unverändert sind 4 Träger):** BISENIUS Ben 384 · CASTELLANO 50 · DA CONCEICAO 384 · DEISCHTER 50 · DIDELOT Loïc 50 · **EPPS Charly F0039** · MAQUIL Xavier 384 · METZLER Bernard 50 · SCHUSTER Jeff 210 (+0+50) · VAN DER WEKEN 50. CLEMENT Liliane (kein Comité) bleibt (0+50).
- **Excel:** Ausnahme in `CH` und `L` über `$O{r}<>"J"`; `CJ` braucht sie nicht, dort wird vorher schon auf N/R geprüft. Die Klammerzahl in L stieg dadurch 16 → 17.
- **Verifikation:** `pruefe_abgleich.py` → 0 Abweichungen (772), `pruefe_formeln.py` → 0 Fehler, 0 Zellen mit `=` im `<f>`, ZIP intakt. Sicherung `…regeln-2026-09-27_2301.xlsm`.


## Cotisation – Comité-Mindestbetrag 50 € – 2026-09-27

- **Vorgabe:** Wer im Comité sitzt, zahlt **mindestens 50 €** – also **nicht** `(0+50)` und **nicht** der Haushaltscode eines anderen. `METZLER Bernard` (2019, Secrétaire technique) zeigte nur `F0026`, jetzt **50**. `CLEMENT Liliane` (T=4, kein Comité) bleibt **(0+50)**.
- **Marker – und eine Fehleinschätzung meinerseits:** Zuerst hatte ich 11 Personen (Spalte T = 1). Richtig sind **10**; `KREMER Philippe` hat zwar T=1, aber kein Comité-Eintrag. Verlässlich ist die **Spalte `Comité`** (CSV) bzw. **BI** in der Mappe – alle drei Marker (`Comité`, BI, T=1) treffen exakt dieselben 10. Der CAT-Code unterscheidet sich zwischen CSV (Export 24.09.) und Mappe (26.09.) – deshalb auf `Comité` gestützt, nicht auf den Zahlencode.
- **Umsetzung als *Mindestbetrag*, nicht als fester Betrag:** trifft nur, wenn das Ergebnis bisher `""`, `"0"`, der Haushaltscode oder `(0+50)` war. Ein Rechnungsträger im Comité zahlt weiter seinen Tarif: BISENIUS Ben 384, DA CONCEICAO 384, MAQUIL 384, SCHUSTER 210 (+0+50).
- **Wirkung: 6 Zeilen, +100 €** (die 4 übrigen sind nur Notationswechsel `(0+50)` → `50`): CASTELLANO, DEISCHTER, DIDELOT, EPPS, METZLER, VAN DER WEKEN.
- **Excel: die Regel musste in DREI Spalten.** Die Ausgabekette `L` fragt nacheinander `CD` (Manuell) → `CH` → `CJ` → Träger/Familiencode ab. Nur eine zu ändern hieße: Excel ≠ `pruef_cotisation`.
  - `CH` (Personenwert): im Reservisten-Zweig Committee+kein Träger → 50 statt `(0+50)`
  - `CJ` (XSEULwert): bei Status N/R Committee+kein Träger → 50 statt `(0+50)`
  - `L` (Cotisatioun): im Nicht-Träger-Zweig `IF($BI<>"","50",…)`
- **Neue Schranke im Schreibskript:** Klammerbalance. Die neue L-Formel hatte zunächst 16 öffnende / 17 schließende Klammern – `pruefe_formeln.py` hätte es erst beim Öffnen gezeigt. `cotisation_regeln_setzen.py` prüft das jetzt vor dem Schreiben.
- **Nebenbefund:** Die geteilten Formeln fielen von 210 auf 88 Master, weil **Excel die Datei am 27.09. um 22:46 selbst gespeichert** hat (mein letzter Schreibvorgang war 22:30) und dabei Gruppen aufgelöst hat. Nebeneffekt: die Mappe **öffnet nachweislich ohne Reparatur-Dialog**. Vor dem Schreiben per `~$`-Sperrdatei geprüft, dass sie nicht offen war.
- **Verifikation:** `pruefe_abgleich.py` → 0 Abweichungen (772 Zeilen), `pruefe_formeln.py` → 0 Fehler, 0 Zellen mit `=` im `<f>`, Klammern 16/16, ZIP intakt, `CD` (Manuell) unangetastet, 590 Namen. Sicherung `…regeln-2026-09-27_2252.xlsm`.


## Cotisation – Status X: Spalte darf nur J/R/N/X enthalten – 2026-09-27

- **Vorgabe:** In „Spielt J/R/N“ stehen ausschließlich **J, R, N oder X**. X ist der Status für „nicht spielt, ungeklärt“ und ergibt unter XSEUL **0**.
- **Gefundene Fehlwirkung:** Die Personenwert-Formel prüfte `AND($L<>"J";$L<>"N";$AH<>"")`. Das trifft **jeden** Wert außer J und N – also auch **X** und jeden Tippfehler. Ein X-Spieler hätte in Excel den **Reservistenwert (0+50)** bekommen, während Python (`spielt == "R"`) korrekt leer lässt. Excel und Python wären auseinandergegangen, sobald X in der Spalte steht.
- **Fix:** Prüfung auf **exakt `="R"`** statt „<>J und <>N“. Gleiche Stelle in `baut_arbeitsmappe.py` (Spalte `CB`) und in der Live-Mappe (Spalte `CH`).
- **Bestand in der Mappe (Spalte O, Zeilen 2–903):** J 418 · N 313 · R 26 · **leer 145** · X 0. Es gibt also **kein X** – die Spalte ist noch nicht vollständig.
- **Die 17 leeren Zellen mit Datenbezug** (CSV-Zeilen 590–606, Haushaltscodes F0165–F0181) sind **Platzhalter**: kein Name, keine Lizenz, keine Kategorie, kein Geburtsdatum. Sie sind Rechnungsträger und ergeben „kein Spielertarif, kein Zusatz“. Die restlichen ~128 Leerzellen liegen hinter dem Datenbereich.
- **Wirkung des X-Fixes auf die Ausgabe: keine** – heute steht kein X in der Spalte. Die Änderung ist reine Absicherung für den Fall, dass X nachgetragen wird. Soll ich die 17 Platzhalterzeilen mit **X** füllen (rein kosmetisch, ohne Betragswirkung)? Die ~128 Zellen hinter dem Datenbereich würde ich **nicht** anfassen – das sind Vorlagenzeilen.
- **Verifikation:** `pruefe_abgleich.py` → 0 Abweichungen, `pruefe_formeln.py` → 0 Fehler, 0 Zellen mit `=` im `<f>`, ZIP intakt. Sicherung `…regeln-2026-09-27_2230.xlsm`.


## Cotisation – XSEUL nach Spielstatus statt nach Lizenz – 2026-09-27

- **Vorgabe:** XSEUL gilt **300 bei Status J**, **(0+50) bei R und N**, **0 bei sonst**. Damit ist die Lizenz irrelevant – der Code entscheidet der Spielstatus (Spalte `O` / CSV `Spielen J/R/N`).
- **Damit ist auch die offene Frage vom 26.09. beantwortet:** die **23 XSEUL-Reservisten** (Status R) bleiben bei `(0+50)` statt 300. Die 5.750 € sind damit entschieden – es fließt **kein** 300 für Reservisten.
- **Wirkung gegenüber der vorherigen Lizenz-Regel: 4 Zeilen, −1.000 €** – die XSEUL-Leute mit Status N, die zusätzlich einen Spielerpass hatten und deshalb noch 300 bekamen: GOERENS Yves (Z211), PETOUO Berthold (Z418), PETTINGER Kim (Z420), WELSCH Mike (Z568).
- **Endverteilung XSEUL (74 Zeilen):** 35 × 300 (Status J) · 37 × (0+50) (Status N/R) · 1 × 384 (ANSAY) · 1 × „XSEUL“ (Nicht-Träger, zeigt nur den Code). XSEUL-Summe **12.734 €**.
- **ADR-Ausnahme bleibt bestehen:** die ANSAY-Brüder teilen eine gelistete Adresse und sind beide Status J → **1× 384** statt 2× 300. Das ist der Familientarif für einen echten Haushalt, kein XSEUL-Sonderfall.
- **Umsetzung:** `pruef_cotisation.py`, `pruefe_abgleich.py` und Spalte `CD` in `baut_arbeitsmappe.py`; in der Live-Mappe Spalte **CJ** (nicht CD – CD ist „Manuell“).
- **Formel CJ (Live-Mappe):** `=IF($Q{r}<>"XSEUL","",IF(AND(LEFT($BV{r},4)="ADR:",$BY{r}>=2),"",IF($O{r}="J",TEXT(Cotisation!$B$5,"0"),IF(OR($O{r}="N",$O{r}="R"),"(0+"&TEXT(Cotisation!$B$4,"0")&")","0"))))`
- **Verifikation:** `pruefe_abgleich.py` → 0 Abweichungen (772 Zeilen), `pruefe_formeln.py` → 0 Fehler (26.014 Zellen). Skript `cotisation_regeln_setzen.py` mit Schranken für Zellreihenfolge, Duplikate und geteilte Formeln; **0 Zellen mit `=` im `<f>`** (das war ein eigener Fehler, der den Reparatur-Dialog ausgelöst hätte).


## Cotisation – XSEUL 300 gilt nur für Spieler (Offizielle → 0+50) – 2026-09-27

- **Befund aus Stripe:** `BLANC Max` (Z66, Trainer) hatte **300** statt `(0+50)`. Er hat Status `N` und **nur eine Offiziellenlizenz** (6846), keinen Spielerpass.
- **Regel-Lücke:** `XSEUL;300` wurde **pauschal pro Zeile** vergeben, unabhängig von der Rolle. In einer normalen Familie bekommt ein Offizieller sauber `(0+50)` – unter XSEUL dagegen 300. XSEUL ist damit faktisch ein Spieler-Pauschbetrag, wurde aber für alle vergeben.
- **Fix:** Der XSEUL-Zweig prüft jetzt die Rolle.
  - Spielerlizenz (`liz_sp`) → 300 wie bisher
  - **nur Offiziellenlizenz** → `(0+50)` (Zuschlag-Regel, wie in normalen Familien)
  - keine Lizenz → 300 wie bisher (siehe unten, warum)
  - Betroffen in `pruef_cotisation.py`, `baut_arbeitsmappe.py` Spalte `CD` und `pruefe_abgleich.py`.
- **Wirkung exakt 7 Zeilen, −1.750 €** (300 → 50): BLANC Max (Z66), CASTELLANO Virginio (Z93), FRANTZEN Garry (Z195), KREMER Armand (Z296), PIETRASIK Katarzyna (Z423), STREITZ Eliane (Z523), WOLMERING Kevin (Z573). XSEUL-Summe 15.084 → 13.334 €.
- **Wichtig – die 3 ohne jede Lizenz bleiben bei 300:** `DIDELOT-SCHOEN Arsène` (Z133, **Träger** der XSEUL-Gruppe), `KREMER Billy` (Z295), `MARZADORI Sascha` (Z357). Lässt man sie durchfallen, wird der Träger zum Regeltarif gezogen und bekäme **384** – ein Artefakt der Gruppierung, weil alle 74 XSEUL-Personen in einer Gruppe stecken. Deshalb bewusst konservativ.
- **Excel-Formel `CD` (XSEULwert), Baustein neu:**
  `=IF($P{r}<>"XSEUL","",IF(AND(LEFT($BP{r},4)="ADR:",$BS{r}>=2),"",IF(AND($AH{r}<>"",$AH{r}<>"///"),TEXT(Cotisation!$B$5,"0"),IF(COUNTIFS($AI{r}:$AK{r},"<>",$AI{r}:$AK{r},"<>///")>0,"(0+"&TEXT(Cotisation!$B$4,"0")&")",TEXT(Cotisation!$B$5,"0")))))`
  Offiziellen-Lizenzspalten laut `SP_LIZ_OFF = ("AI","AJ","AK")`; `///` zählt wie in `BV`/`ist_lizenz` als leer.
- **Verifikation:** `pruefe_abgleich.py` → **0 Abweichungen** (772 Zeilen), `pruefe_formeln.py` → **0 Fehler** (26.014 Zellen, 43 Muster).
- **Weiterhin offen:** die **23 XSEUL-Reservisten** (Spielerlizenz + Status R) bekommen `(0+50)` statt 300 = **5.750 €** — Entscheidung vom 26.09. war bewusst, ist aber als offen notiert.
- **Falle bei eigenen Prüfskripten:** Spaltennamen im CSV (`GC 2026-09-24 …csv`) weichen ab (`Spielen J/R/N` statt `Spieler J/R/N`) — die Auflösung gehört aus `pruef_cotisation` (`SPALTEN_ALT`), eigenes Nachschlagen liefert leere Werte. Außerdem **keine Namenskollision**: eine Hilfsfunktion `z()` überschrieb einmal die Zusatz-Regel und machte sie truthy → Ausgaben um 50 € zu hoch.


## Cotisation – Personenwert vs. Familientarif 384 (BISENIUS Ben Z64) – 2026-09-27

- **Befund aus Stripe:** Familie BISENIUS (Haushalt **F0059**, 5 Mitglieder, 4 aktiv lizenziert) zahlte **50** statt **384**. Ursache: Rechnungsträger BEN (Z64) hat Status `R` (Reserve) → die Regel *Personenwert `(0+50)`* griff und lief der Familientarif-Prüfung **vor**, obwohl `tarif` intern korrekt 384 war.
- **Regel-Lücke:** Der Code kannte das Prinzip „384 ist Maximum“ nur für den **Zuschlag** (`ZusatzBeiFamilie=NEIN`, Formel `CA`/`BY`). Für den **Personenwert** fehlte es – ein Reservist im Haushalt drückte die ganze Familie auf 50.
- **Fix (3 Stellen, damit Python und Excel identisch rechnen):**
  - `pruef_cotisation.py`: neue Schranke `familienmax = (tarif == tarife["familie"] and fam not in (XSEUL_CODE, GAJGL_CODE))`; die beiden Reservisten-/GAJGL-Zweige greifen nur noch bei `not familienmax`. **Namentliche Ausnahmen (BOURG) bleiben unberührt.**
  - `baut_arbeitsmappe.py`, Spalte `CB` (Personenwert): `AND($BY<>Cotisation!$B$3, OR($P="XSEUL",$P="GAJGL"), …)` als zusätzliche Bedingung.
  - `pruefe_abgleich.py`: dieselbe Schranke in der Excel-Nachbildung.
- **Wirkung exakt 1 Zeile:** Z64 BISENIUS Ben `(0+50)` → **384**. Summe +334 €.
- **Bewusst NICHT geändert (Gegenprobe):**
  - `BINGEN Fränk` Z57 (F0015, nur **1** aktiv lizenziert) bleibt `(0+50)` – Familientarif greift nicht.
  - Die **23 XSEUL-Reservisten** bleiben `(0+50)`. XSEUL ist kein Familiencode, sondern ein Fixbetrag 300 pro Zeile; die offene Frage aus dem 26.09. („fallen die 23 finanziell von 300 auf 50?“) ist damit **weiterhin offen** = 23 × 250 € = 5.750 €. Eine zu grobe Fassung (`personenwert and tarif != familie`) hätte genau diese 23 auf 300 zurückfallen lassen – deshalb die zusätzliche XSEUL/GAJGL-Ausnahme.
  - **Achtung Datenmodell:** alle 72 XSEUL-Personen landen in **einer** Gruppe (`famkey == "XSEUL"`), weil Zeile `pruef_cotisation.py` den Code als Gruppenschlüssel nutzt. Dadurch ist `sp_gesamt = 35` und `tarif` intern 384, obwohl der Wert nie ausgegeben wird. Bei zukünftigen Regeln nicht auf dieses `tarif` verlassen.
- **Verifikation:** `pruef_cotisation.py` läuft, `pruefe_abgleich.py` → **0 Abweichungen** Python ↔ Excel (772 Zeilen), `pruefe_formeln.py` → **0 Fehler** in 26.014 Formelzellen.
- **Offen:** Die Live-Mappe `GC 2026-09-26 …mit-Cotisation.xlsm` hat die alte Regel noch in **CH** (Personenwert, 902 Formeln, **0 geteilte Formeln** → chirurgisch ersetzbar). Stripe rechnet über `pruef_cotisation.py` und ist dadurch bereits korrekt.


## Cotisation – Excel-Reparatur behoben & Finale Arbeitsmappe erstellt – 2026-09-26

- **Ursache der Reparaturmeldung exakt isoliert:**
  - Standardfunktion `DATEVALUE(date_text)` erwartet in Microsoft Excel genau 1 Argument.
  - In den Formelvorlagen für `BQ` (Schluessel) und `CC` (Alterspruefung) war ein zweites Datumsformat-Argument angegeben: `DATEVALUE($J{r},"DD.MM.YYYY")` bzw. `DATEVALUE(Cotisation!$B$11,"DD.MM.YYYY")`.
  - Excel wertete dies beim Öffnen als unzulässige Syntax einer nativen Funktion und triggerte den Reparatur-Dialog in allen betroffenen Dateien (H1 und H2).
- **Verifikation via Testserie I:**
  - Bereinigte Testdateien in `_testbausteine_i/` mit 1-Argument-`DATEVALUE` öffneten in Excel ausnahmslos ohne Fehlermeldung (`I4_nur-BQ-korrigiert`, `I5_nur-CC-korrigiert`, `I1_Gruppe-A`, `I2_Gruppe-B`, `I3_alle_korrigiert`).
- **Finale Arbeitsmappe aktualisiert:**
  - Fix fest in `docs/cotisation/baut_arbeitsmappe.py` übernommen.
  - `Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm` neu gebaut (14 Helfer + Ausgabeformel M + Config-Blatt `Cotisation`).
  - Prüfskripte `pruefe_formeln.py` (19.839 Formelzellen syntaktisch sauber) und `pruefe_abgleich.py` (0 Abweichungen Python <-> Excel) erfolgreich bestanden.


## Cotisation – neue Regeln (R/GAJGL/Ausnahmen) + Abgleich Vereins-OS – 2026-09-26

- **Neue Personenregeln** in Spalte L, umgesetzt in `pruef_cotisation.py` und `baut_arbeitsmappe.py`:
  - Spieler mit Spielerlizenz und Status **M = R** (Reserve) **oder** Familiencode **GAJGL** → `(0+50)` **auf der eigenen Zeile** (neue Helfer-Spalte `CA Personenwert`, Config `Cotisation!B10`).
  - Namentliche Ausnahmen gelten **pro Zeile**, nicht mehr nur auf dem Rechnungsträger: BOURG Jeannot **und** BOURG-THIELEN Gaby → beide `Don ? +(0 +50)` (Leerzeichen exakt wie Vorgabe).
  - Reihenfolge: leer → `BV Manuell` → `CA Personenwert` → XSEUL 300 → GAJGL 0 → nicht Träger → Familientarif.
  - Spieler mit Antwort N entscheiden freiwillig über `BV Manuell` (50 € = Stimmrecht AG, in keiner Spalte ableitbar).
- **Auswirkung:** 66 Zeilen weichen von den 233 Werten der Saison 2025/26 ab, davon 43 gewollt (23× 300→(0+50) XSEUL-Reservisten, 15× 0→(0+50) GAJGL, BINGEN Fränk, beide Bourg, BISENIUS/SERRES). Offen: fallen die 23 XSEUL-Reservisten finanziell von 300 auf 50?
- **Vereins-OS-Abgleich** (`docs/cotisation/vereins-os-abgleich.md`): Beitraglogik existiert an 3 Stellen, C-Code-Liste an 3 weiteren. Zwei echte Fehler gefunden und behoben:
  - `client/src/lib/registrationLogic.ts` `getCotisation()`: **`playerCount` war Parameter, wurde aber nie benutzt** → Familientarif 384 fehlte in der App. Jetzt `playerCount >= 2` → 384, Tarife als `COTISATION_RATES` exportiert, Notation vereinheitlicht. `tsc --noEmit` fehlerfrei.
  - `join.html`: C0007/C0008/C0010 zeigten **200 €** für Jugendliche, App und Excel rechnen **210 €**. Angepasst (sichtbare Anzeige im Anmeldeformular).
- **Kernerkenntnis zu den Codes:** AC-Codes (Berechtigung), CAT-Codes (FLH-Kategorie) und C-Codes (Tarifdefinition) sind **keine** Doppelung – sie beantworten drei verschiedene Fragen. Empfehlung: umbenennen (Rollenprofil / Tarifdefinition) + Zuordnungstabelle, **keine** Datenmigration.
- Vereins-OS-Aufgaben `code-list-improvement-plan.csv` CL-02/CL-05/CL-10 sind mit dem Abgleich adressiert; offen bleiben Alterslogik (Kategorie K vs. CNS-Alter), Trainer-Codes (7 C vs. 5 AC) und U4/Kidssport.



## Cotisation-Formel (Spalte L) – Bausatz + Prüfskript – 2026-09-26

- Neuer Ordner `docs/cotisation/`:
- **Datenlage geklärt:** Spalte L = Cotisatioun (Ziel), M = Spielen J/R/N, **O = Code Courrier neu = Familien-ID** (N = alter code courrier), K = Alterskategorie (SEN/U25/?), J = Geburtsdatum, AG = Spielerlizenz, AH/AI/AJ = Offizielle-/ZS-/SR-Lizenz, BB = Officiel. Quelle: `Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv`, 771 Datenzeilen.
- **Achtung Layout:** Die .xlsm (`GC 2026-09-24 …xlsm`) hat ein **anderes Spaltenlayout** (C=Alterskategorie, D=Cotisatioun, M=Code Courrier neu, AE=Spielerlizenz, AF/AG/AH=Offizielle, AO=Geburtsdatum) und **keine Spalte „Spielen J/R/N"**. Die Formeln im README gelten für das CSV-Layout. Vor dem Einfügen prüfen, welche Datei offen ist.
- **Empirische Befunde aus 348 Familien / 771 Zeilen:**
  - `XSEUL` (74) und `GAJGL` (15) werden **pro Zeile** ausgewertet, nicht als Familie (ANSAY Luka SEN und Mathis U25 haben beide 300 unter demselben Code).
  - Rechnungsträger ist in der Praxis die **erste Zeile des Familienblocks** (144/144 = 100 %), nicht das älteste Geburtsdatum (82 %). Beides per Schalter `TraegerRegel` wählbar, Standard `Erste`.
  - 166 Zeilen haben **keine** Familien-ID, aber Spielstatus `J` → sie brauchen eine Ersatz-ID (`@ZEILE`), sonst bleiben sie unkotiert.
  - 257 Zeilen haben `///` als Geburtsdatum, 442 haben `K='?'` → Fallback-Datum 73415 (31.12.2100) nötig.
  - `+50` ist **pauschal pro Familie**, nicht pro Person (CLEMENT/METZLER: 2 Offizielle → `(0+50)`), und **entfällt beim Tarif 384** (384 ist Maximum).
- **Ergebnis:** 747/771 = **96,9 %** Übereinstimmung mit der bestehenden Spalte L; davon sind 18 Abweichungen „bisher leer" (Vervollständigung) und 5 freiwillige Beiträge der Offiziellen, die nicht ableitbar sind → dafür Spalte `Manuell`.
- **8 Fehler der alten LET-Formel behoben:** Zirkelbezug (`B_E;$M$2:$M$5000` las die eigene Spalte), Zeilenversatz `A4`/`B5`, Ältesten-Konflikt (`J5=Aeltester` UND `ZÄHLENWENNS($O$2:$O5)=1` → bei Gleichstand gar keine Ausgabe), Doppelrechnung ohne Geburtsdatum, `MINWENNS` über `///`-Text, 4× `SUMMENPRODUKT` über 4999 Zeilen (Performance), Tarife/Namen fest im Formeltext.
- **Formeln jetzt auch in Excel:** `baut_arbeitsmappe.py` erzeugt `Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm` (Kopie, Original per SHA-256 nachweislich unverändert). Blatt `Cotisation` (Tarife/Schalter/Ausnahmen in Zellen, vorne eingefügt) + Spalte L (772 Zeilen) + Helfer BN:BZ (11 Formeln) + BW als Sicherung der 233 bisherigen Ergebnisse.
- **Wichtig:** Die alte Formel lag in L2:L773 als **Array-Formel mit `_xlfn.LET`/`_xlpm.`-Präfixen**. Neuer Bausatz daher **prefix-frei** (IF/AND/OR/NOT/COUNTIFS/IFERROR/INDEX/MATCH/SUMPRODUCT/MIN/TEXT/ROW/DATEVALUE/ISNUMBER) – läuft in jeder Excel-Version, LibreOffice und Google Sheets. Datei enthält keine Charts/PivotTables/Bilder/Datenvalidierungen, nur VBA → openpyxl-Roundtrip verlustfrei, `keep_vba=True` und `fullCalcOnLoad=True` gesetzt.
- **Beim Abgleich gefundene und behobene Fehler im ersten Entwurf:** Sicherung kopierte Array-Formel-Objekte statt Ergebnisse (jetzt `data_only=True`); `BU` markierte die **letzte** statt der **ersten** Zeile (`ZÄHLENWENNS(...)=1`); `IF(BU;"";…)` hätte den Träger ausgeblendet statt die anderen (jetzt `NOT($BU)`); AH/AI/AJ-Bereiche ohne `$` vor der Spalte (jetzt absolut).
- Verifikation: `python3 docs/cotisation/pruef_cotisation.py` läuft fehlerfrei (96,9 %); alle 12 Formeln in README und Datei maschinell auf Klammerbalance, Spaltenzuordnung und `_xlfn`-Freiheit geprüft; Selbsttest-Tabelle mit Sollwerten (Zeilen 2, 5, 11, 27, 57, 72) im README.

## Generator – Frauen-Block zentrierter + U11-Tournoi-Adresse – 2026-09-25

- Frauen-Block (links, inkl. Coupe-Slot und Zusatzteams) von `left:20` auf `left:90` gerückt: weiter weg vom linken Posterrand, näher ans Männer-Spiel in der Mitte.
- Tournoi-Adresse: Der magische Scanner setzt bei Kategorie `Tournoi` jetzt einen Hallencode-Fallback (`hallCodes[game.halle]`), sodass das U11-Heimturnier (Halle 290101) die Adresse `21, rue des Prés | L-7561 Mersch` im Landscape-Poster (Datum+Adresse unter dem Block) und Portrait anzeigt.
- Verifikation: alle 6 Inline-Skripte `node --check`, `git diff --check` sauber; gepusht (`ea4ada8`).


## Generator – U11-Turnier 18.10. ergänzt + doppelter Wochenend-Button entfernt – 2026-09-25

- `allGamesData` ergänzt um `JUGEND: U11 Espoir`, `18.10.26 09:30`, Heimspiel `Mersch75 - Tournoi`, Halle `290101`, Nr. `U11T181026`.
- Der Wochenend-Loader (12.10.–18.10.26) erzeugt daraus `JUGEND: U11 Espoir 18.10.26 09:30 290101 Mersch75 - Tournoi`; der magische Scanner setzt U11 Espoir korrekt auf Kategorie `Tournoi`, Gegner `Tournoi`, Datum `2026-10-18`, Zeit `09:30`, Heim `home1`.
- Im Landscape-Poster erscheint das U11-Turnier in der rechten Turniergrafik mit Badge `U11`, Datum `SO - 18.10.2026 - 09h30` und Mersch-Logo (Heimturnier).
- Doppelter Button `#btn-weekend-next` („Nächstes Wochenende laden“) aus `generator.html` entfernt; es existiert nur noch ein Button mit dieser ID.
- Verifikation: jsdom-Test für den kompletten Ablauf (Wochenauswahl → Scanner → Landscape-Vorschau) erfolgreich; alle 10 Inline-Skripte `node --check`, `git diff --check` sauber.


## Generator – Landscape-Aufteilung neu (Frauen links, Männer Mitte, rechte Spalte) – 2026-09-25

- Ursache des Durcheinanders: Commit `d2b2eea` hatte die alte, flexible Landscape-Slot-Logik durch feste Positionen ersetzt; dadurch überlappten die Jugendblöcke und der Turnierbereich verschwand je nach Auswahl.
- Neue feste Aufteilung im Meisterschafts-Poster:
  - **Links:** Frauen groß (`top:350px;left:20px`)
  - **Mitte:** Männer groß (`top:350px;left:570px`, bei fehlenden Frauen mittig)
  - **Rechts oben:** Turniergrafik `--- TOURNOI ---` plus U9/U11/U7 (`top:95px;left:1140px`)
  - **Rechts darunter:** U13-P1 (`top:275px`), U13-P2 (`top:425px`), U15 (`top:575px`) – U15 immer unten
- Turniergrafik nutzt echte Turnierlogos und zeigt ohne aktives Turnier für U9/U11/U7 konsequent den 3D-Ball (`renderLandscapeTournamentStrip()`).
- Zusatzteams H2 und U11 Elite landen in der freien linken Spalte oberhalb der Frauen, damit nichts verloren geht oder die rechte Spalte sprengt.
- `renderLandscapeGame()` akzeptiert jetzt Slot-Overrides (`logoSize`, `badgeW`, `badgeH`, `badgeFont`, `titleFont`, `dateFont`, `locFont`, `gap`) für kompakte rechte Blöcke.
- Verifikation: 18.10.-Spieltag in echter DOM-Umgebung (jsdom) gerendert – Frauen links, Männer mittig, U13-P1 → U13-P2 → U15 rechts, Turniergrafik mit U9/U11/U7, ohne Turnier 3× 3D-Ball; alle 10 Inline-Skripte `node --check`, `git diff --check` sauber.


## Generator – Meisterschaft & Turnier-Anzeige bereinigt – 2026-09-25

- Spieltag 17./18.10.2026 (2 Senior- + 3 Jugendspiele) als Referenz geprüft.
- Jugend-Slots im Landscape-Poster von `[40, 500, 800, 1200]` auf `[40, 440, 840, 1240]` korrigiert; die ca. 360px breiten Blöcke überlappen sich dadurch nicht mehr.
- Der Turnierbereich wird im Meisterschafts-Poster immer gerendert; ohne aktives Turnier zeigt `renderLandscapeTournoiPanel()` konsequent den 3D-Ball mit „Kein Turnier aktiv“.
- Alles mit Kategorie `Tournoi` wird dem Turnierbereich zugeordnet; Coupe-Zweig und Youth-Modus leeren den Turnierbereich weiterhin getrennt.
- Landscape und Portrait verwenden denselben Fallback: fehlende bzw. leere Turnier-Logos werden durch `CONFIG.ballLogo` ersetzt; leere Portrait-Logo-Felder (`l2 = ""`) sind entfernt.
- Verifikation: 10 Inline-Skripte via `node --check`, `js/flh-live-sync.js`, Turnierverhalten (aktiv/inaktiv), Slot-Geometrie, 3D-Ball-Asset und `git diff --check` erfolgreich.


## Generator – Coupe als eigener Postermodus – 2026-09-25
- Coupe-Spiele werden im Landscape-Poster nicht mehr zusammen mit Meisterschafts-/Season-Games gerendert; sobald mindestens ein sichtbares Coupe-Spiel vorhanden ist, gilt der separate Coupe-Zweig.
- Reihenfolge im Coupe-Zweig bleibt Frauen – Männer – U15; die Spielart-Checkbox „Coupe“ gilt weiterhin für beide Vorschau- und Exportlogik.
- Der Pokal ist kein globales, absolut positioniertes Element mehr, sondern wird relativ im blauen U15-Coupe-Block mittig über dessen Badge/Titel erzeugt und verkleinert dargestellt.
- Entfernt wurde die alte globale Trophy-Positionierung; das bestehende Coupe-Asset bleibt `assets/Coupe de Luxembourg2026.webp`.


## Agent 11 – Strukturierung & Cleanup – 2026-09-25
## Generator – Coupe-Spiele integriert – 2026-09-25

- `generator.html`: Separate Schaltfläche „Coupe dieses Wochenende laden“ ergänzt.
- `js/flh-live-sync.js`: Coupe-Kategorien (`H-C-LN`, `D-C-LN`, `H-C-FLH`, `U15G-C`, `U13M-C`) liefern gemeinsam `COUPE:`-markierte Spiele an den Generator.
- Generator trennt Coupe- und Championship-Spiele beim Wochenende-Laden; Coupe-Spiele werden in den magischen Scanner mit Kategorie `Coupe` und passender Mannschafts-ID (`s1`, `fe`, `u15`, `u13p1`) übergeben.
- Bestehende Championship-/M75-Daten bleiben unverändert und werden nicht ersetzt.
- Syntaxprüfung für `js/flh-live-sync.js` und alle Inline-Skripte in `generator.html` sowie `git diff --check` erfolgreich.


## Generator – Sichtbarkeit der Posterbereiche – 2026-09-25

- Checkboxen im LS-/Landscape- und Portrait-Poster ermöglichen, einzelne Mannschaften/Spielblöcke ein- oder auszublenden.
- Auswahl wird unter `mersch75-generator-poster-visibility-v1` im Local Storage gespeichert und beim Neuladen wiederhergestellt.
- Landscape-Rendering berücksichtigt die Checkboxen auch im Coupe-Zweig; die feste Reihenfolge Frauen – Männer – U15 bleibt erhalten.
- Portrait-Haupt- und Zusatzspiele verwenden dieselbe Checkbox-Auswahl; Vorschau und Export folgen der Auswahl.
- Syntaxprüfung aller Inline-Skripte, FLH-Sync-Prüfung und `git diff --check` erfolgreich.


## Generator – Pokalposition LS-Poster – 2026-09-25
- Coupe-Pokal im LS-/Landscape-Poster aus der mittigen Position entfernt.
- Rechts mittig über dem U15-Spiel platziert und von 230×290 px auf 300×375 px vergrößert.
- Asset-Pfad `assets/Coupe de Luxembourg2026.webp` geprüft; Vorschau-/Export-Logik unverändert.
- `node --check` für FLH-Sync und Inline-Skripte sowie `git diff --check` erfolgreich.


- Homepage-Navigation inventarisiert und eine rückwärtskompatible Zielstruktur unter `docs/structure/pages/` dokumentiert.
- Kategorien für Home, Live-Center, Training, Club, News, Community, Media, Kontakt/Service, Rechtliches, Verwaltung und Shared angelegt.
- Aktive Root-Dateien nicht verschoben: GitHub Pages liefert aus dem Root aus und die bestehenden URLs/Referenzen wären sonst gebrochen.
- `hallo_agent11.txt` erstellt; Struktur-Dokumentation und Verzeichnisse validiert.

## Agent 10 – i18n & Mehrsprachigkeit – 2026-09-25

- Sprachmatrix für LB/FR/DE/EN/PT geprüft; `misc-i18n.js` enthält die neuen Galerie-, Memories- und Legal-Schlüssel in allen fünf Sprachen.
- `script.js` um `navMemories` in allen fünf Sprachpaketen ergänzt; dynamisches Agent-4-Menü enthält jetzt `memories.html` neben `gallery.html` und aktualisiert Labels beim Sprachwechsel.
- Fallback-Kette in `script.js` implementiert: gewählte Sprache → LB → FR → EN → DE → PT; unbekannte Sprachwerte werden auf LB normalisiert.
- `gallery.html` und `memories.html` starten mit korrektem `lang="lb-LU"`; Sprachwechsler aktualisiert das `html.lang` zur Laufzeit.
- `hallo_agent10.txt` erstellt; i18n-Syntax- und Diff-Prüfung erfolgreich.


## Agent 9 – Performance & Asset-Optimierung – 2026-09-25

### 1. Bild-Optimierung (LCP/CLS)
- Bestand: 232× WebP + 207× AVIF bereits modern; 131× PNG / 66× JPG bleiben nur dort, wo sie aktiv referenziert sind (keine Duplikate angelegt, keine Dateien umbenannt — AGENTS.md-konform).
- `picture`-Elemente mit AVIF→WebP→PNG-Fallback existieren bereits (z. B. Ball, Teamfotos, Zesumme-Staark-Logo in `news.html`).
- LCP (Hero-Poster `index.html`): `fetchpriority="high"` + `decoding="async"` auf Hero-`<img>` (statisch + dynamisch via `setPoster()` neu erzeugtes Bild) + `<link rel="preload" as="image">` für `Matchday 260926 LSP.webp`.
- `loading="lazy"` nachgerüstet: `join.html` (2× unterhalb Viewport: Memberskaart-Modal, Footer-Logo; Hero-Logo bewusst `eager`), `statistics-25-26.html` (4× JS-generierte Kids-Teamfotos), `news.html` (alle Feed-Cards unterhalb der ersten auf `lazy` + `decoding="async"`; nur NEXTGEN-Hero bleibt `eager`).
- CLS: neue Regel `.news-card-bg, .news-card-poster { aspect-ratio: 16/9 }` in `styles.css` reserviert Bildplatz vor dem Laden. Hero-`.news-card-hero` hatte bereits `aspect-ratio: 16/9`.
- Korrigiert: falscher MIME-Typ `type="image/avif"` auf einer `.webp`-Source im dynamischen `setPoster()` entfernt (verhinderte ggf. Preload-Miss).
- `generator.html`-Canvas-Bilder bewusst ohne `loading` (Export-Logik, `crossorigin` nötig) — nicht angefasst.

### 2. DOM-Reduzierung (konservativ, kein Risiko)
- CSS-Klassen-Scan (449 definierte Klassen): 69 nur 1× gefunden — fast alle sind JS-Toggles (`is-open`, `menu-open`), seitenweite Klassen oder i18n-Ziele → **keine Klasse gelöscht** (Löschen wäre DRY-Verstoß-Risiko ohne RUM-Daten).
- Stattdessen: 1 toter HTML-Kommentar (zeitgesteuerte Slide-Vorlage in `index.html`, historisch überholt) — bewusst BEHALTEN, da aktive Dokumentation für Redakteure. Keine auskommentierten Legacy-Blöcke in `styles.css` (nur 1-zeilige Sektions-Header).
- Echte Redundanz entfernt: doppelte AVIF-`<source>`-Zeile auf `.webp`-Datei im `setPoster()`-JS (siehe oben).

### 3. Caching-Logik
- `generator.html` Portrait-Hintergrund: CSS-`background:url(...)` + JS-Preload `bg.src` bekamen Cache-Buster `?v=20260925a9` → neue Hintergrunddatei erscheint ohne Hard-Reload; Version bumpbar pro Poster-Update.
- `index.html` Poster-Refresh (`#poster-set-btn`): nutzt bereits `?t=Date.now()`-Buster auf beiden Orientierungen (Portrait + Landscape) — verifiziert, unverändert korrekt.
- JS/CSS-Buster (`script.js?v=...`, `styles.css?v=...`) seitenweit vorhanden — unverändert.

### Verification
- `git diff --check` sauber; `loading=`-Counts: index 16 / news 16 / join 5 / stats 3→7; alle geänderten `src` lösen auf Disk auf.
- `hallo_agent9.txt` = `Cline ist startklar!` ✓
- Commits: `perf(...)` (Bilder/LCP/CLS) — PSD `assets/Unbenannt-1.psd` (13 MB) bewusst NICHT committet.

---

## Agent 8 – Git-Management & Konfliktauflösung – 2026-09-25

### Konfliktanalyse
- `git status`: uncommittet waren `gallery.html`, `misc-i18n.js`, `memory-bank/progress.md` (Agent-6-Arbeit) + untracked `assets/Unbenannt-1.psd` (13 MB, NICHT committet), `hallo_agent6.txt`.
- Konfliktmarker-Scan (`<<<<<<<`/`>>>>>>>`/`=======`) in `generator.html`, `index.html`, `script.js`, `styles.css`: **0 Treffer — keine Merge-Konflikte**.
- `git diff --check`: sauber (keine Whitespace-Fehler). Keine unmerged Pfade (`git ls-files -u` leer), kein Stash, Branch `main` synchron mit `origin/main`.
- Code-Zusammenführung: nichts zusammenzuführen nötig — `generator.html`/`index.html`/`script.js`/`styles.css` sind unverändert gegenüber HEAD (`a445abc`); parallele Agenten-Änderungen (Galerie/i18n) überschneiden sich nicht mit Generator/Carousel/Live-Center/Menü.

### Commit-Struktur (atomar)
- `ffb583b feat(gallery): Mannschaftsbilder-Bereich Saison 25/26 + i18n (Agent 6)` — `gallery.html`, `misc-i18n.js`, `hallo_agent6.txt`.
- Folgend: `chore(agent8): Git-Status verifiziert + hallo_agent8.txt` — dieser Eintrag + `hallo_agent8.txt`.
- Bewusst NICHT committet: `assets/Unbenannt-1.psd` (13 MB Arbeitsdatei, kein Deployment-Asset).

### Deployment-Check (GitHub Pages)
- `CNAME` = `mersch75.lu` ✓, `.nojekyll` vorhanden ✓, `index.html` im Root ✓.
- Kein `.github/workflows/` nötig (Pages via Branch-Deploy); kein Buildschritt (statisches HTML/CSS/JS).
- `index.html`-Referenzen: lokale `src`/`href` lösen auf (`?v=`-Query ausgenommen, ok); externe Links (flh.lu, Social, ehftv) unverändert.
- Validierung: `node --check misc-i18n.js` OK, `gallery.html` HTML-Parse OK, alle 14 `src` auf Disk (2× `?v=`-Cache-Buster ausgenommen = erwartet).
- `hallo_agent8.txt` = `Cline ist startklar!` ✓

---

## Agent 6 – Galerie-Ordner + Mannschaftsbilder – 2026-09-25

### Aufgabe
1. Auf `gallery.html` einen Folder/Bereich für Mannschaftsbilder anlegen (Bilder der Equippen einsetzen können).
2. Zusatz: `hallo_agent6.txt` im Root mit Inhalt `Cline ist startklar!`.
3. NICHT anfassen: `generator.html`, `live-center.html`, `_carousel_clean.py`, `js/flh-live-sync.js` (Generator-Bildkoordination daher bewusst NICHT umgesetzt — Eingriff wäre gegen die Vorgabe).

### Umsetzung
- Neuer Ordner `assets/pages/gallery/` (Repo-Konvention: page-spezifische Assets; keine Duplikate — Teamfotos bleiben Single-Source in `assets/shared/media/Ekippe Fotoen Saison 25-26/`, Galerie referenziert sie nur).
- `gallery.html`: neue responsive Sektion `gallery-teams` (Badge/Titel/Beschreibung + 9 Karten FE/H1/U15/U13/U11/U11-Espoir/U9/U7/U4, `loading="lazy"`, Grid 3→2→1 Spalten). Bestehende Coming-soon-Karte bleibt erhalten.
- `misc-i18n.js`: neue Keys `galleryTeamsBadge/Title/Desc` in allen 5 Sprachen (lb/fr/de/en/pt), an bestehende `galleryBadge/Title/Desc` angehängt.

### Verification
- `node --check misc-i18n.js` + `node --check script.js` OK; HTML-Parse OK.
- Alle 14 `src`-Referenzen in `gallery.html` lösen URL-dekodiert auf Disk auf (0 missing).
- `hallo_agent6.txt` = `Cline ist startklar!` ✓
- `git status`: nur `gallery.html`, `misc-i18n.js` modifiziert + `assets/pages/gallery/`, `hallo_agent6.txt` neu; Generator/Live-Dateien unberührt.

---

## NEXTGEN-Slide + Menü-Fix – 2026-09-25

### Aufgabe
1. `Media/Hauptseite/Nextgen Poster.webp` (3548×1787, Landscape) als neuen Carousel-Slide in `index.html` **und** als Karte in `news.html` einbauen, Klick → `nextgen.html`. Poster an Carousel-Dimensionen anpassen, nicht umgekehrt.
2. Menü-Button („Menü" klick → nichts geschieht) reparieren.

### Umsetzung
- Poster-Datei als Repo-Asset aufgenommen: `Media/Hauptseite/Nextgen Poster.webp` (`git add`), referenziert als `Media/Hauptseite/Nextgen%20Poster.webp`.
- `index.html`: neuer erster Slide `news-slide-nextgen` mit `<a class="news-slide-link" href="nextgen.html">` um das Poster-Bild. Bild nutzt bestehende Carousel-Geometrie (`flex: 0 0 100%`, `min-height: clamp(240px, 36vw, 390px)`) + neu `object-fit: contain` (Klassen `.events-background-contain`/`.news-nextgen-image`, Link-Block `.news-slide-link`) → Poster passt sich der Box an.
- `news.html`: neue Karte `<a class="news-card news-card-link news-slide-nextgen" href="nextgen.html">` vor der Hero-Karte, mit `.news-card-link` (Block, ohne Deko) + `.news-card-bg-contain` (`object-fit: contain`) in `styles.css`.
- `KEEP` in `_carousel_clean.py`/`_clean_v2.py` um `news-slide-nextgen` ergänzt → Skript: `Keeping: 3 / Removing: 0`, exit 0.
- Menü-Root-Cause: **2 konkurrierende Click-Handler** auf `.nav-toggle` – `initializeMobileMenu()` (Zeile 89, toggelt nur `.site-nav.is-open`) und `initializeSiteMenu()` (Zeile 2714, toggelt `.site-nav.is-open` + `.site-menu-backdrop.is-open` + `body.menu-open`) hoben sich gegenseitig auf → Klick = No-Op. **Fix:** doppelten Toggle-Handler aus `initializeMobileMenu()` entfernt (nur ESC-Schließlogik bleibt); Öffnen/Schließen läuft ausschließlich über `initializeSiteMenu()`.

### Verification
- `node --check script.js` OK; lokaler Server + headless Chrome: `site-menu-shell/-primary/-secondary/-close/-backdrop` vorhanden, simulierter Menü-Klick → `CLICKRESULT:OPEN-OK|aria=true|backdrop=1|body=true`, keine JS-Fehler.
- `index.html`: 3 `<article>` (nextgen/coupe-fe/ag), divs 35/35, endet `</html>`; `nextgen.html` live HTTP 200.

---

## Floumaart-Slide entfernt (index.html) – 2026-09-25

### Aufgabe
Slide mit Floumaart-zu-Schous-Poster (blauer Kasten, „Mir sinn dobäi!!") aus dem News-Carousel entfernen.

### Umsetzung
- `<article class="… news-slide-floumaart …">`-Block (inkl. Bild `assets/shared/media/Floumaart zu Schous.webp`) aus `index.html` entfernt → Carousel hat jetzt **2 Slides** (`news-slide-coupe-fe`, `news-slide-ag`). Datei-Bild bleibt auf Disk erhalten; `news.html` nutzt es weiterhin (5 Treffer dort, bewusst nicht angefasst).
- Zugehörige, nun verwaiste CSS-Regeln in `styles.css` entfernt (7 Block-Regeln: Desktop-Block + Mobile-Media-Query) → 0 Treffer `news-slide-floumaart` in `index.html`/`styles.css`.
- `KEEP`-Listen in `_carousel_clean.py` und `_clean_v2.py` auf `{'news-slide-coupe-fe', 'news-slide-ag'}` aktualisiert (Guard bleibt konsistent: Skriptlauf = `Keeping: 2 / Removing: 0`, exit 0).

### Verification
- `index.html`: 2 `<article>`, divs 35/35, sections 5/5, endet mit `</html>`.

---

## Carousel-Skript + 3-Slides-Verifikation – 2026-09-25

### Befund
- `_carousel_clean.py` läuft **fehlerfrei** (`Keeping: 3 / Removing: 0`, exit 0); der gemeldete Bug (nicht definierte `track_content_start`/`track_end_pos`) ist **nicht mehr vorhanden** – auch `_clean_v2.py` enthält diese Variablen nicht (grep: 0 Treffer). Beide Skripte sind zeilenweise + idempotent umgesetzt, Guard `kept != 3` vorhanden.
- `index.html`: genau **3 `<article>`** (`news-slide-floumaart`, `news-slide-coupe-fe`, `news-slide-ag`), Datei endet mit `</html>`; kein Bezug mehr auf entfernte Slides (z. B. `news-slide-luxqf3`).
- `hallo_agent2.txt` = `Cline ist startklar!` ✓
- Live-Check lief bereits idempotent (`diff` nach Skriptlauf: identisch) → keine Änderung, **kein Commit/Push nötig**; HEAD == origin/main (`5426786`). Einzig untracked: `assets/Unbenannt-1.psd` (nicht Teil der Aufgabe, liegen gelassen).

---

## Live-Center: Alte Resultate (vor 15.08.2026) entfernt – 2026-09-24

### Problem
Live-Center zeigte wieder Resultate aus der Vorsaison (25/26, Spiele Feb–Mai 2026), obwohl nur 2 Spiele (20.09.26) gespielt waren.

### Root Cause (in `js/flh-live-sync.js`)
1. `CURRENT_PERIOD_ID = '137'` = **Saison 25/26**; laut FLH-`po`-Menü ist die aktuelle Periode **142** (26/27).
2. `REQUESTS` nutzten noch die **alten `cl`-Klassen-IDs** der Saison 25/26 (153713, 152653, …).
3. Folge: `fetchAllGames()` holte 70 Alt-Spiele (mit Resultaten) und `mergeLiveSeasonGames()` mischte sie in `allGamesData` → Anzeige vor dem Saisonstart.
4. Zusätzlich: falsche `sGID`-Werte bei den 2 gespielten Spielen (3276105/3357291 = Vorsaison-Spiele) → Merge über sGID schlug fehl bzw. verlinkte falsche SBO-Berichte.

### Fix (neue `cl`-IDs via FLH-API verifiziert; 5 Kategorien)
| Kategorie | alt `cl` | **neu `cl`** |
|---|---|---|
| Männer (H-PRO) | 153713 | **167931** |
| Frauen (D-PRO) | 152653 | **168031** |
| U15G | 156341 | **168871** |
| U13M-P1 | 152106 (PE) | **168526** |
| U13M-P2 | – | **168531** |
- `CURRENT_PERIOD_ID` `'137'` → `'142'`.
- Turnier-Requests (u15fin, u11el, u11elpf, u11es, u9, u7) entfernt – Tournoi hat keine Resultate/Tabellen (Aussage Nutzer).
- **Saison-Guard** `SEASON_START = 15.08.2026` in `fetchCompetitionGames`: Live-Spiele davor werden verworfen (unparsebare Daten bleiben erhalten).
- `buildMergeKey` → `buildMergeKeys` (Mehrfach-Schlüssel `nr|` **und** `sbo|sGID`) + `mergeLiveSeasonGames` merged über beliebigen Treffer.
- Neu exportiert: `MerschFlhSync.dedupeByGameNumber()` (führt statisch/Live über `gNo` zusammen, behält Eintrag mit Resultat) – aufgerufen in `live-center.html` (`applyLiveCenterCorrections`) und `generator.html` (`applyGeneratorLiveGames`).
- `live-center.html`: sGID der 2 gespielten Spiele korrigiert → `3504081` (Frauen) / `3504641` (Männer).
- `renderStandingsPanel()` nutzt jetzt die **Live-Tabellen** (`window.__liveStandings`) statt nur der statischen Null-Astellung; Fallback bleibt.
- Cache-Bust: `flh-live-sync.js?v=20260714a` → `?v=20260924a` (live-center.html, generator.html).

### Verifikation (Node-Tests gegen echte FLH-API)
- Live-Payload: **47 Spiele, 0 vor 15.08.2026, 0 Fehler**; 5 Tabellen (Männer/Frauen/U15G/U13-P1/U13-P2).
- Merge+Saisonfilter Live-Center: **50 Einträge, 0 Duplikate, 0 Alt-Spiele**; Resultate: Frauen 25:22, Männer 29:27 (20.09.26).
- Generator: **47 Einträge, 0 Duplikate, 0 Alt-Spiele**.
- Archiv (`live-center-25-26.html` + `data/flh-archive-2526.json`): Merge-Ausgabe **identisch zu vorher** (148 Einträge) – **Archiv unberührt** (`git status` sauber für `data/`, `sbo-archiv/`, `live-center-25-26.html`).
- `node --check js/flh-live-sync.js` OK; alle Inline-Scripts in `live-center.html`/`generator.html` syntaktisch OK.

### Nicht angefasst (Anweisung Nutzer)
- `data/flh-archive-*.json`, `data/sbo-index-*.json`, `sbo-archiv/**`, `live-center-25-26.html` (Archiv).

---

## News-Carousel Cleanup (index.html) – 2026-09-23

### Goal
News-Carousel in `index.html` auf genau 3 Slides kürzen: `news-slide-floumaart`, `news-slide-coupe-fe`, `news-slide-ag`.

### Critical Incident
- Ein früherer Bereinigungslauf hat `index.html` auf **155 Zeilen abgeschnitten** (alles nach dem Track-Schluss: news-arrow-Buttons, news-dots, Footer, alle `<script>`s, `</body></html>`).
- Dieser kaputte Stand wurde versehentlich in Commit `37d172a` mitgecommitted und gepusht → Live-Seite war betroffen.
- **Reparatur:** Vollständige Datei aus `HEAD~1` (714 Zeilen, 12 Slides) wiederhergestellt, dann Cleanup erneut sauber ausgeführt → 531 Zeilen.

### Root Cause (Skript-Bugs)
1. Ältere Versionen: inkonsistente Variablennamen (`content_start` vs. `track_content_start`) und `rfind('<div', …)`, das das innere statt das Track-Div traf.
2. `_clean_v2.py` (1. Fassung): `in_track` wurde nie auf `False` gesetzt → nach dem Track-Div wurde **alle restlichen Zeilen bis EOF verworfen** (dieser Abbruch verursachte die 155-Zeilen-Datei).

### Solution (jetzt in `_carousel_clean.py` und `_clean_v2.py`)
- **Zeilenweise** Verarbeitung statt Region-Slicing: nur `<article …news-slide…>`-Blöcke (bis `</article>`) werden gefiltert, **alle anderen Zeilen laufen unverändert durch** → Track/Viewport-Divs, Buttons, Scripts, Footer bleiben garantiert intakt.
- Guard: `kept != 3` → Fehlermeldung und **kein Schreiben** der Datei.
- Idempotent: 2. Lauf ergibt `Keeping: 3 / Removing: 0`.

### Verification
- 531 Zeilen, genau 3 `<article>`, Klassen: `news-slide-ag`, `news-slide-coupe-fe`, `news-slide-floumaart`
- Tag-Balance: 37/37 `div`, 3/3 `article`, 5/5 `section`, 1× `</body></html>`
- `news-arrow-prev/next` (Zeile ~170) und `news-dots` vorhanden; kein JS/HTML-Bezug auf entfernte Slide-Klassen (nur Cache-Buster `script.js?v=…luxqf3`, der ist unrelated)
- `hallo_agent2.txt` = `Cline ist startklar!`

### Nachtrag (gleicher Tag): Poster-Pfad-Fix
- `37d172a` hatte `Matchday 260926 LSP.webp` und `Portrait 26092026.webp` nach `Media/` (ohne Unterordner) gelegt, aber `index.html` referenziert beide unter `Media/Hauptseite/` (11 Stellen: srcset, Poster-Download-Links, Cache-Busting-JS).
- **Fix (Commit `0738124`):** `git mv` beider Dateien nach `Media/Hauptseite/` (dort lagen auch die Vorgänger `current-matchposter.*`). Pfade `Media/…` ohne `Hauptseite/` wurden nirgends referenziert.
- Verifiziert: alle 11 Referenzen + Stichproben (`inside.html`, Logos) lösen auf Disk auf.

---

## Generator.html - Saison 2026/27 Fixes

### Issues Fixed:
1. **Portrait-Poster Hintergrundbild** - Das alte `portrait-poster-neu.png` (enthält bereits alte Spiele) wird **nicht mehr** als CSS-Hintergrund verwendet. Stattdessen: fester dunkler Hintergrund `#0d1b2a`. Das Portrait wird komplett dynamisch gerendert (alte Spiele können nicht mehr "doppelt" erscheinen).
2. **Tournoi-Slot-Anzeige** - Wenn kein Turnier aktiv ist, wird ein "Kein Turnier aktiv" Platzhalter angezeigt, sodass Jugend-Teams nicht falsch zusammenrutschen
3. **Jugend-Abstände** - Jugend-Teams haben jetzt besseren Abstand zwischen sich und den Männer-Teams durch erweiterte `youthCols`-Liste und optimierte Top-Positionen
4. **Youth-Modus Toggle** - Der Jugend-Modus funktioniert jetzt korrekt mit sauberer Trennung zwischen Turnier-, Jugend- und Männer-Slots
5. **Layout-Logik** - Turnier-Slot (`l-dynamic-tournoi`), Jugend-Slots (`youth3col` mit getrennten Spalten) und Männer-Slots (`l-dynamic-main`) sind jetzt sauber getrennt
6. **Einzelnes Portrait-Spiel** - Bei genau einem ausgewählten Spiel wird der Block auf 50% Breite gesetzt und horizontal mittig angezeigt
7. **`renderPortraitDataUrl()`** - Wartet nicht mehr auf ein Hintergrundbild, das bereits veraltete Spiele enthielt. Nur Fonts und dynamische Bilder werden gewartet.

### Root Cause:
Das Bild `assets/portrait-poster-neu.png` war **kein leeres Hintergrundbild**, sondern ein bereits gerendertes Poster mit alten Spielen. Als es als CSS-Background genutzt wurde, wurden alte Spiele fest ins Bild gebacken und die neuen nur darübergelegt → sichtbare "alt + neu"-Doppelung.

### Technical Changes:
- **CSS** (line 159): `#poster-portrait` background changed from `url("assets/portrait-poster-neu.png")` → `#0d1b2a` (einfarbig dunkel)
- **JS** `renderPortraitDataUrl()`: Removed background image load wait; only waits for fonts and `<img>` elements
- **JS** `updatePortraitPreview()`: Single portrait game → 50% width + centered via flex container
- **Landscape Layout**: youthCols `[40, 500, 800, 1200]`, youth top 600/660, clear tournoi/youth/senior separation

### Verification:
- Generator im Browser öffnen → alle Teams durchklicken → Landscape + Portrait prüfen
- Portrait zeigt NUR dynamische Inhalte (neue Spiele), kein altes Hintergrundbild mehr
- Bei genau einem Spiel → Block 50% Breite, zentriert
- "Poster herunterladen" → sauberes Portrait ohne alte Spiele darunter

---

## 2026-09-23: Homepage-Poster + Menü-Diagnose

### 1) Poster: Landscape statt Portrait auf index.html
- **Wunsch:** Die erste Seite soll das Landscape-Poster zeigen, nicht das Portrait.
- **Änderung:** `<picture id="landscape-poster-pic">` vereinacht zu einer einzigen WebP-Quelle + `<img>`-Fallback, beide = `Media/Hauptseite/Matchday 260926 LSP.webp`. Portrait-`<source>` (Mobil-Hochkant) und Portrait-Fallback entfernt. **Download-Buttons (Landscape/Portrait) unverändert.**
- **Hinweis:** Auf dem Handy (Hochkant) wird das Landscape-Poster jetzt ebenfalls angezeigt (hochkant gedreht), statt des Portrait-Posters.

#### Korrektur (gleicher Tag, finale Variante)
- **User-Klärung:** gewünscht ist das responsive Original-Verhalten:
  - Handy **Hochkant** (≤900px + portrait) → **Portrait**-Poster
  - Handy **Querformat** → **Landscape**-Poster
  - **PC** (jede Orientierung) → **nur Landscape**-Poster
- **Finale Struktur:** Portrait-`<source>` mit `media="(max-width: 900px) and (orientation: portrait)"` zurück, Landscape als `<source>` (ohne media) und als `<img>`-Fallback (statt früher Portrait-Fallback). Der wirkungslose `type="image/avif"`-Source (zeigte auf .webp) entfällt.

### 2) Menü "geht nicht mehr auf" – Diagnose: Live funktioniert es
- Headless-Chrome-Test von `https://mersch75.lu/`: **kein JS-Fehler**, `script.js` lädt, DOM enthält `site-menu-shell`/`site-menu-primary`/`site-menu-close` → `initializeSiteMenu()` läuft komplett durch; beide Poster-Pfade liefern HTTP 200.
- Wahrscheinlichste Ursache beim Reporter: **Browser-Cache des defekten Zwischenstands `37d172a`** (index.html auf 155 Zeilen beschnitten, ohne `<script src="script.js">` → Menü konnte gar nicht funktionieren). Abhilfe: **hart neu laden** (Cmd+Shift+R / Safari: Website neu laden), HTML-Cache auf GitHub Pages läuft nach ≤10 min aus.
- Reihenfolge in script.js geprüft: `initializeMobileMenu` (Z89) und `initializeSiteMenu` (Z2714) laufen **vor** `initializeNewsCarousel` (Z2718) – ein Carousel-Fehler könnte das Menü nicht brechen (und es gibt keinen).

### Verification
- `index.html`: 3 Artikel, 37/37 div, 5/5 section, endet `</html>`, 530 Zeilen.
- Referenzen des geänderten picture-Blocks prüfen: `Matchday 260926 LSP.webp` → 200 live.
## 2026-09-23 – Alte Portrait-Bilder endgültig entfernt
- `assets/Portrait Poster hellerer Hintergrund.png`, `assets/portrait-poster-neu.png`, `assets/assets/portrait-poster-neu.png` gelöscht (git rm), verschachtelter `assets/assets/`-Ordner entfernt.
- Repo-weit (ohne .kilo/.git) null Referenzen auf alte Bilder; einzige Quellen: CSS Zeile 159 + Export `renderPortraitDataUrl()` Zeile 2462 → `assets/PortraitBild mit hellem Hintergrund23092026.webp`.
- Achtung: Browser-Cache – Seite mit Hard-Reload (Strg/Cmd+Shift+R) neu laden.

## FLH-Cup-Synchronisierung (Agent 13)
- `js/flh-live-sync.js` lädt zusätzlich die aktuellen Coupe-Klassen der FLH: H-C-LN, D-C-LN, H-C-FLH, U15G-C und U13M-C.
- Coupe-Spiele werden als markierte Datensätze in den bestehenden Live-Sync aufgenommen; der Bereich „Coupe“ in `live-center.html` ersetzt seine bisherigen statischen Platzhalter durch die aktuellen FLH-Daten, sofern welche geliefert werden.
- Bestehende statische Coupe-Einträge bleiben als Fallback erhalten, wenn die FLH-Schnittstelle nicht erreichbar ist.
- Validiert mit `node --check` und `git diff --check`.



## 2026-09-25: Coupe-Poster und LS-Poster
- Drei Coupe-/Senior-Spiele werden im Landscape-Poster nebeneinander in drei gleich breiten Spalten dargestellt.
- Das Desktop-Asset `Coupe de Luxembourg2026.png` wurde als optimiertes WebP nach `assets/Coupe de Luxembourg2026.webp` übernommen.
- Der Pokal ist im Landscape-/LS-Poster zentriert über dem Spielbereich eingebunden und für den Canvas-Export mit `crossorigin="anonymous"` markiert.

## 2026-09-25 (Folz): Coupe-Layout finalisiert
- Coupe-Poster: alle drei Spiele (Frauen/Männer/U15) rendern dank `forceBig` im großen Senioren-Zweig (150px-Icons, 120px-Badge) in einer Reihe bei `left: 76 / 570 / 1064`.
- Coupe-Pokal: ein Pokal-Image (`coupe-trophy`) rechts im freien Bereich über dem letzten Block (`top: 150`, Mitte = Blockmitte 1293 dank CSS `translateX(-50%)`); Per-Team-Pokal im `big`-Zweig nur noch ohne `forceBig`.
- Tournoi-Strip (Landscape) wird jetzt nur gerendert, wenn mindestens ein aktives Team (U11 Espoir/U9/U7/U4) den Typ „Tournoi“ hat — bei Coupe und Meisterschaft ohne Tournoi bleibt der Bereich leer.
- Validiert mit `node --check` (alle 6 Inline-Skripte) und `git diff --check`; Commits `b970092` und `d0614a8` gepusht.

- Bestehende Ein-Spiel-Zentrierung und Spiellogik bleiben erhalten.

## 2026-09-26: Cotisation – Spaltenumbau, Älteste-Regel, Reparatur-Fix

**Auslöser:** Der Benutzer hat die Mitgliederliste in Excel umgebaut –
`Spielen J/R/N` → `Spieler J/R/N` und nach **Spalte L** verschoben,
`Cotisatioun` jetzt in **M**, neue Eingabespalte **N `BEZAHLT J/N`**
(771 Zeilen vorbelegt mit `N`) für den Kassierer. Seine Arbeitsfassung ist
`TEST1_nur-calcchain.xlsm`; dort öffnet die Datei **ohne** Reparatur-Meldung,
also ist das Entfernen von `xl/calcChain.xml` harmlos.

**Neue Spaltenordnung (Blatt `Membres 2026_2027`):**
`J` Geburt · `K` Alterskategorie · `L` Spieler J/R/N · `M` Cotisatioun (Ziel) ·
`N` BEZAHLT J/N · `P` Code Courrier neu (Haushalt) · `AH` Spielerlizenz ·
`AI/AJ/AK` Offizielle-/ZS-/SR-Lizenz · letzte Datenspalte `BN` (66).
Helfer deshalb ab `BP` (68) bis `CE` (83).

**Quinn-Fall (vom Benutzer gemeldet):** Ruben (Jg. 2011, Spieler, Zeile 5)
hatte keinen Betrag, Nicole (Jg. 1976, Offizielle, Zeile 7) sollte
`210 (+0+50)` tragen. Ursache: `TraegerRegel` stand auf `Erste` – das trifft
die Altdatei zwar in 144/144 Fällen, ist aber fachlich falsch.
**Umgestellt auf `Aelteste`** (`tarife-cotisation.csv` → `TraegerRegel;Aelteste`).
Jetzt: Ruben → `F0002`, Robert → `F0002`, Nicole → `210 (+0+50)`.

**Familiencode statt Leerzelle:** Zeilen ohne eigenen Betrag zeigen jetzt den
Haushaltscode `Fxxxx` (335 Zeilen), damit die Zugehörigkeit auf einen Blick
sichtbar ist. 184 Zeilen bleiben leer – das sind Phantomzeilen ohne Namen,
Geburtsdatum und Lizenz.

**Reparatur-Meldung: Ursache gefunden und behoben.** In der ersten Fassung
wurden die Zellen jeder Zeile per Regex neu ausgelesen und zusammengesetzt;
dabei gingen `t="array" ref="…"` und `cm="1"` verloren. Jetzt wird nur die
Zelle **M** an ihrer Stelle per Textersatz ersetzt (Stil `s=` bleibt), die
Helfer werden hinten angehängt und sortiert, **keine** andere Zelle wird
angefasst. Neu: `pruefe_datei.py` prüft Wohlgeformtheit aller XML-Teile,
aufsteigende Spaltenfolge (773/773), unveränderte Übernahme aller

## 2026-09-26 (Nachtrag): Reparatur-Meldung gefunden, Abgleich Python ↔ Excel

**Ursache der „Problem bei einigen Inhalten"-Meldung:** in der Kopfzeile
wurden die Zeilen-Attribute vertauscht. Der Quelltext jeder Zeile beginnt
`<row r="1" spans="1:66" ht="54" customHeight="1" x14ac:dyDescent="0.2">`;
im Bausatz stand `m1.group(2)` (der Zellinhalt) an der Stelle der Attribute.
Ergebnis: `<row r="1"> spans="1:66" ht="54" … <c r="A1"…` – die Attribute
lagen als **Text in der Zeile**. Das ist schema-widrig, aber XML-noch
wohlgeformt, deshalb hat es der Wohlgeformtheits-Test nicht gesehen.
`pruefe_datei.py` prüft jetzt zusätzlich Punkt 3b „Fremde Inhalte in `<row>`",
und `regression_row1.py` erzeugt die kaputte Fassung absichtlich – der Test
schlägt darauf an, die neue Fassung ist sauber.

**Nichts entfernt:** `pruefe_spalten.py` belegt es – 66 Spalten in beiden
Dateien, 0 fehlend, 0 Zellen der Quelle ohne Wert mehr in der Datei.

**Abgleich Python ↔ Excel** (`pruefe_abgleich.py`, 772 Zeilen, **0 Abweichungen**)
hat drei echte Fehler aufgedeckt, die vorher in der Datei standen:
1. `parse_datum` gab für Excel-Serienzahlen `None` zurück. Spalte J enthält fast
   nur Zahlen (ANSAY Luka = 37023) → alle numerischen Daten bekamen 73415 und
   „Älteste" wurde zu „letzte Zeile des Blocks". Jetzt: `12.05.2001` und `37023`

## 2026-09-26 (Nachtrag 2): Excel repariert weiterhin – Bisektionsserie

Der Attribut-Fehler in Zeile 1 war **eine** Ursache, aber nicht die einzige:
Excel meldet weiterhin „Wir haben ein Problem bei einigen Inhalten erkannt".

**Alle Offline-Prüfungen bestehen:**
- `pruefe_alle_blaetter.py`: alle 13 Worksheet-XML schema-konform – aufsteigende
  Spalten, keine Dubletten, `r`-Attribute passend, `<c>`-Kinder in der
  Reihenfolge `f` → `v`/`is`, `<worksheet>`-Elemente in Schema-Reihenfolge
- `pruefe_formeln.py`: **16 850 Formelzellen, 32 Muster, 0 Fehler** – Klammern
  balanciert, bekannte Funktionen, Bereichsbezüge in richtiger Richtung.
  (Der erste Lauf meldete 9 Fehler – das war mein eigener Extraktor, der an
  `<f t="shared" si="…"/>` zerbrach; jetzt wird mit XML geparst.)
- `diff_paket.py`: `[Content_Types].xml`, `workbook.xml`, `workbook.xml.rels`
  und `app.xml` unterscheiden sich nur in den vier erwarteten Zeilen
- Paket: 37 Einträge in beiden Dateien, `[Content_Types].xml` zuerst, keine
  Verzeichnis-Einträge, `macroEnabled`-ContentType, `vbaProject.bin` vorhanden,
  keine Namenskollision mit `Cotisation`, `localSheetId` 0/1/2/8 unverändert

Damit ist der Fehler offline nicht auffindbar. `testbausteine.py` erzeugt
deshalb eine **Bisektionsserie** in `Vereins-OS/docs/_testbausteine/`, die von
`TEST1_nur-calcchain.xlsm` (nachweislich sauber) ausgehend jeweils **genau eine**
Änderung einführt:

| Datei | Änderung | kaputt ⇒ Ursache |
|---|---|---|
| B0 | nur calcChain entfernt | Kontrolle |
| B1 | + Blatt 1 (M, Helfer, Kopf) | Werkzeugblatte |
| B2 | + neues Blatt Cotisation | workbook/rels/Content_Types |
| B3 | + nur `app.xml` | app.xml |
| B4 | + nur `fullCalcOnLoad` | calcPr |
| B5 | alles zusammen (muss die Meldung zeigen) | erst die Kombination |

   liefern dieselbe Serienzahl.
2. `Schluessel − ZEILE()/1000000` ließ bei gleichem Geburtsdatum die *spätere*
   Zeile gewinnen → `+ ZEILE()/1000000`.
3. Doppeltes `[1:]` auf Config-CSV verlor `BOURG Jeannot` und den einzigen
   Haushalt `1, Medernacherstrooss` → BOURG zeigte `F0006` statt
   `Don ? +(0 +50)`, ANSAY je 300 statt einmal 384. Neu: `pruef_cotisation.
   liese_config()` erkennt vorhandene Kopfzeilen selbst.
4. Der Zweig „Tarif 0" ging beim Umbau verloren: Offizielle zeigten
   `0 (+0+50)` statt `(0+50)`, leere Zeilen `0` statt nichts.
5. `XSEUL` wirkt **pro Zeile** → der Zweig steht vor der Träger-Prüfung.

**Stichproben jetzt:** BOURG Jeannot `Don ? +(0 +50)` · ANSAY **Luka 384**,
Mathis `XSEUL` · QUINN Nicole `210 (+0+50)`, Ruben/Robert `F0002` ·
FERNANDEZ `(0+50)` · Phantomzeilen leer.
**Korrigierte Summe:** **57.728 €** (251 Betragszeilen). Früher genannte
Werte (86.074 / 86.319 / 86.324 €) waren **falsch** – da summierte das
Prüfskript auch die Ziffern der Haushaltscodes `F0002` mit.
Verteilung: 104× 210 · 53× 300 · 42× 384 · 44× (0+50) · 6× 210(+0+50) · 2× Don.


## 2026-09-26 (Nachtrag 3): Übersicht als Dauerwerkzeug

**Meldung:** „BRÜCK und BÜCHLER haben keine Cotisation, obwohl Spielerlizenz
vorhanden." Prüfung per `erkl_zeile.py`: die Werte **sind** vorhanden –
BÜCHLER Z155 Maxime = 384, BRÜCK Z225 Felix = 384. Die anderen Familienmitglieder
zeigen den Haushaltscode, weil nur EINE Zeile pro Haushalt die Rechnung trägt
(sonst wären es 2× 384). Der Fehler lag also nicht in der Berechnung.

**Neu:** `docs/cotisation/uebersicht.py` – schreibt
`docs/cotisation/Cotisation-UEBERSICHT.csv` (771 Zeilen × 13 Spalten, inkl.
„Rechnung traegt" und „Begruendung") und meldet auf der Konsole unter anderem:

* **Echte Lücken: KEINE** – jeder Haushalt, in dem jemand mit Lizenz spielt,
  trägt in *irgendeiner* Zeile einen Betrag. Das ist die Prüfung, die genau
  diesen Meldungsfall automatisch findet.
* 69 Spieler mit Lizenz zeigen den Haushaltscode statt eines Betrags
  (Erklärung steht in der Spalte „Rechnung traegt").
* 183 leere Zeilen = Phantomzeilen ohne Namen/Geburtsdatum/Lizenz,
  aber z. T. mit Spalte `L = J` – **Datenpflege-Kandidaten**.
* 23 von 181 Haushalten ohne Spieler mit Lizenz.

`erkl_zeile.py <ZeilenNr>` zeigt den kompletten Rechenweg einer Familie
(Personen, Spieler mit Lizenz, Tarif, Träger).

**Wichtig für den Wahrheitswert:** Die Werte stehen in der gebauten Datei als
`<v>` drin – wenn sie in Excel nach der Reparatur leer sind, **frisst die
Reparatur sie**. Deshalb bleibt die Bisektionsserie B0–B5 der entscheidende
nächste Schritt.

Originalzellen (0 fehlend, 0 verändert) sowie `app.xml` und `calcChain`.

**Wert-Rückfallebene:** Der Bausatz liest das Blatt der Quelldatei selbst
(`liese_blatt`) – der CSV-Export hat wegen der Umsortierung eine andere
Zeilenreihenfolge – und schreibt das Ergebnis des Python-Referenzmodells als
`<v>` in jede M-Zelle. Die Mappe zeigt also schon vor der Neuberechnung durch
Excel die richtigen Werte.

## 2026-09-26 (Nachtrag 4): Bisektionsergebnis B0–B5 und Unterspalte B1

**Ergebnis der ersten Serie (vom Benutzer getestet):** nur **B1** und **B5**
zeigen die Reparatur-Meldung. B0 (nur calcChain), B2 (nur neues Blatt
`Cotisation`), B3 (nur `app.xml`) und B4 (nur `fullCalcOnLoad`) sind **sauber**.

⇒ Die Ursache steckt ausschließlich in den Änderungen an **Blatt 1**
(`Membres 2026_2027`). Die Paket-Schritte (workbook.xml, rels,
Content_Types, app.xml) und `fullCalcOnLoad` sind nachweislich unschuldig.

**Hypothese `metadata.xml` verworfen:** `cm=` kommt in Blatt 1 (771×),
Blatt 2 (772×) und Blatt 3 (299×) vor, zusammen 1.842. Nach dem Ersetzen der
M-Zellen bleiben 1.071 auf Blatt 2/3 – `metadata.xml` ist also weiterhin
referenziert, kein verwaister Teil.

**Zwei Korrekturen im Bausatz:**

1. **`t="str"` nur noch für echte Texte.** Bisher bekam *jede* M-Zelle mit
   Inhalt `t="str"` – auch bei numerischem Wert (`<c r="M155" t="str">…<v>384</v>`).
   Das ist eine Typabweichung und ein plausibler Reparaturgrund. Zahlen kommen
   jetzt ohne `t`-Attribut, Texte (Familiencodes, `Don ? +(0 +50)`) weiter mit
   `t="str"`.
2. **`spans` wird pro Zeile berechnet** statt pauschal 1:83 – eine Zeile ohne
   Helferzellen hätte sonst einen falschen Hinweis bekommen.

**Eigener Fehler, vom Validator gefangen:** beim Einbau von `spans_anpassen`
fehlte das schließende `</row>`; `pruefe_datei.py` und
`pruefe_alle_blaetter.py` meldeten sofort „mismatched tag" für alle Varianten.
Nach der Korrektur sind alle vier Unterspalten strukturell sauber.

**Neue Testserie** `testbausteine_b1.py` → `Vereins-OS/docs/_testbausteine_b1/`,
schaltet die drei Bestandteile der Blatt-1-Änderung einzeln zu
(`baue_membres_sheet(xml, werte, mit_m, mit_helper, mit_kopf)`):

| Datei | M-Zellen | Helfer BP:CE | Kopfzeile BP1:CE1 | Zellen Zeile 1/2 |
|---|---|---|---|---|
| B1a | neu | nein | nein | 66 / 66 |
| B1b | alt | ja | nein | 66 / 82 |
| B1c | alt | nein | ja | 82 / 66 |
| B1d | neu | ja | ja | 82 / 82 |

Wichtig: B1d entspricht dem alten B1, enthält aber die `t="str"`-Korrektur.
Ist B1d **jetzt sauber**, war die Typabweichung die Ursache.


**Ergebnis:** 253 Beträge, 335 Familiencodes, 184 leer, **Summe 86.319 €**.


## 2026-09-26 (Nachtrag 5): B1b ist die Stelle, AutoFilter entdeckt

**Neues Testergebnis des Benutzers:** B1a (nur M-Zellen ersetzen) **sauber**,
B1c (nur Kopfzeile) **sauber**, **B1b und B1d zeigen die Meldung**.
⇒ Die Ursache sitzt eindeutig in den **angehängten Helferzellen BP:CE** in den
Datenzeilen 2–773. Der Ersatz der M-Formeln und die Kopfzeile sind unschuldig.

**Neuer Befund im Blatt 1 — AutoFilter mit Sortierzustand:**

```xml
<autoFilter ref="A1:BN772" xr:uid="{00000000-0009-0000-0000-000000000000}">
  <sortState ref="A2:BN772" xmlns:xlrd2="…/2017/richdata2">
    <sortCondition ref="P1:P772"/>
  </sortState>
</autoFilter>
```

Der Filter endet bei **BN/Zeile 772**, die Dimension der Quelle bei **Zeile 773**
– die Quelldatei öffnet trotzdem sauber, die Ungereimtheit ist also nicht allein
fatal. Sie wird durch die Erweiterung bis **CE** aber verschärft.
Auch die `xr:uid`-Werte sind auffällig (mehrfach identisch) – die Datei ist
offenbar durch ein Fremdwerkzeug gelaufen (Google-Sheets-Export o. ä.).

**Neu in `pruefe_alle_blaetter.py`:** Prüfung 4 „Bereichs-Ungereimtheiten" –
vergleicht `dimension`, `autoFilter`, `sortState` und `mergeCells`. Sie meldet
in der gebauten Datei „autoFilter endet in Zeile 772, dimension in Zeile 773";
die Quelldatei hat denselben Befund, weitere Blätter (sheet2) ebenfalls
(pre-existing, tolerated).

**Eskalationsserie** `testbausteine_b1b.py` → `_testbausteine_b1b/`, acht Dateien,
die das Anhängen schrittweise aufbauen und die Filterfrage klären:

| Datei | Inhalt |
|---|---|
| E1 | 1 Zelle BP als Konstante |
| E2 | 1 Zelle BP als Formel |
| E3 | nur eine leere Zelle `<c r="BXn"/>` |
| E4 | alle Helfer als Konstanten |
| E5 | alle Helfer als Formeln (= B1b) |
| E6 | E5 + AutoFilter/sortState auf CE erweitert |
| E7 | E5 ohne AutoFilter |
| E8 | E5 + Filter auf CE **und** Zeile 772 (vollständig konsistent) |

Alle acht sind strukturell sauber (Validator). Interpretation:
E1/E2 kaputt → Anhängen bzw. Formel · E3 kaputt → leere Zelle ·
E4 sauber/E5 kaputt → Formelinhalte · E6/E7/E8 sauber → AutoFilter-Bereich.

**Offen:** In Excel öffnen und bestätigen, dass keine Reparatur-Meldung mehr
kommt; danach entscheiden, ob `TEST1_nur-calcchain.xlsm` oder die Datei vom
24.09. die kanonische Basis wird und die Vereins-OS-Skripte darauf zeigt.

## Cotisation – Blatt Stripe_Export + Stripe-Brücke – 2026-09-27

- **Neues Blatt `Stripe_Export`** in `…_mit-Cotisation.xlsm` (sheet14, A1:M773):
  - Eine Zeile pro Membres-Zeile, zeigt nur `TRAEGER`-Haushalte mit Betrag, sonst leer.
  - `A` FamID · `B` Rechnung_trägt · `C` Betrag_EUR (Zahl, `VALUE(L)`) ·
    `D` Betrag_Text (Rohtext, zeigt auch `(0+50)`/`Don ? …`) · `E` Email (AX) ·
    `F/G` Nom/Prenom · `H` Adresse · `I` Mitglieder (`COUNTIF`) ·
    `J` Bezahlt_JN (N) · `K/L/M` manuell: Stripe_Status, Stripe_Link, Bemerkung.
  - Nur einfache Zeilenformeln (keine Matrix) → läuft in Excel **und** Google Sheets.
  - Validierung: 26.788 Formelzellen / 38 Muster / 0 Fehler; Paket-Check unverändert
    (nur vorbestehende Filter-Befunde 772 vs. 773).
- **Stripe-Brücke** `scripts/google-apps-script-stripe-bridge.js` (Google-Sheet-Spiegel):
  - `syncStripe()` erzeugt pro offener Zeile (Betrag>0, Bezahlt≠J, Status leer) einen
    Stripe **Payment Link** (`STRIPE_MODE=payment_link`) oder eine **Invoice**
    (`STRIPE_MODE=invoice`, Versand via Stripe), schreibt Status+Link zurück.
  - Setup: `STRIPE_SECRET_KEY` als Script-Eigenschaft, Zeit-Trigger täglich 06:00,
    Menü „M75 Stripe → Jetzt synchronisieren".
- **Offen:** Spiegel Excel→Google Sheet einrichten (Import/Sync); `Bezahlt J/N`
  (N) ↔ Export-Spalte J abgleichen; Entscheidung Payment Link vs. Invoice pro Saison.
- **Spalte N mit „N" vorbefüllt (27.09.):** `N2:N773` enthalten jetzt überall ein
  `N` (zentriert, Inline-Text). Der Tresorier ändert bezahlte Zeilen manuell auf
  `J`. Hellblau-Markierung und Stripe-Export (`Bezahlt_JN`) laufen unverändert
  weiter. Validiert: 26.788 Zellen / 0 Fehler.

- **Hellblau-Markierung Spalte N (27.09.):** Bedingte Formatierung `N2:N773` —
  hellblau (`FFBDD7EE`), sobald `L` derselben Zeile einen Betrag/Derivat enthält
  (`384`, `210`, `300`, `(0+50)`, `Don ? …`). `Fxxxx`-Codes, `XSEUL`/`GAJGL` und
  leere Zellen bleiben weiss. Formel: `AND($L2<>"",LEFT($L2,1)<>"F",…)`.
  Validiert: 26.788 Zellen / 0 Fehler, keine neuen Paket-Befunde.

- **GAJGL ausgenommen (27.09.):** `Stripe_Export`-Spalte A zeigt keine Zeilen mit
  `Q="GAJGL"` mehr (reine Info-Zeilen der Mitgliederliste, 15 Zeilen mit `(0+50)`).
  Formel: `AND(BW=TRAEGER, L<>"", Q<>"GAJGL")`. Validiert: 26.788 Zellen / 0 Fehler.


## Cotisation auf Dauerbetrieb – Kapazität, Rename, Stripe-Sync (2026-09-27)

Die Mappe war auf eine Einmal-Berechnung ausgelegt (alles fest auf Zeile 773).
Drei Nacharbeiten für den laufenden Betrieb:

- **Kapazität `KAPAZITAET = 900` (127 Reservezeilen über den 772 Datenzeilen):**
  - Neue Konstante in `build_perfect_workbook.py`; `LETZTE` bleibt die belegte
    Datenzeile der Quelle, `KAPAZITAET` ist das Formelende.
  - `fuege_reserve_zeilen_hinzu()` erzeugt Zeilen 774–900 mit L-Formel, `N`="N"
    und allen Helfern `BP:CE` (ohne `<v>`-Cache, `fullCalcOnLoad` rechnet).
  - Alle Bereichsverweise der Helfer (`{l}`) zeigen jetzt auf `KAPAZITAET`, damit
    Neuzugänge in `COUNTIFS`/`SUMPRODUCT` (Haushaltsgrösse) mitzählen.
  - `dimension`, `autoFilter`, `sortState`, `_FilterDatabase` und beide CF-Blöcke
    auf 900 gestreckt. Vorher stand `autoFilter`/`sortState` auf **772** obwohl
    Daten bis 773 reichen — dieser Alt-Befund ist damit weg.
  - `Stripe_Export` führt 1:1 bis Zeile 900 mit (Spalte I `COUNTIF` bis 900).
- **Blattname dynamisch (`blattname_lesen()`):** Der Build liest den Namen des
  Datenblatts (sheet1.xml) aus `xl/workbook.xml` + Rels. Wird das Blatt in Excel
  umbenannt, bauen alle Formeln auf den neuen Namen. Weicht er von
  `BLATT_ERWARTET` ab, gibt das Skript eine Warnung aus. Leerzeichen werden
  automatisch quotiert. `Cotisation` und `Stripe_Export` bleiben fest benannt.
- **Farblogik in beiden Blättern, mit Bezahlt-Quittung:**
  - Datenblatt `N2:N900`: offen = **hellblau** (dxfId 2), `N`="J" = **grün**
    (dxfId 0, der vorhandene Grün-Eintrag), `stopIfTrue` auf der grünen Regel.
  - `Stripe_Export` `J2:J900`: gleiche Logik, aber nur wenn `A` (FamID) gefüllt
    ist — leere Zeilen bleiben weiss.
  - Formel offen: `AND($L2<>"",LEFT($L2,1)<>"F",$L2<>"XSEUL",$L2<>"GAJGL",$N2<>"J")`.
- **Bug behoben: Phantom-FamID in leeren Zeilen.** `BP` lieferte bei leerem
  Haushaltscode `"@"&ROW()`; in den 167 leeren Zeilen 607–773 hätte Excel damit
  `BW`="TRAEGER" und Text `@774` in `L` erzeugt und Stripe-Rechnungen ausgelöst.
  Jetzt `IF($Q="","",…)` → leere Zeilen bleiben vollständig stumm. Kein
  bestehender Datenwert ändert sich (kein `Q`-Leerwert in 2–606).
- **Doku:** `docs/cotisation/README.md`, neuer Abschnitt „Blatt umbenannt /
  neue Mitglieder“ mit den Betriebsregeln. Hinweise zu Neuzugängen und
  Umbenennungen im Apps-Script ergänzt (liest `getLastRow`, keine festen Zeilen).
- **Validierung:** 29.963 Formelzellen / 38 Muster / **0 Fehler**; Paket-Check
  12 Befunde (3 Typen), alle in **Altblättern** (`sheet2` Cotisations-Filter,
  `sheet10` ohne `_rels`) — **keine** in den bearbeiteten Blättern; openpyxl
  liest 14 Blätter, CF in beiden Blättern korrekt erkannt.
- **Datei umbenannt (27.09.):** Der Tresorier hat die fertige Mappe in
  `GC 2026-09-26 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm` umbenannt
  (reiner Rename, keine Excel-Bearbeitung — Grösse/Zeitstempel identisch zum
  Build). Konsequenz: Der Zielpfad war in **16 Skripten** hart kodiert, ein
  späterer Build hätte eine zweite Datei mit dem alten Namen erzeugt.
  - Neu `docs/cotisation/mappe.py`: einzige Quelle für Pfade.
    `quelle()` = Original (nie anfassen), `ziel()` = Standardname, sonst
    **neueste** `*_mit-Cotisation*.xlsm` (umbenannt erkannt), sonst Abbruch.
    Excel-Sperrdateien `~$…` werden ausgeschlossen.
  - `build_perfect_workbook.py`, `pruefe_formeln.py`, `pruefe_alle_blaetter.py`
    nutzen jetzt `mappe.ziel()`; Pfad weiterhin per `sys.argv[1]` überschreibbar.
  - Fallback-Logik getestet: umbenannte Datei erkannt, Standardname hat Vorrang,
    leerer Ordner bricht mit klarer Meldung ab.
  - Regel: nur **eine** `*_mit-Cotisation*.xlsm` im Docs-Ordner halten, sonst
    ist „die neueste“ mehrdeutig (im README dokumentiert).

## Stripe-Export: 71 XSEUL-Rechnungen fehlten (2026-09-27)

- **Symptom:** „Ich sehe bei Stripe nicht viele XSEUL, das kann doch nicht sein?“
- **Ursache:** Das Tor in `Stripe_Export` Spalte A verlangte `BW="TRAEGER"`.
  `XSEUL` ist aber **kein Haushaltscode**, sondern ein Status für
  Einzelpersonen: alle 74 XSEUL-Zeilen bekommen in `BP` denselben Wert
  `"XSEUL"` (der `ADR:`-Zweig greift nur bei Adressen aus
  `haushalte-cotisation.csv`, und dort steht genau **eine** Adresse).
  → eine 74-köpfige Pseudo-Gruppe → **genau ein** Träger → 1 statt 73 Rechnungen.
- **Messung** (neu `docs/cotisation/pruefe_stripe_export.py`, Soll/Ist gegen
  `pruef_cotisation.berechne()`): Soll **234** Rechnungen (Zeilen mit echtem
  Betrag, ohne GAJGL), vorher im Export **163** → **+71** fehlend, davon
  49 × 300 € („Sondercode XSEUL“) und 23 × `(0+50)` („Spieler mit Status R“).
- **Fix** in `baue_stripe_sheet()`: zweites Tor über die zeilen-eigenen
  Beträge, die das Python-Modell ebenfalls kennt:
  `AND(L<>"", Q<>"GAJGL", OR(BW="TRAEGER", BX<>"", CB<>"", CD<>""))`
  → `BX` manuell, `CB` Personenwert/Ausnahme, `CD` XSEULwert.
  Ergebnis: **234 = 234**, keine F-Code-Angehörigen und keine GAJGL im Export.
- **Farbregel nachgezogen:** `$Q2<>"GAJGL"` in beiden CF-Regeln — die 15
  GAJGL-Zeilen waren trotz Ausschluss im Stripe-Export blau markiert
  („einzeln“), was der Realität widersprach.
- **`syncStripe()`:** offene Posten ohne reinen Zahlenbetrag (`(0+50)` → Spalte C
  leer) erzeugten bisher **keinen** Link und wurden kommentarlos übersprungen.
  Sie landen jetzt im Ausführungsprotokoll als
  `ACHTUNG – N offene Posten … manuell in Stripe anlegen`.
- **Neue Prüfskripte:** `pruefe_stripe_export.py` (Soll/Ist, Exit-Code 1 bei
  Verlust), `pruefe_stripe_tor.py` (liest das Tor aus der gebauten Datei).
## Spalte O: undefinierter Wert "X" loescht still eine Rechnung (2026-09-27)

- **Symptom:** „Wenn ich in Spalte O ein X einsetze, wird L = 0.– und es wird
  kein Beleg bei Stripe angelegt.“
- **Befund (empirisch, `docs/cotisation/test_spielt_x.py`, Ist 234 Rechnungen /
  55 428 €):** Das ist **kein Absturz, sondern die dokumentierte Tariflogik** —
  aber die Falle ist teuer und bisher unsichtbar.
  - `O` kennt genau drei Werte: `J` (300/210/384), `R` (0+50), `N` (kein
    Spielertarif). **`X` kommt in keiner einzigen Formel vor** und wird wie
    „leer" behandelt: die Person ist weder Spieler noch Reserve.
  - Folge 1: ist noch ein lizenzierter Spieler im Haushalt, fällt 384 € auf
    210/300 € und der Betrag wandert auf die **andere** Zeile (44 Haushalte
    betroffen). Folge 2: ist sie der einzige lizenzierte Spieler, sind Tarif
    und Zuschlag 0 → `L` wird **leer** (nicht „0.–") und der Haushalt
    verliert die Rechnung komplett (Beispiel Z12 ANDRADE SOUSA 210 € → keine
    Rechnung). Im Mittel **−129 €** pro `X`, im Extremfall −384 €.
  - Nebenwirkung: `N` bedeutet „spielt nicht" und ergibt `(0+50)`, `X` ergibt
    **gar nichts** — ein Tippfehler kostet also eine ganze Rechnung, ohne
    jede Rückmeldung in der Mappe.
- **Fix:** neue CF-Regel `O2:O900` mit neuem dxf (rot `FFFFC7CE`, Text
  `FF9C0006`): `AND($O2<>"",$O2<>"J",$O2<>"R",$O2<>"N")` → jeder undefinierte
  Wert ist jetzt sofort rot sichtbar. Am Betrag ändert sich **nichts** (keine
  Fachlogik-Anderung ohne Freigabe).
- **Doku:** README-Abschnitt „Spalte O – was die Werte J / R / N / X bedeuten“
  mit der Empfehlung `R` (0+50) bzw. `BX` (Manuell) statt `X`.
- **Validierung:** 30.641 Formelzellen / 38 Muster / 0 Fehler; Paket-Check 12
  Befunde (unverändert Altblätter); Stripe-Logik 234 = 234; CF in openpyxl:
  `N2:N900` → dxf 0 + 2, `O2:O900` → dxf 3.
- **Offen (Fachentscheidung):** soll `X` künftig eine eigene Bedeutung
  bekommen (z. B. wie `N`, oder wie `R`)? Bewusst **nicht** eigenmächtig
  umgesetzt, weil das die Beträge des Clubs verändert.

## Stripe_Export Spalte C war bei 34 Rechnungen leer (2026-09-27)

- **Symptom:** „Im Stripe_Export steht kein Betrag, was die Person zu zahlen
  hat – warum?“
- **Ursache:** Spalte C war `IFERROR(VALUE(L),"")`. `VALUE` kann nur reine
  Zahlen — und `L` enthält an **34 von 234** Rechnungszeilen **Text**:
  28 × `(0+50)` und 6 × `210 (+0+50)`. `VALUE` scheiterte, `IFERROR` lieferte
  `""` → Betrag leer → `syncStripe()` übersprang die Zeile
  (`!(betrag > 0)`), also **kein Beleg**. Weitere 2 Zeilen (`Don ?`) sind
  bewusst nicht im Export, der Betrag steht dort fachlich nicht fest.
- **Fix:** Parser in Spalte C statt reinem `VALUE`:
  `"384"`→384 · `"(0+50)"`→**50** (0 Basis + 50 Zuschlag) ·
  `"210 (+0+50)"`→**210** (die +50 sind Bestandteil, nicht zusätzlich) ·
  `"Don ? …"`→leer. Alles in `IFERROR`, bleibt Excel- und Google-Sheets-tauglich.
  Spalte **D** behält den Rohtext zur Kontrolle.
- **Ergebnis:** **234/234** Rechnungen mit Betrag, Summe **56.828 €**
  (vorher 200 mit Betrag). `pruefe_stripe_export.py` misst die Abdeckung
  jetzt mit und gibt die Summe aus.
- **Test:** neu `docs/cotisation/test_betrag_parse.py` (10 Fälle inkl.
  `F0001`/`XSEUL`/leer, die weiterhin leer bleiben müssen) — 0 Abweichungen
  zur Excel-Formel. Parser als Python-Pendant in `pruefe_stripe_export.py`
  (`betrag_zahl()`), damit Modell und Datei dieselbe Logik messen.
- **Fehler dabei behoben:** erste Einfügung landete mitten in der
  `zellen`-Liste → `SyntaxError` im Build; Parse-Ausdruck jetzt vor der Liste.
- **Validierung:** 30.641 Formelzellen / 38 Muster / 0 Fehler; Paket-Check 12
  Befunde (unverändert Altblätter); Stripe-Tor korrekt; JS-Syntax ok.

## Stripe ohne Google: Direktweg Excel -> Stripe (2026-09-27)

- **Auslöser:** „Du sprichst von Google Sheet, aber das haben wir noch nicht,
  nur Excel, oder?" — korrekt, es gibt **kein** Google-Sheet. Der
  Google-Spiegel war eine Option von mir, nicht eine Gegebenheit.
- **Konsequenz:** `scripts/google-apps-script-stripe-bridge.js` war damit
  **nicht lauffähig** (es liest ein Blatt `Stripe_Export` in einer
  Google-Datei, die es nicht gibt). Statt eine neue Infrastruktur
  vorauszusetzen, jetzt der Direktweg ohne Google.
- **Neu `docs/cotisation/stripe_sync.py`:** liest dieselbe Quelle wie der Build
  und rechnet mit `pruef_cotisation` (nachgebautes, gegen die Mappe
  geprüftes Modell), legt pro offener Zeile einen Stripe Payment Link an
  (`metadata[famid]`, `metadata[excel_zeile]`, `metadata[saison]`) und
  schreibt den Stand in `…_mit-Cotisation.stripe-status.json` neben der
  Mappe — **nicht** in die Mappe, damit keine Excel-Bearbeitung verloren geht.
  Bereits angelegte Zeilen werden nie erneut gebucht.
- **Sicherheitsnetze (alle getestet):** ohne `--apply` nur Vorschau und **kein**
  Stripe-Kontakt; `--apply` ohne `STRIPE_SECRET_KEY` bricht ab; ein
  `sk_live_…`-Key bricht ohne `M75_LIVE_OK=1` ab; Key nur aus der
  Umgebungsvariable, nie aus dem Repo. Statusdatei entsteht nur nach echtem
  Lauf (verifiziert: nach den Abbruchtests keine Datei vorhanden).
- **Probelauf:** 234 Rechnungen, 234 offen, Summe **56.828,00 €**, 2 ohne
  E-Mail. Die FamIDs der Vorschau bestätigen die Gruppierung: `F0103`, `XSEUL`
  und `ADR:1,MEDERNACHERSTROOSS` (der einzige konfigurierte Haushalt).
- **Modell erweitert:** `pruef_cotisation.berechne()` liefert jetzt zusätzlich
  `famkey` (Wert der Excel-Hilfe `BP`/FamID) im Ergebnis-Dict — additiv, die
  bestehenden Auswertungen bleiben unverändert.
- **Was der Benutzer noch braucht:** verifiziertes Stripe-Konto
  (Vereinsname, Adresse, IBAN, RCS, Ausweis) und den Secret Key
  (`sk_test_…` zuerst) als Umgebungsvariable. Für den E-Mail-Absender später
  eine verifizierte Stripe-Domain.
- **Doku:** README-Abschnitt „Stripe starten – ganz ohne Google“ inkl.
  Sicherheitstabelle und dem Hinweis **nur einen der beiden Wege** benutzen
  (sonst doppelte Links).
- **Sicherheitsbefund (gemeldet, nicht geändert):** in
  `scripts/google-apps-script-join-webapp.js` steht der Token
  `m75-join-9f36-secure-2026` im Klartext im öffentlichen GitHub-Pages-Repo.
  Vor dem Stripe-Key rotieren.

## Drittperson: Sicherung vor dem Überschreiben (2026-09-27)

- **Frage:** „Wenn eine Drittperson, also der Tresorier, alles von Stripe hat,
  kann er mit dieser Excel Sheet arbeiten?“
- **Klärung (im README dokumentiert):** Er kann mit der Datei arbeiten
  (Mitglieder eintragen ab Zeile 774, `N` = `J` markieren, `Stripe_Export`
  prüfen) — die **Payment Links kann er nicht selbst erzeugen**, das läuft über
  `stripe_sync.py` auf dem Mac. Rollen getrennt: Tresorier markiert, ich
  buche.
- **Rechtefrage ausdrücklich benannt:** `sk_live_…` ist kein teilbares
  Passwort, sondern Vollzugriff auf das Konto (Kundendaten, Rückerstattungen,
  Preise). Empfehlung: eigener Stripe-Zugang mit beschränkten Rollen statt
  Key teilen. Alternative für „ohne Mac": Google-Weg mit Trigger — dort
  braucht er denselben Key, also dieselbe Entscheidung.
- **Gefundene Falle, sofort entschärft:** `build_perfect_workbook.py` erzeugt die
  Mappe **immer neu aus dem Original**. Sämtliche `J`-Markierungen und neu
  eingetragenen Mitglieder des Tresoriers lägen ausschliesslich in der
  bisherigen Datei und wären beim nächsten Build spurlos weg.
  → Der Build legt jetzt vorher eine Sicherung mit Zeitstempel ab:
  `…_mit-Cotisation.backup-<Jahr-MM-DD_hhmm>.xlsm` (verifiziert, erste
  Sicherung `…backup-2026-09-27_1148.xlsm` entstanden).
- **Folge mitbedacht:** Die Sicherungen passen auf das Namensmuster
  `*_mit-Cotisation*.xlsm` und wären damit Kandidaten für `mappe.ziel()`.
  `mappe.ziel()` schliesst jetzt `*.backup-*` aus (ebenso wie `~$…`).
  Verifiziert: Standardname wird weiterhin korrekt erkannt.
- **Fehler dabei behoben:** `import datetime` + `datetime.now()` →
  `AttributeError` (die Klasse heisst `datetime.datetime`). Jetzt
  `from datetime import datetime`.

## Betrieb mit Google-Drive-Kopie beim Tresorier (2026-09-27)

- **Klarstellung:** Die Arbeitsmappe liegt beim Tresorier in **Google Drive**,
  er hat **keinen** Stripe-Key und kommt nicht an den Mac. Auf diesem Rechner
  gibt es kein Google Drive — es existieren also **zwei Stände**, die
  auseinanderlaufen können. Genau das ist im README als Ablauf festgelegt:
  *Er* lädt herunter, arbeitet in Excel, lädt hoch; *ich* verarbeite die
  hochgeladene Datei und lade das Ergebnis zurück.
- **Werkzeuge pfad-unabhängig gemacht:** `mappe.py` kennt jetzt
  `set_ziel(pfad)` (fest verankerte Arbeitsdatei) und `DOCS` ist über
  `M75_COTISATION_DOCS` überschreibbar. `build_perfect_workbook.py` und
  `stripe_sync.py` haben `--datei <pfad>`.
  **Verifiziert** mit einer Kopie in `/tmp/m75-drive-test/`: Build und Sync
  verarbeiteten die fremde Datei, die Sicherungskopie entstand dort korrekt,
  danach Testordner aufgeräumt. Standardpfad danach unverändert geprüft.
- **Kritische Warnung dokumentiert:** Die `.xlsm` darf **nicht** in Google
  Sheets geöffnet werden — das zerlegt bedingte Formatierungen, Helfer-Spalten
  `BP:CE` und das Blatt `Stripe_Export`. Drive ist die **Ablage**, Sheets ist
  **nicht** die Arbeitsumgebung.
- **Weiterhin geltend:** nur eine `…_mit-Cotisation.xlsm` in Bearbeitung;
  `.backup-<Zeitstempel>`-Dateien sind Archive, keine Arbeitsdateien.
- **Validierung nach den Umbauten:** 30.641 Formelzellen / 0 Fehler;
  Paket-Check 12 Befunde (Altblätter); Stripe-Logik 234 = 234.

## Neue Mitglieder wurden NICHT berücksichtigt – behoben (2026-09-27)

- **Frage:** „Wenn ich neue Mitglieder in das Excel setze, würden die
  automatisch berücksichtigt?“ — **Nein, es gab drei echte Brüche in der Kette.**
- **Bruch 1 – falsche Datei:** `stripe_sync.py` und `pruefe_stripe_export.py`
  lasen `QUELLE` (das **Original** vom 24.09.), nicht die Arbeitsdatei. Ein in
  Zeile 774 eingetragenes Mitglied wäre im Excel sichtbar, aber **nie** in
  Stripe gelandet. → Neu `mappe.datenquelle()`: rechnet auf der Arbeitsdatei
  (`ziel()`), fällt nur auf das Original zurück, wenn es keine gibt.
- **Bruch 2 – Zeilenleser endete bei 773:** `ba.liese_blatt()` lieferte
  Zeilen 2–773 fest; die Reservezeilen 774–900 waren für das Modell unsichtbar.
  → Liest jetzt bis zur letzten vorhandenen Zeile.
- **Bruch 3 – Inline-Text wurde nicht gelesen:** der Zeilenleser kannte nur
  `t="s"` (Shared Strings) und `<v>`. Der Build schreibt die Kopfzeilen der
  neuen Spalten M/N/O sowie alle Texte als `t="inlineStr"` (damit die
  String-Tabelle unangetastet bleibt) → die Kopfzeile **Spielt J/R/N** kam als
  **leer** an, das Modell brach mit „FEHLENDE SPALTEN“ ab. → `inlineStr`-Zweig
  ergänzt; zusätzlich `Spielt J/R/N` als Alias in `SPALTEN_ALT`.
- **End-to-End-Test** `docs/cotisation/test_neues_mitglied.py`: schreibt ein
  Testmitglied direkt ins XML (Inline-Text/Zahlen, aufsteigende
  Spaltenreihenfolge, vorhandene Zellen werden *ersetzt* statt verdoppelt) und
  ruft dasselbe Modell auf wie der Sync.
  Ergebnis: `Zeile 774 TESTFALL Neumitglied`, famkey `F9999`, **L = 300**
  (Tarif SEN), Traeger ja, rechnungsfähig ja.
  Zwei eigene Testfehler dabei gefunden und behoben: doppelte Zelle `O774`
  (die bestehende leere Zelle gewann beim Lesen) und ein `str`/`bytes`-Fehler.
- **Fachbefund für den Betrieb:** ohne **`K` = Alterskategorie (`SEN`/`U25`)**
  gibt es **keinen** Tarif, `L` bleibt leer und es entsteht **keine Rechnung** —
  bei einem neuen Mitglied also das wichtigste Pflichtfeld. Im README als
  Pflichtfeld-Tabelle dokumentiert.
- **Regel dokumentiert:** Für die laufende Saison ist **kein Build nötig**
  (L und `Stripe_Export` rechnen live). Ein Build aus dem Original **würde
  Neuzugänge verwerfen** — sie blieben nur in der Sicherung. Deshalb nach
  Neuzugängen: Datei sichern, Build nur wenn die Zeilen auch ins Original
  übernommen werden sollen.
- **Bestand unverändert:** 234 Rechnungen / 56.828 €, 0 Formelfehler,
  Paket-Check 12 Befunde (Altblätter).

## Spalte AI „Bénévole (B)" automatisch setzen (2026-09-27)

- **Auftrag:** In Spalte AI ein „B“ setzen, wenn ein Name in A steht, die
  Spalten AH, AI, AJ, AK, AL, AM, AN alle leer sind und kein GAJGL in P/Q steht.
- **Wichtig:** Der Benutzer hat die Arbeitsmappe in Excel bearbeitet und
  **selbst eine Spalte eingefügt** (AI „Bénévole (B)“), wodurch alle Spalten ab
  AI um eine Position gewandert sind. Ohne erneutes Lesen wäre jede
  Spaltenannahme falsch gewesen. Stand bei zwei Analyse-Runden unterschiedlich
  (13:57: Spalte Y / AI = U13F; 14:20: AI = Bénévole) — Regel: nach jeder
  Excel-Bearbeitung den Ist-Stand neu lesen, nicht zwischenspeichern.
- **GAJGL steht in Q („Code Courrier neu“, 15 Zeilen), in P kommt es nie vor.**
  Die Sperre wurde auf **beide** Spalten gelegt, damit sie unabhängig von der
  Spaltenbenennung trägt.
- **Ergebnis:** 590 Zeilen mit Namen, davon **200** erfüllen die Regel →
  200 Zellen in AI auf „B“ gesetzt. Im Blatt waren bereits **57 eigene B’s**
  vom Benutzer vorhanden (Zeilen ab 27) → gesamt **260**.
- **Rahmenlinien:** Spalte AI hatte sie schon vollständig (775 Zellen wie AH/AK).
  Beim Setzen bleibt das Formatattribut `s="58“` erhalten — **260/260 B-Zellen
  haben volle Rahmenlinien** (lrtb), nachgeprüft.
- **Skript `docs/cotisation/benevole_setzen.py`:** zählt erst (`--apply`
  schreibt), chirurgisches XML-Schreiben, Sicherungskopie mit Zeitstempel,
  XML-Validierung vor dem Schreiben, idempotent (zweiter Lauf findet 0 neue
  Zeilen, weil AI dann nicht mehr leer ist).

### Zwei eigene Fehler (beide gefunden und behoben)

1. **Datei kurzzeitig zerstört:** Der Zell-Ersetzungsausdruck übernahm das
   `r="…“`-Attribut mit (`<c r="AI2"r="AI2" …>`) **und** die Offsets des
   Zellen-Treffers wurden auf `m.group(0)` statt auf `m.group(3)` angewandt —
   damit wurde jede bearbeitete Zeile vorn abgeschnitten. Symptom:
   `ParseError: not well-formed`. **Kein Datenverlust:** Die vom Skript
   automatisch angelegte Sicherung hat den 14:20-Stand wiederhergestellt.
   Lehre: XML vor dem Schreiben validieren (ist jetzt eingebaut) und
   Offsets immer auf derselben Gruppe anwenden.
2. **`--datei` wurde ignoriert:** `mappe.set_ziel()` wertet nur
   `build_perfect_workbook.py` aus. Beim Test mit Kopie schrieb das Skript in
   die **echte** Datei. Am Auffallen der Kontrollzahl (0 statt 200 B in der
   Kopie) erkannt. Jetzt wertet `benevole_setzen.py` `--datei` selbst aus.



## Cotisation – finales Spaltenlayout L/M/N/O + saubere Neuberechnung – 2026-09-27

- **Ziel-Layout umgesetzt** (`docs/cotisation/build_perfect_workbook.py`, neu):
  - `L` = `Cotisatioun` (NEU berechnet, 772 Formelzellen + vorberechnete `<v>`-Werte)
  - `M` = `Cotisation 2` (manuelle J/N/R-Werte 1:1 erhalten: 417× J, 311× N, 26× R)
  - `N` = `Bezahlt J/N` (neu, leer für Kassierer – 772/772 leer)
  - `O` = `Spielt J/R/N` (neu, exakte Kopie von M – 772/772 identisch, steuert die Formeln)
  - `P`/`Q`+ = alte Spalten N+ um 2 nach rechts (`code courrier`→P, `Code Courrier neu`→Q,
    Lizenzen AG:AJ→AI:AL, Fragen AW:AZ→AY:BB, letzte Datenspalte BM→BO)
  - Helfer BP:CE (68–83) mit expliziten `<cols>`-Breiten angehängt.
- **Bugs gefunden & behoben** (alle hätten Excel-Reparatur oder falsche Werte bedeutet):
  - `shift_cell_ref` traf auch String-Literale (`DATE(2001,7,17)` → `W25`) und Funktionsnamen →
    jetzt nur echte Zellbezüge ausserhalb von `"…"`.
  - `parse_cells`-Regex schluckte den Body der Folgezelle bei `<c …/>` → Phantom-Duplikat
    BX2/BY2; `check_all_circ.py` meldete dadurch fälschlich `BX → BS/BT/BU` und `V → V`.
  - `<cols>`-Bereiche, die die Einfügegrenze überspannten (16–32, 36–47), wurden still
    fallengelassen → jetzt einzelspalten-genau aufgeteilt.
  - `app.xml`-Blattname landete vor den benannten Bereichen statt hinter dem letzten Blatt;
    `_FilterDatabase` (BM772), `autoFilter`/`sortState` (BM772) und Hyperlink-Anker (AV→AX)
    werden jetzt konsistent auf BO mitgezogen.
- **Validierung der gebauten Mappe** (`…_mit-Cotisation.xlsm`, 3.777.180 Bytes):
  - `pruefe_formeln.py`: **19.068 Formelzellen, 32 Muster, 0 Fehler**.
  - Zirkelbezugs-Check mit korrektem Parser: **keine Selbstreferenzen** (L hängt nur von
    BW/BX/CA/CB/CD ab, keine Zyklen).
  - `pruefe_alle_blaetter.py`: nur noch vorbestehende Befunde (Filter endet 772 vs.
    Dimension 773 – identisch in der Quelldatei; sheet10 ohne `_rels`).
- **Hausputz:** One-Shot-Skripte (`_val1.py`, `check_i3.py`, `test_fast_shift*.py`,
  `test_openpyxl_*.py`, `update_arbeitsmappe.py`) gelöscht; Rest (`baut_arbeitsmappe.py`
  vs. `build_perfect_workbook.py`) noch nicht zusammengeführt.
- **Offen:** Datei in Excel öffnen und bestätigen, dass keine Reparatur-Meldung kommt;
  danach `baut_arbeitsmappe.py` auf das neue Layout umstellen bzw. ersetzen.

## 2026-09-28 — Spielberechtigung (Spielerpass + Medico) durchgesetzt

**Entscheidung des Benutzers:** Die Daten sind der Ist-Zustand; die Leute sind
noch in der Datenbank, spielen aber nicht. Die Regel wird kostenwirksam
umgesetzt, nicht nur gewarnt.

**Regel:** Status `J` zählt nur mit
1. echtem Spielerpass in `AO` (`XXX` = Antrag bei der FLH, Lizenz existiert
   noch nicht → zählt nicht; alle 19 Vorkommen sind exakt `xxx`), und
2. Medico in `AX` ≥ Jahresgrenze. `AX` enthält das **Jahr bis wann gültig**,
   nicht das Untersuchungsjahr (`///` und Text wie `Apte` zählen nicht).

**Umsetzung:**
- `pruef_cotisation.py`: neue Hilfsfunktion `spielberecht()`, benutzt an allen
  drei Stellen, an denen „J" als Spieler gewertet wurde — Spielerzählung für
  den Familientarif, XSEUL-Zweig, Comité-Mindestbetrag. `TARIFE_STD` bekam
  `medicojahr`.
- `pruefe_abgleich.py`: dieselbe Regel in der Excel-Nachbildung.
- `cotisation_regeln_setzen.py`: neue Hilfsspalte **`CL (Spielberecht)`** mit
  `=IF(AND($O="J",$AO<>"",$AO<>"xxx",ISNUMBER($AX),$AX>=Cotisation!$B$13),1,0)`.
  `BY`/`BZ`/`CA` (SpielerGes/SEN/U25) zählen jetzt über `$CL=1`. `CJ` und `L`
  und `CH` nutzen `$CL` statt `$O="J"`.
- Jahresgrenze an **einer** Stelle: `Cotisation!B13` (Blatt `Cotisation`,
  Zeile 13, neu) und `tarife-cotisation.csv` als `MedicoJahr`. Am 01.01.2027
  an beiden Stellen auf 2027 setzen.
- `spielberechtung_liste.py` (neu) schreibt
  `Vereins-OS/docs/cotisation/spielberechtung-ohne-pass.md`.

**Zwei echte Fehler, die dabei auffielen und behoben sind:**
- Beim Ersetzen einer **geteilten** Formel wurde das Attribut `ref="…"`
  entfernt. Damit ist die Zelle kein Master mehr, die Follower zeigen ins
  Leere → genau die Reparatur-Meldung von damals. Jetzt bleiben `t="shared"`,
  `ref` und `si` **alle** erhalten, ersetzt wird nur der Formeltext.
- `colpos()` bekam den Zellbezug `"Z776"` statt des Spaltennamens → 667 statt 26,
  keine Einfügeposition, Zelle hing ans Zeilenende. `zelle_einfuegen()` ist jetzt
  dokumentiert und prüft beide Fälle.

**Wirkung:** 235 Posten / 53.846 € → **192 Posten / 40.706 €** (−13.140 €).
250 Mitglieder mit Status `J`, davon **182 spielberecht**, 57 Haushalte betroffen.

**Offen:** Die Mappe enthält für die geänderten Zellen keine gelesenen Werte
mehr (`<v>` entfernt, damit Excel neu rechnet). `pruefe_abgleich.py` meldet
deshalb bis zum Öffnen+Speichern in Excel ~122 Abweichungen — das sind
veraltete Cache-Werte, keine Fehler. Danach erneut laufen lassen.

## 2026-09-29 — Status X, Prüfwerkzeug, Rückabwicklung eines Fehlerschlusses

**Korrektur an der Diagnose vom 28.09.** Die 122 „Abweichungen" waren **keine
veralteten Cache-Werte**, sondern zwei Fehler in `pruefe_abgleich.py`:
1. Die Datei verglich gegen `TEST1_nur-calcchain.xlsm` vom 27.09. (alte
   Arbeitsfassung) statt gegen die Live-Mappe.
2. `ba.rechne_werte()` liest die Mappe **überhaupt nicht** — es rechnet selbst
   mit dem Python-Modell nach. Das Skript verglich also zwei Python-Implementierungen
   und konnte eine falsche Excel-Formel prinzipiell nicht finden.

**Neu: `pruefe_excel_gegen_python.py`** vergleicht die Werte, die **Excel
selbst** berechnet und gespeichert hat, mit der Python-Referenz. Damit kamen
28 echte Abweichungen heraus — und **zwei echte Fehler**, die behoben sind:
- `210 (+0+50)260` bei SCHUSTER Jeff: der Comité-Zuschlag wurde an den String
  *angehängt* statt ersetzt. Der Stripe-Parser hätte 210 statt 260 gelesen.
- ~310 Leerzeilen unter den Daten bekamen über `CH="0"` eine Rechnung `"0"`.
  Die erste Schranke in L prüft jetzt zusätzlich `$A`.

**Excel ist per AppleScript steuerbar** (`osascript`, Excel läuft bereits).
Ablauf: `calculate full rebuild` + `save`. Vorsicht: `cotisation_regeln_setzen.py`
ersetzt die Datei auf der Platte, während Excel sie offen hat — Excel muss dann
neu **geöffnet** werden, sonst speichert es die alte Fassung über die neue.

**Status X — Regelsatz vom Benutzer:**
> Alle mit X in Spalte O dürfen **nicht** in Stripe erscheinen, **außer** sie
> gehören zu einem Haushalt, wo ein Betrag fällig wäre.

Messung: **64 X-Personen, davon 32 Rechnungsträger.** Ein erster Versuch, X
per Formel auf „0" zu setzen, kostete **32 Haushaltsrechnungen**, weil der
Rechnungsträger dann 0 € trug. Zurückgenommen — die X-Schranke gehört **nicht**
in die L-Formel. Umsetzung stattdessen nur im Export:
`pruefe_stripe_export.echter_betrag()` gibt für `"0"` `False` zurück, damit
0-€-Posten nicht entstehen. Haushaltsbeträge auf X-Rechnungsträgern bleiben
unberührt. `pruefe_x_personen.py` prüft das und meldet Verstöße.

**Stand:** 181 Posten / 38.898 €, 8 echte Excel-gegen-Python-Unterschiede offen.
Die Differenz zu den früher genannten 40.706 € ist **nicht aufgeklärt** und
vor dem Export zu klären.




---

## 2026-09-29 — Reparatur der Mappe + Card-IDs ergänzt

**Reparatur-Ursache (aufgeklärt):** `cotisation_regeln_setzen.py` wurde mit
`--apply` ausgeführt, während die Mappe **noch in Excel offen war** (Sperrdatei
`~$…xlsm`). Zusätzlich fasst das Skript `calcChain.xml` nicht an. Beim
nächsten Speichern setzte Excel seine veraltete In-Memory-Version durch und
**verwarf die 6 neu eingefügten Formelzellen `CC583…CE585`** — das war die
Meldung „Inhalte reparieren". Genau die Zellen fehlten danach auch im
Vergleich mit der Sicherung.

**Wiederherstellung:**
1. beschädigte Datei als `…REPARIERT-verdacht-2026-09-29_0800.xlsm` gesichert
2. Stand `…regeln-2026-09-29_0758.xlsm` zurückgespielt
3. `calcChain.xml` samt Content-Type- und Relationship-Eintrag entfernt
4. Excel öffnete die Mappe **ohne** Reparatur, baute die Kette neu auf

**Offene Regel-Lücke:** `--apply` verlangt weiterhin, dass die Mappe in Excel
**geschlossen** ist. Das ist bisher nur dokumentiert, nicht erzwungen.


**Card-IDs ergänzt** (`docs/cotisation/cardids_generieren.py`) in der Datei
`GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm`
(umbenannt von `…2026-09-26…`; `mappe.py` `ZIEL_NAME` und 4 Skripte
mit hartem Pfad wurden mitgezogen):
- Spalte D = `Card-ID`, 8 Zeichen aus `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`
- Uniqueness gegen xlsm (580) + `data.db` (580) + `Sekretariat.db` (0) = 585
- **10 Mitglieder** ohne ID: Zeilen 180, 188, 201, 462, 464, 523, 534, 535,
  584, 586 — davon STREITZ Eliane (Z523), die `.kilo/agent/
  memberslescht-sync.md` als „Spezialfall (manuell)" führt; auf Rückfrage
  trotzdem generiert.
- Sicherung: `…cardids-2026-09-29_0954.xlsm`
- vor dem Schreiben geprüft: XML, Zellreihenfolge, doppelte Zellen,
  geteilte Formeln (426/370 unverändert); danach in Excel neu gerechnet
- **Stand: 0 fehlende Card-IDs** in den echten Datenzeilen 2..591

**Auffällig, NICHT geändert:** `VU4AUkF6` (Z12 ANDRADE SOUSA Matilde) —
Kleinschreibung, das einzige musterabweichende Vorkommen. Bewusst
überlassen, weil es eine **bestehende** ID ist.

**Noch offen:**
- die 10 neuen IDs sind **nur im xlsm**, nicht in `data.db` / `Sekretariat.db`
- 5 echte Excel-gegen-Python-Unterschiede (RESSEL, ROCHA MAJERUS, ZEBROWSKY
  Silvia, ZELLER Sarah, ZELLER Mortitz)
- Stripe-Payment-Links unverändert; **kein** `--apply`-Lauf, kein Secret Key

**Bisheriger Prüfstand:** 181 Posten / 39.218 €. Die früher genannten
40.706 € und die in einem Zwischenbericht genannten „320 € aus KREMER +
KRIER" sind **nicht belegt** — der Betragseffekt der Python-Korrektur wurde
nie gemessen.

---

## 2026-09-29 (II) — Defekte Pfade repariert, Ordner aufgeräumt

**Umbenennung der Mappe** durch den Tresorier:
`GC 2026-09-26 …_mit-Cotisation.xlsm` → `GC 2026-09-29 …_mit-Cotisation.xlsm`.

**Folge: 15 hartkodierte Pfade in 14 Skripten waren tot.** Sie erwarteten
`GC 2026-09-24 …_mit-Cotisation.xlsm`, das es schon lange nicht mehr gab.
Betroffen u. a. `pruefe_datei.py`, `pruefe_spalten.py`, `lese_m.py`,
`baut_arbeitsmappe.py`. Alle auf den neuen Namen gesetzt.

**`mappe.py` ist die zentrale Stelle** (`ZIEL_NAME` + Fallback auf die
neueste `*_mit-Cotisation*.xlsm`). Der Fallback prüfte vorher nur gegen
`.backup-` — Sicherungen mit `.regeln-`, `.cardids-`, `.alterskat-`,
`.kopf-`, `.benevole-`, `.REPARIERT-` hätten als Arbeitsdatei gewählt
werden können. Jetzt werden alle Sicherungssuffixe ausgeschlossen.

**Neu: `docs/cotisation/pfadcheck.py`** meldet bei der nächsten Umbenennung
sofort, welche Skripte brechen (unterscheidet Eingaben von selbst erzeugten
Dateien). Stand: `KAPUTT (0)`.

### Aufräumen — verschieben, nicht löschen

`*.xlsm` steht in `.gitignore` → **es gibt kein Rettungsnetz.**
`docs/cotisation/archivieren.py` prüft vor dem Umzug, welche xlsm Skripte
**lesen**, bricht bei Kollision, nimmt Pflichtdateien explizit aus der
Liste und führt danach den Pfadcheck erneut aus.

**29 Dateien → `Vereins-OS/docs/_archiv/` (113 MB)**
(22 Sicherungen, TEST2a/b/c, `_temp_shifted.xlsm`, 3 veraltete `~$`)

**Bleiben (5, alle Pflicht):**

- `GC 2026-09-29 …_mit-Cotisation.xlsm` (Live)
- `GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm` (**QUELLE** — `mappe.py` +
  `baut_arbeitsmappe.py`)
- `GC MEMBERSLESCHT 2026-2027.xlsm` (ältestes Original, 17.09.)
- `TEST1_nur-calcchain.xlsm` (13 Skripte)
- `TEST2_nur-blatt1.xlsm` (`check_backups.py`)

**Endabnahme:** 5 echte Excel-gegen-Python-Unterschiede · Stripe 181 /
39.218 € · X-Regel hält · Pfadcheck `KAPUTT (0)` — alles **unverändert**.



---

## 2026-09-29 (III) — Commits und Push

**Repo `mersch75test.github.io`** — `46acd25` (57 Dateien, 7694 Zeilen)
> fix(cotisation): veraltete xlsm-Pfade reparieren, Pfadcheck + Archiv-Tool
> ergaenzen

Erfasst: die komplette Werkzeugkette in `docs/cotisation/` (51 Skripte waren
nie versioniert), die Pfad-Korrekturen, `pfadcheck.py`, `archivieren.py`,
`cardids_generieren.py`, sowie `memory-bank/progress.md`.

**Repo `Vereins-OS`** — `d7105e6` (5 Dateien, 370 Zeilen)
> docs(cotisation): Anleitung + Integration Context erfassen, xlsm-Sicherungen
> sperren

- `ANLEITUNG-Cotisation-Tresorier.md` nannte noch `GC 2026-09-26 …` → korrigiert
- `spielberechtung-ohne-pass.md`, `memory-bank/integrationContext.md`,
  `.clinerules` erstmals versioniert
- `.gitignore`: `*.xlsm.bak*` (die `…bak-ohne-Formeln` ist eine Memberslescht
  und fiel vorher **nicht** unter `*.xlsm` — DSGVO-Lücke geschlossen),
  dazu `playwright-report/`, `test-results/`

**Vorher geprüft:** Secret-Scan beider Repos (nur Platzhalter wie
`sk_test_...`, keine echten Keys) · alle `.py` kompilierbar · Pfadcheck
`KAPUTT (0)`.

**Beide Pushes bestätigt** (lokal == origin). GitHub Pages: `status: built`
auf `46acd25`, `mersch75.lu/` und `/join.html` → HTTP 200.

**Bewusst nicht committet:** `hallo.txt` (Testdatei), `_agent10_check.py`,
`assets/Unbenannt-1.psd`, `assets/assets/`, `docs/pruefe-fanshop-slide.py`,
`scripts/google-apps-script-stripe-bridge.js` — alle unabhängig von dieser
Arbeit.
