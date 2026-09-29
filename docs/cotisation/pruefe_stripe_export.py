"""Prueft die Rechnungslogik des Blatts Stripe_Export gegen das Python-Modell.

FRAGE: Warum stehen so wenige XSEUL-Zeilen im Stripe-Export?
      Jede Zeile mit echtem Betrag sollte genau eine Rechnung ergeben.

Zwei Tore, die im Blatt wirken:
  ALT  Spalte A zeigt eine Zeile nur, wenn BW="TRAEGER" (Rechnungstraeger des
       Haushalts). EIN Traeger je BP-Gruppe -> alle 74 XSEUL-Zeilen teilen sich
       BP="XSEUL" und damit EINEN Traeger -> 1 Rechnung statt 73.
  NEU  zusaetzlich rechnungsfaehig, wer einen ZEILEN-EIGENEN Betrag hat
       (BX manuell, CB Personenwert/Ausnahme, CD XSEULwert). Das entspricht
       der Modelllogik in pruef_cotisation.berechne().

Aufruf:  python3 docs/cotisation/pruefe_stripe_export.py
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe  # noqa: E402

import pruef_cotisation as pr  # noqa: E402
import baut_arbeitsmappe as ba   # noqa: E402
import build_perfect_workbook as bp  # noqa: E402


def lade_modell():
    cfg = lambda n: pr.liese_config(bp.CONFIG / n)  # noqa: E731
    tarife = pr.lade_tarife(bp.CONFIG / "tarife-cotisation.csv")
    ausnahmen = {(n.strip().upper(), p.strip().upper()): a.strip()
                 for n, p, a in cfg("ausnahmen-cotisation.csv")}
    haushalte = {pr.normalisiere_adresse(a.strip())
                 for a, _b, *_r in ((r + ["", ""])[:3] for r in cfg("haushalte-cotisation.csv"))
                 if a.strip()}
    import zipfile
    with zipfile.ZipFile(mappe.datenquelle()) as z:
        teile = {n: z.read(n) for n in z.namelist()}
    zeilen = ba.liese_blatt(teile, "xl/worksheets/sheet1.xml")
    return pr.berechne(zeilen, ausnahmen, *tarife, haushalte), cfg


def echter_betrag(v) -> bool:
    """L-Wert, der eine Rechnung ausloest - kein Code, kein Leerwert."""
    v = (v or "").strip()
    if not v or v == "XSEUL" or v.startswith("F"):
        return False
    # "0" heisst ausdruecklich "zahlt nichts". Das trifft auf die 64 Personen
    # mit Status X zu (Spalte O): sie sollen NICHT in Stripe auftauchen.
    # Keine davon ist Rechnungstraeger - die Haushaltsrechnung steht auf einer
    # anderen Zeile und bleibt unberuehrt. Ohne diese Zeile wuerde der Export
    # 64 leere 0-EUR-Posten anlegen; Stripe nimmt zu 0 EUR ohnehin keine
    # Payment Links an.
    if v == "0":
        return False
    return v[0].isdigit() or v.startswith("(")


# Gruende aus pruef_cotisation.berechne(), die einen ZEILEN-EIGENEN Betrag
# ergeben. Genau diese Faelle sind im Excel an BX (manuell), CB (Personenwert)
# und CD (XSEULwert) erkennbar - das ist die Entsprechung zum neuen Tor.
EIGENER_BETRAG = (
    "manuelle Vorgabe",
    "namentliche Ausnahme",
    "Spieler mit Status R",
    "Spieler mit Lizenz und offener Frage",
    "Sondercode XSEUL",
)


def betrag_zahl(v):
    """Entspricht der Parser-Formel in Spalte C (siehe test_betrag_parse.py)."""
    s = str(v or "").strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        pass
    if s[0] == "(":
        k, e = s.find("+"), s.find(")")
        if k == -1 or e == -1:
            return None
        try:
            return float(s[k + 1:e])
        except ValueError:
            return None
    k = s.find("(")
    if k == -1:
        return None
    # NUR die Zahl vor "(" - der Zusatz in "210 (+0+50)" wird NICHT addiert.
    # Am 2026-09-27 war kurz der Versuch, ihn zu addieren (6 Posten, 300 EUR);
    # zurueckgenommen, weil die Ausnahme ausdruecklich nur SCHUSTER Jeff gilt
    # und nicht den weiteren Mitgliedern.
    try:
        return float(s[:k])
    except ValueError:
        return None


def main() -> int:
    ergebnis, _cfg = lade_modell()

    soll = [x for x in ergebnis
            if echter_betrag(x["neu"]) and x["fam"] != "GAJGL"]
    alt = [x for x in soll if x["ist_traeger"]]
    neu = [x for x in soll if x["ist_traeger"] or x["grund"] in EIGENER_BETRAG]
    fehlend = [x for x in soll if x not in alt]

    print(f"Zeilen mit echtem Betrag (ohne GAJGL) : {len(soll)}")
    print(f"  ALT  Spalte A nur bei BW=TRAEGER      : {len(alt)}")
    print(f"  NEU  + zeilen-eigener Betrag (BX/CB/CD): {len(neu)}")
    print(f"  fehlende Rechnungen ALT               : {len(fehlend)}")
    fam: dict[str, int] = {}
    for x in fehlend:
        fam[x["fam"]] = fam.get(x["fam"], 0) + 1
    print("  davon je Haushaltscode:", dict(sorted(fam.items(), key=lambda kv: -kv[1])[:8]))

    # Betragsabdeckung in Spalte C
    mit_c = [x for x in soll if betrag_zahl(x["neu"]) is not None]
    ohne_c = [x for x in soll if betrag_zahl(x["neu"]) is None]
    summe = sum(betrag_zahl(x["neu"]) for x in mit_c)
    print()
    print(f"Spalte C mit Zahl (Stripe kann buchen)  : {len(mit_c)}/{len(soll)}"
          f"  Summe {summe:,.0f} EUR".replace(",", "."))
    print(f"Spalte C leer (manuell noetig)          : {len(ohne_c)}")
    for x in ohne_c[:6]:
        print(f"   Z{x['excel_zeile']:<4} {x['nom'][:16]:<16} L={x['neu']!r}")

    print()
    print("Beispiele (fehlen im Export, obwohl Betrag vorhanden):")
    for x in fehlend[:8]:
        print(f"   Z{x['excel_zeile']:<4} {x['nom'][:18]:<18} {x['vorname'][:14]:<14} "
              f"Code={x['fam'][:8]:<8} L={x['neu']:<10} {x['grund'][:34]}")
    print()
    ok = len(fehlend) == 0
    print("ERGEBNIS:", "ok - jede Zeile mit Betrag wird exportiert" if ok
          else f"{len(fehlend)} Zeilen fallen durch das TRAEGER-Tor")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
