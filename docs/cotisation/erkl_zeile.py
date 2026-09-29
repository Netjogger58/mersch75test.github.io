"""Zeigt fuer konkrete Namen den kompletten Rechenweg."""
import sys

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")
import pruef_cotisation as pr
import baut_arbeitsmappe as ba
import zipfile

SUCHBEGRIFFE = [s.upper() for s in (sys.argv[1:] or ["BRÜCK", "BÜCHLER", "BRUCK"])]

teile = {}
with zipfile.ZipFile(ba.QUELLE) as z:
    for n in z.namelist():
        teile[n] = z.read(n)
blatt = ba.finde_blatt(teile, ba.BLATT)
zeilen = ba.liese_blatt(teile, blatt)
werte = ba.rechne_werte(teile, blatt)

kopf = [c.strip() for c in zeilen[0]]


def idx(name):
    # akzeptiert entweder den Schlüssel aus SPALTEN oder den rohen Kopfnamen
    if name in pr.SPALTEN:
        name = pr.SPALTEN[name]
    if name in kopf:
        return kopf.index(name)
    for alt in pr.SPALTEN_ALT.get(name, ()):
        if alt in kopf:
            return kopf.index(alt)
    return -1


def z(r, name):
    i = idx(name)
    return zeilen[r - 1][i].strip() if 0 <= i < len(zeilen[r - 1]) else ""


treffer = [r for r in range(pr.ERSTE_DATENZEILE, len(zeilen))
           if any(s in z(r, "nom").upper() for s in SUCHBEGRIFFE)]

if not treffer:
    # Unschweife Suche: Sonderzeichen ignorieren (BRÜCK vs BRUCK) und
    # ggf. verstelte Zeilennummern aus der Kommandozeile annehmen.
    import unicodedata

    def roh(s):
        s = unicodedata.normalize("NFKD", s.upper())
        return "".join(c for c in s if not unicodedata.combining(c))

    wunsch = [roh(s) for s in SUCHBEGRIFFE]
    numerisch = [int(a) for a in sys.argv[1:] if a.isdigit()]
    treffer = [r for r in range(pr.ERSTE_DATENZEILE, len(zeilen))
               if any(s in roh(z(r, "nom")) or s in roh(z(r, "vorname")) for s in wunsch)
               or r in numerisch]
    print("Erweiterte Suche:", ", ".join(wunsch), "->", len(treffer), "Treffer",
          (f"(Zeilen {numerisch})" if numerisch else ""))

# Zugehoerige Familien
familien = {z(r, "fam") for r in treffer if z(r, "fam")}
alle = sorted({r for r in range(pr.ERSTE_DATENZEILE, len(zeilen))
               if z(r, "fam") in familien})

print("Gesucht:", ", ".join(SUCHBEGRIFFE))
print("Familien:", ", ".join(sorted(familien)), "| zugehoerige Zeilen:", len(alle))
print()
for f in sorted(familien):
    g = [r for r in alle if z(r, "fam") == f]
    print("=" * 118)
    print(f"FAMILIE {f}   ({len(g)} Personen)")
    print("=" * 118)
    print("%-5s %-11s %-10s %-4s %-3s %-10s %-10s %-8s %-8s %-16s"
          % ("Zeile", "Nom", "Prénom", "K", "L", "Geburt", "Spielerliz", "Offiz", "ZS/SR", "Ausgabe M"))
    print("-" * 118)
    for r in sorted(g):
        print("%-5d %-11s %-10s %-4s %-3s %-10s %-10s %-8s %-8s %-16r"
              % (r, z(r, "nom")[:11], z(r, "vorname")[:10], z(r, "kategorie")[:4],
                 z(r, "spielt")[:3], z(r, "naissance")[:10],
                 (z(r, "liz_sp") or "-")[:10], (z(r, "liz_off") or "-")[:8],
                 (z(r, "liz_sr") or "-")[:8], werte.get(r, "")))
    spieler = [r for r in sorted(g) if z(r, "spielt") == "J" and z(r, "liz_sp")]
    liz_sen = [r for r in spieler if z(r, "kategorie") == "SEN"]
    liz_u25 = [r for r in spieler if z(r, "kategorie") == "U25"]
    print("-" * 118)
    print("  Spieler mit Lizenz : %s" % ([f"{r} {z(r,'vorname')}" for r in spieler] or "KEINE"))
    print("    davon SEN/U25    : %d / %d" % (len(liz_sen), len(liz_u25)))
    if len(spieler) >= 2 or (liz_sen and liz_u25):
        tarif = 384
    elif liz_sen:
        tarif = 300
    elif liz_u25:
        tarif = 210
    else:
        tarif = 0
    print("  daraus Tarif (BY)  : %s" % tarif)
    for r in sorted(g):
        ergebnis = werte.get(r, "")
        if ergebnis:
            print("  Zeile %-5d -> %r" % (r, ergebnis))
    print()
