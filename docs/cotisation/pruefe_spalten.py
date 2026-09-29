"""Vergleicht Spalten und Zellinhalte von Quelldatei und gebauter Datei.

Beantwortet die Frage: wurde eine Spalte entfernt oder ein Inhalt verloren?
"""
import collections
import re
import sys
import zipfile

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")

Q = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "TEST1_nur-calcchain.xlsm")
Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")


def ci(name):
    n = 0
    for c in name:
        n = n * 26 + ord(c) - 64
    return n


def lst(sp):
    s = ""
    while sp:
        sp, r = divmod(sp - 1, 26)
        s = chr(65 + r) + s
    return s


def lade(pfad):
    z = zipfile.ZipFile(pfad)
    ss = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", s, re.S))
          for s in re.findall(r"<si>(.*?)</si>",
                             z.read("xl/sharedStrings.xml").decode("utf-8"), re.S)]
    d = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
    kopf, daten = {}, collections.defaultdict(dict)
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', d, re.S):
        r = int(m.group(1))
        for c in re.finditer(r'<c r="([A-Z]+)\d+"[^>]*?(?:/>|>(.*?)</c>)', m.group(2), re.S):
            sp, inh = c.group(1), c.group(2) or ""
            v = re.search(r"<v>(.*?)</v>", inh, re.S)
            if not v:
                continue
            roh = v.group(1)
            wert = ss[int(roh)] if 't="s"' in c.group(0) else roh
            if r == 1:
                kopf[sp] = wert
            else:
                daten[r][sp] = wert
    return kopf, daten


ka, da = lade(Q)
kb, db = lade(Z)

print("Spalten in deiner Datei :", len(ka), "->", sorted(ka, key=ci)[:3], "...",
      sorted(ka, key=ci)[-3:])
print("Spalten in der neuen   :", len(kb))
fehlend = sorted(set(ka) - set(kb), key=ci)
print("FEHLENDE Spalten        :", fehlend or "keine")
hinzu = sorted(set(kb) - set(ka), key=ci)
print("NEUE Spalten            :", ", ".join(f"{s}={kb[s]}" for s in hinzu))

# Inhalte: alle Zellen der Quelle, die keine Formel in M ist
verloren = 0
geaendert = []
for r, zellen in da.items():
    for sp, wert in zellen.items():
        if sp == "M":
            continue                      # wird absichtlich neu berechnet
        if db.get(r, {}).get(sp) != wert:
            verloren += 1
            if len(geaendert) < 8:
                geaendert.append((r, sp, wert, db.get(r, {}).get(sp)))
print()
print("Zellen der Quelle ohne Wert mehr in der neuen Datei:", verloren)
for g in geaendert:
    print("   Zeile %-5s %-3s  war=%-22r neu=%r" % g)

# M: alt vs neu
alt_m = sum(1 for r in da if da[r].get("M"))
neu_m = sum(1 for r in db if db[r].get("M"))
print()
print("Spalte M: Quelle %d Werte, neue Datei %d Werte" % (alt_m, neu_m))
