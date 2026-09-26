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
import sys
import datetime


# --------------------------------------------------------------- Spaltenzuordnung
# Bewusst ueber Header-Namen und nicht ueber Spaltenbuchstaben: die Mitgliederliste
# existiert in zwei Layouts (CSV-Export und .xlsm-Blatt "Cotisations").
SPALTEN = {
    "nom": "Nom(s)",
    "vorname": "Prénom(s)",
    "naissance": "Naissance (JJ/MM/AA)",
    "kategorie": "Alterskategorie",
    "cotis": "Cotisatioun",
    "spielt": "Spielen J/R/N",
    "fam": "Code Courrier neu",
    "liz_sp": "Pass Nummer (Licences Joueurs / Joueuses)",
    "liz_off": "Licences Off (officiels)",
    "liz_zs": "Licences ZS (secrétaires / chronométreurs)",
    "liz_sr": "Licences SR (arbitre)",
    "officiel": "Officiel",  # optionale Zusatzspalte
    "manuell": "Manuell",  # optionale Spalte, gewinnt immer
}

# ------------------------------------------------------------------- Vorgabewerte
TARIFE_STD = {
    "sen": 300,
    "u25": 210,
    "familie": 384,
    "zusatz": 50,
    "xseul": 300,
    "gajgl": 0,
}
ZUSATZ_BEI_FAMILIE_STD = False
# Rechnungstraeger: "Erste"   -> erste Zeile des Familienblocks (entspricht 144/144 = 100 %
#                      der bestehenden Datei) oder "Aelteste" -> aeltestes Geburtsdatum
#                      (entspricht 86/233 = 37 % der bestehenden Datei, entspricht der
#                      urspruenglichen Anforderung). Umschalten ueber
#                      tarife-cotisation.csv -> TraegerRegel.
TRAEGER_REGEL_STD = "Erste"
# Zuschlag auch dann, wenn die Rolle als Offizieller nur in der Spalte "Officiel" steht
# (ohne Lizenznummer in AH/AI/AJ)
OFFICIEL_ACHZ_STD = False
XSEUL_CODE, GAJGL_CODE = "XSEUL", "GAJGL"
FALLBACK_SERIAL = 73415   # 31.12.2100 -> "///" und Leerwerte landen am Tabellenende
ERSTE_DATENZEILE = 2      # Excel-Zeilenummer der ersten Datenzeile
STUFE = 1000000.0         # Zeilen-Nachschlag = ZEILE()/1000000


# ---------------------------------------------------------------------- Helfer
def lade_csv(pfad: pathlib.Path, trenner: str = ";") -> list[list[str]]:
    with open(pfad, encoding="utf-8-sig", errors="replace", newline="") as fh:
        return [r for r in csv.reader(fh, delimiter=trenner) if any(c.strip() for c in r)]


def parse_datum(wert: str):
    """DD.MM.YYYY / DD/MM/YYYY -> Excel-Serialzahl. Sonst None."""
    s = (wert or "").strip()
    if not s or set(s) <= set("/-."):
        return None
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


def lade_tarife(pfad: pathlib.Path) -> tuple[dict, bool, str, bool]:
    tarife = dict(TARIFE_STD)
    zusatz_bei_familie = ZUSATZ_BEI_FAMILIE_STD
    traeger_regel = TRAEGER_REGEL_STD
    officiel_auch = OFFICIEL_ACHZ_STD
    if not pfad.exists():
        return tarife, zusatz_bei_familie, traeger_regel, officiel_auch
    for key, wert, _bem in lade_csv(pfad)[1:]:
        key, wert = key.strip().lower(), wert.strip()
        if key == "zusatzbeifamilie":
            zusatz_bei_familie = wert.upper().startswith(("J", "Y", "W"))
        elif key == "zusatzauschofficiel":
            officiel_auch = wert.upper().startswith(("J", "Y", "W"))
        elif key == "traegerregel":
            traeger_regel = wert if wert[:1].upper() in ("E", "A") else TRAEGER_REGEL_STD
        elif key in tarife:
            try:
                tarife[key] = int(float(wert))
            except ValueError:
                print(f"! Tarif '{key}' ist keine Zahl: {wert!r}", file=sys.stderr)
    return tarife, zusatz_bei_familie, traeger_regel, officiel_auch


def lade_ausnahmen(pfad: pathlib.Path) -> dict[tuple[str, str], str]:
    ausnahmen: dict[tuple[str, str], str] = {}
    if not pfad.exists():
        return ausnahmen
    for nom, vorname, ausgabe in lade_csv(pfad)[1:]:
        if ausgabe.strip():
            ausnahmen[(nom.strip().upper(), vorname.strip().upper())] = ausgabe.strip()
    return ausnahmen


# ------------------------------------------------------------------ Kernlogik
def berechne(zeilen, ausnahmen, tarife, zusatz_bei_familie, traeger_regel="Erste",
             officiel_auch=False):
    """Gibt je Zeile ein Ergebnis-Dict zurueck - 1:1 die Excel-Formel."""
    kopf = [c.strip() for c in zeilen[0]]

    def spalte(name: str) -> int:
        try:
            return kopf.index(name)
        except ValueError:
            return -1

    idx = {k: spalte(v) for k, v in SPALTEN.items()}
    fehlend = [v for k, v in SPALTEN.items() if k not in ("manuell", "cotis") and idx[k] < 0]
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
        famkey.append(fam if fam else f"@{excel_zeile}")
        d = parse_datum(zelle(z, "naissance"))
        basis = FALLBACK_SERIAL if d is None else d
        schluessel.append(basis - excel_zeile / STUFE)
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
        liz_sp = bool(zelle(z, "liz_sp"))
        liz_off = any(zelle(z, k) for k in ("liz_off", "liz_zs", "liz_sr"))
        officiel = zelle(z, "officiel")
        grp = [daten[j] for j in idxs]

        def spielt_und_hat_lizenz(other, kategorie=None):
            return (zelle(other, "spielt") == "J"
                    and bool(zelle(other, "liz_sp"))
                    and (kategorie is None or zelle(other, "kategorie") == kategorie))

        sp_gesamt = sum(1 for o in grp if spielt_und_hat_lizenz(o))
        sp_sen = sum(1 for o in grp if spielt_und_hat_lizenz(o, "SEN"))
        sp_u25 = sum(1 for o in grp if spielt_und_hat_lizenz(o, "U25"))
        zusatz_pers = sum(
            1 for o in grp
            if (not zelle(o, "liz_sp") and (any(zelle(o, k) for k in ("liz_off", "liz_zs", "liz_sr"))
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

        # 1) komplett leere Zeile
        if not fam and not spielt:
            wert, grund = "", "leer (kein Code, kein Status)"
        # 2) Sondercodes - pro Zeile, keine Familiengruppierung
        elif fam == XSEUL_CODE:
            wert, grund = str(tarife["xseul"]), "Sondercode XSEUL"
        elif fam == GAJGL_CODE:
            wert, grund = str(tarife["gajgl"]), "Sondercode GAJGL"
        # 3) nur beim Rechnungstraeger
        elif i != traeger[key]:
            wert, grund = "", "nicht Rechnungstraeger"
        # 4) manuelle Vorgabe
        elif zelle(z, "manuell"):
            wert, grund = zelle(z, "manuell"), "manuelle Vorgabe"
        # 5) namentliche Ausnahme
        elif (zelle(z, "nom").upper(), zelle(z, "vorname").upper()) in ausnahmen:
            wert = ausnahmen[(zelle(z, "nom").upper(), zelle(z, "vorname").upper())]
            grund = "namentliche Ausnahme"
        # 6) Regeltarif
        elif tarif == 0 and zusatz == 0:
            wert, grund = "", "kein Spielertarif, kein Zusatz"
        elif tarif == 0:
            wert, grund = f"(0+{zusatz})", "nur Offizielle-/Zusatzkosten"
        else:
            wert = f"{tarif} (+0+{zusatz})" if zusatz else str(tarif)
            grund = f"Tarif {tarif}"
            if zusatz:
                grund += f" + {zusatz} Zuschlag (pauschal, {zusatz_pers} Person/en)"

        ergebnis.append({
            "excel_zeile": excel_zeile,
            "nom": zelle(z, "nom"),
            "vorname": zelle(z, "vorname"),
            "fam": fam or "(einzeln)",
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

    tarife, zusatz_bei_familie, traeger_regel, officiel_auch = lade_tarife(hier / "tarife-cotisation.csv")
    ausnahmen = lade_ausnahmen(hier / "ausnahmen-cotisation.csv")
    zeilen = lade_csv(args.quelle)

    print(f"Quelle            : {args.quelle.name}")
    print(f"Tarife            : {tarife}  Zusatz@Familie={zusatz_bei_familie}  Officiel={officiel_auch}")
    print(f"Ausnahmen         : {len(ausnahmen)}")

    # Vergleich beider Rechnungstraeger-Regeln (mit aktiver Offizielle-Erkennung)
    for regel in ("Erste", "Aelteste"):
        erg = berechne(zeilen, ausnahmen, tarife, zusatz_bei_familie, regel, officiel_auch)
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
