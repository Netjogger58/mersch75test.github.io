"""Prueft die Status-X-Regel gegen die Live-Mappe.

Regel: wer in Spalte O ein X hat, darf NICHT in Stripe erscheinen - ausser
sein Haushalt schuldet einen Betrag, dann tritt er als Rechnungstraeger auf.

Aufruf:  python3 docs/cotisation/pruefe_x_personen.py
"""
import pathlib
import re
import sys
import zipfile

MAPPE = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")

z = zipfile.ZipFile(MAPPE)
sheet = z.read("xl/worksheets/sheet1.xml").decode("utf-8")
strings = re.findall(r"<si>(?:<t[^>]*>)?(.*?)(?:</t>)?</si>",
                     z.read("xl/sharedStrings.xml").decode("utf-8"), re.S)


def zelle(r, c):
    m = re.search(r'<c r="%s%d"([^>]*)>(.*?)</c>' % (c, r), sheet, re.S)
    if not m:
        return ""
    v = re.search(r"<v>(.*?)</v>", m.group(2), re.S)
    if not v:
        return ""
    return (strings[int(v.group(1))] if 't="s"' in m.group(1)
            else v.group(1)).strip()


zeilen = [int(m) for m in re.findall(r'<row r="(\d+)"', sheet)]
x_zeilen = [r for r in zeilen if zelle(r, "A") and zelle(r, "O") == "X"]

traeger = [r for r in x_zeilen if zelle(r, "CC") == "TRAEGER"]
mit_betrag = [r for r in traeger if zelle(r, "L") and zelle(r, "L") != "0"]
ohne = [r for r in traeger if not (zelle(r, "L") and zelle(r, "L") != "0")]

print(f"X-Personen gesamt              : {len(x_zeilen)}")
print(f"davon Rechnungstraeger         : {len(traeger)}")
print(f"  mit Haushaltsbetrag (ok)     : {len(mit_betrag)}")
print(f"  ohne Betrag (nicht in Stripe): {len(ohne)}")
print(f"nicht Traeger (nur Haushaltcode): "
      f"{len(x_zeilen) - len(traeger)}")

fehler = [r for r in ohne if zelle(r, "L") == "0"]
if fehler:
    print(f"\nACHTUNG: {len(fehler)} X-Traeger zeigen '0' - ihr Haushalt "
          f"verliert die Rechnung. Z.B. Zeile {fehler[0]} "
          f"{zelle(fehler[0], 'A')}")
else:
    print("\nKein X-Rechnungstraeger ohne Haushaltsbetrag - die Regel haelt.")
