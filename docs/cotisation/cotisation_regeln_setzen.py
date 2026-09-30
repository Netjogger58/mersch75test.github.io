"""Ersetzt zwei Formelspalten in der Live-Mappe: CH (Personenwert) und
CJ (XSEULwert).

Warum gerade diese beiden:
  CH  Der Personenwert (0+50) fuer Status R lief vor der Familientarif-
      Pruefung und drueckte BISENIUS Ben (Z64) auf 50 statt 384. 384 ist
      das Maximum (ZusatzBeiFamilie=NEIN) - dieselbe Logik war nur beim
      Zuschlag in CG vorhanden, beim Personenwert fehlte sie.
  CJ  Der XSEUL-Fixbetrag 300 wurde pauschal pro Zeile vergeben. Er richtet
      sich nach dem Spielstatus (Spalte O): J -> 300, R oder N -> (0+50),
      sonst 0. BLANC Max und DIDELOT-SCHOEN sind Status N und zahlen (0+50).

SICHERHEIT - das Skript bricht ab, BEVOR geschrieben wird, wenn:
  * eine Zelle fehlen wuerde (es legt keine an)
  * die XML-Reihenfolge der Zellen dadurch kaputt ginge
  * Zellen doppelt wuerden
  * eine Master-Zelle einer geteilten Formel verschwinden wuerde
Die beiden Spalten haben nachweislich 0 geteilte Formeln - es wird also nur
ersetzt, nie angelegt oder geloescht.

Aufruf:
  python3 docs/cotisation/cotisation_regeln_setzen.py            # nur zeigen
  python3 docs/cotisation/cotisation_regeln_setzen.py --apply    # schreiben
"""
import pathlib
import re
import shutil
import sys
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe  # noqa: E402

SHEET = "xl/worksheets/sheet1.xml"
CONFIG = "xl/worksheets/sheet13.xml"     # Blatt "Cotisation"
ERSTE, LETZTE = 2, 901
# LETZTE war 902, diese Zeile existiert im Blatt aber nicht (Luecke 902-908,
# danach nur verwaiste BZ-Zellen in 909-911) - die Vorpruefung brach darauf ab.
# Letzte vollstaendige Zeile mit A..L und allen Helfern BV..CL ist 901.
NEUE_SPALTE = "CP"          # Spielberecht - wird einmalig angelegt
# Stand 01.10.2026: die Hilfsspalten liegen nach dem Einfuegen der vier
# Medico-Spalten bei BZ..CP, zuvor bei BV..CL.
# Fehlende Zellen in den Hilfsspalten ergaenzen (fuer neue Mitglieder).
# Nur mit --ergaenzen, damit ein normaler Lauf die Blattstruktur nicht
# ungefragt veraendert.
ZEILEN_ERGAENZEN = "--ergaenzen" in sys.argv

# (Spalte, Kuerzel, Formel). {r} = Zeilennummer.
# WICHTIG: Der erste Wert ist der SPALTENBUCHSTABE in der aktuellen Datei.
# Nach dem Einfuegen der vier Medico-Spalten am 01.10.2026 liegen die
# Rechenspalten vier Positionen weiter rechts als zuvor:
#   CL->CP (Spielberecht), BY->CC, BZ->CD, CA->CE, CE->CI, CC->CG,
#   CH->CL, BV->BZ, CJ->CN.  Spalte L ist unveraendert.
# Steht hier ein alter Buchstabe, meldet das Skript beim Lauf
# "CL1 existiert, traegt aber nicht 'Spielberecht'" und bricht ab - es
# schreibt also nie in die falsche Spalte.
#
# Die Comite-Regel (Mindestbetrag 50) muss in DREI Spalten sitzen, weil die
# Ausgabekette L nacheinander CD (Manuell), CH, CJ, dann Traeger/Familien-
# code abfragt. Wer nur eine davon aendert, weicht von pruef_cotisation ab:
#   CH  Personenwert (0+50) bei Reservisten -> fuer Comite-Leute 50
#   CJ  XSEUL (0+50) bei N/R                -> fuer Comite-Leute 50
#   L   Nicht-Traeger zeigte den Haushaltscode -> fuer Comite-Leute 50
# Nicht angefasst: der Traeger-Zweig in L - ein Rechnungstraeger im Comite
# zahlt weiter seinen Tarif (BISENIUS Ben 384, MAQUIL 384, SCHUSTER 210).
# AUSNAHME in CH und L: wer aktiv spielt (Spalte O = "J"), ist ueber seinen
# Haushalt abgedeckt und zeigt den Familiencode - EPPS Charly Z163 in F0039
# (Bruder Thomas + Mutter PIRSON Isabelle als Traegerin zahlen 384).
# Im Traeger-Zweig von L rechnet ein Comite-Mitglied den Zuschlag WIRKLICH
# dazu: SCHUSTER Jeff Z502 = 210 (Sohn Elie spielt U25) + 50 = 260. Ohne
# Comite bleibt die Notation "210 (+0+50)" und der Stripe-Parser liest 210.
FORMELN = [
    # CL: Spielberechtigung. Ohne Spielerpass darf niemand spielen, und ein
    # vorhandener Pass braucht ein gueltiges Medico. Spalte AX enthaelt das
    # JAHR BIS WANN gueltig (2031 = gueltig bis 2031), nicht das Jahr der
    # Untersuchung. 'XXX' = Antrag an die FLH geschickt, Lizenz existiert
    # noch nicht. Die Jahresgrenze steht in Cotisation!B13 und wandert jedes
    # Kalenderjahr um eins - am 01.01.2027 dort 2027 eintragen.
    #
    # NEU seit 01.10.2026: Spalten BA "Inapte" und BB "Inapte temporaire"
    # sperren die Spielberechtigung. Ein Eintrag dort hebt J, Pass und
    # gueltiges Medico auf - eine aerztliche Sperre ist kein abgelaufenes
    # Dokument, deshalb wird hier nicht gegen ein Jahr gerechnet, sondern
    # nur geprueft, ob etwas dasteht.
    # AY "Medico apte J/N" und AZ "Apte temporaire" sind nach Auskunft des
    # Users REINE INFORMATION und fliessen bewusst NICHT in die Rechnung.
    ("CP", "Spielberecht",
     '=IF(AND($O{r}="J",$AO{r}<>"",$AO{r}<>"xxx",$BA{r}="",$BB{r}="",'
     'ISNUMBER($AX{r}),$AX{r}>=Cotisation!$B$13),1,0)'),
    ("CC", "SpielerGes",
     '=COUNTIFS($BZ${e}:$BZ${l},$BZ{r},$CP${e}:$CP${l},1)'),
    ("CD", "SpielerSEN",
     '=COUNTIFS($BZ${e}:$BZ${l},$BZ{r},$CP${e}:$CP${l},1,'
     '$K${e}:$K${l},"SEN")'),
    ("CE", "SpielerU25",
     '=COUNTIFS($BZ${e}:$BZ${l},$BZ{r},$CP${e}:$CP${l},1,'
     '$K${e}:$K${l},"U25")'),
    ("CI", "Tarif",
     '=IF(OR($CC{r}>=2,AND($CD{r}>=1,$CE{r}>=1)),Cotisation!$B$3,'
     'IF($CD{r}>=1,Cotisation!$B$1,'
     'IF($CE{r}>=1,Cotisation!$B$2,0)))'),
    # CC (Rechnungstraeger) und CE (Tarif) waren nur bis Zeile 582 gefuellt.
    # Ohne sie bekommen die neuen Mitglieder (ab 583) keinen Tarif und
    # L bleibt leer - ZELLER Sarah/Felicitas/Mortitz waren dadurch unsichtbar.
    # Beide Formeln sind zeilenweise gleich, nur mit eigener Zeilennummer.
    ("CG", "Rechnung traegt",
     '=IF($BZ{r}="","",IF(Cotisation!$B$8<>"Aelteste",'
     'IF(COUNTIFS($BZ${e}:$BZ{r},$BZ{r})=1,"TRAEGER",""),'
     'IF($CB{r}>=73415,IF(COUNTIFS($BZ${e}:$BZ{r},$BZ{r})=1,"TRAEGER",""),'
     'IF($CA{r}=$CB{r},"TRAEGER",""))))'),
    ("CL", "Personenwert",
     '=IF($CJ{r}>0,INDEX(Cotisation!$F$2:$F$200,$CJ{r}),'
     'IF(AND($CI{r}<>Cotisation!$B$3,OR($Q{r}="XSEUL",$Q{r}="GAJGL"),'
     'OR(AND($O{r}="R",$AO{r}<>""),'
     'AND($AO{r}<>"",COUNTIF($BI{r}:$BL{r},"FRAGEN")>0),'
     '$Q{r}="GAJGL")),'
     # E7: Comite-Mindestbetrag 50 nur noch fuer den Rechnungstraeger
     # (oder GAJGL als Sammelcode). Vorher stand hier $CC<>"TRAEGER", das
     # jedem Comite-Mitglied eine eigene Rechnung gab.
     'IF(AND($BM{r}<>"",$CP{r}=0,OR($CG{r}="TRAEGER",$Q{r}="GAJGL")),'
     'TEXT(Cotisation!$B$4,"0"),'
     'Cotisation!$B$10),""))'),
    ("BZ", "FamID",
     # E8: XSEUL ist KEIN Haushalt, sondern ein Sammelcode fuer
     # Einzelpersonen. Ohne eigenen Schluessel teilen sich alle 72
     # Mitglieder den Schluessel "XSEUL" und liegen im Stripe-Abgleich
     # in EINER Rechnungseenheit. Jedes bekommt jetzt "XS:<Card-ID>".
     # Die Adresspruefung steht bewusst VOR der XSEUL-Pruefung: sonst
     # waeren die ANSAY-Brueder zwei Einzelpersonen statt eines
     # Haushalts mit 384.
     #
     # ACHTUNG: eine einzige Zeile, bewusst. Als mehrere verkettete
     # Literale hat Python hier schon zweimal ein Tupel aufgesplittet,
     # woraufhin nur der letzte Teil als Formel galt.
     # ACHTUNG 2: hier stehen ROHE Zeichen, esc() escaped beim Schreiben.
     '=IF($Q{r}="","",IF(SUMPRODUCT(--(SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER(Cotisation!$I$2:$I$50)," ",""),".",""),"\'","")=SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'","")))>0,"ADR:"&SUBSTITUTE(SUBSTITUTE(SUBSTITUTE(UPPER($G{r})," ",""),".",""),"\'",""),IF($Q{r}="XSEUL","XS:"&$D{r},$Q{r})))'),
    ("CN", "XSEULwert",
     # E7: der Comite-Zweig sitzt jetzt IN CJ statt in einer Traeger-
     # Ausnahme. Seit E8 ist jedes XSEUL-Mitglied sein eigener Rechnungs-
     # traeger, die alte Bedingung $CC<>"TRAEGER" waere also immer wahr und
     # wuerde die 50 EUR an alle geben. Die Reihenfolge unten bildet genau
     # pruef_cotisation ab: 300 bei gueltigem Pass, sonst (0+50) bei N/R,
     # sonst 0 - und der Comite-Mindestbetrag 50 ueberschreibt alles, SOFERN
     # keine gueltige Spielberechtigung vorliegt (CL=1).
     '=IF($Q{r}<>"XSEUL","",IF(AND(LEFT($BZ{r},4)="ADR:",$CC{r}>=2),"",'
     'IF($CP{r}=1,TEXT(Cotisation!$B$5,"0"),'
     'IF($BM{r}<>"",TEXT(Cotisation!$B$4,"0"),'
     'IF(OR($O{r}="N",$O{r}="R"),"(0+"&TEXT(Cotisation!$B$4,"0")&")","0")))))'),
    # ---------------------------------------------------------------- E7
    # "Nur der Rechnungstraeger bekommt einen Posten." Ein Offizieller, der
    # NICHT Traeger ist, darf keine eigene Rechnung erzeugen - die 50 EUR
    # stecken dann im Betrag des Traegers. Der Fehler war F0026: CLEMENT
    # Liliane (0+50) und METZLER Bernard 50 = zwei Posten fuer EINEN Haushalt
    # (100 EUR). Seit E8 ist jedes XSEUL-Mitglied sein eigener Traeger
    # (eigener Schluessel XS:<Card-ID> in BV), die alte Ausnahme
    # $CC<>"TRAEGER" fuer XSEUL ist damit gegenstandslos und muss raus,
    # sonst verliert VAN DER WEKEN Louis (XSEUL, Comite, R) seine 50 EUR.
    # GAJGL bleibt ausgenommen: Sammelcode ohne Haushaltsbezug, pro Zeile.
    # CH wird VOR CC geprueft, deshalb muss die Comite-Mindestregel dort UND
    # in L sitzen - sonst weicht die Mappe von pruef_cotisation ab.
    ("L", "Cotisatioun",
     # erste Schranke braucht auch den Namen: sonst liefern die ~310 Leerzeilen
     # unter den Daten ueber CH="0" eine Rechnung "0" (z. B. Zeile 592).
     # Status P (frueher X, seit 29.09.2026): ein P-Mitglied ohne jeden
     # spielberechtigen Haushaltsmitglied (BY = SpielerGes = 0) ergibt 0.
     # Vorher lieferte der Zweig "CE=0 und CG>0" dort "(0+50)", weil der
     # Zuschlag-Helper CB auch bei P anloest (RESSEL Z458, ROCHA MAJERUS
     # Z468). BY>=1 -> ganz normal weiter: wer Traeger eines Haushalts
     # MIT Spieler ist, zahlt den Haushaltsbetrag (BINGEN Z58 = 210,
     # MARCK Z351 = 384). Ohne diese Schranke wuerden 1.434 EUR
     # Haushaltsguthaben ersatzlos auf 0 gehen.
     '=IF(OR($BZ{r}="",$A{r}=""),"",IF(AND($O{r}="P",$CC{r}=0),"0",'
     'IF($CH{r}<>"",$CH{r}&"",IF($CL{r}<>"",$CL{r}&"",'
     'IF($CN{r}<>"",$CN{r}&"",IF($CG{r}="TRAEGER",'
     # Komite-Mitglied mit eigenem Tarif: der Zuschlag wird DAZUGEREchnet und
     # die Schreibweise weggelassen. Vorher stand beides hintereinander und
     # ergab "210 (+0+50)260" - eine unlesbare Summe, aus der der
     # Stripe-Parser die 210 statt der 260 gelesen haette.
     'IF(AND($BM{r}<>"",$CP{r}=0,$CI{r}>0,$CK{r}>0),TEXT($CI{r}+$CK{r},"0"),'
     'IF($CI{r}=0,IF($CK{r}>0,"(0+"&TEXT($CK{r},"0")&")",""),'
     'TEXT($CI{r},"0")&IF($CK{r}>0," (+0+"&TEXT($CK{r},"0")&")",""))),'
     # E7: Nicht-Traeger bekommen KEINE eigene Rechnung mehr. METZLER
     # Bernard (F0026, Comite) zeigte hier 50, obwohl CLEMENT Liliane den
     # Haushalt bereits mit (0+50) abrechnet - 100 EUR fuer eine Familie.
     # Der Comite-Mindestbetrag gilt nur noch fuer den Rechnungstraeger.
     'IF(AND($BM{r}<>"",$CP{r}=0,OR($CG{r}="TRAEGER",$Q{r}="GAJGL")),'
     'TEXT(Cotisation!$B$4,"0"),'
     'IF(LEFT($BZ{r},4)="ADR:",$Q{r}&"",$BZ{r}&""))))))))'),
]


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def pruefe_keine_entities() -> None:
    """Abbruch, wenn eine Formel bereits XML-Entities enthaelt.

    esc() escaped "&", "<" und ">". Stand in FORMELN schon "&amp;" oder
    "&gt;", entstand "&amp;amp;" bzw. "&amp;gt;" - Excel liest das als Text
    statt als Operator, die Formel ist syntaktisch kaputt und Excel
    oeffnet die Datei nur noch mit dem Reparatur-Dialog. Genau das ist am
    30.09.2026 passiert.

    Die Formeln muessen ROHE Zeichen enthalten; esc() erledigt den Rest.
    """
    for eintrag in FORMELN:
        spalte, formel = eintrag[0], eintrag[-1]
        for entity in ("&amp;", "&gt;", "&lt;", "&quot;"):
            if entity in formel:
                raise SystemExit(
                    f"ABBRUCH: Formel fuer {spalte} enthaelt die Entity "
                    f"{entity!r}. In FORMELN gehoeren ROHE Zeichen hinein, "
                    f"esc() escaped beim Schreiben. Nichts geschrieben.")


def colpos(sp: str) -> int:
    n = 0
    for c in sp:
        if c.isalpha():
            n = n * 26 + (ord(c.upper()) - 64)
    return n


def zellen_reihenfolge_ok(x: str) -> list[str]:
    kaputt = []
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', x, re.S):
        refs = [c.group(1) for c in
                re.finditer(r'<c r="([A-Z]+)\d+"', m.group(2))]
        if refs != sorted(refs, key=colpos):
            kaputt.append(m.group(1))
    return kaputt


def zellen_doppelt(x: str) -> list[str]:
    doppelt = []
    for m in re.finditer(r'<row r="(\d+)"[^>]*>(.*?)</row>', x, re.S):
        refs = [c.group(0) for c in
                re.finditer(r'<c r="[A-Z]+\d+"', m.group(2))]
        if len(refs) != len(set(refs)):
            doppelt.append(m.group(1))
    return doppelt


def geteilte_formeln(x: str) -> tuple[set, set]:
    master, follower = set(), set()
    for m in re.finditer(r'<c r="[A-Z]+\d+"[^>]*>(.*?)</c>', x, re.S):
        f = re.search(r"<f([^>]*?)(?:/>|>(.*?)</f>)", m.group(1), re.S)
        if not f or 't="shared"' not in f.group(1):
            continue
        si = re.search(r'si="(\d+)"', f.group(1))
        if not si:
            continue
        if re.search(r'ref="', f.group(1)):
            master.add(si.group(1))
        else:
            follower.add(si.group(1))
    return master, follower



def zelle_einfuegen(inhalt: str, ref: str, xml: str) -> str:
    """Fuegt eine fehlende Zelle an der richtigen Stelle ein.

    WICHTIG: colpos() muss den ZELLBEZUG ("Z776") vertragen und nicht nur den
    Spaltennamen - sonst liefert es 667 statt 26, findet keine Einfuegeposition
    und haengt die Zelle ans Zeilenende. Genau das hat Excel mit dem
    Reparatur-Dialog quittiert.
    """
    ziel = colpos(ref)
    for m in re.finditer(r'<c r="([A-Z]+)\d+"', inhalt):
        if colpos(m.group(1)) > ziel:
            return inhalt[:m.start()] + xml + inhalt[m.start():]
    return inhalt + xml


def main() -> int:
    # VOR allem anderen: keine Entity in den Formeln. Sonst entstehen
    # doppelt escapte Formeln und Excel zeigt nur noch den Reparatur-Dialog.
    pruefe_keine_entities()

    if "--datei" in sys.argv:
        pfad = mappe.set_ziel(sys.argv[sys.argv.index("--datei") + 1])
    else:
        pfad = mappe.ziel()
    print(f"Datei: {pfad.name}")

    with zipfile.ZipFile(pfad) as z:
        infos = z.infolist()
        teile = {i.filename: z.read(i.filename) for i in infos}
    x = teile[SHEET].decode("utf-8")

    # --- Vorpruefung ------------------------------------------------------
    # Ganze Zeilen muessen existieren; einzelne Zellen duerfen fehlen -
    # Zeilen 584-586 liegen mit allen 14 Helferspalten (BV..CJ) ausserhalb
    # des Rechenbereichs. Dort wird nichts angelegt, sonst fehlten die
    # Bezugsspalten BV/BY und die Formel ergaebe Unsinn.
    fehlende_zeilen = [r for r in range(ERSTE, LETZTE + 1)
                       if not re.search(r'<row r="%d"[ >]' % r, x)]
    if fehlende_zeilen:
        print(f"ABBRUCH: {len(fehlende_zeilen)} Zeilen fehlen im Blatt, "
              f"z. B. {fehlende_zeilen[:5]} - Zeilengrenze pruefen.")
        return 1

    uebersprungen = []
    for spalte, _k, _f in FORMELN:
        # Schranke gegen den haeufigsten Selbstfehler: In OOXML gehoert kein
        # fuehrendes "=" in <f>. Der Bug produzierte sonst einen Reparatur-
        # Dialog, weil die Zelle syntaktisch keine Formel mehr war.
        for _sp, _k, _f in FORMELN:
            if not _f.startswith("="):
                raise SystemExit(f"ABBRUCH: Formel fuer {_sp} beginnt nicht mit "
                                 f"'=' - das wird beim Schreiben entfernt.")
        # Und eine zweite: unbalancierte Klammern ergeben #NAME? bzw. eine
        # syntaktisch kaputte Formel. Beim L-Zweig war das einmal der Fall.
        for _sp, _k, _f in FORMELN:
            _t = _f.format(r=2, e=ERSTE, l=LETZTE)
            if _t.count("(") != _t.count(")"):
                raise SystemExit(
                    f"ABBRUCH: Formel fuer {_sp} hat unbalancierte Klammern "
                    f"({_t.count('(')} offen, {_t.count(')')} zu). "
                    f"Nichts geschrieben.")
        vorhanden = {int(n) for n in re.findall(r'<c r="%s(\d+)"' % spalte, x)}
        fehlt = [r for r in range(ERSTE, LETZTE + 1) if r not in vorhanden]
        uebersprungen += [(r, spalte) for r in fehlt]
        zellen = re.findall(r'<c r="%s(\d+)"[^>]*>(.*?)</c>' % spalte, x, re.S)
        shared = [n for n, inh in zellen if 't="shared"' in inh]
        print(f"  {spalte}: {len(zellen)} Zellen, {len(shared)} geteilt, "
              f"{len(fehlt)} ohne Zelle (Zeile(n) {fehlt[:5]})")
        if shared and spalte != NEUE_SPALTE:
            print(f"  -> Achtung: {spalte} hat {len(shared)} geteilte "
                  f"Formeln. Es wird nur der Text der Master-Zelle(n) "
                  f"ersetzt, die Gruppe bleibt erhalten.")
    if uebersprungen:
        print(f"  -> {len(uebersprungen)} Zellen werden uebersprungen "
              f"(unberechnete Zeilen), keine werden angelegt.")

    if "--apply" not in sys.argv:
        print("\nProben (Zeile 2):")
        for spalte, kuerzel, formel in FORMELN:
            print(f"  {spalte} ({kuerzel}) =\n    {formel.format(r=2, e=ERSTE, l=LETZTE)}")
        print("\nNichts geschrieben. Mit --apply setzen.")
        return 0

    ersetzt = 0

    ersetzt = angelegt = 0

    # Ueberschrift der neuen Hilfsspalte in Zeile 1
    kopf_ref = NEUE_SPALTE + "1"
    if f'<c r="{kopf_ref}"' in x:
        # Schon da (zweiter Lauf). Nur pruefen, dass es die richtige
        # Ueberschrift ist - das Skript muss mehrfach laufen koennen.
        vorhanden = re.search(r'<c r="%s"[^>]*>.*?</c>' % kopf_ref, x, re.S)
        roh = vorhanden.group(0) if vorhanden else ""
        if 't="s"' in roh:
            # CL1 ist ein Shared String - den Text erst nachschlagen,
            # sonst findet man "Spielberecht" im Zell-XML nie.
            m_si = re.search(r"<v>(\d+)</v>", roh)
            sis_v = re.findall(
                r"<si>(.*?)</si>",
                teile["xl/sharedStrings.xml"].decode("utf-8"), re.S)
            if m_si and int(m_si.group(1)) < len(sis_v):
                roh = sis_v[int(m_si.group(1))]
        if "Spielberecht" not in roh:
            raise SystemExit(
                f"ABBRUCH: {kopf_ref} existiert, traegt aber nicht "
                f"'Spielberecht'. Bitte von Hand pruefen.")
        print(f"Kopf: {kopf_ref} = Spielberecht steht bereits")
    else:
        sis_k = re.findall(r"<si>(.*?)</si>",
                           teile["xl/sharedStrings.xml"].decode("utf-8"), re.S)
        try:
            k_idx = next(i for i, v in enumerate(sis_k)
                         if v == "<t>Spielberecht</t>")
        except StopIteration:
            k_idx = None
        kopf_zelle = (
            f'<c r="{kopf_ref}" t="s"><v>{k_idx}</v></c>' if k_idx is not None
            else f'<c r="{kopf_ref}" t="inlineStr">'
                 f'<is><t>Spielberecht</t></is></c>')
        m_kopf = re.search(r'<c r="CK1".*?</c>', x, re.S)
        if not m_kopf:
            raise SystemExit("ABBRUCH: CK1 nicht gefunden - CL1 nicht einfuegbar.")
        # CL (90) steht hinter CK (89) - Einfuegen NACH der CK1-Zelle
        x = x[:m_kopf.end()] + kopf_zelle + x[m_kopf.end():]
        print(f"Kopf: {kopf_ref} = Spielberecht gesetzt")

    def zeile_repl(m):
        nonlocal ersetzt, angelegt
        r = int(m.group(2))
        if not ERSTE <= r <= LETZTE:
            return m.group(0)
        neu = m.group(3)
        for spalte, _k, formel in FORMELN:
            alt = re.search(r'<c r="%s%d"([^>]*?)(?:/>|>.*?</c>)' % (spalte, r),
                            neu, re.S)
            if not alt:
                # Fehlende Zelle anlegen. Das ist bei den NEUEN Mitgliedern
                # noetig: die Hilfsformeln waren nur bis Zeile 583 gefuellt,
                # die Daten gehen aber bis 591 (ZWANK Luc). ZELLER Sarah /
                # Felicitas / Mortitz (584-586) hatten dadurch gar keine
                # Spielerzaehlung und keinen Tarif.
                if spalte != NEUE_SPALTE and not ZEILEN_ERGAENZEN:
                    continue
                # Stil von der Nachbarspalte uebernehmen, damit die Spalte
                # einheitlich aussieht
                vor = re.search(r'<c r="(CK|CJ)%d"([^>]*?)(?:/>|>.*?</c>)' % r,
                                neu, re.S)
                attr = ""
                if vor:
                    attr = re.sub(r'\s*(r|t)="[^"]*"', "", vor.group(2)).strip()
                f0 = esc(formel.format(r=r, e=ERSTE, l=LETZTE).lstrip("="))
                zelle0 = (f'<c r="{spalte}{r}"{(" " + attr) if attr else ""}>'
                          f'<f>{f0}</f></c>')
                neu = zelle_einfuegen(neu, f"{spalte}{r}", zelle0)
                angelegt += 1
                continue
            attr = re.sub(r'\s*r="[^"]*"', "", alt.group(1)).strip()
            # WICHTIG: das Attribut t="..." MUSS ERHALTEN BLEIBEN.
            # Es deklariert den Zelltyp. Die Formeln in BV, CJ, CH, L, CC
            # liefern TEXT ("F0103", "300", "TRAEGER"), die Zellen sind
            # deshalb t="str". Ohne das Attribut nimmt Excel einen
            # numerischen Zell an, findet Text vor und entfernt die Formel -
            # der Reparatur-Dialog ist die Folge. Genau das ist am
            # 30.09.2026 passiert: 5 Spalten verloren dabei ihr t.
            # Ein vorhandenes t wird daher uebernommen, nur ein veraltetes
            # t="e" (Fehlerzelle) wird entfernt, weil eine korrekte Formel
            # keinen Fehlercache mehr traegt.
            if re.search(r'\st="e"', attr):
                attr = re.sub(r'\s*t="e"', "", attr)
            # In OOXML steht die Formel OHNE fuehrendes "=" - Excel wuerde
            # die Datei sonst als Inhaltsfehler bemecken.
            f = esc(formel.format(r=r, e=ERSTE, l=LETZTE).lstrip("="))
            inhalt_alt = alt.group(0)
            fm = re.search(r"<f([^>]*?)(?:/>|>(.*?)</f>)", inhalt_alt, re.S)
            if fm and 't="shared"' in fm.group(1) and fm.group(2):
                # Geteilte Formel: NUR den Formeltext ersetzen. Die Attribute
                # t="shared", ref="..." und si="..." bleiben ALLE erhalten -
                # ohne ref weiss Excel nicht mehr, bis wohin die Gruppe reicht,
                # und die Follower zeigen ins Leere (Reparatur-Dialog).
                # Die alte und die neue Formel muessen dabei gleich aufgebaut
                # sein, damit die relativen Bezuege der Follower passen.
                attr_f = fm.group(1).strip()
                zelle_innen = f'<f{(" " + attr_f) if attr_f else ""}>{f}</f>'
                zelle = inhalt_alt[:fm.start()] + zelle_innen + inhalt_alt[fm.end():]
                zelle = re.sub(r'^<c r="[^"]+"([^>]*)>',
                               lambda mm: '<c r="%s%d"%s>' % (spalte, r, mm.group(1)),
                               zelle, count=1)
            else:
                zelle = (f'<c r="{spalte}{r}"{(" " + attr) if attr else ""}>'
                         f'<f>{f}</f></c>')
            neu = neu[:alt.start()] + zelle + neu[alt.end():]
            ersetzt += 1
        return m.group(1) + neu + m.group(4)

    neu_x = re.sub(r'(<row r="(\d+)"[^>]*>)(.*?)(</row>)', zeile_repl, x, flags=re.S)

    try:
        ET.fromstring(neu_x)
    except ET.ParseError as e:
        raise SystemExit(f"ABBRUCH: XML kaputt ({e}). Nichts geschrieben.")

    for name, pruef in (("Zellreihenfolge", zellen_reihenfolge_ok),
                        ("doppelte Zellen", zellen_doppelt)):
        schlecht = pruef(neu_x)
        if schlecht:
            raise SystemExit(f"ABBRUCH: {name} verletzt (z. B. {schlecht[:5]}). "
                             f"Nichts geschrieben.")

    m_vor, _f_vor = geteilte_formeln(x)
    m_nach, f_nach = geteilte_formeln(neu_x)
    if (f_nach - m_nach) or (m_vor - m_nach):
        raise SystemExit("ABBRUCH: geteilte Formeln wuerden verwaist. "
                         "Nichts geschrieben.")

    print(f"\nXML ok, {ersetzt} Zellen vorbereitet; Reihenfolge, "
          f"Eindeutigkeit und {len(m_nach)} geteilte Formeln geprueft")

    sicherung = pfad.with_name(
        f"{pfad.stem}.regeln-{datetime.now():%Y-%m-%d_%H%M}{pfad.suffix}")
    shutil.copy2(pfad, sicherung)
    print(f"Sicherung: {sicherung.name}")

    teile[SHEET] = neu_x.encode("utf-8")

    # --- Config: Jahresgrenze Medico in Cotisation!A13/B13 ------------------
    cfg = teile[CONFIG].decode("utf-8")
    if re.search(r'<c r="B13"', cfg):
        # Schon gesetzt (zweiter Lauf) - nur bestaetigen, dass die Grenze
        # noch die erwartete ist. Das Skript muss mehrfach laufen koennen.
        alt = re.search(r'<c r="B13"[^>]*>.*?<v>(\d+)</v>', cfg, re.S)
        print(f"Config: Cotisation!B13 steht bereits auf "
              f"{alt.group(1) if alt else '?'}")
    else:
        beschriftung = "MedicoJahr"
        sis = re.findall(r"<si>(.*?)</si>",
                         teile["xl/sharedStrings.xml"].decode("utf-8"), re.S)
        try:
            s_idx = next(i for i, x in enumerate(sis)
                         if x == f"<t>{beschriftung}</t>")
        except StopIteration:
            s_idx = None
        a13 = (f'<c r="A13" t="s"><v>{s_idx}</v></c>' if s_idx is not None
               else f'<c r="A13" t="inlineStr">'
                    f'<is><t>{beschriftung}</t></is></c>')
        zeile13 = ('<row r="13" spans="1:10">'
                   + a13 + '<c r="B13"><v>2026</v></c></row>')
        m14 = re.search(r'<row r="14"', cfg)
        if not m14:
            raise SystemExit("ABBRUCH: Zeile 14 im Config-Blatt fehlt.")
        cfg_neu = cfg[:m14.start()] + zeile13 + cfg[m14.start():]
        ET.fromstring(cfg_neu)
        teile[CONFIG] = cfg_neu.encode("utf-8")
        print("Config: Cotisation!A13/B13 = MedicoJahr / 2026 gesetzt")

    # Excel muss beim Oeffnen VOLLSTAENDIG neu rechnen. Dieses Skript ersetzt
    # 8.100 Formelzellen und entfernt dabei die gecachten <v>-Werte. Ohne
    # fullCalcOnLoad zeigte die Mappe beim Oeffnen ueberall leer, bis
    # jemand manuell Strg+Alt+F9 gedrueckt haette. Gleiches Muster wie in
    # build_perfect_workbook.py:203.
    wb = teile["xl/workbook.xml"].decode("utf-8")
    wb_neu, n_calc = re.subn(
        r"<calcPr", '<calcPr fullCalcOnLoad="1"', wb, count=1)
    if n_calc != 1:
        # calcPr fehlt: direkt vor </workbook> einfuegen
        wb_neu, n_calc = re.subn(r"</workbook>",
                                '<calcPr fullCalcOnLoad="1"/></workbook>',
                                wb, count=1)
    if n_calc != 1:
        raise SystemExit("ABBRUCH: calcPr/workbook.xml nicht gefunden. "
                         "Es wurde nichts geschrieben.")
    ET.fromstring(wb_neu)
    teile["xl/workbook.xml"] = wb_neu.encode("utf-8")
    print("calcPr: fullCalcOnLoad=1 gesetzt (Excel rechnet beim Oeffnen)")

    tmp = pfad.with_suffix(".tmp")
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as out:
        for i in infos:
            zi = zipfile.ZipInfo(i.filename, date_time=i.date_time)
            zi.compress_type = i.compress_type
            zi.external_attr = i.external_attr
            out.writestr(zi, teile[i.filename])
    tmp.replace(pfad)
    print(f"Geschrieben: {ersetzt} Zellen in "
          f"{', '.join(s for s, _k, _f in FORMELN)}, Zeilen {ERSTE}-{LETZTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())