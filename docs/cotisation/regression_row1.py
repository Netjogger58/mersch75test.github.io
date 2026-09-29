"""Regressions-Test: erzeugt absichtlich die alte, kaputte Zeile 1
(Attribute als Text in der Zeile) und prueft, dass der Checker sie findet."""
import re
import shutil
import zipfile

Q = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "TEST1_nur-calcchain.xlsm")
KAPUTT = "/tmp/KAPUTT_alte_fassung.xlsm"

with zipfile.ZipFile(Q) as zin:
    teile = {n: zin.read(n) for n in zin.namelist()}
    namen = zin.namelist()

d = teile["xl/worksheets/sheet1.xml"].decode("utf-8")
alt = '<row r="1" spans="1:66" ht="54" customHeight="1" x14ac:dyDescent="0.2">'
neu = '<row r="1">'
assert alt in d
kaputt = d.replace(alt, neu + alt[len('<row r="1"'):-1] + ">", 1)
# so wird es der Bausatz getan hat: Attribute landen als Text im Zeilenkoerper
teile["xl/worksheets/sheet1.xml"] = kaputt.encode("utf-8")
with zipfile.ZipFile(KAPUTT, "w", zipfile.ZIP_DEFLATED) as zout:
    for n in namen:
        zout.writestr(n, teile[n])

print("Kaputte Datei geschrieben:", KAPUTT)
print("Zeile 1 jetzt:", re.search(r"<row r=\"1\".{0,120}", kaputt, re.S).group(0))
