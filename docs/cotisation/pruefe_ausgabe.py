"""Liest die gebaute Datei und vergleicht Spalte M mit dem Python-Modell."""
import re
import sys
import zipfile

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")

Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")

z = zipfile.ZipFile(Z)
ss = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", s, re.S))
      for s in re.findall(r"<si>(.*?)</si>", z.read("xl/sharedStrings.xml").decode("utf-8"), re.S)]
d = z.read("xl/worksheets/sheet1.xml").decode("utf-8")


def unesc(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&quot;", '"').replace("&apos;", "'"))


def zelle(r, sp):
    m = re.search(r'<c r="%s%d"[^>]*?(?:/>|>(.*?)</c>)' % (sp, r), d, re.S)
    if not m or not m.group(1):
        return ""
    v = re.search(r"<v>(.*?)</v>", m.group(1), re.S)
    if not v:
        return ""
    roh = unesc(v.group(1))
    return ss[int(roh)] if 't="s"' in m.group(0) else roh


zeilen = {int(m.group(1)) for m in re.finditer(r'<row r="(\d+)"', d)}
daten = sorted(r for r in zeilen if 2 <= r <= 773)

print("=== QUINN (deine Zeilen 5-7) ===")
for r in (5, 6, 7):
    print("  Z%-4d %-9s %-9s J=%-7s K=%-4s L=%-2s P=%-7s AH=%-7s AI=%-6s -> M=%r"
          % (r, zelle(r, "A")[:9], zelle(r, "B")[:9], zelle(r, "J"), zelle(r, "K"),
             zelle(r, "L"), zelle(r, "P"), zelle(r, "AH"), zelle(r, "AI"), zelle(r, "M")))

print()
print("=== Verteilung Spalte M ===")
import collections
c = collections.Counter(zelle(r, "M") for r in daten)
for k, v in c.most_common(12):
    print("  %-16s %d" % (repr(k), v))
print("  Summe Betraege:",
      sum(int(m.group(0)) for r in daten for m in re.finditer(r"\d+", zelle(r, "M") or "")))

print()
print("=== Helfer in Zeile 5 ===")
for sp, name in (("BP", "FamID"), ("BQ", "Schluessel"), ("BR", "Aeltester"),
                 ("BS", "SpielerGes"), ("BV", "Zusatz"), ("BW", "Traeger"),
                 ("BY", "Tarif"), ("CA", "Zuschlag"), ("CB", "Personenwert"),
                 ("CD", "XSEULwert"), ("CE", "Sicherung")):
    m = re.search(r'<c r="%s5"[^>]*>(.*?)</c>' % sp, d, re.S)
    hat_f = "<f>" in (m.group(1) if m else "")
    v = re.search(r"<v>(.*?)</v>", m.group(1), re.S) if m else None
    print("  %-3s %-14s Formel=%-5s Wert=%s" % (sp, name, hat_f, v.group(1) if v else "-"))
