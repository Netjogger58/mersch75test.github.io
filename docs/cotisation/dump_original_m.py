import zipfile
import xml.etree.ElementTree as ET

f = "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm"
with zipfile.ZipFile(f) as z:
    shared = ET.fromstring(z.read("xl/sharedStrings.xml"))
    strings = [t.text for t in shared.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t")]
    sheet1 = ET.fromstring(z.read("xl/worksheets/sheet1.xml"))

ns = {"s": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
counts = {}
for r in range(2, 774):
    row = sheet1.find(f'.//s:row[@r="{r}"]', ns)
    if row is not None:
        c = row.find(f's:c[@r="M{r}"]', ns)
        if c is not None:
            v = c.find("s:v", ns)
            val = strings[int(v.text)] if c.get("t") == "s" and v is not None and v.text.isdigit() else (v.text if v is not None else "")
            counts[val] = counts.get(val, 0) + 1
        else:
            counts["[leer]"] = counts.get("[leer]", 0) + 1

print("Distribution of manual M values in GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm:")
for val, count in sorted(counts.items(), key=lambda kv: -kv[1]):
    print(f"  {repr(val)}: {count}")

