"""Entfernt die veraltete calcChain.xml aus der Arbeitsmappe.

Anlass: Excel meldete "Entfernte Datensätze: Formel von
/xl/calcChain.xml-Part". Die calcChain ist ein reiner Reihenfolge-Cache:
Nach dem Ersetzen von 8.997 Formelzellen passt sie nicht mehr zu den
tatsaechlich vorhandenen Formeln, und Excel verweigert daraufhin die
Datei.

Die Kette wird von Excel beim naechsten Speichern neu aufgebaut, der Inhalt
der Zellen bleibt unberuehrt. Das ist der uebliche Weg, eine calcChain
nach programmatischen Formelaenderungen zu invalidieren.
"""
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, '/Users/netjogger58/CascadeProjects/mersch75test.github.io/'
                 'docs/cotisation')
import mappe  # noqa: E402

CALC = 'xl/calcChain.xml'


def main() -> int:
    pfad = mappe.datenquelle()
    with zipfile.ZipFile(pfad) as z:
        infos = z.infolist()
        teile = {i.filename: z.read(i.filename) for i in infos}

    if CALC not in teile:
        print('keine calcChain vorhanden - nichts zu tun')
        return 0

    print('Datei      :', pfad.name)
    print('calcChain  :', len(teile[CALC]), 'Zeichen,',
          len(re.findall(r'<c r=', teile[CALC].decode('utf-8'))), 'Eintraege')

    del teile[CALC]

    # Beziehung in workbook.xml.rels entfernen
    rels = 'xl/_rels/workbook.xml.rels'
    r = teile[rels].decode('utf-8')
    r_neu = re.sub(r'<Relationship[^>]*calcChain\.xml"[^>]*/>', '', r)
    if r_neu != r:
        ET.fromstring(r_neu)
        teile[rels] = r_neu.encode('utf-8')
        print('rels       : calcChain-Beziehung entfernt')

    # Content-Type-Override entfernen
    ct = '[Content_Types].xml'
    c = teile[ct].decode('utf-8')
    c_neu = re.sub(r'<Override[^>]*calcChain\.xml"[^>]*/>', '', c)
    if c_neu != c:
        ET.fromstring(c_neu)
        teile[ct] = c_neu.encode('utf-8')
        print('ContentType: calcChain-Override entfernt')

    sicherung = pfad.with_name(
        pfad.stem + '.vor-calcchain-' + datetime.now().strftime('%Y-%m-%d_%H%M')
        + pfad.suffix)
    shutil.copy2(pfad, sicherung)
    print('Sicherung  :', sicherung.name)

    tmp = pfad.with_suffix('.tmp')
    with zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            if i.filename == CALC:
                continue
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            out.writestr(zi, teile[i.filename])
    tmp.replace(pfad)
    print('geschrieben: calcChain entfernt - Excel baut sie neu auf')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
