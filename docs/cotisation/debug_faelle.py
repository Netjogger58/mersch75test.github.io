import sys

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")
import pruef_cotisation as pr
import baut_arbeitsmappe as ba
import zipfile

teile = {}
with zipfile.ZipFile(ba.QUELLE) as z:
    for n in z.namelist():
        teile[n] = z.read(n)
zeilen = ba.liese_blatt(teile, ba.finde_blatt(teile, ba.BLATT))
kopf = [c.strip() for c in zeilen[0]]


def z(r, name):
    i = kopf.index(name) if name in kopf else -1
    for alt in pr.SPALTEN_ALT.get(name, ()):
        if i < 0 and alt in kopf:
            i = kopf.index(alt)
    return zeilen[r - 1][i].strip() if 0 <= i < len(zeilen[r - 1]) else f"<Spalte fehlt:{name}>"


print("=== BOURG Zeile 18 (Ausnahme) ===")
print("  Nom       :", repr(z(18, "Nom(s)")))
print("  Vorname   :", repr(z(18, "Prénom(s)")))
print("  suche     :", pr.normalisiere_adresse("x") and
      ("BOURG", "JEANNOT") in {(n.strip().upper(), p.strip().upper())
                              for n, p, _ in ba.liese_config(ba.CONFIG / "ausnahmen-cotisation.csv")[1:]})
print("  Datei     :", [(n, p, a) for n, p, a in
                       ba.liese_config(ba.CONFIG / "ausnahmen-cotisation.csv")])

print()
print("=== ANSAY Zeile 534/535 (Haushalt) ===")
for r in (534, 535):
    print("  Z%-4d %-10s %-9s fam=%-7s L=%-2s K=%-4s AH=%-7s AI=%-6s"
          % (r, z(r, "Nom(s)"), z(r, "Prénom(s)"), z(r, "Code Courrier neu"),
             z(r, "Spieler J/R/N"), z(r, "Alterskategorie"),
             z(r, "Pass Nummer (Licences Joueurs / Joueuses)"),
             z(r, "Licences Off (officiels)")))
    print("        Adresse=%r  normalisiert=%r"
          % (z(r, "Adresse"), pr.normalisiere_adresse(z(r, "Adresse"))))

print()
print("  Haushalt-Datei:", [(n, b[:40]) for n, p, b in
                            ba.liese_config(ba.CONFIG / "haushalte-cotisation.csv")])
print("  normalisiert  :", [pr.normalisiere_adresse(n)
                            for n, p, b in ba.liese_config(ba.CONFIG / "haushalte-cotisation.csv")[1:]])

print()
print("=== Zeile 607 (Phantomzeile) ===")
print("  Nom=%r  fam=%r  L=%r  P=%r" % (z(607, "Nom(s)"), z(607, "Code Courrier neu"),
                                        z(607, "Spieler J/R/N"), z(607, "Code Courrier neu")))
