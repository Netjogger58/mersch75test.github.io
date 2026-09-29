"""Abgleich: Python-Referenz gegen die Excel-Formel, Zelle fuer Zelle.

Geprueft werden die Punkte, an denen Python und Excel sich unterscheiden koennten:
  * die Zusatz-Regel (Offizielle-Lizenz: /// gilt in beiden als leer)
  * die Spieler-Zaehlung (Status J UND Lizenz in AH)
  * der Rechnungstraeger (Aelteste = kleinster Schluessel, Gleichstand nach Zeile)
  * der Familiencode in Zeilen ohne eigenen Betrag
"""
import pathlib
import sys

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")
import pruef_cotisation as pr                                      # noqa: E402
import baut_arbeitsmappe as ba                                     # noqa: E402

import zipfile                                                     # noqa: E402

# WICHTIG: Verglichen wird gegen die LIVE-Mappe, nicht gegen
# ba.QUELLE. Die zeigt auf TEST1_nur-calcchain.xlsm vom 27.09. - eine alte
# Arbeitsfassung. Damit verglichen wurde bis eben eine Datei, die weder die
# Regeln vom 27./28.09. noch die Spielberechtigung kennt; die gemeldeten
# "Abweichungen" waren ein Messfehler, nicht ein Rechenfehler.
# Ueberschreiben mit:  python3 pruefe_abgleich.py <mappe.xlsm>
LIVE = pathlib.Path(
    "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
    "GC 2026-09-29 MEMBERSLESCHT 2026-2027_mit-Cotisation.xlsm")
MAPPE = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else LIVE
if not MAPPE.exists():
    raise SystemExit(f"ABBRUCH: {MAPPE} gibt es nicht.")
print(f"Verglichen wird gegen: {MAPPE.name}")

teile = {}
with zipfile.ZipFile(MAPPE) as z:
    for n in z.namelist():
        teile[n] = z.read(n)
blatt = ba.finde_blatt(teile, ba.BLATT)

werte = ba.rechne_werte(teile, blatt)
zeilen = ba.liese_blatt(teile, blatt)

kopf = [c.strip() for c in zeilen[0]]


def spalten_index():
    out = {}
    for k, name in pr.SPALTEN.items():
        i = kopf.index(name) if name in kopf else -1
        if i < 0:                       # umbenannte Kopfzeile?
            for alt in pr.SPALTEN_ALT.get(name, ()):
                if alt in kopf:
                    i = kopf.index(alt)
                    break
        out[k] = i
    return out


idx = spalten_index()


def z(r, k):
    i = idx[k]
    return (zeilen[r - 1][i].strip() if 0 <= i < len(zeilen[r - 1]) else "")


# --- Excel-Nachbau der Helfer, unabhängig von pr.berechne ---------------------
import collections                                                    # noqa: E402
ERSTE, LETZTE = ba.ERSTE, ba.LETZTE
haust = {pr.normalisiere_adresse(r[0].strip())
         for r in pr.liese_config(ba.CONFIG / "haushalte-cotisation.csv") if r[0].strip()}

famkey = {}
for r in range(ERSTE, LETZTE + 1):
    f = z(r, "fam")
    adr = pr.normalisiere_adresse(z(r, "adresse"))
    famkey[r] = ("ADR:" + adr) if adr in haust else (f or f"@{r}")


def spielberecht(r) -> bool:
    """Status J zaehlt nur mit echtem Spielerpass UND gueltigem Medico.
    Spalte AX enthaelt das Gueltigkeitsjahr, nicht das Untersuchungsjahr."""
    p = z(r, "liz_sp")
    if not p or p.upper().startswith("XXX"):
        return False
    m = z(r, "medico")
    return m.isdigit() and int(m) >= T["medicojahr"]

gruppe = collections.defaultdict(list)
for r in range(ERSTE, LETZTE + 1):
    gruppe[famkey[r]].append(r)

schluessel, spieler, zusatz, traeger = {}, {}, {}, {}
for key, rows in gruppe.items():
    for r in rows:
        d = pr.parse_datum(z(r, "naissance"))
        basis = 73415 if d is None else d
        schluessel[r] = basis + r / 1000000.0
    sp_ges = sum(1 for o in rows if z(o, "spielt") == "J" and spielberecht(o))
    sp_sen = sum(1 for o in rows if z(o, "spielt") == "J" and spielberecht(o)
                 and z(o, "kategorie") == "SEN")
    sp_u25 = sum(1 for o in rows if z(o, "spielt") == "J" and spielberecht(o)
                 and z(o, "kategorie") == "U25")
    zz = sum(1 for o in rows
             if (not z(o, "liz_sp") and any(pr.ist_lizenz(z(o, k))
                                            for k in ("liz_off", "liz_zs", "liz_sr")))
             or (z(o, "liz_sp") and z(o, "spielt") in ("N", "R")))
    klein = min(schluessel[o] for o in rows)
    for r in rows:
        spieler[r] = (sp_ges, sp_sen, sp_u25)
        zusatz[r] = zz
        traeger[r] = (rows[0] if klein >= 73415 - 1e-9
                      else min(rows, key=lambda o: (schluessel[o], o)))

tarife = pr.lade_tarife(ba.CONFIG / "tarife-cotisation.csv")
T, ZUSATZ_BEI_FAMILIE, TRAEGER_REGEL, OFFICIEL, RES = tarife
AUSNAHMEN = {(n.strip().upper(), p.strip().upper()): a.strip()
             for n, p, a in pr.liese_config(ba.CONFIG / "ausnahmen-cotisation.csv")}

abweichung = []
for r in range(ERSTE, LETZTE + 1):
    key = famkey[r]
    sp_ges, sp_sen, sp_u25 = spieler[r]

    # --- BY Tarif -----------------------------------------------------------
    if sp_ges >= 2 or (sp_sen >= 1 and sp_u25 >= 1):
        tarif = T["familie"]
    elif sp_sen >= 1:
        tarif = T["sen"]
    elif sp_u25 >= 1:
        tarif = T["u25"]
    else:
        tarif = 0
    # --- CA Zuschlag (pauschal pro Familie, nicht bei 384) ------------------
    zz = T["zusatz"] if (zusatz[r] >= 1 and (ZUSATZ_BEI_FAMILIE or tarif != T["familie"])) else 0
    # --- CD XSEULwert -------------------------------------------------------
    # XSEUL richtet sich nach dem Spielstatus: J -> 300, R/N -> (0+50),
    # sonst 0. Kein Durchfallen bei "kein Status": sonst wuerde der Traeger
    # der 74-kopfigen XSEUL-Gruppe den Familientarif 384 bekommen.
    xseul = ""
    if z(r, "fam") == "XSEUL" and not (key.startswith("ADR:") and sp_ges >= 2):
        if z(r, "spielt") == "J":
            xseul = str(T["xseul"])
        elif z(r, "spielt") in ("N", "R"):
            xseul = f"(0+{T['zusatz']})"
        else:
            xseul = "0"
    # --- CB Personenwert ---------------------------------------------------
    # faellt weg, wenn der Haushalt den Familientarif 384 zahlt (Maximum) -
    # sonst wuerde ein Reservist die ganze Familie auf 50 druecken (Z64).
    ausnahme = AUSNAHMEN.get((z(r, "nom").upper(), z(r, "vorname").upper()))
    familienmax = (tarif == T["familie"] and z(r, "fam") not in ("XSEUL", "GAJGL"))
    if ausnahme:
        personenwert = ausnahme
    elif (not familienmax and z(r, "liz_sp")
          and (z(r, "spielt") == "R" or z(r, "fam") == "GAJGL")):
        personenwert = RES
    elif (not familienmax and z(r, "liz_sp")
          and any(z(r, k) == "FRAGEN"
                  for k in ("frage1", "frage2", "frage3", "frage4"))):
        personenwert = RES
    else:
        personenwert = ""

    # --- M in genau der Reihenfolge der Excel-Formel ------------------------
    #     BP ist nie leer (sonst "@"&ZEILE), deshalb gibt es hier KEINEN
    #     Sonderfall "leere Zeile" - eine Zeile ohne Tarif bleibt einfach leer.
    if personenwert:
        erwartet = personenwert
    elif xseul:                              # XSEUL wirkt PRO ZEILE
        erwartet = xseul
    elif traeger[r] == r:
        if tarif == 0:
            erwartet = f"(0+{zz})" if zz > 0 else ""
        else:
            erwartet = f"{tarif}" + (f" (+0+{zz})" if zz > 0 else "")
    else:
        erwartet = z(r, "fam") or key       # Nicht-Traeger: Haushaltscode

    # --- Comite-Mindestbetrag ---------------------------------------------
    # Wer im Comite sitzt, zahlt mindestens 50 (Stimmrecht an der AG) - also
    # weder der Haushaltscode noch "(0+50)". Ein Traeger, der schon 210/300/
    # 384 zahlt, bleibt unberuehrt: Mindestbetrag, kein fester Betrag.
    # AUSNAHME: wer aktiv spielt (Status J), ist ueber den Haushalt abgedeckt
    # und zeigt den Familiencode - EPPS Charly Z163 (F0039 zahlt 384).
    # Genau 10 Personen (geprueft: CSV-Spalte 'Comite' == BI in der Mappe).
    if (z(r, "comite") and not (z(r, "spielt") == "J" and spielberecht(r))
            and (erwartet in ("", "0")
                 or erwartet in (z(r, "fam"), key)
                 or erwartet.startswith("(0+"))):
        erwartet = str(T["zusatz"])
    # Comite-Mitglied: der Zuschlag wird WIRKLICH berechnet statt notiert.
    # SCHUSTER Jeff Z502: Sohn Elie spielt U25 = 210, plus 50 = 260 (er
    # erreicht das Maximum 384 nicht). Ohne Comite bleibt die Notation
    # "210 (+0+50)" und der Parser liest 210.
    elif z(r, "comite") and "(+0+" in erwartet and erwartet.endswith(")"):
        try:
            _b = float(erwartet.split("(")[0].strip())
            _z = float(erwartet.rsplit("+", 1)[1].rstrip(")").strip())
            erwartet = str(int(_b + _z))
        except ValueError:
            pass

    if erwartet != werte.get(r, ""):
        abweichung.append((r, z(r, "nom"), z(r, "vorname"), werte.get(r, ""), erwartet))

print("Verglichen:", LETZTE - ERSTE + 1, "Zeilen")
print("Abweichungen Python <-> Excel-Nachbau:", len(abweichung))
for a in abweichung[:10]:
    print("   Zeile %-5d %-10s %-9s  Python=%-16r Excel=%r" % a)
