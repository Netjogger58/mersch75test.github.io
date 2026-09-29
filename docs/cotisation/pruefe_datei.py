"""Prueft die erzeugte Arbeitsmappe auf alles, was Excel zum Reparieren bringt.

    python3 pruefe_datei.py                       # Standard: Quelle + gebaute Datei
    python3 pruefe_datei.py <quelle> <ziel>       # zum Testen alter Fassungen
"""
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

Q = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "TEST1_nur-calcchain.xlsm")
Z = ("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
     "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
if len(sys.argv) > 2:
    Q, Z = sys.argv[1], sys.argv[2]

zaehler = re.compile(r"([A-Z]+)")
def ci(name):
    n = 0
    for c in name:
        n = n * 26 + ord(c) - 64
    return n


def spalten_pro_zeile(xml):
    """Gibt pro Zeile die Liste der Spaltennummern zurueck."""
    out = {}
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', xml, re.S):
        r = int(m.group(1))
        out[r] = [ci(x) for x in re.findall(r'<c r="([A-Z]+)\d+"', m.group(2))]
    return out


zaehler_fehler = []
zaehler_ok = 0
with zipfile.ZipFile(Q) as za, zipfile.ZipFile(Z) as zb:
    qname = za.namelist()
    # 1) Alle Teile vorhanden?
    fehlt = [n for n in qname if n not in zb.namelist() and n != "xl/calcChain.xml"]
    print("1) Teile fehlen:", fehlt or "keine")
    print("2) Neue Teile :", [n for n in zb.namelist() if n not in qname])

    # 3) XML-Wohlgeformtheit ALLER Teile
    kaputt = []
    for n in zb.namelist():
        if n.endswith((".xml", ".rels")):
            try:
                ET.fromstring(zb.read(n))
            except ET.ParseError as e:
                kaputt.append(f"{n}: {e}")
    print("3) XML kaputt:", kaputt or "keins")

    # 3b) SCHEMA-Fehler, die Wohlgeformtheit NICHT erkennt: Text oder fremde
    #     Elemente direkt in <row>. Genau das hat die Reparatur-Meldung ausgeloest,
    #     weil die Zeilen-Attribute (spans, ht, ...) faelschlich als Text in die
    #     Zeile geschrieben wurden.
    schemafehler = []
    for n in zb.namelist():
        if not re.match(r"xl/worksheets/sheet\d+\.xml$", n):
            continue
        wurzel = ET.fromstring(zb.read(n))
        for row in wurzel.iter():
            if not row.tag.endswith("}row") and row.tag != "row":
                continue
            ns = row.tag.split("}")[0].lstrip("{")
            for kind in list(row):
                if kind.tag in (f"{{{ns}}}c", f"{{{ns}}}extLst"):
                    continue
                schemafehler.append(f"{n} Zeile {row.get('r')}: <{kind.tag.split('}')[-1]}>")
            if row.text and row.text.strip():
                schemafehler.append(f"{n} Zeile {row.get('r')}: Text '{row.text.strip()[:40]}'")
    print("3b) Fremde Inhalte in <row>:", schemafehler[:6] if schemafehler else "keine",
          f"(gesamt {len(schemafehler)})")

    # 4) Blatt-Mitglieder finden
    wb = zb.read("xl/workbook.xml").decode("utf-8")
    rid = re.search(r'<sheet[^>]*name="Membres 2026_2027"[^>]*r:id="([^"]+)"', wb).group(1)
    rels = zb.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    pfad = "xl/" + re.search(r'Id="%s"[^>]*Target="([^"]+)"' % rid, rels).group(1).lstrip("/")
    neu = zb.read(pfad).decode("utf-8")
    ridq = re.search(r'<sheet[^>]*name="Membres 2026_2027"[^>]*r:id="([^"]+)"',
                     za.read("xl/workbook.xml").decode("utf-8")).group(1)
    relsq = za.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    pfadq = "xl/" + re.search(r'Id="%s"[^>]*Target="([^"]+)"' % ridq, relsq).group(1).lstrip("/")
    alt = za.read(pfadq).decode("utf-8")
    print(f"4) Blatt-XML: Quelle {pfadq} -> Ziel {pfad}")

    # 5) Spalten aufsteigend? (Excel verlangt das strikt)
    sn, sa = spalten_pro_zeile(neu), spalten_pro_zeile(alt)
    for r, cols in sn.items():
        if cols != sorted(cols) or len(cols) != len(set(cols)):
            zaehler_fehler.append(f"Zeile {r}: Spalten nicht aufsteigend")
        else:
            zaehler_ok += 1
    print(f"5) Zeilen mit aufsteigenden Spalten: {zaehler_ok}/{len(sn)}")
    for f in zaehler_fehler[:5]:
        print("     !", f)

    # 6) Sind alle Originalzellen unveraendert enthalten?
    fehlend_zellen, geaendert = [], []
    for r, cols in sa.items():
        m_neu = re.search(r'<row r="%d"[^>]*>(.*?)</row>' % r, neu, re.S)
        if not m_neu:
            continue
        inhalt_neu = m_neu.group(1)
        m_alt = re.search(r'<row r="%d"[^>]*>(.*?)</row>' % r, alt, re.S)
        alt_cells = re.findall(r'<c r="[A-Z]+%d"[^>]*?(?:/>|>.*?</c>)' % r, m_alt.group(1), re.S)
        for c in alt_cells:
            ref = re.search(r'r="([A-Z]+\d+)"', c).group(1)
            if ref.startswith("M"):
                continue          # wird absichtlich ersetzt
            if c not in inhalt_neu:
                (fehlend_zellen if ('<f' in c or 'cm=' in c) else geaendert).append(ref)
    print("6) Originalzellen mit Formel/Metadaten, die FEHLEN:", len(fehlend_zellen),
          zaehler_fehler[:0] or (fehlend_zellen[:5] if fehlend_zellen else ""))
    print("   sonstige Zellen veraendert:", len(geaendert), geaendert[:5] if geaendert else "")

    # 7) cm= und t="array" unveraendert vorhanden?
    print("7) cm= im Blatt  alt/neu:", alt.count("cm="), "/", neu.count("cm="))
    print("   t=\"array\" alt/neu  :", alt.count('t="array"'), "/", neu.count('t="array"'))

    # 8) Stichproben
    for r in (2, 5, 437, 438, 439):
        m = re.search(r'<row r="%d"[^>]*>(.*?)</row>' % r, neu, re.S)
        if not m:
            continue
        mz = re.search(r'<c r="M%d".*?</c>' % r, m.group(1), re.S)
        print(f"8) M{r}: {(mz.group(0)[:120] if mz else 'FEHLT')}")
