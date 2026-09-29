"""Vergleicht die in meinen Formeln benutzten Funktionen mit der Quelldatei.

Die Quelldatei wurde von Excel selbst geschrieben. Alles, was Excel dort
ohne _xlfn.-Praefix schreibt, ist im Format gueltig. Funktionen, die dort gar
nicht vorkommen, sind Kandidaten fuer einen Praefix-Bedarf.
"""
import collections
import re
import zipfile

QUELLE = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
          "TEST1_nur-calcchain.xlsm")
ZIEL = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
        "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")

FUNKTION = re.compile(r"([A-Za-z_][A-Za-z0-9_.]*)\s*\(")


def sammle(pfad, nur_blatt=None):
    z = zipfile.ZipFile(pfad)
    zaehler = collections.Counter()
    for n in z.namelist():
        if not n.startswith("xl/worksheets/") or not n.endswith(".xml"):
            continue
        if nur_blatt and nur_blatt not in n:
            continue
        d = z.read(n).decode("utf-8", "replace")
        for m in re.finditer(r"<f[^>]*>(.*?)</f>", d, re.S):
            for f in FUNKTION.finditer(m.group(1)):
                zaehler[f.group(1)] += 1
    return zaehler


q = sammle(QUELLE)
print("Funktionen in den Formeln der QUELLDATEI:")
for k, v in sorted(q.items()):
    print("   %-24s %d" % (k, v))
print()

meine = ["IF", "ISNUMBER", "IFERROR", "DATEVALUE", "ROW", "SUMPRODUCT", "MIN",
         "COUNTIFS", "AND", "OR", "MATCH", "COUNTIF", "EDATE", "LEFT", "TEXT",
         "INDEX", "TRIM", "UPPER", "SUBSTITUTE", "NOT", "MAX"]
print("VON MIR BENUTZT - kommt in der Quelle vor?")
unbekannt = []
for f in meine:
    v = q.get(f, 0)
    if v:
        print("   %-14s %-6d ok" % (f, v))
    else:
        print("   %-14s %-6s *** NICHT IN DER QUELLE ***" % (f, "-"))
        unbekannt.append(f)
print()
print("Nicht belegte Funktionen:", ", ".join(unbekannt) or "keine")
print()
print("Praefix-Funktionen der Quelle:",
      [k for k in q if k.startswith("_xlfn") or k.startswith("_xlpm")])
