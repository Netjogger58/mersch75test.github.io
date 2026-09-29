import zipfile, re

files = [
    "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm",
    "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm.bak-ohne-Formeln",
    "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/TEST1_nur-calcchain.xlsm",
    "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/TEST2_nur-blatt1.xlsm"
]

for f in files:
    try:
        with zipfile.ZipFile(f) as z:
            s1 = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
            shared = z.read("xl/sharedStrings.xml").decode("utf-8")
            # count M values
            m_vals = re.findall(r'<c r="M\d+"[^>]*>(?:<v>(\d+)</v>)?', s1)
            print(f, "exists! Size:", len(s1))
            # check M2:
            m2 = re.search(r'<c r="M2"[^>]*>(.*?)</c>', s1)
            print("  M2:", m2.group(0) if m2 else "none")
    except Exception as e:
        print(f, "error:", e)
