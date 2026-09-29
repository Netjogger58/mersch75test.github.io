import csv

with open("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv", encoding="utf-8-sig") as f:
    reader = csv.reader(f, delimiter=";")
    row1 = next(reader)
    print("CSV Headers count:", len(row1))
    for i, h in enumerate(row1[:25]):
        print(f"  Col {i+1} ({chr(65+i) if i < 26 else ''}): {h}")
