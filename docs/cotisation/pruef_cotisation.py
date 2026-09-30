#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
pruef_cotisation.py - rechnet die Cotisation-Formel (Spalte L) in Python nach und
vergleicht das Ergebnis mit den bestehenden Werten der Mitgliederliste.

Bildet exakt die Excel-Logik aus docs/cotisation/cotisation-formeln.md ab:

  1. Zeile ohne Familiencode (O) UND ohne Spielstatus (M) -> leer
  2. O = XSEUL -> 300 (pro Zeile!), O = GAJGL -> 0 (pro Zeile!)
  3. namentliche Ausnahmen (Tiny-Tabelle) -> fester Ausgabewert
  4. Rechnungstraeger = aeltestes Familienmitglied (Geburtsdatum, Gleichstand -> kleinste Zeile)
  5. Tarife: SEN 300 / U25 210 / Familie ab 2 Spielern oder SEN+U25 384
  6. Zusatz: Offizieller ohne Spielerlizenz oder Status N/R -> " (+0+50)"

Aufruf:
    python3 docs/cotisation/pruef_cotisation.py
    python3 docs/cotisation/pruef_cotisation.py --quelle MEINE.csv --bericht abweichungen.csv
"""
from __future__ import annotations

import argparse
import collections
import csv
import pathlib
import re
import sys
import datetime


# --------------------------------------------------------------- Spaltenzuordnung
# Bewusst ueber Header-Namen und nicht ueber Spaltenbuchstaben: die Mitgliederliste
# existiert in zwei Layouts (CSV-Export und .xlsm-Blatt "Cotisations").
SPALTEN = {
    "nom": "Nom(s)",
    "vorname": "Prénom(s)",
    # Card-ID: stabile Kennung fuer E8 (eigener Haushaltsschluessel je
    # XSEUL-Mitglied, "XS:<Card-ID>"). In beiden Layouts vorhanden
    # (Spalte D) - ohne sie faellt nur die Schluesselvergabe auf die Zeilennummer.
    "cardid": "Card-ID",
    "naissance": "Naissance (JJ/MM/AA)",
    "kategorie": "Alterskategorie",
    "cotis": "Cotisatioun",
    # Kopfzeile wurde am 26.09.2026 umbenannt: "Spielen J/R/N" -> "Spieler J/R/N".
    # Beide Namen werden akzeptiert, siehe SPALTEN_ALT.
    "spielt": "Spieler J/R/N",
    "fam": "Code Courrier neu",
    "liz_sp": "Pass Nummer (Licences Joueurs / Joueuses)",
    "liz_off": "Licences Off (officiels)",
    "liz_zs": "Licences ZS (secrétaires / chronométreurs)",
    "liz_sr": "Licences SR (arbitre)",
    "officiel": "Officiel",  # optionale Zusatzspalte
    "manuell": "Manuell",  # optionale Spalte, gewinnt immer
    "adresse": "Adresse",  # nur fuer die Haushaltsliste (Spalte I im Blatt Cotisation)
    # Spalten AW:AZ - steht in einer davon "FRAGEN", ist die Person eine
    #_spielerin mit Lizenz und offener Frage, also (0+50) auf der eigenen Zeile
    "frage1": "Email",
    "frage2": "@mersch75.lu",
    "frage3": "Communicateur",
    "frage4": "Membres commission des jeunes",
    # Comite-Mitgliedschaft. In der CSV und in der Live-Mappe fuellt genau
    # dieselben 10 Personen (geprueft 2026-09-27): die Spalte 'Comite' in der
    # CSV entspricht BI in der Mappe, der CAT-Code 1 steht dort fuer T.
    "comite": "Comité",
    # Spielberechtigung: AX = "Prochain Medico", enthaelt das Gueltigkeitsjahr.
    "medico": "Prochain \nMédico",
}
# Alternativ-Namen fuer Kopfzeilen, die zwischenzeitlich umbenannt wurden.
SPALTEN_ALT = {
    # "Spielt J/R/N/X" ist die Fassung im Blatt seit 2026-09-27 (X = Status
    # ungeklaert). Ohne diesen Eintrag faellt die Spaltenauflosung zurueck und
    # der komplette Stripe-Lauf bricht mit 'FEHLENDE SPALTEN' ab.
    "Spieler J/R/N": ("Spielen J/R/N", "Spieler J/R/N", "Spielt J/R/N",
                      "Spielt J/R/N/X", "Spielt J/R/N/P"),
    "BEZAHLT J/N": ("BEZAHLT J/N", "Bezahlt J/N"),
}

# ------------------------------------------------------------------- Vorgabewerte
TARIFE_STD = {
    "sen": 300,
    "u25": 210,
    "familie": 384,
    "zusatz": 50,
    "xseul": 300,
    "gajgl": 0,
    # Spielberechtigung: Spalte AX ("Prochain Medico") enthaelt das JAHR BIS
    # WANN gueltig, nicht das Jahr der Untersuchung. Wer drin steht, darf
    # spielen; alles darunter ist abgelaufen.
    # ACHTUNG: wandert jedes Kalenderjahr um eins - am 01.01.2027 auf 2027
    # setzen, sonst ist ab dem Neujahr niemand mehr spielberecht.
    "medicojahr": 2026,
}
ZUSATZ_BEI_FAMILIE_STD = False
# Rechnungstraeger: "Aelteste" (Standard) -> aeltestes Familienmitglied nach Geburtsdatum,
#                      Gleichstand/Geburtsdatum unbekannt -> oberste Zeile des Blocks.
#                      Beispiel QUINN: Ruben (Jg. 2011, Spieler) steht in Zeile 5, Nicole
#                      (Jg. 1976, Offizielle) in Zeile 7 -> 210 (+0+50) steht auf Nicole.
#                   "Erste"    -> erste Zeile des Familienblocks (entspricht 144/144 = 100 %
#                      der bisherigen Datei, aber nicht der fachlichen Regel).
# Umschalten ueber tarife-cotisation.csv -> TraegerRegel.
TRAEGER_REGEL_STD = "Aelteste"
# Nicht-Receiver-Zeilen (z. B. Familienangehoerige ohne eigenen Tarif) zeigen den
# Familiencode Fxxxx an, damit die Zugehoerigkeit auf einen Blick sichtbar ist.
# Der Wert wird erst bei BEZAHLT = J durch den tatsaechlichen Betrag ersetzt.
NICHTTRAEGER_CODE_ANZEIGEN = True
# Zuschlag auch dann, wenn die Rolle als Offizieller nur in der Spalte "Officiel" steht
# (ohne Lizenznummer in AH/AI/AJ)
OFFICIEL_ACHZ_STD = False
XSEUL_CODE, GAJGL_CODE = "XSEUL", "GAJGL"
# Status in Spalte O (Kopf "Spielt J/R/N/P"), der seit 29.09.2026 das
# fruehere X abloest: "spielt nicht / ungeklaert". Ein P-Mitglied ist kein
# Spieler, zahlt aber 0 statt gar nichts, solange sein Haushalt selbst
# keinen spielberechtigen Spieler hat.
NICHT_SPIELER_CODE = "P"
AUSNAHMEN_STD = {("BOURG", "JEANNOT"): "Don ? +(0 +50)",
                ("BOURG-THIELEN", "GABY"): "Don ? +(0 +50)"}
# Spieler mit Status R (Reserve) oder Familiencode GAJGL zahlen 0 + 50
RESERVISTEN_WERT_STD = "(0+50)"
FALLBACK_SERIAL = 73415   # 31.12.2100 -> "///" und Leerwerte landen am Tabellenende
ERSTE_DATENZEILE = 2      # Excel-Zeilenummer der ersten Datenzeile
STUFE = 1000000.0         # Zeilen-Nachschlag = ZEILE()/1000000


# ---------------------------------------------------------------------- Helfer
def lade_csv(pfad: pathlib.Path, trenner: str = ";") -> list[list[str]]:
    with open(pfad, encoding="utf-8-sig", errors="replace", newline="") as fh:
        return [r for r in csv.reader(fh, delimiter=trenner) if any(c.strip() for c in r)]


def parse_datum(wert: str):
    """Gibt die Excel-Serienzahl zurueck (Textdatum oder schon numerisch).

    WICHTIG: in der Mitgliederliste liegt das Geburtsdatum meist als Excel-
    Serienzahl vor (z. B. ANSAY Luka = 37023, QUINN Nicole = 28106), nicht als
    Text "12.05.2001". Die alte Fassung gab fuer Zahlen None zurueck - damit
    bekamen alle numerischen Daten den Ersatzwert 73415 und die Regel
    "Rechnungstraeger = Aelteste" wurde faktisch zu "letzte Zeile des Blocks".
    Das trifft die uebrige Spalte J mit Zahlen."""
    s = (wert or "").strip()
    if not s or set(s) <= set("/-."):
        return None
    # Schon eine Excel-Serialzahl: nur Ziffern mit hoechstens einem Punkt
    # (37023 / 40675.0). Ein Textdatum hat mindestens zwei Trenner und faellt
    # damit durch - "12.05.2001" darf NICHT als Zahl gelesen werden.
    if re.fullmatch(r"\d{1,6}(\.\d+)?", s):
        return float(s)
    for trenner in (".", "/", "-"):
        if trenner in s:
            teile = s.split(trenner)
            if len(teile) == 3:
                try:
                    tt, mm, jj = int(teile[0]), int(teile[1]), int(teile[2])
                except ValueError:
                    return None
                if jj < 100:
                    jj += 2000
                try:
                    return (datetime.date(jj, mm, tt) - datetime.date(1899, 12, 30)).days
                except ValueError:
                    return None
    return None


def lade_tarife(pfad: pathlib.Path) -> tuple[dict, bool, str, bool, str]:
    tarife = dict(TARIFE_STD)
    zusatz_bei_familie = ZUSATZ_BEI_FAMILIE_STD
    traeger_regel = TRAEGER_REGEL_STD
    officiel_auch = OFFICIEL_ACHZ_STD
    reservisten_wert = RESERVISTEN_WERT_STD
    if not pfad.exists():
        return tarife, zusatz_bei_familie, traeger_regel, officiel_auch, reservisten_wert
    for key, wert, _bem in lade_csv(pfad)[1:]:
        key, wert = key.strip().lower(), wert.strip()
        if key == "zusatzbeifamilie":
            zusatz_bei_familie = wert.upper().startswith(("J", "Y", "W"))
        elif key == "zusatzauschofficiel":
            officiel_auch = wert.upper().startswith(("J", "Y", "W"))
        elif key == "reservistenwert":
            reservisten_wert = wert
        elif key == "traegerregel":
            traeger_regel = wert if wert[:1].upper() in ("E", "A") else TRAEGER_REGEL_STD
        elif key in tarife:
            try:
                tarife[key] = int(float(wert))
            except ValueError:
                print(f"! Tarif '{key}' ist keine Zahl: {wert!r}", file=sys.stderr)
    return tarife, zusatz_bei_familie, traeger_regel, officiel_auch, reservisten_wert


def lade_ausnahmen(pfad: pathlib.Path) -> tuple[dict[tuple[str, str], str], list[str]]:
    ausnahmen: dict[tuple[str, str], str] = {}
    haushalte: list[str] = []
    if not pfad.exists():
        return ausnahmen, haushalte
    for nom, vorname, ausgabe in lade_csv(pfad)[1:]:
        if ausgabe.strip():
            ausnahmen[(nom.strip().upper(), vorname.strip().upper())] = ausgabe.strip()
    # gleiche Adresse = ein Haushalt (z. B. ANSAY-Brueder, beide Code XSEUL)
    haushaltdatei = pfad.parent / "haushalte-cotisation.csv"
    if haushaltdatei.exists():
        for adresse, _besch in lade_csv(haft:=haushaltdatei)[1:]:
            if adresse.strip():
                haushalte.append(normalisiere_adresse(adresse))
    return ausnahmen, haushalte


def normalisiere_adresse(a: str) -> str:
    """Adressen fuer den Vergleich vereinheitlichen: Gross/Klein egal, Leerzeichen und
    Punkte raus. '22, RUE DE COLMAR-BERG' und '22,RUE DE COLMAR-BERG' sind dann gleich."""
    return "".join(a.upper().split()).replace(".", "").replace("'", "")


KOPF_MARKER = ("schlüssel", "nom", "prénom", "adresse", "bemerkung", "wert")


def ist_kopfzeile(zeile: list[str]) -> bool:
    """Erkennt, ob die erste Zeile einer Config-CSV wirklich eine Kopfzeile ist.

    WICHTIG: `ausnahmen-cotisation.csv` und `haushalte-cotisation.csv` haben
    KEINE Kopfzeile, `tarife-cotisation.csv` schon. Ein blindes `[1:]` hat
    deshalb previously die erste Ausnahme (BOURG Jeannot) und den einzigen
    Haushalt (ANSAY, 1 Medernacherstrooss) verschluckt - die Datei zeigte
    deshalb bei ANSAY zweimal 300 statt einmal 384."""
    zellen = [c.strip().lower() for c in zeile]
    return any(c in KOPF_MARKER for c in zellen)


def liese_config(pfad) -> list[list[str]]:
    """Liest eine Config-CSV und ueberspringt die Kopfzeile NUR, wenn eine da ist."""
    pfad = pathlib.Path(pfad)
    if not pfad.exists():
        return []
    with open(pfad, encoding="utf-8-sig", newline="") as fh:
        zeilen = [r for r in csv.reader(fh, delimiter=";") if any(c.strip() for c in r)]
    return zeilen[1:] if zeilen and ist_kopfzeile(zeilen[0]) else zeilen


def ist_lizenz(wert: str) -> bool:

    """Entspricht der Excel-Bedingung  <spalte><>"<>;  <spalte><>"///"  in der
    Helferformel BV: eine Lizenz zaehlt nur, wenn wirklich eine Nummer steht.
    In der Mitgliederliste steht in ungepflegten Zeilen der Platzhalter /// -
    der wuerde sonst bei jedem Offiziellen ohne Spielerlizenz einen Zuschlag
    von 50 EUR ausloesen. Wichtig fuer den Abgleich Python <-> Excel."""
    s = (wert or "").strip()
    return bool(s) and s != "///"


# ------------------------------------------------------------------ Kernlogik
def berechne(zeilen, ausnahmen, tarife, zusatz_bei_familie, traeger_regel=TRAEGER_REGEL_STD,
             officiel_auch=False, reservisten_wert=RESERVISTEN_WERT_STD, haushalte=()):
    """Gibt je Zeile ein Ergebnis-Dict zurueck - 1:1 die Excel-Formel."""
    kopf = [c.strip() for c in zeilen[0]]

    def spalte(name: str) -> int:
        try:
            return kopf.index(name)
        except ValueError:
            for alt in SPALTEN_ALT.get(name, ()):  # umbenannte Kopfzeilen
                if alt in kopf:
                    return kopf.index(alt)
            # Leerraum ignorieren: im Blatt heisst die Spalte
            # 'Spielt            J/R/N' (12 Leerzeichen), erwartet wird
            # 'Spielt J/R/N'. Ohne das bricht der komplette Stripe-Lauf ab -
            # es gab dafuer keinen Statusdatei-Eintrag, weil nie ein Link
            # erzeugt wurde. Geprueft 2026-09-27, Fehler war schon vorher da.
            def norm(s: str) -> str:
                return " ".join(s.split())

            for kandidat in (name,) + SPALTEN_ALT.get(name, ()):
                for i, k in enumerate(kopf):
                    if norm(k) == norm(kandidat):
                        return i
            return -1

    idx = {k: spalte(v) for k, v in SPALTEN.items()}
    fehlend = [v for k, v in SPALTEN.items()
               if k not in ("manuell", "cotis") and not k.startswith("frage")
               and idx[k] < 0]
    if fehlend:
        raise SystemExit(
            "FEHLENDE SPALTEN in der Quelldatei: " + ", ".join(fehlend) +
            "\n  Erwartet wird die Kopfzeile der Mitgliederliste (Blatt 'Membres 2026_2027')."
        )

    def zelle(zeile, key):
        i = idx[key]
        return zeile[i].strip() if 0 <= i < len(zeile) else ""

    daten = zeilen[1:]
    n = len(daten)

    # Helfer wie in den Excel-Spalten BN (Familie), BO (Schluessel), BP (Aeltester)
    famkey, schluessel, exrow = [], [], []
    for i, z in enumerate(daten):
        excel_zeile = ERSTE_DATENZEILE + i
        fam = zelle(z, "fam")
        if not fam:
            key = f"@{excel_zeile}"
        else:
            # gleiche Adresse = ein Haushalt, auch wenn die Codes verschieden sind
            adr = normalisiere_adresse(zelle(z, "adresse"))
            key = ("ADR:" + adr) if adr in haushalte else fam
            # E8 (Umsetzung): XSEUL ist KEIN Haushalt, sondern ein Sammelcode
            # fuer Einzelpersonen. Trotzdem bekommen alle 72 denselben
            # Schluessel "XSEUL" und liegen damit im Stripe-Abgleich in EINER
            # Rechnungseenheit. Jedes Mitglied bekommt deshalb einen eigenen
            # Schluessel "XS:<Card-ID>".
            # Wichtig: die Adress-Haushalte (Spalte G/I, ANSAY-Brueder) bleiben
            # unangetastet - die Adresspruefung oben hat schon VOR hier zu
            # "ADR:..." aufgeloest, und Zweig 4 braucht genau dieses Praefix, um
            # die beiden XSEUL-Bruder als 1x 384 zu behandeln statt als 2x 300.
            if fam == XSEUL_CODE and not key.startswith("ADR:"):
                key = "XS:" + (zelle(z, "cardid") or str(excel_zeile))
        famkey.append(key)
        d = parse_datum(zelle(z, "naissance"))
        basis = FALLBACK_SERIAL if d is None else d
        # + statt - : bei gleichem Geburtsdatum gewinnt die OBERSTE Zeile.
        # Mit "-" hat spaeteren Zeilen der kleinere Schluessel und damit das
        # Mandat - genau umgekehrt (ANSAY: Luka Z534, Mathis Z535).
        schluessel.append(basis + excel_zeile / STUFE)
        exrow.append(excel_zeile)

    gruppen: dict[str, list[int]] = collections.defaultdict(list)
    for i, key in enumerate(famkey):
        gruppen[key].append(i)

    aeltester = {}
    erste = {}
    letzte = {}
    for key, idxs in gruppen.items():
        aeltester[key] = min(idxs, key=lambda i: (schluessel[i], exrow[i]))
        erste[key] = min(idxs, key=lambda i: exrow[i])
        letzte[key] = max(idxs, key=lambda i: exrow[i])
    traeger = erste if traeger_regel[:1].upper() == "E" else aeltester

    ergebnis = []
    for i, z in enumerate(daten):
        excel_zeile = ERSTE_DATENZEILE + i
        key = famkey[i]
        idxs = gruppen[key]
        fam, spielt, kat = zelle(z, "fam"), zelle(z, "spielt"), zelle(z, "kategorie")
        ist_comite = bool(zelle(z, "comite"))
        liz_sp = bool(zelle(z, "liz_sp"))
        liz_off = any(ist_lizenz(zelle(z, k)) for k in ("liz_off", "liz_zs", "liz_sr"))
        officiel = zelle(z, "officiel")
        grp = [daten[j] for j in idxs]

        def spielberecht(other) -> bool:
            """Ohne Spielerpass darf niemand spielen, und ein vorhandener
            Pass braucht ein gueltiges Medico (Spalte AX = Gueltigkeitsjahr).

            - Pass: echte Nummer. 'XXX' = Antrag an die FLH geschickt, die
              Lizenz existiert noch nicht -> zaehlt nicht.
            - Medico: AX ist das Jahr BIS WANN gueltig. '///', leer oder ein
              Wert kleiner als medicojahr = abgelaufen.
            """
            p = zelle(other, "liz_sp")
            if not p or p.upper().startswith("XXX"):
                return False
            m = zelle(other, "medico")
            return m.isdigit() and int(m) >= tarife["medicojahr"]

        def spielt_und_hat_lizenz(other, kategorie=None):
            return (zelle(other, "spielt") == "J"
                    and spielberecht(other)
                    and (kategorie is None or zelle(other, "kategorie") == kategorie))

        sp_gesamt = sum(1 for o in grp if spielt_und_hat_lizenz(o))
        sp_sen = sum(1 for o in grp if spielt_und_hat_lizenz(o, "SEN"))
        sp_u25 = sum(1 for o in grp if spielt_und_hat_lizenz(o, "U25"))
        zusatz_pers = sum(
            1 for o in grp
            if (not zelle(o, "liz_sp") and (any(ist_lizenz(zelle(o, k)) for k in ("liz_off", "liz_zs", "liz_sr"))
                                            or (officiel_auch and zelle(o, "officiel"))))
            or (bool(zelle(o, "liz_sp")) and zelle(o, "spielt") in ("N", "R"))
        )

        if sp_gesamt >= 2 or (sp_sen >= 1 and sp_u25 >= 1):
            tarif = tarife["familie"]
        elif sp_sen >= 1:
            tarif = tarife["sen"]
        elif sp_u25 >= 1:
            tarif = tarife["u25"]
        else:
            tarif = 0

        # Offizielle zahlen 0, freiwillig 50 (Stimmrecht AG). Der Zuschlag ist pauschal
        # pro Familie (nicht pro Person) und entfaellt beim Familientarif 384 = Maximum.
        zusatz = tarife["zusatz"] if (zusatz_pers
                                      and (zusatz_bei_familie or tarif != tarife["familie"])) else 0

        # Personenbezogener Wert: gilt auf DIESER Zeile, unabhaengig vom Rechnungstraeger
        # 384 ist das Maximum (siehe ZusatzBeiFamilie): zahlt der Haushalt den
        # Familientarif, faellt der Personenwert weg. Sonst wuerde ein Reservist
        # im Haushalt die ganze Familie auf 50 druecken - BISENIUS Ben Z64:
        # 5 Mitglieder, 4 aktiv lizenziert, er ist Rechnungstraeger.
        # XSEUL/GAJGL sind Sondercodes, keine Familientarife - dort bleibt es.
        familienmax = (tarif == tarife["familie"]
                       and fam not in (XSEUL_CODE, GAJGL_CODE))
        ausnahme = ausnahmen.get((zelle(z, "nom").upper(),
                                  zelle(z, "vorname").upper()))
        if ausnahme:
            personenwert, personen_grund = ausnahme, "namentliche Ausnahme"
        elif (not familienmax and liz_sp
              and fam in (XSEUL_CODE, GAJGL_CODE)
              and (spielt == "R" or fam == GAJGL_CODE
                   or any(zelle(z, k) == "FRAGEN"
                          for k in ("frage1", "frage2", "frage3", "frage4")))):
            personenwert = reservisten_wert
            personen_grund = (
                ("Spieler mit Status R" if spielt == "R"
                 else "Sondercode GAJGL" if fam == GAJGL_CODE
                 else "Spieler mit Lizenz und offener Frage (AW:AZ)"))
        else:
            personenwert, personen_grund = "", ""

        # 1) komplett leere Zeile
        if not fam and not spielt:
            wert, grund = "", "leer (kein Code, kein Status)"
        # 2) manuelle Vorgabe - gewinnt immer
        elif zelle(z, "manuell"):
            wert, grund = zelle(z, "manuell"), "manuelle Vorgabe"
        # 3) Ausnahme oder Reservist/GAJGL-Spieler - gilt auf dieser Zeile
        elif personenwert:
            wert, grund = personenwert, personen_grund
        # 4) Sondercodes - pro Zeile, keine Familiengruppierung.
        #    XSEUL entfaellt nur, wenn die Person in einem GELISTETEN Haushalt
        #    (Spalte G) mit mindestens 2 aktiven Spielern sitzt - z. B. die
        #    ANSAY-Brueder: gleiche Adresse, beide XSEUL, also 1x 384.
        #    Wichtig: XSEUL selbst ist KEIN Familiencode (72 Einzelpersonen),
        #    darum darf die 300er-Regel nicht pauschal wegfallen.
        elif fam == XSEUL_CODE and not (key.startswith("ADR:") and sp_gesamt >= 2):
            # XSEUL richtet sich nach dem Spielstatus, nicht nach der Lizenz:
            #   J        -> 300  (der Fixbetrag fuer Spieler)
            #   R oder N -> (0+50)
            #   sonst     -> 0
            # BLANC Max (nur Offiziellenlizenz) und DIDELOT-SCHOEN (keine
            # Lizenz) sind beide Status N und landen damit bei (0+50).
            # Kein Durchfallen bei "kein Status": sonst wuerde der Traeger der
            # 74-kopfigen XSEUL-Gruppe den Familientarif 384 bekommen.
            if spielt == "J" and spielberecht(z):
                wert, grund = str(tarife["xseul"]), "Sondercode XSEUL (Status J)"
            elif spielt == "J":
                wert, grund = ("0",
                               "Sondercode XSEUL, kein gültiger Spielerpass "
                               "oder Medico abgelaufen")
            elif spielt in ("N", "R"):
                wert, grund = (f"(0+{tarife['zusatz']})",
                               f"Sondercode XSEUL, Status {spielt}")
            else:
                wert, grund = "0", "Sondercode XSEUL, kein Spielstatus"
        elif fam == GAJGL_CODE:
            wert, grund = str(tarife["gajgl"]), "Sondercode GAJGL"
        # 5) nur beim Rechnungstraeger
        elif i != traeger[key]:
            # Nicht-Receiver-Zeilen: Familiencode anzeigen statt Leerklick, damit sofort
            # erkennbar ist, zu welchem Haushalt die Person gehoert (Spalte BEZAHLT = J
            # blendet das spaeter durch den echten Betrag ersetzen bzw. ausblenden).
            if NICHTTRAEGER_CODE_ANZEIGEN and fam and not fam.startswith("ADR:"):
                wert, grund = fam, f"nicht Rechnungstraeger (Familie {fam})"
            else:
                wert, grund = "", "nicht Rechnungstraeger"
        # 6) Regeltarif
        elif tarif == 0 and zusatz == 0:
            # Status P heisst "spielt nicht / ungeklaert". Ein P-Mitglied
            # erhaelt daher AUSDRUECKLICH 0 und nicht etwa ein leeres Feld -
            # so steht es auch in den uebrigen Faellen (XSEUL ohne Status).
            # Voraussetzung ist, dass der HAUSHALT keinen echten Spieler hat:
            # ist jemand aus der Familie spielberecht (J + Pass + Medico),
            # zahlt der Traeger den Haushaltsbetrag - auch wenn er selbst P
            # ist (BINGEN Fränk Z58 = Traeger, BINGEN Dani Z57 = Spieler,
            # 210). Nur eine Familie ganz ohne Spieler faellt auf 0.
            if spielt == NICHT_SPIELER_CODE and not sp_gesamt:
                wert, grund = "0", "Status P, kein Spielertarif im Haushalt"
            else:
                wert, grund = "", "kein Spielertarif, kein Zusatz"
        elif tarif == 0:
            wert, grund = f"(0+{zusatz})", "nur Offizielle-/Zusatzkosten"
        else:
            wert = f"{tarif} (+0+{zusatz})" if zusatz else str(tarif)
            grund = f"Tarif {tarif}"
            if zusatz:
                grund += f" + {zusatz} Zuschlag (pauschal, {zusatz_pers} Person/en)"

        # Comite-Zusatzregel: wer im Comite sitzt (Spalte 'Comite' in der CSV,
        # BI bzw. CAT-Code 1 in der Mappe) zahlt mindestens 50 - Stimmrecht an
        # der AG. Also NIE "(0+50)" und NIE der Haushaltscode eines anderen.
        # METZLER Bernard (Sekretaer) zeigte vorher nur F0026, jetzt 50.
        # AUSNAHME: wer aktiv SPIELT (Status J), ist ueber seinen Haushalt
        # abgedeckt und zeigt weiter den Familiencode - EPPS Charly Z163 ist
        # Spieler in F0039, das 384 zahlt (Bruder Thomas + Mutter PIRSON
        # Isabelle als Traegerin). Er darf nicht auf 50 heruntergesetzt werden.
        # Ein Traeger, der selbst 210/300/384 zahlt, bleibt ohnehin unberuehrt.
        # CLEMENT Liliane ist nicht im Comite und bleibt bei (0+50).
        # E7 (Umsetzung): Ein Offizieller, der NICHT Rechnungstraeger ist,
        # bekommt KEINE eigene Rechnung; die 50 EUR stecken dann im Betrag des
        # Traegers. Genau das war der Fehler in F0026: CLEMENT Liliane (0+50)
        # und METZLER Bernard 50 = zwei Posten fuer EINEN Haushalt (100 EUR).
        # Die Ausnahme gilt nur fuer GAJGL: das ist wie XSEUL ein Sammelcode
        # ohne Haushaltsbezug, dort bleibt die Pro-Zeile-Berechnung. XSEUL
        # braucht die Ausnahme nicht mehr - seit E8 (eigener Schluessel
        # "XS:<Card-ID>") ist jedes XSEUL-Mitglied sein eigener Traeger und
        # faellt damit ganz normal unter die Traeger-Regel.
        if (ist_comite and not (spielt == "J" and spielberecht(z))
                and (i == traeger[key] or fam == GAJGL_CODE)
                and (wert in ("", "0") or wert == fam
                     or wert.startswith("(0+"))):
            wert, grund = str(tarife["zusatz"]), "Comité-Mitglied, Minimum 50"
        elif ist_comite and "(+0+" in wert and wert.endswith(")"):
            # Comite-Mitglied: der Zuschlag wird WIRKLICH berechnet, nicht nur
            # notiert - SCHUSTER Jeff (Praesident): Sohn Elie spielt U25 = 210,
            # plus 50 = 260. Er erreicht das Maximum 384 nicht, also 260.
            # Fuer alle ohne Comite bleibt die Notation "(0+50)" stehen und
            # der Parser liest weiter nur die Zahl davor (also 210).
            basis = wert.split("(")[0].strip()
            zusatz = wert.rsplit("+", 1)[1].rstrip(")").strip()
            try:
                summe = int(float(basis) + float(zusatz))
            except ValueError:
                summe = None
            if summe is not None:
                wert, grund = str(summe), (
                    f"Tarif {basis} + {zusatz} Zuschlag, Comité-Mitglied")

        ergebnis.append({
            "excel_zeile": excel_zeile,
            "nom": zelle(z, "nom"),
            "vorname": zelle(z, "vorname"),
            "fam": fam or "(einzeln)",
            # famkey = Wert der Excel-Hilfe BP (FamID). Wird fuer den
            # Stripe-Abgleich gebraucht: das ist die Rechnungsadresse, nicht
            # der Rohcode aus Q. Leerer Code ergibt "@<Zeile>" (Phantomzeile).
            "famkey": key,
            "kategorie": kat,
            "spielt": spielt,
            "bestehend": zelle(z, "cotis"),
            "neu": wert,
            "grund": grund,
            "ist_traeger": i == traeger[key],
        })
    return ergebnis


# --------------------------------------------------------------------- Bericht
def main() -> int:
    hier = pathlib.Path(__file__).resolve().parent
    standard = pathlib.Path(
        "/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
        "GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv"
    )
    p = argparse.ArgumentParser(description="Cotisation-Formel gegen die Mitgliederliste pruefen")
    p.add_argument("--quelle", type=pathlib.Path, default=standard,
                   help="CSV-Export der Mitgliederliste (Blatt 'Membres 2026_2027')")
    p.add_argument("--bericht", type=pathlib.Path, default=None,
                   help="optional: CSV-Datei mit allen Abweichungen")
    args = p.parse_args()

    if not args.quelle.exists():
        print(f"! Quelldatei nicht gefunden: {args.quelle}", file=sys.stderr)
        return 2

    tarife, zusatz_bei_familie, traeger_regel, officiel_auch, reservisten_wert = lade_tarife(
        hier / "tarife-cotisation.csv")
    ausnahmen, haushalte = lade_ausnahmen(hier / "ausnahmen-cotisation.csv")
    zeilen = lade_csv(args.quelle)

    print(f"Quelle            : {args.quelle.name}")
    print(f"Tarife            : {tarife}  Zusatz@Familie={zusatz_bei_familie}  Officiel={officiel_auch}")
    print(f"Ausnahmen         : {len(ausnahmen)}")
    print(f"Reservistenwert   : {reservisten_wert}")
    print(f"Haushalte (Adresse): {len(haushalte)} {haushalte}")

    # Vergleich beider Rechnungstraeger-Regeln (mit aktiver Offizielle-Erkennung)
    for regel in ("Erste", "Aelteste"):
        erg = berechne(zeilen, ausnahmen, tarife, zusatz_bei_familie, regel, officiel_auch,
                      reservisten_wert, haushalte)
        ab = [e for e in erg if e["bestehend"] != e["neu"]]
        quote = (len(erg) - len(ab)) / len(erg) * 100
        marke = "  <- aktiv" if regel == traeger_regel else ""
        print(f"  Traeger={regel:<9} Uebereinstimmend {len(erg) - len(ab):>4}/{len(erg)} "
              f"({quote:5.1f} %)  Abweichungen {len(ab):>3}{marke}")
        if regel == traeger_regel:
            ergebnis, abweichungen = erg, ab

    traeger_mit_wert = sum(1 for e in ergebnis if e["ist_traeger"] and e["neu"])
    print(f"\nZeilen            : {len(ergebnis)}")
    print(f"Rechnungstraeger  : {traeger_mit_wert} Zeilen mit Ausgabe")
    print(f"Abweichungen      : {len(abweichungen)}")

    gruppen = collections.Counter((e["bestehend"] or "(leer)", e["neu"] or "(leer)") for e in abweichungen)
    for (alt, neu), anzahl in gruppen.most_common(12):
        print(f"   {anzahl:>4}x  bisher={alt:<14} neu={neu}")

    if args.bericht:
        with open(args.bericht, "w", encoding="utf-8-sig", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=["excel_zeile", "nom", "vorname", "fam",
                                               "kategorie", "spielt", "bestehend", "neu", "grund"],
                               delimiter=";", extrasaction="ignore")
            w.writeheader()
            w.writerows(abweichungen)
        print(f"\nAbweichungsliste : {args.bericht}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
