# Spezifikation der Beitrags- und Gebührenlogik 2026/27

**Status:** Entwurf zur Freigabe · 29.09.2026
**Zweck:** Umsetzung der fünf Vereinsregeln als eindeutige, prüfbare
Berechnungsvorgabe. Grundlage für Excel-Formel, Python-Modell und System-Prompt.

**Regelquelle (wortgetreu übernommen):**

1. **Haushalts-Obergrenze:** maximaler Pauschalbetrag pro Haushalt **384 €**.
2. **Spieler und Offizielle mit Doppelrolle:** wer spielt **und** Offizieller
   ist, zahlt **stets nur den Höchstbetrag** – 210 €, 300 € oder 384 € für den
   gesamten Haushalt. **Keine Addition.**
3. **Fakultativer Zuschlag für Offizielle:** Offizielle-Lizenzen sind
   **optional**. Entweder **50 € inkl. Stimmrecht** oder **0 € ohne
   Stimmrecht**.
4. **Comité-Mitglieder:** aktive Offizielle im Comité zahlen einen
   **Pflichtbeitrag von mindestens 50 €**.
5. **Wechselwirkungen:**
   * Im **maximalen Familienbeitrag 384 €** ist die 50 € für das Comité
     **bereits inkludiert**.
   * Zahlt ein Comité-Mitglied **lediglich als Elternteil einen Jugendbeitrag
     (210 €)**, greift die Inklusion **nicht**:
     **210 € + 50 € = 260 €**.

---

## 1. Begriffe

| Begriff | Definition |
|---|---|
| **Haushalt** | Alle Mitglieder mit derselben Haushaltskennung. Genau ein Mitglied ist **Rechnungsträger** (Träger), es trägt die gesamte Summe. |
| **Spieler** | Status `J` **und** gültiger Spielerpass **und** gültiges Medico. Nur dann entsteht ein Spielertarif. |
| **Offizieller** | Person mit mindestens einer Offiziellen-Lizenz: `Off` (Officiële), `ZS` (secretariaat / chrono), `SR` (arbitre). |
| **Comité-Mitglied** | Person mit Eintrag im Comité **und** einer aktiven Offiziellen-Lizenz. |
| **Zahlender Offizieller** | Offizieller, der **für 50 € mit Stimmrecht** optiert hat. |
| **Jugendbeitrag** | Tarif für Spieler unter 25 bzw. in einer Jugendkategorie = **210 €**. |
| **Familienbeitrag** | 384 €, erreicht mit ≥ 2 Spielern im Haushalt oder mit 1 SEN + 1 U25. |

---

## 2. Eingangsdaten je Mitglied

| Feld | Quelle | Werte |
|---|---|---|
| `haus_id` | Haushaltscode | Kennung |
| `geboren` | Geburtsdatum | Datum, `///`, leer |
| `ist_spieler` | Status + Pass + Medico | ja / nein |
| `ist_offiziell` | Offizielle-Lizenz(en) | ja / nein |
| `ist_comite` | Comité-Eintrag | ja / nein |
| `opt_stimmrecht` | **NEUES Feld**, siehe § 8 | ja / nein |
| `ist_traeger` | automatisch bestimmt | ja / nein |

> `opt_stimmrecht` ist das **einzige neue Eingabefeld**, das Regel 3
> überhaupt erst abbildbar macht. Ohne dieses Feld gibt es keine Wahlfreiheit,
> sondern nur eine automatische 50 €.


---

## 3. Schritt 1 – Haushaltstarif

```
SPIELER   = { m ∈ Haushalt : m.ist_spieler }
n         = |SPIELER|
hat_SEN   = ∃ m ∈ SPIELER : Kategorie(m) = SEN
hat_U25   = ∃ m ∈ SPIELER : Kategorie(m) = U25 oder Jugend

TARIF =
    384 €   wenn  n ≥ 2  oder  (hat_SEN und hat_U25)
    300 €   wenn  n = 1 und hat_SEN
    210 €   wenn  n = 1 und hat_U25
      0 €   wenn  n = 0
```

**Regel 1 (Obergrenze)** ist damit strukturell erfüllt: `TARIF ≤ 384` per
Konstruktion. Es gibt keinen Pfad zu einem Wert über 384 €.

---

## 4. Schritt 2 – Zuschlag 50 €

Der Zuschlag ist **ein Betrag pro Haushalt** und hängt am **Rechnungsträger**,
nicht an beliebigen Mitgliedern.

```
T = der Rechnungstraeger des Haushalts

ZUSCHLAG =
    0 €    wenn  TARIF = 384                             ← Regel 5, Inklusion
    0 €    wenn  TARIF = 300                             ← Regel 5, Inklusion
    0 €    wenn  TARIF = 210 und T.ist_spieler = ja      ← Regel 2
    50 €   wenn  T.ist_comite = ja                       ← Regel 4, Pflicht
    50 €   wenn  T.opt_stimmrecht = ja                   ← Regel 3, freiwillig
      0 €   sonst
```

> ⚠️ **Nur der Rechnungsträger löst den Zuschlag aus.** Ein Offizieller,
> der selbst **nicht** Rechnungsträger ist, erzeugt **keine eigene
> Rechnung** – sonst bekäme ein Haushalt zwei Posten. Genau das passiert
> heute bei `F0026`: CLEMENT `(0+50)` und METZLER `50`, zusammen 100 € für
> **einen** Haushalt.

> 💡 **Es gibt keinen Pfad zu 350 €.** Im Erwachsenen- und im Maximaltarif
> sind die 50 € **inkludiert** – Beschluss vom 29.09.2026, Referenz
> **VAN DER WEKEN Louis** (Spielerpass und Zeitnehmer-Lizenz): Ergebnis
> **300 €**, nicht 300 + 50. Additiv werden die 50 € nur, wenn der
> Rechnungsträger **selbst kein Spieler ist** und den Haushalt allein mit
> einem **Jugendbeitrag von 210 €** vertritt: **210 + 50 = 260 €**.

**Die Reihenfolge ist zwingend:** Die beiden Inklusionsprüfungen stehen
**vor** der Zuschlagprüfung. Ohne sie ergäbe ein Comité-Haushalt
384 + 50 = 434 € und würde Regel 1 verletzen.

---

## 5. Schritt 3 – Betrag des Rechnungsträgers

```
T = das Mitglied des Haushalts mit  ist_traeger = ja

GESAMT = TARIF + ZUSCHLAG
```

Daraus folgt automatisch:

| Fall | Rechnung | Ergebnis |
|---|---|---|
| Träger ist Spieler, Haushalt mit 2 Spielern | 384 + 0 | **384** |
| **Spieler SEN allein** (auch mit Offiziellen-Funktion) | 300 + 0 | **300** |
| **Spieler U25 allein** (auch mit Offiziellen-Funktion) | 210 + 0 | **210** |
| **Spieler und Offizieller** (Doppelrolle) | kein Zuschlag | **210 / 300** |
| Senior-Spieler, Träger ist ein **Nichtspieler im Comité** | 300 + 0 | **300** |
| Nicht-Spieler, Offizieller **mit** Stimmrecht, 210er-Tarif | 210 + 50 | **260** |
| **Comité-Mitglied als Elternteil, Jugendbeitrag** | 210 + 50 | **260** |
| Comité-Mitglied, kein Tarif im Haushalt | 0 + 50 | **50** |
| Offizieller **ohne** Stimmrecht | 0 + 0 | **0** |
| Offizieller, aber **nicht** Rechnungsträger | — | **kein eigener Posten** |

---

## 6. Warum Regel 2 automatisch aus Schritt 2 folgt

Ein **Spieler** wird nie in `FREIWILLIG` aufgenommen. Die Bedingung
`¬m.ist_spieler` sorgt dafür, dass die Doppelrolle **nicht** addiert wird.
Der Spieler behält 210 € oder 300 €, und ab zwei Spielern gilt ohnehin der
Höchstbetrag 384 €.

> **Wichtig:** Regel 2 gilt nur, solange `ist_spieler` **wahr** ist. Ein
> Mitglied mit Spielerlizenz, aber Status `N` oder `R`, ist nach der
> Spielberechtigkeitsregel **kein Spieler** und fällt in die Offiziellenlogik.

---

## 7. Vollständige Pseudocode-Implementierung

```python
def beitrag(haushalt):
    spieler = [m for m in haushalt if m.ist_spieler]
    n       = len(spieler)
    hat_sen = any(m.kategorie == "SEN" for m in spieler)
    hat_u25 = any(m.kategorie in ("U25", "JUGEND") for m in spieler)
    t       = next(m for m in haushalt if m.ist_traeger)

    # Schritt 1 - Haushaltstarif
    if n >= 2 or (hat_sen and hat_u25):
        tarif = 384
    elif n == 1 and hat_sen:
        tarif = 300
    elif n == 1 and hat_u25:
        tarif = 210
    else:
        tarif = 0

    # Schritt 2 - Zuschlag. Haengt am RECHNUNGSTRAEGER, nicht am Haushalt.
    if tarif in (300, 384):                       # Regel 5: Inklusion
        zuschlag = 0
    elif tarif == 210 and t.ist_spieler:          # Regel 2: Spieler
        zuschlag = 0
    elif t.ist_comite:                            # Regel 4: Pflicht
        zuschlag = 50
    elif t.opt_stimmrecht:                        # Regel 3: freiwillig
        zuschlag = 50
    else:
        zuschlag = 0

    # Schritt 3 - Gesamtbetrag des Rechnungstraegers
    return min(tarif + zuschlag, 384)      # Regel 1 als Schutzschranke
```

`min(..., 384)` ist nach dem Beschluss vom 29.09.2026 **doppelt redundant**:
Im 300er- und im 384er-Fall wird nicht addiert, und die einzige Addition
(210 + 50) ergibt 260. Das rechnerische Maximum der Spezifikation ist
**384 €**. Die Schranke bleibt trotzdem eingebaut – sie garantiert Regel 1,
auch wenn später ein Tarif dazukommt.

---

## 8. Datenfeld für die Wahlfreiheit

Für Regel 3 braucht es ein Feld, das heute **nicht existiert**.

| | |
|---|---|
| **Vorschlag** | neue Spalte **`CN` `Stimmrecht (50/0)`**, direkt rechts von `CL` |
| **Werte** | `50` = Offizieller mit Stimmrecht, `0` oder leer = ohne Stimmrecht |
| **Pflicht bei** | jeder Person mit Offiziellen-Lizenz |
| **Nicht bei** | Spielern – die zahlen nach Regel 2 nie einen Zuschlag |

Ohne dieses Feld müsste Regel 3 als „50 €, sobald eine Offiziellen-Lizenz
vorhanden ist“ ausgelegt werden. Das wäre **nicht dieselbe Regel**, weil
dann niemand auf 0 € stellen kann.


---

## 9. Testfälle (Soll-Werte zum Nachrechnen)

| # | Haushalt | Erwartet | Regel |
|---|---|---|---|
| T1 | 1 Spieler SEN, sonst nichts | **300** | 1 |
| T2 | 1 Spieler U25, sonst nichts | **210** | 1 |
| T3 | 2 Spieler (U25 + U25) | **384** | 1 |
| T4 | 1 SEN + 1 U25 | **384** | 1 |
| T5 | 1 U25-Spieler, Elternteil Offizieller **mit** Stimmrecht | **260** | 3, 5 |
| T6 | 1 U25-Spieler, Elternteil Offizieller **ohne** Stimmrecht | **210** | 3 |
| T7 | 1 U25-Spieler, Elternteil im **Comité** | **260** | 4, 5 |
| T8 | 1 U25-Spieler, Elternteil im **Comité**, 2. Spieler im Haus | **384** | 5 Inklusion |
| T9 | U25-Spieler **und** Offizieller (Doppelrolle) | **210** | 2 – keine Addition |
| T10 | 2 Spieler, einer davon Offizieller im Comité | **384** | 2 + 5 |
| T11 | Offizieller mit Stimmrecht, kein Spieler im Haus | **50** | 3 |
| T12 | Offizieller ohne Stimmrecht, kein Spieler im Haus | **0** | 3 |
| T13 | Comité-Mitglied, kein Spieler im Haus | **50** | 4 |
| T14 | 2 Offizielle mit Stimmrecht, kein Spieler | **50** | 3 – nur einmal |
| T15 | Spieler SEN + Offizieller mit Stimmrecht | **300** | 2 – keine Addition |
| T16 | Spieler SEN, Träger ist ein **Nichtspieler im Comité** | **300** | 5 Inklusion, **kein 350** |
| T17 | Spieler SEN, Träger Nichtspieler mit Stimmrecht | **300** | 5 Inklusion |
| T18 | U25-Spieler, Elternteil im Comité | **260** | 5 **ohne** Inklusion |
| T19 | Spieler SEN als Träger, **anderes** Mitglied im Comité | **300** | 2 – der Träger entscheidet |

> **T8 und T10** sichern die Inklusion im 384er-Fall ab (nicht 434 €).
> **T9, T15 und T19** sichern Regel 2 ab (Doppelrolle addiert nichts).
> **T16 und T17 sind die neuen Prüfsteine für den Beschluss vom 29.09.2026:**
> ein 300er-Haushalt wird **nie** zum 350er-Haushalt, egal wer Träger ist.
> **T18** ist das Gegenstück: dort wird sehr wohl addiert, weil der Träger
> selbst kein Spieler ist.

Die Testfälle sind als ausführbares Skript hinterlegt:
`python3 docs/cotisation/spec_pruefen.py` rechnet alle 19 durch und meldet
Abweichungen. **Stand: 19 von 19 bestanden.**

---

## 10. Abgleich mit der aktuellen Mappe

| Regel | Umsetzung heute | Bewertung |
|---|---|---|
| 1 – Obergrenze 384 |Tarif endet bei 384, kein Pfad darüber | **erfüllt** |
| 2 – Doppelrolle | Zuschlag nur bei `keine Spielerlizenz`; Spieler lösen ihn nicht aus | **erfüllt**, Grenze siehe E1 |
| 3 – **optional** 50/0 | 50 € wird **automatisch** ausgelöst, sobald eine Offiziellen-Lizenz existiert. **Keine Wahl möglich.** | **nicht erfüllt** |
| 4 – Comité minimum 50 | vorhanden, greift bei `(0+50)`, leer, `0` oder Fremdcode | **erfüllt** |
| 5 – 384 inkludiert 50 | Zuschlag entfällt bei `CE = 384` | **erfüllt** |
| 5 – 300 inkludiert 50 | **nicht umgesetzt** | **Fehlbestand** |
| 5 – 210 + 50 = 260 | umgesetzt, Fall SCHUSTER Jeff | **erfüllt** |
| nur **ein** Posten je Haushalt | **nicht eingehalten** | **Fehlbestand** |

### Zwei Fehlbestände, die aus diesem Beschluss folgen

**1. Ein 300er-Haushalt kann heute 350 € ergeben.** Zusätzlich zu einem
300er-Träger bekommt ein Comité-Mitglied auf einer **anderen** Zeile desselben
Haushalts eine eigene 50-€-Rechnung. Genau das beschreibt der Beschluss mit
VAN DER WEKEN Louis: die 50 € sind inkludiert und dürfen nicht zusätzlich
berechnet werden.

**2. Manche Haushalte bekommen mehr als eine Rechnung.** Gemessen in der
Live-Mappe:

| Haushalt | Posten | Summe | Wer |
|---|---|---|---|
| `F0026` | 2 | **100 €** | CLEMENT `(0+50)` + METZLER `50` |
| `XSEUL` | 61 | 9.800 € | Sammelcode, siehe unten |

Bei `XSEUL` handelt es sich **nicht** um einen Haushalt: 72 Mitglieder tragen
diesen Code, und das Modell gruppiert sie unter einem gemeinsamen Schlüssel.
Das ist kein Fehler der Beitragshöhe, sondern ein Fehler der
**Haushaltsbildung** – XSEUL ist laut eigener Regel *kein* Familiencode
(siehe Kapitel 11 der Anleitung) und darf nicht als eine gemeinsame
Rechnungseenheit behandelt werden.

**Fazit:** Die Beitragshöhen 1, 2, 4 und 5a sind korrekt. **Offen bleiben
Regel 3 (Wahlfreiheit), die Inklusion im 300er-Fall und die Ein-Posten-
Regel je Haushalt.**

---

## 11. Offene Entscheidungen

| Nr | Frage | Warum sie wichtig ist | Vorschlag |
|---|---|---|---|
| **E1** | Gilt Regel 2 auch für jemanden mit Spielerlizenz, aber Status `N` oder `R`? | Er ist formal kein Spieler. Heute bekommt er 50 €. | Regel 2 **nur** bei echtem Spielstatus `J`. So ist es heute. |
| **E2** | ~~350 € bei Comité-Träger mit 300-Tarif~~ | — | **ENTSCHIEDEN am 29.09.2026: es gibt kein 350 €.** Die 50 € sind im Erwachsenentarif inkludiert (Referenz VAN DER WEKEN Louis). |
| **E3** | Wird die Wahl 50/0 **pro Person** oder **pro Haushalt** getroffen? | Pro Person ist genauer, aber aufwendiger. | **Pro Person.** Mehrere Offizielle im Haus können unterschiedlich wählen. |
| **E4** | Gilt Regel 4 auch für ein Comité-Mitglied **ohne** Offiziellen-Lizenz? | Regel 4 sagt „aktive Offizielle im Comité“. | **Nein.** Ohne Lizenz kein Pflichtbeitrag. |
| **E5** | Zählen Jugendspieler in einer Jugendkategorie (U7 bis U17) als U25 für die 210 €? | Im Blatt liegen 14 Jugendspalten, die Alterskategorie K kennt nur `SEN` und `U25`. | **Ja**, Jugend = 210 €. Sonst hätten Jugend-Haushalte keinen Tarif. |
| **E6** | Was passiert bei XSEUL und GAJGL? | Beide Sondercodes berühren die Haushaltsbildung. | Unverändert lassen: GAJGL = 0 €, XSEUL nach Spielstatus. |
| **E7** | Bekommt ein Offizieller, der **nicht** Rechnungsträger ist, eine eigene Rechnung? | Heute ja. Das erzeugt zwei Posten je Haushalt (`F0026` = 100 €). | **Nein.** Nur der Rechnungsträger bekommt einen Posten. Die 50 € sind in seinem Betrag enthalten. |
| **E8** | Wie wird verhindert, dass 72 `XSEUL`-Mitglieder als eine Rechnungseenheit behandelt werden? | Der Sammelcode erzeugt heute 61 Posten in einem Schlüssel. | Jedes `XSEUL`-Mitglied bekommt einen **eigenen** Haushaltsschlüssel, z. B. `XS:<Card-ID>`. |

---

## 12. System-Prompt für eine automatisierte Berechnung

```text
Du berechnst den Mitgliedsbeitrag eines Haushalts nach den Regeln eines
luxemburgischen Sportvereins. Antworte ausschließlich mit der Struktur
"Ergebnis | Grund | Regelbezug".

SCHRITT 1 – HAUSHALTSTARIF
Zähle die Mitglieder, die gleichzeitig ALLE drei Bedingungen erfüllen:
  a) Status "J" (spielt),
  b) gültiger Spielerpass (XXX zählt NICHT als Lizenz),
  c) gültiges Medico (Gültigkeitsjahr >= aktuelles Jahr).
Diese heißen Spieler.
  - 2 oder mehr Spieler                      -> Tarif 384
  - 1 SEN und 1 Spieler U25 oder Jugend      -> Tarif 384
  - genau 1 Spieler, Kategorie SEN           -> Tarif 300
  - genau 1 Spieler, U25 oder Jugend         -> Tarif 210
  - kein Spieler                             -> Tarif 0
Der Tarif eines Haushalts übersteigt NIEMALS 384.

SCHRITT 2 – ZUSCHLAG 50
Der Zuschlag haengt am RECHNUNGSTRAEGER, nicht am ganzen Haushalt.
Bezeichne ihn mit T und pruefe IN DIESER REIHENFOLGE:
  a) Ist der Tarif 384? Dann Zuschlag 0.
  b) Ist der Tarif 300? Dann Zuschlag 0.
     (Die 50 fuer Comite und Offizielle sind im Erwachsenen- und im
      Maximalbeitrag BEREITS INKLUDIERT. Es gibt kein 350.)
  c) Ist der Tarif 210 und ist T selbst Spieler? Dann Zuschlag 0.
  d) Ist T im Comite? Dann Zuschlag 50 (Pflicht).
  e) Hat T auf Stimmrecht optiert (Feld Stimmrecht = 50)? Dann Zuschlag 50.
  f) Sonst Zuschlag 0.
Der Zuschlag wird nur EINMAL pro Haushalt berechnet, nicht pro Person.
Ein Offizieller, der NICHT Rechnungstraeger ist, bekommt KEINE eigene
Rechnung. Die 50 Euro stecken im Betrag des Rechnungstraegers.

SCHRITT 3 – GESAMTBETRAG
Der Gesamtbetrag ist Tarif + Zuschlag und wird auf den Rechnungstraeger
des Haushalts gebucht. Andere Mitglieder des Haushalts zahlen nichts
eigenes; sie zeigen nur den Haushaltscode.

WICHTIGE AUSNAHMEN:
- Wer Spieler UND Offizieller ist, zahlt NUR den Spielertarif.
  Es wird NICHTS addiert. Regel 2 geht vor.
- Ein Comite-Mitglied, das als Elternteil nur einen Jugendbeitrag von 210
  fuer seinen Sohn oder seine Tochter zahlt, bekommt den Comite-Beitrag
  ZUSAETZLICH: 210 + 50 = 260. Die Inklusion gilt nur beim 384er-Tarif.
- Offizielle-Lizenzen sind freiwillig. Ohne Opt-in auf Stimmrecht
  betragen sie 0, auch wenn sie eine Lizenz besitzen.
- Der Gesamtbetrag ist 0, wenn im Haushalt niemand spielberechtig ist und
  niemand auf Stimmrecht optiert hat.
```

> → offene Entscheidung **E1**, siehe § 9.
