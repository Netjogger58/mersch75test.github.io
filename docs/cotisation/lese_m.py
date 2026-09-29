"""Liest die konkreten Zellen M der genannten Zeilen aus der gebauten Datei."""
import re
import zipfile

Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")

z = zipfile.ZipFile(Z)
ss = ["".join(re.findall(r"<t[^>]*>(.*?)</t>", s, re.S))
      for s in re.findall(r"<si>(.*?)</si>",
                         z.read("xl/sharedStrings.xml").decode("utf-8"), re.S)]
d = z.read("xl/worksheets/sheet1.xml").decode("utf-8")


def unesc(s):
    return (s.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
            .replace("&quot;", '"').replace("&apos;", "'"))


def zelle(r, sp):
    m = re.search(r'<c r="%s%d"([^>]*?)(?:/>|>(.*?)</c>)' % (sp, r), d, re.S)
    if not m:
        return "<Zelle fehlt>", ""
    attr, kinhalt = m.group(1), m.group(2) or ""
    v = re.search(r"<v>(.*?)</v>", kinhalt, re.S)
    if not v:
        return ("kein Wert (nur Formel)" if "<f>" in kinhalt else "leer"), attr
    roh = unesc(v.group(1))
    if 't="s"' in attr:
        roh = ss[int(roh)]
    return roh, attr


print("%-6s %-10s %-10s %-4s %-3s %-9s %-10s %-28s %-10s"
      % ("Zeile", "Nom", "Prenom", "K", "L", "Haushalt", "Lizenz", "M-Wert", "Attr"))
print("-" * 105)
for r in (154, 155, 156, 157, 224, 225, 226, 227, 5, 7, 18, 607):
    nom = zelle(r, "A")[0]
    pre = zelle(r, "B")[0]
    k = zelle(r, "K")[0]
    l = zelle(r, "L")[0]
    hh = zelle(r, "P")[0]
    liz = zelle(r, "AH")[0]
    mw, attr = zelle(r, "M")
    print("%-6d %-10s %-10s %-4s %-3s %-9s %-10s %-28r %-10s"
          % (r, str(nom)[:10], str(pre)[:10], k, l, hh, liz or "-", mw, attr[:12]))
