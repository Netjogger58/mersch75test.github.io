import zipfile
from xml.etree import ElementTree as ET

for pfad, name in [
    ('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/GC 2026-09-24 MEMBERSLESCHT 2026-2027.xlsm', 'GC Original'),
    ('/Users/netjogger58/CascadeProjects/Vereins-OS/docs/TEST1_nur-calcchain.xlsm', 'TEST1')
]:
    with zipfile.ZipFile(pfad) as z:
        shared = ET.fromstring(z.read('xl/sharedStrings.xml'))
        strings = [t.text for t in shared.findall('.//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')]
        sheet1 = ET.fromstring(z.read('xl/worksheets/sheet1.xml'))
        ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        row1 = sheet1.find('.//s:row[@r="1"]', ns)
        headers = {}
        for c in row1.findall('s:c', ns):
            r = c.get('r').rstrip('0123456789')
            t = c.get('t')
            v = c.find('s:v', ns)
            val = v.text if v is not None else ''
            if t == 's' and val.isdigit():
                val = strings[int(val)]
            headers[r] = val
        print(f'=== {name} ===')
        for col in ['J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q']:
            print(f'  {col}: {headers.get(col)}')
        for col, h in headers.items():
            if 'bezahlt' in str(h).lower():
                print(f'  FOUND BEZAHLT at {col}: {h}')
