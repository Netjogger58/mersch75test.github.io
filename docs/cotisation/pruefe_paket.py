import re
import zipfile

Q = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "TEST1_nur-calcchain.xlsm")
Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")

for p, l in ((Q, "QUELLE"), (Z, "NEU   ")):
    n = zipfile.ZipFile(p).namelist()
    print(l, "erster Eintrag:", repr(n[0]), "| Eintraege:", len(n),
          "| Verzeichnis-Eintraege:", sum(1 for x in n if x.endswith("/")))

z = zipfile.ZipFile(Q)
wb = z.read("xl/workbook.xml").decode("utf-8")
dn = re.findall(r'<definedName name="([^"]+)"', wb)
print()
print("Definierte Namen:", len(dn))
print("  Kollision mit 'Cotisation':", [x for x in dn if "cotisation" in x.lower()])
print("  localSheetId-Werte:", sorted(set(re.findall(r'localSheetId="(\d+)"', wb))))
ct = z.read("[Content_Types].xml").decode("utf-8")
print()
print("ContentType xl/workbook.xml:",
      re.search(r'PartName="/xl/workbook.xml" ContentType="([^"]+)"', ct).group(1))
print("Default fuer 'bin':",
      re.findall(r'<Default Extension="bin" ContentType="([^"]+)"', ct))
print("Vorhandene Blatt-Overrides:", len(re.findall(r"worksheets/sheet\d+\.xml", ct)))
print("vbaProject:", [n for n in z.namelist() if "vba" in n.lower()])
