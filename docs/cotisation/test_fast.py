import zipfile, re

Z = "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm"
with zipfile.ZipFile(Z) as z:
    for name in z.namelist():
        if "sheet" in name and name.endswith(".xml"):
            print("Checking", name)
            xml = z.read(name).decode("utf-8")
            print("  Length:", len(xml))
print("Done")
