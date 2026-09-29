import re
import zipfile
import collections

Z = "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"

with zipfile.ZipFile(Z) as z:
    for sname in ["xl/worksheets/sheet1.xml"]:
        xml = z.read(sname).decode("utf-8")
        cells = {}
        for m in re.finditer(r'<c r="([A-Z]+)(\d+)"[^>]*>.*?<f[^>]*>(.*?)</f>', xml, re.S):
            col, row, f = m.groups()
            cells[(col, int(row))] = f

        print(f"{sname}: {len(cells)} formula cells found.")
        deps = collections.defaultdict(set)
        for (col, row), f in cells.items():
            for ref in re.finditer(r'(?<![A-Z0-9_!])\$?([A-Z]{1,3})\$?(\d+)(?![0-9])', f):
                r_col, r_row = ref.groups()
                r_row = int(r_row)
                if (r_col, r_row) in cells:
                    deps[col].add(r_col)

        print("Dependencies among formula columns in sheet1:")
        for c, targets in sorted(deps.items()):
            print(f"  {c} -> {sorted(targets)}")
