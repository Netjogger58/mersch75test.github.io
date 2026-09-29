import re
import sys
import zipfile
import pathlib
from datetime import datetime
import xml.etree.ElementTree as ET


import mappe

DOCS = mappe.DOCS
QUELLE = mappe.quelle()

# --datei <pfad> erlaubt das Bauen in eine beliebige Kopie, z. B. die aus
# Google Drive geladene Datei. Ohne die Option gilt der Standardname.
if "--datei" in sys.argv:
    ZIEL = mappe.set_ziel(sys.argv[sys.argv.index("--datei") + 1])
    print(f"Arbeitsdatei festgelegt: {ZIEL}")
else:
    ZIEL = mappe.ziel()

BLATT = "Membres 2026_2027"   # wird zur Laufzeit aus der Quelle gelesen (siehe oben)
BLATT_ERWARTET = BLATT
CONFIG_BLATT = "Cotisation"
ERSTE, LETZTE = 2, 773        # LETZTE = letzte belegte Datenzeile der Quelle
KAPAZITAET = 900              # Formeln/Automationen bis hierher -> Reserve fuer neue Mitglieder
assert KAPAZITAET >= LETZTE

SP = dict(BP=68, BQ=69, BR=70, BS=71, BT=72, BU=73, BV=74, BW=75, BX=76,
          BY=77, BZ=78, CA=79, CB=80, CC=81, CD=82, CE=83)

SP_ZIEL = "L"          # Spalte mit der Ausgabe: Cotisatioun
SP_SPIELT = "O"        # Spalte Spielt J/R/N (Eingabe)
SP_BEZAHLT = "N"       # Spalte Bezahlt J/N (Eingabe Kassierer)
SP_FAM = "Q"           # Code Courrier neu (Haushaltscode)
SP_LIZ_SP = "AI"       # Spielerlizenz
SP_LIZ_OFF = ("AJ", "AK", "AL")
SP_MANUELL = "BX"      # Helfer: manuelle Vorgabe
SP_SICHER = "CE"       # Helfer: Sicherung

CONFIG = pathlib.Path("/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")

def col_name(i: int) -> str:
    s = ""
    while i:
        i, r = divmod(i - 1, 26)
        s = chr(65 + r) + s
    return s

def col_idx(name: str) -> int:
    n = 0
    for c in name:
        n = n * 26 + ord(c) - 64
    return n

def esc(s: str) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))

def zelle_text(ref, text):
    return f'<c r="{ref}" t="inlineStr"><is><t xml:space="preserve">{esc(text)}</t></is></c>'

def zelle_formel(ref, formel):
    return f'<c r="{ref}"><f>{esc(str(formel).lstrip("="))}</f></c>'

def zelle_leer(ref):
    return f'<c r="{ref}"/>'

# Helfer-Definitionen angepasst auf neues Spalten-Layout:
# SP_SPIELT = O, SP_FAM = Q, SP_LIZ_SP = AI, SP_LIZ_OFF = AJ, AK, AL, Fragen = AY:BB
HELFER = [
    (SP["BP"], "FamID",
     # LEERER Haushaltscode -> "" (kein Phantom-FamID!). Ein Zeilen-Sentinel wie
     # "@"&ROW() wuerde in L als Text "@774" erscheinen, BW als "TRAEGER" und
     # eine Stripe-Rechnung ausloesen. Leere Zeilen bleiben so restlos stumm.
     '=IF($Q{r}="","",IF(SUMPRODUCT(--('
     'SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Cotisation!$I$2:$I$50)," ",""),".",""),"\'","")'
     '=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'","")))>0,'
     '"ADR:"&SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'",""),$Q{r}))'),
    (SP["BQ"], "Schluessel",
     '=IF(ISNUMBER($J{r}),$J{r},IFERROR(DATEVALUE($J{r}),73415))+ROW()/1000000'),
    (SP["BR"], "Aeltester",
     '=SUMPRODUCT(MIN(($BP${e}:$BP${l}=$BP{r})*$BQ${e}:$BQ${l}'
     '+($BP${e}:$BP${l}<>$BP{r})*10^15))'),
    (SP["BS"], "SpielerGes",
     '=COUNTIFS($BP${e}:$BP${l},$BP{r},$O${e}:$O${l},"J",$AI${e}:$AI${l},"<>")'),
    (SP["BT"], "SpielerSEN",
     '=COUNTIFS($BP${e}:$BP${l},$BP{r},$O${e}:$O${l},"J",$AI${e}:$AI${l},"<>",$K${e}:$K${l},"SEN")'),
    (SP["BU"], "SpielerU25",
     '=COUNTIFS($BP${e}:$BP${l},$BP{r},$O${e}:$O${l},"J",$AI${e}:$AI${l},"<>",$K${e}:$K${l},"U25")'),
    (SP["BV"], "Zusatz",
     "=" + "+".join('COUNTIFS($BP${e}:$BP${l},$BP{r},$AI${e}:$AI${l},"",'
                    + c + '${e}:' + c + '${l},"<>",' + c + '${e}:' + c + '${l},"<>///")'
                    for c in SP_LIZ_OFF)
     + "+" + "+".join('COUNTIFS($BP${e}:$BP${l},$BP{r},$AI${e}:$AI${l},"<>",$O${e}:$O${l},"'
                      + v + '")' for v in ("N", "R"))),
    (SP["BW"], "Traeger",
     '=IF($BP{r}="","",IF(Cotisation!$B$8<>"Aelteste",'
     'IF(COUNTIFS($BP${e}:$BP{r},$BP{r})=1,"TRAEGER",""),'
     'IF($BR{r}>=73415,IF(COUNTIFS($BP${e}:$BP{r},$BP{r})=1,"TRAEGER",""),'
     'IF($BQ{r}=$BR{r},"TRAEGER",""))))'),
    (SP["BY"], "Tarif",
     '=IF(OR($BS{r}>=2,AND($BT{r}>=1,$BU{r}>=1)),Cotisation!$B$3,'
     'IF($BT{r}>=1,Cotisation!$B$1,IF($BU{r}>=1,Cotisation!$B$2,0)))'),
    (SP["BZ"], "AusnahmeNr",
     '=IFERROR(MATCH($A{r}&"|"&$B{r},Cotisation!$G$2:$G$200,0),0)'),
    (SP["CA"], "Zuschlag",
     '=IF(AND($BV{r}>=1,OR(Cotisation!$B$7="JA",$BY{r}<>Cotisation!$B$3)),Cotisation!$B$4,0)'),
    (SP["CB"], "Personenwert",
     '=IF($BZ{r}>0,INDEX(Cotisation!$F$2:$F$200,$BZ{r}),'
     'IF(OR(AND($O{r}<>"J",$O{r}<>"N",$AI{r}<>""),'
     'AND($AI{r}<>"",COUNTIF($AY{r}:$BB{r},"FRAGEN")>0),$Q{r}="GAJGL"),Cotisation!$B$10,""))'),
    (SP["CC"], "Alterspruefung",
     '=IFERROR(IF(IF(EDATE(IF(ISNUMBER($J{r}),$J{r},DATEVALUE($J{r})),'
     '12*Cotisation!$B$12)>DATEVALUE(Cotisation!$B$11),"U25","SEN")'
     '<>$K{r},"PRUEFEN",""),"")'),
    (SP["CD"], "XSEULwert",
     '=IF($Q{r}<>"XSEUL","",IF(AND(LEFT($BP{r},4)="ADR:",$BS{r}>=2),"",'
     'TEXT(Cotisation!$B$5,"0")))'),
]

FORMEL_L = (
    '=IF($BP{r}="","",'
    'IF($BX{r}<>"",$BX{r}&"",'
    'IF($CB{r}<>"",$CB{r}&"",'
    'IF($CD{r}<>"",$CD{r}&"",'
    'IF($BW{r}="TRAEGER",'
    'IF($BY{r}=0,'
    'IF($CA{r}>0,"(0+"&TEXT($CA{r},"0")&")",""),'
    'TEXT($BY{r},"0")&IF($CA{r}>0," (+0+"&TEXT($CA{r},"0")&")",""))&"",'
    'IF(LEFT($BP{r},4)="ADR:",$Q{r}&"",$BP{r}&""))))))'
)

def shift_cell_ref(ref_str: str) -> str:
    """Verschiebt Zellreferenzen >= N um +2 Spalten, NUR ausserhalb von
    String-Literalen ("...") und nur echte Zellbezuege (kein $, keine
    Funktions-/Bereichsnamen wie DATE, CAT_JOUEUR, VLOOKUP).
    Beispiel: N2 -> P2, O2 -> Q2, AG2 -> AI2."""
    # Teile in String-Literale und Code auf; nur Code-Teile anfassen
    teile = re.split(r'("[^"]*")', ref_str)
    for i in range(0, len(teile), 2):
        def repl(m):
            col, row = m.group(1), m.group(2)
            idx = col_idx(col)
            if idx >= 14:  # N ist 14
                col = col_name(idx + 2)
            return f"{col}{row}"
        teile[i] = re.sub(r'(?<![A-Z$\'\"!_])([A-Z]{1,3})(\d+)(?![\d(])', repl, teile[i])
    return "".join(teile)

def blattname_lesen(teile: dict) -> str:
    """Liest den Namen des Datenblatts (sheet1.xml) aus der Quell-Mappe.
    -> Wird das Blatt in Excel umbenannt, passt sich der Build automatisch an."""
    wb = teile["xl/workbook.xml"].decode("utf-8")
    rels = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    ziel = {}
    for tag in re.findall(r"<Relationship\b[^>]*/?>", rels):
        rid_m = re.search(r'Id="([^"]+)"', tag)
        tgt_m = re.search(r'Target="([^"]+)"', tag)
        if rid_m and tgt_m:
            ziel[rid_m.group(1)] = tgt_m.group(1).lstrip("/")
    for tag in re.findall(r"<sheet\b[^>]*/?>", wb):
        name_m = re.search(r'name="([^"]+)"', tag)
        rid_m = re.search(r'r:id="([^"]+)"', tag)
        if not (name_m and rid_m):
            continue
        if ziel.get(rid_m.group(1), "").endswith("worksheets/sheet1.xml"):
            return name_m.group(1)
    return BLATT_ERWARTET


def baue_neue_arbeitsmappe():
    with zipfile.ZipFile(QUELLE) as zin:
        teile = {n: zin.read(n) for n in zin.namelist()}
        reihenfolge = list(zin.namelist())

    # CalcChain entfernen
    teile.pop("xl/calcChain.xml", None)
    reihenfolge = [n for n in reihenfolge if n != "xl/calcChain.xml"]
    rels_wb = re.sub(r'<Relationship[^>]*calcChain\.xml[^>]*/>', "", teile["xl/_rels/workbook.xml.rels"].decode("utf-8"))
    ct = re.sub(r'<Override[^>]*calcChain\.xml[^>]*/>', "", teile["[Content_Types].xml"].decode("utf-8"))

    # Config-Sheet Cotisation hinzufügen
    sys.path.insert(0, str(CONFIG))
    import baut_arbeitsmappe as ba
    config_xml_str = ba.baue_config_sheet()
    config_part = "xl/worksheets/sheet13.xml"
    teile[config_part] = config_xml_str.encode("utf-8")
    reihenfolge.append(config_part)

    # Blattname dynamisch aus der Quelle lesen -> Rename im Excel ist safe
    BLATT = blattname_lesen(teile)
    if BLATT != BLATT_ERWARTET:
        print(f"! Blattname der Quelle ist '{BLATT}' (erwartet '{BLATT_ERWARTET}').")
        print("  Alle Formeln werden auf den neuen Namen gebaut - bitte README-")
        print("  Abschnitt 'Blatt umbenannt' pruefen (Cotisation-Bezuege bleiben).")

    # Workbook.xml anpassen
    rid = "rIdCotisation"
    wb_str = teile["xl/workbook.xml"].decode("utf-8")
    wb_str = wb_str.replace("</sheets>", f'<sheet name="{CONFIG_BLATT}" sheetId="13" r:id="{rid}"/></sheets>')
    wb_str = re.sub(r"<calcPr([^>]*?)/>",
                    lambda m: "<calcPr" + re.sub(r'\sfullCalcOnLoad="[^"]*"', "", m.group(1)) + ' fullCalcOnLoad="1"/>',
                    wb_str, count=1)
    teile["xl/workbook.xml"] = wb_str.encode("utf-8")

    # Workbook.xml.rels anpassen
    rels_wb = rels_wb.replace("</Relationships>",
                              f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" '
                              f'Target="worksheets/sheet13.xml"/></Relationships>')
    teile["xl/_rels/workbook.xml.rels"] = rels_wb.encode("utf-8")

    # [Content_Types].xml anpassen
    ct = ct.replace("</Types>",
                    f'<Override PartName="/{config_part}" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/></Types>')
    teile["[Content_Types].xml"] = ct.encode("utf-8")

    # docProps/app.xml anpassen: Zaehler +1 UND Blattname in TitlesOfParts
    # DIREKT hinter dem letzten echten Blattnamen (nicht vor den
    # benannten Bereichen wie _FilterDatabase etc.)
    if "docProps/app.xml" in teile:
        app = teile["docProps/app.xml"].decode("utf-8")
        blaetter = re.findall(r'<sheet name="([^"]+)"', wb_str)
        titel = re.findall(r"<vt:lpstr>([^<]*)</vt:lpstr>",
                           re.search(r"<TitlesOfParts>(.*?)</TitlesOfParts>", app, re.S).group(1))
        letztes = [t for t in reversed(titel) if t in blaetter][-1]
        app = re.sub(r"(Arbeitsblätter</vt:lpstr></vt:variant><vt:variant><vt:i4>)(\d+)(</vt:i4>)",
                     lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app, count=1)
        app = re.sub(r'(<TitlesOfParts><vt:vector size=")(\d+)(")',
                     lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app, count=1)
        app = app.replace(f"<vt:lpstr>{letztes}</vt:lpstr>",
                          f"<vt:lpstr>{letztes}</vt:lpstr><vt:lpstr>{CONFIG_BLATT}</vt:lpstr>", 1)
        teile["docProps/app.xml"] = app.encode("utf-8")

    # _FilterDatabase des Membres-Blatts auf BO erweitern (war BM) und bis
    # KAPAZITAET strecken. Der Blattname kommt aus der Quelle (siehe oben),
    # damit ein in Excel umbenanntes Datenblatt weiterhin funktioniert.
    wb_str = wb_str.replace(f"'{BLATT}'!$A$1:$BM$772",
                            f"'{BLATT}'!$A$1:$BO{KAPAZITAET}")
    teile["xl/workbook.xml"] = wb_str.encode("utf-8")

    # Nun das Hauptblatt sheet1.xml (Membres 2026_2027) umbauen:
    s1 = teile["xl/worksheets/sheet1.xml"].decode("utf-8")

    # Shared Strings laden
    shared_root = ET.fromstring(teile["xl/sharedStrings.xml"])
    shared_strings = ["".join(t.text or "" for t in si.findall(".//{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t"))
                      for si in shared_root.findall("{http://schemas.openxmlformats.org/spreadsheetml/2006/main}si")]

    print(f"Loaded {len(shared_strings)} shared strings.")

    # Berechne Werte für L mit Python-Referenzmodell
    import pruef_cotisation as pr
    def cfg(name):
        return pr.liese_config(CONFIG / name)
    tarife = pr.lade_tarife(CONFIG / "tarife-cotisation.csv")
    ausnahmen = {(n.strip().upper(), p.strip().upper()): a.strip()
                 for n, p, a in cfg("ausnahmen-cotisation.csv")}
    haushalte = {pr.normalisiere_adresse(a.strip())
                 for a, _b, *_rest in ((r + ["", ""])[:3] for r in cfg("haushalte-cotisation.csv"))
                 if a.strip()}
    zeilen_raw = ba.liese_blatt(teile, "xl/worksheets/sheet1.xml")
    ref_ergebnis = pr.berechne(zeilen_raw, ausnahmen, *tarife, haushalte)
    werte_l = {x["excel_zeile"]: x["neu"] for x in ref_ergebnis}
    print(f"Calculated {len(werte_l)} reference values for Cotisatioun (Col L).")

    return teile, reihenfolge, s1, shared_strings, werte_l
def transformiere_cols(s1_xml: str) -> str:
    """Passt <cols> an: Spalten >= 14 (N) ruecken um +2 nach rechts.
    Bereiche, die die Grenze ueberspannen (z.B. min=16 max=32), werden
    korrekt aufgeteilt. N/O und Helfer BP:CE erhalten eigene Breiten."""
    def cols_repl(m):
        cols_content = m.group(1)
        # Alle Einzelspalten mit ihrem Attributsatz sammeln
        einzel = {}  # idx -> attr_str (ohne min/max)
        for col_tag in re.finditer(r'<col ([^>]+)/>', cols_content):
            attr_str = col_tag.group(1)
            attrs = dict(re.findall(r'(\w+)="([^"]+)"', attr_str))
            c_min = int(attrs.get("min", 1))
            c_max = int(attrs.get("max", 1))
            rest = re.sub(r'\s*(min|max)="\d+"', "", attr_str).strip()
            for i in range(c_min, c_max + 1):
                neu = i + 2 if i >= 14 else i
                einzel[neu] = rest
        # Breiten fuer N (14) und O (15)
        einzel[14] = 'width="13" customWidth="1"'
        einzel[15] = 'width="13" customWidth="1"'
        # Breiten fuer Helfer 68..83 (BP..CE)
        for h_col in range(68, 84):
            einzel.setdefault(h_col, 'width="14" customWidth="1"')
        # Aufeinanderfolgende Spalten mit gleichem Attributsatz gruppieren
        idxs = sorted(einzel)
        gruppen = []
        start = prev = idxs[0]
        for i in idxs[1:]:
            if i == prev + 1 and einzel[i] == einzel[start]:
                prev = i
            else:
                gruppen.append((start, prev, einzel[start]))
                start = prev = i
        gruppen.append((start, prev, einzel[start]))
        out = "<cols>" + "".join(
            f'<col min="{a}" max="{b}" {at}/>' for a, b, at in gruppen) + "</cols>"
        return out

    return re.sub(r'<cols>(.*?)</cols>', cols_repl, s1_xml, flags=re.S)


def parse_cells(r: int, content: str):
    # Selbstschliessende Zellen (<c .../>) haben KEINEN Body (None),
    # sonst wuerde das Regex den Body der NAECHSTEN Zelle schlucken
    # und Duplikate wie BX2+BY2 mit gleichem Inhalt erzeugen.
    matches = list(re.finditer(r'<c r="([A-Z]+)%d"([^>]*?)(/>|>(.*?)</c>)' % r, content, re.S))
    cells = {}
    for cm in matches:
        if cm.group(3) == "/>":
            cells[cm.group(1)] = (cm.group(2), None)
        else:
            cells[cm.group(1)] = (cm.group(2), cm.group(4))
    return cells

def zeile_1_repl(row_attr: str, cells_by_col: dict) -> str:
    new_cells = []
    for c_idx in range(1, 14):
        c_name = col_name(c_idx)
        if c_name in cells_by_col:
            attr, body = cells_by_col[c_name]
            if c_name == "M":
                new_cells.append((13, zelle_text("M1", "Cotisation 2")))
            else:
                tag = f'<c r="{c_name}1"{attr}/>' if body is None else f'<c r="{c_name}1"{attr}>{body}</c>'
                new_cells.append((c_idx, tag))
    new_cells.append((14, zelle_text("N1", "Bezahlt J/N")))
    new_cells.append((15, zelle_text("O1", "Spielt J/R/N")))

    for c_name, (attr, body) in cells_by_col.items():
        idx = col_idx(c_name)
        if idx >= 14:
            new_idx = idx + 2
            new_c_name = col_name(new_idx)
            tag = f'<c r="{new_c_name}1"{attr}/>' if body is None else f'<c r="{new_c_name}1"{attr}>{body}</c>'
            new_cells.append((new_idx, tag))

    kopf_helfer = {SP["BX"]: "Manuell", SP["CE"]: "Cotisation_alt"}
    for spalte, titel, _m in HELFER:
        kopf_helfer[spalte] = titel
    for s, titel in kopf_helfer.items():
        new_cells.append((s, zelle_text(f"{col_name(s)}1", titel)))

    new_cells.sort(key=lambda x: x[0])
    max_c = new_cells[-1][0]
    clean_attr = re.sub(r'\sspans="[^"]*"', "", row_attr)
    return f'<row r="1" spans="1:{max_c}"{clean_attr}>' + "".join(c[1] for c in new_cells) + "</row>"
def zeile_daten_repl(r: int, row_attr: str, cells_by_col: dict, werte_l: dict) -> str:
    # Bereichsende = KAPAZITAET (nicht LETZTE), damit spaeter eingetragene
    # Mitglieder (Zeile > 773) in ihren Haushaltszaehlungen mitzaehlen.
    fmt = dict(r=r, e=ERSTE, l=KAPAZITAET)
    new_cells = []

    m_tuple = cells_by_col.get("M")
    m_body = m_tuple[1] if m_tuple else ""
    m_val_match = re.search(r'<v>(.*?)</v>', m_body or "")
    m_val = m_val_match.group(1) if m_val_match else ""
    m_is_shared = 't="s"' in (m_tuple[0] if m_tuple else "")

    for c_idx in range(1, 12):
        c_name = col_name(c_idx)
        if c_name in cells_by_col:
            attr, body = cells_by_col[c_name]
            tag = f'<c r="{c_name}{r}"{attr}/>' if body is None else f'<c r="{c_name}{r}"{attr}>{body}</c>'
            new_cells.append((c_idx, tag))

    # L: Neue Berechnungsformel für Cotisatioun
    f_l = esc(FORMEL_L.format(**fmt).lstrip("="))
    w_l = werte_l.get(r, "")
    l_stil = ' s="593"'
    if w_l and w_l.isdigit():
        z_l = f'<c r="L{r}"{l_stil}><f>{f_l}</f><v>{esc(w_l)}</v></c>'
    elif w_l:
        z_l = f'<c r="L{r}"{l_stil} t="str"><f>{f_l}</f><v>{esc(w_l)}</v></c>'
    else:
        z_l = f'<c r="L{r}"{l_stil}><f>{f_l}</f></c>'
    new_cells.append((12, z_l))

    # M: Bleibt erhalten (Cotisation 2)
    if "M" in cells_by_col:
        attr, body = cells_by_col["M"]
        tag = f'<c r="M{r}"{attr}/>' if body is None else f'<c r="M{r}"{attr}>{body}</c>'
        new_cells.append((13, tag))

    # N: Bezahlt J/N -> überall "N" voreintragen (zentriert, Stil 573 wie O).
    # Der Tresorier ändert bezahlte Zeilen manuell auf "J". Als Inline-Text,
    # damit kein sharedStrings-Eintrag nötig ist.
    new_cells.append((14, f'<c r="N{r}" s="573" t="inlineStr"><is>'
                         f'<t xml:space="preserve">N</t></is></c>'))

    # O: Spielt J/R/N
    if m_val:
        t_attr = ' t="s"' if m_is_shared else ''
        s_attr = ' s="573"'
        z_o = f'<c r="O{r}"{s_attr}{t_attr}><v>{m_val}</v></c>'
    else:
        z_o = zelle_leer(f"O{r}")
    new_cells.append((15, z_o))

    # Spalten >= N um +2 verschieben
    for c_name, (attr, body) in cells_by_col.items():
        idx = col_idx(c_name)
        if idx >= 14:
            new_idx = idx + 2
            new_c_name = col_name(new_idx)
            if body and "<f" in body:
                def f_repl(fm):
                    return f"<f>{shift_cell_ref(fm.group(1))}</f>"
                body_mod = re.sub(r'<f[^>]*>(.*?)</f>', f_repl, body)
            else:
                body_mod = body
            tag = f'<c r="{new_c_name}{r}"{attr}/>' if body_mod is None else f'<c r="{new_c_name}{r}"{attr}>{body_mod}</c>'
            new_cells.append((new_idx, tag))

    # Helferzellen BP..CE anhaengen (BX=Manuell bleibt bewusst leer)
    for spalte, _t, muster in HELFER:
        new_cells.append((spalte, zelle_formel(f"{col_name(spalte)}{r}", muster.format(**fmt))))
    new_cells.append((SP["BX"], zelle_leer(f"BX{r}")))

    # Sicherung der alten L-Formel nach CE
    l_tuple = cells_by_col.get("L")
    if l_tuple and l_tuple[1]:
        alt_l_val = re.search(r'<v>(.*?)</v>', l_tuple[1])
        if alt_l_val and alt_l_val.group(1).strip():
            new_cells.append((SP["CE"], f'<c r="CE{r}" t="inlineStr"><is><t xml:space="preserve">{alt_l_val.group(1)}</t></is></c>'))

    new_cells.sort(key=lambda x: x[0])
    max_c = new_cells[-1][0]
    clean_attr = re.sub(r'\sspans="[^"]*"', "", row_attr)
    return f'<row r="{r}" spans="1:{max_c}"{clean_attr}>' + "".join(c[1] for c in new_cells) + "</row>"

def baue_reserve_zeile(r: int) -> str:
    """Komplett ausgestattete Reservezeile fuer ein NEU eintragbares Mitglied.
    Enthaelt L-Formel, N='N' (Bezahlt) und alle Helfer BP..CE - ohne Cache-Wert,
    Excel rechnet beim Oeffnen (fullCalcOnLoad). Leere Zeilen liefern in L "",
    in BW "" und damit keine Stripe-Zeile."""
    fmt = dict(r=r, e=ERSTE, l=KAPAZITAET)
    zellen = [
        (12, f'<c r="L{r}" s="593"><f>{esc(FORMEL_L.format(**fmt).lstrip("="))}</f></c>'),
        (13, zelle_leer(f"M{r}")),
        (14, f'<c r="N{r}" s="573" t="inlineStr"><is>'
              f'<t xml:space="preserve">N</t></is></c>'),
        (15, zelle_leer(f"O{r}")),
    ]
    for spalte, _t, muster in HELFER:
        zellen.append((spalte, zelle_formel(f"{col_name(spalte)}{r}", muster.format(**fmt))))
    zellen.append((SP["BX"], zelle_leer(f"BX{r}")))
    zellen.sort(key=lambda x: x[0])
    return (f'<row r="{r}" spans="1:{SP["CE"]}">'
            + "".join(c[1] for c in zellen) + "</row>")


def fuege_reserve_zeilen_hinzu(s1_xml: str) -> str:
    """Haengt die Reservezeilen LETZTE+1..KAPAZITAET ans Ende von <sheetData>."""
    reserve = "".join(baue_reserve_zeile(r) for r in range(LETZTE + 1, KAPAZITAET + 1))
    if "</sheetData>" not in s1_xml:
        raise SystemExit("! kein </sheetData> in sheet1.xml")
    s1_xml = s1_xml.replace("</sheetData>", reserve + "</sheetData>", 1)
    print(f"Reservezeilen {LETZTE + 1}-{KAPAZITAET} hinzugefügt "
          f"({KAPAZITAET - LETZTE} Zeilen für neue Mitglieder).")
    return s1_xml


def transformiere_sheet1(s1_xml: str, werte_l: dict[int, str]) -> str:
    s1_xml = transformiere_cols(s1_xml)

    def zeile_repl(m):
        r = int(m.group(1))
        row_attr = m.group(2)
        content = m.group(3)
        cells_by_col = parse_cells(r, content)

        if r == 1:
            return zeile_1_repl(row_attr, cells_by_col)
        elif ERSTE <= r <= LETZTE:
            return zeile_daten_repl(r, row_attr, cells_by_col, werte_l)
        else:
            return m.group(0)

    s1_xml = re.sub(r'<row r="(\d+)"([^>]*)>(.*?)</row>', zeile_repl, s1_xml, flags=re.S)
    s1_xml = re.sub(r'<dimension ref="A1:[A-Z]+\d+"/>', f'<dimension ref="A1:CE{KAPAZITAET}"/>', s1_xml, count=1)
    # AutoFilter UND eingebettetes sortState gemeinsam auf BO erweitern
    # (altes BM -> BO = +2) und bis KAPAZITAET strecken, damit neu
    # eingetragene Zeilen mitfilterbar sind. xr:uid-Namespaces unangetastet.
    s1_xml = re.sub(r'ref="A1:BM772"', f'ref="A1:BO{KAPAZITAET}"', s1_xml)
    s1_xml = re.sub(r'ref="A2:BM772"', f'ref="A2:BO{KAPAZITAET}"', s1_xml)
    # Reservezeilen LETZTE+1 .. KAPAZITAET mit voller Formel-/Eingabeausstattung
    s1_xml = fuege_reserve_zeilen_hinzu(s1_xml)
    # Hyperlink-Anker >= N (Spalte 14) um +2 nach rechts (z.B. AV2 -> AX2).
    # Anker < 14 bleiben unberuehrt. r:id-Beziehungen bleiben gueltig.
    def _hyp_repl(m):
        pre, col, row, post = m.group(1), m.group(2), m.group(3), m.group(4)
        if col_idx(col) >= 14:
            col = col_name(col_idx(col) + 2)
        return f"{pre}{col}{row}{post}"
    s1_xml = re.sub(r'(<hyperlink ref=")([A-Z]+)(\d+)(")', _hyp_repl, s1_xml)
    return s1_xml

STRIPE_BLATT = "Stripe_Export"

STRIPE_KOPF = [
    ("A", "FamID", 18),
    ("B", "Rechnung_traegt", 22),
    ("C", "Betrag_EUR", 12),
    ("D", "Betrag_Text", 14),
    ("E", "Email", 30),
    ("F", "Nom", 20),
    ("G", "Prenom", 20),
    ("H", "Haushalt_Adress", 30),
    ("I", "Mitglieder", 12),
    ("J", "Bezahlt_JN", 11),
    ("K", "Stripe_Status", 16),
    ("L", "Stripe_Link", 30),
    ("M", "Bemerkung", 30),
]

# Eine Exportzeile pro Membres-Zeile: zeigt nur TRAEGER-Haushalte mit Betrag,
# sonst leer (per Filter ausblendbar). GAJGL-Haushalte (Q="GAJGL") sind reine
# Info-Zeilen in der Mitgliederliste und erscheinen NIE im Export.
# Keine Matrix-Formeln -> robust in allen Excel-Versionen UND Google Sheets.
# K/L/M sind manuell (Stripe-Status, -Link, Bemerkung) und gehoeren dem Stripe-Skript.
def baue_stripe_sheet(dxf_hellblau: int, dxf_gruen: int) -> str:
    kopf = "".join(zelle_text(f"{c}1", t) for c, t, _w in STRIPE_KOPF)
    cols = "".join(
        f'<col min="{i + 1}" max="{i + 1}" width="{w}" customWidth="1"/>'
        for i, (_c, _t, w) in enumerate(STRIPE_KOPF))
    zeilen = [f'<row r="1">{kopf}</row>']
    for r in range(ERSTE, KAPAZITAET + 1):  # direkt an Membres-Zeile gekoppelt
        q = f"'{BLATT}'!"   # Blattname dynamisch (siehe blattname_lesen)
        # Rechnungsfaehig = Haushaltstraeger ODER zeilen-eigener Betrag.
        #   BX = manuelle Vorgabe, CB = Personenwert/Ausnahme, CD = XSEULwert.
        # Warum das zweite Tor noetig ist: alle XSEUL-Zeilen teilen sich den
        # BP-Wert "XSEUL" und haben damit nur EINEN Traeger (BW). Mit der
        # reinen Traeger-Bedingung kaemen 71 von 73 XSEUL-Rechnungen (je 300 EUR)
        # nicht in den Export, obwohl in L ein Betrag steht.
        bed = (f'{q}$L{r}<>"",{q}$Q{r}<>"GAJGL",'
               f'OR({q}$BW{r}="TRAEGER",{q}$BX{r}<>"",{q}$CB{r}<>"",{q}$CD{r}<>"")')
        # C: payable amount as a NUMBER for Stripe. VALUE() alone is not
        # enough: L can be text, and VALUE fails on it, which left the
        # amount empty in Stripe for 34 of 234 invoices:
        #   "(0+50)"       -> 50   (0 base + 50 surcharge = 50 payable)
        #   "210 (+0+50)"  -> 210  (the +50 is a COMPONENT of 210, not extra)
        #   "Don ? …"      -> ""   (unknown, handled manually)
        parse = (f'IFERROR(IF(ISNUMBER(VALUE({q}$L{r})),VALUE({q}$L{r}),'
                 f'IF(LEFT({q}$L{r},1)="(",'
                 f'VALUE(MID({q}$L{r},FIND("+",{q}$L{r})+1,'
                 f'FIND(")",{q}$L{r})-FIND("+",{q}$L{r})-1)),'
                 f'VALUE(LEFT({q}$L{r},FIND("(",{q}$L{r})-1)))),"")')
        zellen = [
            # A: FamID des Traegers
            zelle_formel(f"A{r}", f'=IF(AND({bed}),{q}$BP{r},"")'),
            # B: "Nom Prenom" des Traegers
            zelle_formel(f"B{r}", f'=IF($A{r}="","",{q}$A{r}&" "&{q}$B{r})'),
            # C: payable amount as NUMBER (Parser siehe oben), D: Rohtext
            zelle_formel(f"C{r}", f'=IF($A{r}="","",{parse})'),
            # D: Betrag-Rohtext (zeigt auch "(0+50)", "Don ? …", Familien-Codes)
            zelle_formel(f"D{r}", f'=IF($A{r}="","",{q}$L{r}&"")'),
            # E: Email des Traegers (AX)
            zelle_formel(f"E{r}", f'=IF($A{r}="","",{q}$AX{r})'),
            # F/G: Nom / Prenom einzeln
            zelle_formel(f"F{r}", f'=IF($A{r}="","",{q}$A{r})'),
            zelle_formel(f"G{r}", f'=IF($A{r}="","",{q}$B{r})'),
            # H: Adresse (G)
            zelle_formel(f"H{r}", f'=IF($A{r}="","",{q}$G{r})'),
            # I: Mitglieder im Haushalt (bis KAPAZITAET -> Neuzugaenge zaehlen mit)
            zelle_formel(f"I{r}", f'=IF($A{r}="","",COUNTIF({q}$BP${ERSTE}:$BP${KAPAZITAET},$A{r}))'),
            # J: Bezahlt-Status (N) - "N"/"J" wandert automatisch mit
            zelle_formel(f"J{r}", f'=IF($A{r}="","",{q}$N{r})'),
            # K/L/M: manuell (Stripe-Status, -Link, Bemerkung)
            zelle_leer(f"K{r}"),
            zelle_leer(f"L{r}"),
            zelle_leer(f"M{r}"),
        ]
        zeilen.append(f'<row r="{r}">' + "".join(zellen) + "</row>")
    koerper = "".join(zeilen)
    # Gleiche Markierung wie im Datenblatt: offen = hellblau (dxfId 2),
    # bezahlt = gruen (dxfId 0 = vorhandener Gruen-Eintrag der Mappe).
    cf_stripe = (
        f'<conditionalFormatting sqref="J{ERSTE}:J{KAPAZITAET}">'
        f'<cfRule type="expression" dxfId="{dxf_gruen}" priority="1" stopIfTrue="1">'
        f'<formula>AND($A{ERSTE}&lt;&gt;&quot;&quot;,$J{ERSTE}="J")</formula></cfRule>'
        f'<cfRule type="expression" dxfId="{dxf_hellblau}" priority="2">'
        f'<formula>$A{ERSTE}&lt;&gt;&quot;&quot;</formula></cfRule>'
        f'</conditionalFormatting>')
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            f'<dimension ref="A1:M{KAPAZITAET}"/><sheetViews><sheetView workbookViewId="0"/>'
            '</sheetViews><sheetFormatPr defaultRowHeight="15"/>'
            f'<cols>{cols}</cols><sheetData>{koerper}</sheetData>'
            # Schema-Reihenfolge: sheetData -> autoFilter -> conditionalFormatting
            f'<autoFilter ref="A1:M{KAPAZITAET}"/>{cf_stripe}</worksheet>')

HELLBLAU_FILL = "FFBDD7EE"  # hellblau (Hintergrund für Spalte N bei fälligem Betrag)
GRUEN_FILL = "FFB7E1CD"     # vorhandener Gruen-Eintrag (dxfId 0) = bezahlt
ROT_FILL = "FFFFC7CE"       # Warnrot: Spalte O enthaelt einen undefinierten Wert

# Offen (nicht bezahlt): Betrag in L, aber kein Fxxxx-Code, kein XSEUL/GAJGL.
# $Q<>"GAJGL" schliesst die reinen Infozeilen aus - sie werden nie berechnet
# (gleiche Regel wie im Stripe_Export) und sollen deshalb auch nicht blau sein.
CF_FORMEL_N = ('AND($L2&lt;&gt;&quot;&quot;,LEFT($L2,1)&lt;&gt;&quot;F&quot;,'
               '$L2&lt;&gt;&quot;XSEUL&quot;,$L2&lt;&gt;&quot;GAJGL&quot;,$Q2&lt;&gt;&quot;GAJGL&quot;,$N2&lt;&gt;&quot;J&quot;)')
# Bezahlt: gleiche Bedingung, aber N = "J".
CF_FORMEL_N_BEZAHLT = ('AND($L2&lt;&gt;&quot;&quot;,LEFT($L2,1)&lt;&gt;&quot;F&quot;,'
                       '$L2&lt;&gt;&quot;XSEUL&quot;,$L2&lt;&gt;&quot;GAJGL&quot;,$Q2&lt;&gt;&quot;GAJGL&quot;,$N2=&quot;J&quot;)')


def fuege_cf_hinzu(teile: dict) -> int:
    """Bedingte Formatierung N2:N<Kapazitaet> im Datenblatt:
    hellblau = offener Betrag, gruen = vom Tresorier auf J gesetzt.
    Fxxxx-Codes, XSEUL/GAJGL und leere Zeilen bleiben weiss.
    Gibt die dxfId des Hellblau-Eintrags zurueck (fuer das Stripe-Blatt)."""
    # 1) styles.xml: neuen dxf-Eintrag mit Hellblau-Füllung anhängen
    st = teile["xl/styles.xml"].decode("utf-8")
    m = re.search(r'<dxfs count="(\d+)">(.*?)</dxfs>', st, re.S)
    if not m:
        raise SystemExit("! kein <dxfs>-Block in styles.xml gefunden")
    count = int(m.group(1))
    # WICHTIG: fgColor UND bgColor auf denselben Wert setzen (wie die
    # bestehenden dxf-Einträge). Ein indexed-bgColor (z.B. 64) rendert in
    # Excel als Schwarz statt der gewünschten Füllfarbe.
    neuer_dxf = (f'<dxf><fill><patternFill patternType="solid">'
                 f'<fgColor rgb="{HELLBLAU_FILL}"/>'
                 f'<bgColor rgb="{HELLBLAU_FILL}"/>'
                 f'</patternFill></fill></dxf>')
    # Warnrot fuer undefinierte Werte in Spalte O (darf dort nur J/R/N stehen).
    rot_dxf = (f'<dxf><font><color rgb="FF9C0006"/></font><fill><patternFill '
               f'patternType="solid"><fgColor rgb="{ROT_FILL}"/>'
               f'<bgColor rgb="{ROT_FILL}"/></patternFill></fill></dxf>')
    st = (st[:m.start()] +
          f'<dxfs count="{count + 2}">' + m.group(2) + neuer_dxf + rot_dxf + '</dxfs>' +
          st[m.end():])
    teile["xl/styles.xml"] = st.encode("utf-8")

    # 2) sheet1.xml: <conditionalFormatting> zwischen </autoFilter> und <hyperlinks>
    #    (Schema-Reihenfolge: sheetData, autoFilter, conditionalFormatting, hyperlinks)
    s1 = teile["xl/worksheets/sheet1.xml"].decode("utf-8")
    cf = (f'<conditionalFormatting sqref="N{ERSTE}:N{KAPAZITAET}">'
          f'<cfRule type="expression" dxfId="0" priority="1" stopIfTrue="1">'
          f'<formula>{CF_FORMEL_N_BEZAHLT}</formula></cfRule>'
          f'<cfRule type="expression" dxfId="{count}" priority="2">'
          f'<formula>{CF_FORMEL_N}</formula>'
          f'</cfRule></conditionalFormatting>')
    # Spalte O: alles ausser J/R/N (und leer) wird rot. Ohne diese Warnung
    # verschluckt z. B. ein "X" still eine Rechnung ueber 210-384 EUR, weil
    # weder "J" (Spieler) noch "R"/"N" (Reserve) in irgendeiner Formel steht.
    cf_o = (f'<conditionalFormatting sqref="O{ERSTE}:O{KAPAZITAET}">'
            f'<cfRule type="expression" dxfId="{count + 1}" priority="3">'
            f'<formula>AND($O{ERSTE}&lt;&gt;&quot;&quot;,$O{ERSTE}&lt;&gt;&quot;J&quot;'
            f',$O{ERSTE}&lt;&gt;&quot;R&quot;,$O{ERSTE}&lt;&gt;&quot;N&quot;)</formula>'
            f'</cfRule></conditionalFormatting>')
    cf_blöcke = cf + cf_o
    if "<conditionalFormatting" in s1:
        raise SystemExit("! sheet1.xml enthält bereits conditionalFormatting")
    if "<hyperlinks>" in s1:
        s1 = s1.replace("<hyperlinks>", cf_blöcke + "<hyperlinks>", 1)
    elif "</autoFilter>" in s1:
        s1 = s1.replace("</autoFilter>", "</autoFilter>" + cf_blöcke, 1)
    else:
        s1 = s1.replace("</sheetData>", "</sheetData>" + cf_blöcke, 1)
    teile["xl/worksheets/sheet1.xml"] = s1.encode("utf-8")
    print(f"CF Datenblatt: N{ERSTE}:N{KAPAZITAET} offen=hellblau (dxfId={count}), "
          f"bezahlt=grün (dxfId=0); O{ERSTE}:O{KAPAZITAET} undefiniert=rot "
          f"(dxfId={count + 1}).")
    return count

def baue_komplett():
    print("Baue neue Arbeitsmappe mit vollständigem Layout...")
    teile, reihenfolge, s1_xml, shared_strings, werte_l = baue_neue_arbeitsmappe()

    print("Transformiere sheet1.xml (Spalten N/O einfügen, L neu, Helfer anhängen)...")
    neues_s1 = transformiere_sheet1(s1_xml, werte_l)
    teile["xl/worksheets/sheet1.xml"] = neues_s1.encode("utf-8")

    print("Füge bedingte Formatierung hinzu (N hellblau bei Betrag in L)...")
    dxf_hellblau = fuege_cf_hinzu(teile)   # legt den Hellblau-dxf an, liefert dxfId
    dxf_gruen = 0                          # vorhandener Gruen-Eintrag in der Mappe

    print("Füge Stripe_Export-Blatt hinzu...")
    stripe_part = "xl/worksheets/sheet14.xml"
    teile[stripe_part] = baue_stripe_sheet(dxf_hellblau, dxf_gruen).encode("utf-8")
    reihenfolge.append(stripe_part)
    rid_stripe = "rIdStripeExport"
    wb2 = teile["xl/workbook.xml"].decode("utf-8")
    wb2 = wb2.replace("</sheets>",
                     f'<sheet name="{STRIPE_BLATT}" sheetId="14" r:id="{rid_stripe}"/></sheets>')
    teile["xl/workbook.xml"] = wb2.encode("utf-8")
    rels2 = teile["xl/_rels/workbook.xml.rels"].decode("utf-8")
    rels2 = rels2.replace("</Relationships>",
                          f'<Relationship Id="{rid_stripe}" Type="http://schemas.openxmlformats.org/'
                          f'officeDocument/2006/relationships/worksheet" '
                          f'Target="worksheets/sheet14.xml"/></Relationships>')
    teile["xl/_rels/workbook.xml.rels"] = rels2.encode("utf-8")
    ct2 = teile["[Content_Types].xml"].decode("utf-8")
    ct2 = ct2.replace("</Types>",
                      f'<Override PartName="/{stripe_part}" ContentType="application/vnd.openxmlformats-'
                      f'officedocument.spreadsheetml.worksheet+xml"/></Types>')
    teile["[Content_Types].xml"] = ct2.encode("utf-8")
    if "docProps/app.xml" in teile:
        app2 = teile["docProps/app.xml"].decode("utf-8")
        blaetter2 = re.findall(r'<sheet name="([^"]+)"', wb2)
        titel2 = re.findall(r"<vt:lpstr>([^<]*)</vt:lpstr>",
                            re.search(r"<TitlesOfParts>(.*?)</TitlesOfParts>", app2, re.S).group(1))
        letztes2 = [t for t in reversed(titel2) if t in blaetter2][-1]
        app2 = re.sub(r"(Arbeitsblätter</vt:lpstr></vt:variant><vt:variant><vt:i4>)(\d+)(</vt:i4>)",
                      lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app2, count=1)
        app2 = re.sub(r'(<TitlesOfParts><vt:vector size=")(\d+)(")',
                      lambda m: m.group(1) + str(int(m.group(2)) + 1) + m.group(3), app2, count=1)
        app2 = app2.replace(f"<vt:lpstr>{letztes2}</vt:lpstr>",
                            f"<vt:lpstr>{letztes2}</vt:lpstr><vt:lpstr>{STRIPE_BLATT}</vt:lpstr>", 1)
        teile["docProps/app.xml"] = app2.encode("utf-8")

    # SICHERUNG: der Build erzeugt die Mappe immer NEU aus dem Original. Alles,
    # was der Tresorier zwischendurch eingetragen hat (Spalte N = J, neue
    # Mitglieder, Notizen) liegt NUR in der bisherigen Datei und waere beim
    # Ueberschreiben weg. Deshalb vorher eine Kopie mit Zeitstempel ablegen.
    if ZIEL.exists():
        zeit = datetime.now().strftime("%Y-%m-%d_%H%M")
        sicherung = ZIEL.with_name(f"{ZIEL.stem}.backup-{zeit}{ZIEL.suffix}")
        sicherung.write_bytes(ZIEL.read_bytes())
        print(f"Sicherung der bisherigen Mappe: {sicherung.name}")
        ZIEL.unlink()
    with zipfile.ZipFile(ZIEL, "w", zipfile.ZIP_DEFLATED) as zout:
        for name in reihenfolge:
            if name in teile:
                zout.writestr(name, teile[name])

    print(f"Erfolgreich geschrieben: {ZIEL}")
    print(f"Größe: {ZIEL.stat().st_size} Bytes")

if __name__ == "__main__":
    baue_komplett()

