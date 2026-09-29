import re
import zipfile
from xml.etree import ElementTree as ET

Z = "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"
z = zipfile.ZipFile(Z)
NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

wb = ET.fromstring(z.read("xl/workbook.xml"))
sheet_names = {}
for s in wb.findall(f".//{NS}sheet"):
    sheet_names[s.get("{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id")] = s.get("name")

rels = ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))
sheet_file_to_name = {}
for r in rels.findall(".//{http://schemas.openxmlformats.org/package/2006/relationships}Relationship"):
    rid = r.get("Id")
    target = r.get("Target")
    if target.startswith("worksheets/"):
        target = "xl/" + target
    elif not target.startswith("xl/"):
        target = "xl/" + target
    if rid in sheet_names:
        sheet_file_to_name[target] = sheet_names[rid]

print("Scanning for self-references in formulas...")
for name in sorted(z.namelist()):
    if not re.match(r"^xl/worksheets/sheet\d+\.xml$", name):
        continue
    sheet_title = sheet_file_to_name.get(name, name)
    tree = ET.fromstring(z.read(name))
    found = 0
    for c in tree.iter(f"{NS}c"):
        f = c.find(f"{NS}f")
        if f is None or not (f.text or "").strip():
            continue
        ref = c.get("r")
        text = f.text
        col_m = re.match(r"^([A-Z]+)(\d+)$", ref)
        if not col_m:
            continue
        c_col, c_row = col_m.groups()
        for m in re.finditer(r"(?<![A-Z0-9_!])\$?([A-Z]{1,3})\$?(\d+)(?![0-9])", text):
            r_col, r_row = m.groups()
            if r_col == c_col and r_row == c_row:
                if found < 5:
                    print(f"  [{sheet_title}] {ref}: {text}")
                found += 1
    if found:
        print(f"  Total self-referencing formulas in [{sheet_title}]: {found}")

