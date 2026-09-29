"""Stichproben aus der gebauten Datei: die problematischen Faelle."""
import re
import zipfile

Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
z = zipfile.ZipFile(Z)
ss = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", s, re.S))
      for s in re.findall(r"<si>(.*?)</si>",
                         z.read("xl/sharedStrings.xml").decode("utf-8"), re.S)]
d = z.read("xl/worksheets/sheet1.xml").decode("utf-8")


def un(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&quot;", '"').replace("&apos;", "'"))


def zelle(r, sp):
    m = re.search(r'<c r="%s%d"[^>]*?(?:/>|>(.*?)</c>)' % (sp, r), d, re.S)
    if not m or not m.group(1):
        return ""
    v = re.search(r"<v>(.*?)</v>", m.group(1), re.S)
    if not v:
        return ""
    roh = un(v.group(1))
    return ss[int(roh)] if 't="s"' in m.group(0) else roh


def zeig(nummer, r):
    print("  Z%-4d %-22s %-16s L=%-2s P=%-7s -> M=%r"
          % (r, (zelle(r, "A") + " " + zelle(r, "B"))[:22],
             zelle(r, "K"), zelle(r, "L"), zelle(r, "P"), zelle(r, "M")))


print("=== BOURG: namentliche Ausnahme (vorher 'F0006') ===")
for r in (18, 19):
    zeig("BOURG", r)
print()
print("=== ANSAY: gleicher Haushalt, 1x 384 (vorher 2x 300) ===")
for r in (534, 535):
    zeig("ANSAY", r)
print()
print("=== QUINN: Nicole traegt die Rechnung ===")
for r in (5, 6, 7):
    zeig("QUINN", r)
print()
print("=== Offizielle ohne Tarif: (0+50), nicht '0 (+0+50)' ===")
for r in (32, 68):
    zeig("METZLER", r)
print()
print("=== Phantomzeilen: leer, nicht '0' ===")
for r in (607, 620):
    zeig("PHANTOM", r)

vorhanden = sum(1 for m in re.finditer(r'<c r="M(\d+)"', d) if zelle(int(m.group(1)), "M"))
summe = 0
for r in range(2, 774):
    for x in re.findall(r"\d+", zelle(r, "M") or ""):
        summe += int(x)
print()
print("Zeilen mit Wert in M:", vorhanden)
print("Summe der Betraege:", summe, "EUR")
