"""Zeilenweiser Token-Vergleich einer Zeile: Quelle gegen gebaute Datei."""
import difflib
import re
import sys
import zipfile

Q = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "TEST1_nur-calcchain.xlsm")
Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
ZEILE = int(sys.argv[1]) if len(sys.argv) > 1 else 2


def teil(pfad):
    z = zipfile.ZipFile(pfad)
    return z.read("xl/worksheets/sheet1.xml").decode("utf-8"), z


def zeile(xml, n):
    m = re.search(r'<row r="%d"[^>]*>.*?</row>' % n, xml, re.S)
    return m.group(0) if m else ""


a, za = teil(Q)
b, zb = teil(Z)
za_l, zb_l = zeile(a, ZEILE), zeile(b, ZEILE)

# in Zellen zerlegen
za_z = re.findall(r'<c r="[A-Z]+\d+"[^>]*?(?:/>|>.*?</c>)', za_l, re.S)
zb_z = re.findall(r'<c r="[A-Z]+\d+"[^>]*?(?:/>|>.*?</c>)', zb_l, re.S)
print("Zeile %d: Quelle %d Zellen, neu %d Zellen" % (ZEILE, len(za_z), len(zb_z)))

verglichen = 0
unterschiede = []
for zelle in za_z:
    if zelle in zb_z:
        verglichen += 1
    else:
        unterschiede.append(zelle)

print("identische Zellen:", verglichen)
print("UNTERSCHIEDLICHE Originalzellen:", len(unterschiede))
for u in unterschiede:
    print("  -", u[:150])

print()
print("NEUE Zellen (nur in der gebauten Datei):")
neu = [z for z in zb_z if z not in za_z]
for z in neu:
    print("  +", z[:170])
