"""Was passiert, wenn in Spalte O (Spieler J/R/N) ein X steht?

Der Spielerstatus entscheidet ueber den Tarif:
  J = Spieler mit Lizenz -> zahlt (300/210/384 je nach Haushalt)
  R = Reserve            -> (0+50)
  N = spielt nicht       -> kein eigener Tarif
  X = undefiniert        -> in KEINER Abfrage genannt -> Person faellt komplett raus

Das Skript rechnet beide Faelle durch und vergleicht mit dem Ist-Zustand,
sowohl fuer die betroffene Zeile als auch fuer den ganzen Haushalt.

Aufruf:  python3 docs/cotisation/test_spielt_x.py
"""
import collections
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import pruef_cotisation as pr          # noqa: E402
import pruefe_stripe_export as pse     # noqa: E402

ERSTE = pr.ERSTE_DATENZEILE


def kennzahlen(ergebnis):
    rechnungen = [x for x in ergebnis
                  if pse.echter_betrag(x["neu"]) and x["fam"] != "GAJGL"]
    return {
        "rechnungen": len(rechnungen),
        "summe": sum(int(v) for v in
                     (str(x["neu"]).split(" (+")[0] for x in rechnungen)
                     if v.isdigit()),
        "zeilen_mit_betrag": sum(1 for x in ergebnis if x["neu"]),
    }


def main() -> int:
    zeilen, _ = pse.lade_modell.__wrapped__() if False else (None, None)  # noqa
    # Rohdaten holen (identisch zum Build)
    import zipfile
    import build_perfect_workbook as bp
    import baut_arbeitsmappe as ba
    cfg = lambda n: pr.liese_config(bp.CONFIG / n)  # noqa: E731
    tarife = pr.lade_tarife(bp.CONFIG / "tarife-cotisation.csv")
    ausnahmen = {(n.strip().upper(), p.strip().upper()): a.strip()
                 for n, p, a in cfg("ausnahmen-cotisation.csv")}
    haushalte = {pr.normalisiere_adresse(a.strip())
                 for a, _b, *_r in ((r + ["", ""])[:3] for r in cfg("haushalte-cotisation.csv"))
                 if a.strip()}
    with zipfile.ZipFile(bp.QUELLE) as z:
        teile = {n: z.read(n) for n in z.namelist()}
    roh = [list(r) for r in ba.liese_blatt(teile, "xl/worksheets/sheet1.xml")]
    kopf = roh[0]
    i_spielt = next(i for i, h in enumerate(kopf)
                    if h.strip() in ("Spieler J/R/N", "Spielen J/R/N"))
    i_liz = next(i for i, h in enumerate(kopf)
                 if h.strip() == "Pass Nummer (Licences Joueurs / Joueuses)")
    i_nom = 1
    print(f"Spalte O = Index {i_spielt} ({kopf[i_spielt]!r}), "
          f"Lizenzspalte = Index {i_liz}\n")

    basis = pr.berechne(roh, ausnahmen, *tarife, haushalte)
    kb = kennzahlen(basis)
    print("IST (ohne X):")
    print(f"   Rechnungen: {kb['rechnungen']}   Summe: {kb['summe']} EUR\n")

    # Kandidaten: Zeilen mit J UND Lizenz (echte Spieler)
    kandidaten = [x for x in basis
                  if x["neu"] not in ("",) and roh[x["excel_zeile"] - 1][i_spielt].strip() == "J"
                  and roh[x["excel_zeile"] - 1][i_liz].strip()
                  and not str(roh[x["excel_zeile"] - 1][i_liz]).startswith("///")]

    print(f"{'Zeile':<6}{'Name':<24}{'Code':<8}{'L jetzt':<11}"
          f"{'L mit X':<11}{'Rechnung':<10}Haushalt-Effekt")
    print("-" * 108)
    betroffen_haus = collections.Counter()
    summe_delta = 0
    for x in kandidaten[:220]:
        r = x["excel_zeile"] - 1
        if r >= len(roh):
            continue
        test = [list(z) for z in roh]
        test[r][i_spielt] = "X"
        neu = pr.berechne(test, ausnahmen, *tarife, haushalte)
        y = next(z for z in neu if z["excel_zeile"] == x["excel_zeile"])
        kn = kennzahlen(neu)
        # betrifft die Aenderung einen ganzen Haushalt (gleicher Code)?
        haus = [z for z in neu if z["fam"] == x["fam"] and z["fam"]]
        haus_alt = [z for z in basis if z["fam"] == x["fam"] and z["fam"]]
        anderes = [z for z in haus if z["excel_zeile"] != x["excel_zeile"]
                   and z["neu"] != next((w["neu"] for w in haus_alt
                                         if w["excel_zeile"] == z["excel_zeile"]), None)]
        if anderes:
            betroffen_haus[x["fam"]] += 1
        summe_delta += kn["summe"] - kb["summe"]
        if len(betroffen_haus) <= 6 and (len(sys.argv) > 1 or x["fam"].startswith("F")):
            print(f"{x['excel_zeile']:<6}"
                  f"{(x['nom'] + ' ' + x['vorname'])[:23]:<24}"
                  f"{x['fam'][:7]:<8}{str(x['neu'])[:10]:<11}"
                  f"{str(y['neu'])[:10]:<11}"
                  f"{'ja' if pse.echter_betrag(y['neu']) else 'NEIN':<10}"
                  f"{len(anderes)} weitere Zeile(n) im Haus betroffen"
                  + (f"  [{y['grund'][:30]}]" if y['grund'] != x['grund'] else ""))

    print()
    print(f"X gesetzt in EINER Zeile: Haushalte, in denen sich der Betrag einer")
    print(f"ANDEREN Zeile aendert: {len(betroffen_haus)} -> {dict(list(betroffen_haus.items())[:6])}")
    mittel = summe_delta / max(1, len(kandidaten))
    print(f"Summe aller Rechnungen aendert sich im Mittel um {mittel:+.0f} EUR pro X.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
