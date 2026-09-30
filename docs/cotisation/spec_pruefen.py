"""Prueft die Spezifikation: Pseudocode gegen die 15 Testfaelle."""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))


class M:
    """Ein Mitglied mit den Feldern aus der Spezifikation."""

    def __init__(self, name, spieler=False, offiziell=False,
                 comite=False, stimmrecht=False, kat=None, traeger=False):
        self.name = name
        self.ist_spieler = spieler
        self.ist_offiziell = offiziell
        self.ist_comite = comite
        self.opt_stimmrecht = stimmrecht
        self.kategorie = kat or ("SEN" if spieler else "U25")
        self.ist_traeger = traeger


def beitrag(haushalt):
    """Pseudocode aus Abschnitt 7 der Spezifikation, woertlich uebernommen."""
    spieler = [m for m in haushalt if m.ist_spieler]
    n = len(spieler)
    hat_sen = any(m.kategorie == "SEN" for m in spieler)
    hat_u25 = any(m.kategorie in ("U25", "JUGEND") for m in spieler)
    traeger = next(m for m in haushalt if m.ist_traeger)

    if n >= 2 or (hat_sen and hat_u25):
        tarif = 384
    elif n == 1 and hat_sen:
        tarif = 300
    elif n == 1 and hat_u25:
        tarif = 210
    else:
        tarif = 0

    # Schritt 2 - Zuschlag, ein Betrag pro Haushalt.
    # Die 50 EUR sind im Erwachsenen- und im Maximaltarif INKLUDIERT.
    # Additiv werden sie nur, wenn der Traeger kein Spieler ist und den
    # Haushalt allein mit einem Jugendbeitrag von 210 vertritt.
    if tarif in (300, 384):
        zuschlag = 0
    elif tarif == 210 and traeger.ist_spieler:
        zuschlag = 0
    elif traeger.ist_comite or traeger.opt_stimmrecht:
        zuschlag = 50
    else:
        zuschlag = 0

    return min(tarif + zuschlag, 384), tarif, zuschlag


S = dict(spieler=True, kat="U25")
SEN = dict(spieler=True, kat="SEN")
JUG = dict(spieler=True, kat="JUGEND")

TESTS = [
    ("T1  1 Spieler SEN",                 [M("A", **SEN, traeger=True)],            300, 1),
    ("T2  1 Spieler U25",                 [M("A", **S, traeger=True)],             210, 1),
    ("T3  2 Spieler U25",                 [M("A", **S), M("B", **S, traeger=True)], 384, 1),
    ("T4  SEN + U25",                     [M("A", **SEN), M("B", **S, traeger=True)], 384, 1),
    ("T5  Eltern Offizieller +Stimmrecht", [M("Sohn", **S), M("Eltern", offiziell=True, stimmrecht=True, traeger=True)], 260, "3+5"),
    ("T6  Eltern Offizieller ohne",        [M("Sohn", **S), M("Eltern", offiziell=True, stimmrecht=False, traeger=True)], 210, 3),
    ("T7  Eltern im Comite",              [M("Sohn", **S), M("Eltern", offiziell=True, comite=True, traeger=True)], 260, "4+5"),
    ("T8  Comite + 2 Spieler",            [M("A", **S), M("B", **JUG), M("C", offiziell=True, comite=True, traeger=True)], 384, 5),
    ("T9  Spieler UND Offizieller",       [M("A", offiziell=True, stimmrecht=True, traeger=True, **S)], 210, 2),
    ("T10 2 Spieler, einer Comite",       [M("A", **S), M("B", offiziell=True, comite=True, traeger=True, **S)], 384, "2+5"),
    ("T11 Offizieller +Stimmrecht",       [M("A", offiziell=True, stimmrecht=True, traeger=True)], 50, 3),
    ("T12 Offizieller ohne Stimmrecht",   [M("A", offiziell=True, stimmrecht=False, traeger=True)], 0, 3),
    ("T13 Comite, kein Spieler",          [M("A", offiziell=True, comite=True, traeger=True)], 50, 4),
    ("T14 2 Offizielle +Stimmrecht",      [M("A", offiziell=True, stimmrecht=True, traeger=True), M("B", offiziell=True, stimmrecht=True)], 50, 3),
    ("T15 SEN + Offizieller",             [M("A", offiziell=True, stimmrecht=True, traeger=True, **SEN)], 300, 2),
    ("T16 300er, Traeger Nichtspieler Comite", [M("Sohn", **SEN), M("Opa", offiziell=True, comite=True, traeger=True)], 300, "5 Inklusion"),
    ("T17 300er, Traeger Nichtsp. +Stimmrecht", [M("Tochter", **SEN), M("Eltern", offiziell=True, stimmrecht=True, traeger=True)], 300, "5 Inklusion"),
    ("T18 210er + Comite-Elternteil",      [M("Sohn", **S), M("Eltern", offiziell=True, comite=True, traeger=True)], 260, "5 ohne Inklusion"),
    ("T19 300er, Comite ANDERES Mitglied", [M("A", **SEN, traeger=True), M("B", offiziell=True, comite=True)], 300, 2),
]

print(f"{'Testfall':<36}{'soll':>6}{'ist':>6}{'Tarif':>7}{'Zuschl':>8}  ok")
print("-" * 80)
fehler = 0
for name, haus, soll, regel in TESTS:
    ist, tarif, zus = beitrag(haus)
    ok = ist == soll
    fehler += not ok
    print(f"{name:<36}{soll:>6}{ist:>6}{tarif:>7}{zus:>8}  "
          f"{'ok' if ok else 'FEHLER'}  (Regel {regel})")

print("-" * 80)
print(f"Testfaelle: {len(TESTS)} | Fehler: {fehler}")
print("ERGEBNIS:", "alle Testfaelle bestanden" if not fehler
      else "SPEZIFIKATION IST FEHLERHAFT")
