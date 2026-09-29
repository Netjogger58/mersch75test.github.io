"""Uebersicht ueber die komplette Cotisation-Berechnung.

Liefert:
  * eine Konsolen-Zusammenfassung nach Kategorien
  * eine CSV Cotisation-UEBERSICHT.csv mit allen Zeilen und den Spalten
    Zeile, Nom, Prénom, Kategorie, Spieler(L), Spielerlizenz, Haushalt,
    Personen, Spieler mit Lizenz, Tarif, RECHNUNG TRAEGT, Ausgabewert M, Begruendung

Aufruf:
    python3 docs/cotisation/uebersicht.py
"""
import collections
import csv
import re
import sys

sys.path.insert(0, "/Users/netjogger58/CascadeProjects/mersch75test.github.io/docs/cotisation")
import pruef_cotisation as pr
import baut_arbeitsmappe as ba
import zipfile

CSV_ZIEL = ba.CONFIG / "Cotisation-UEBERSICHT.csv"


def baue():
    teile = {}
    with zipfile.ZipFile(ba.QUELLE) as z:
        for n in z.namelist():
            teile[n] = z.read(n)
    blatt = ba.finde_blatt(teile, ba.BLATT)
    zeilen = ba.liese_blatt(teile, blatt)
    werte = ba.rechne_werte(teile, blatt)
    kopf = [c.strip() for c in zeilen[0]]

    def idx(key):
        name = pr.SPALTEN[key]
        if name in kopf:
            return kopf.index(name)
        for alt in pr.SPALTEN_ALT.get(name, ()):
            if alt in kopf:
                return kopf.index(alt)
        return -1

    ix = {k: idx(k) for k in pr.SPALTEN}

    def z(r, key):
        i = ix[key]
        return (zeilen[r - 1][i].strip() if 0 <= i < len(zeilen[r - 1]) else "")

    zeile_nr = list(range(pr.ERSTE_DATENZEILE, len(zeilen)))
    haushalte = {pr.normalisiere_adresse(r[0].strip())
                 for r in pr.liese_config(ba.CONFIG / "haushalte-cotisation.csv") if r[0].strip()}

    famkey = {}
    for r in zeile_nr:
        fam = z(r, "fam")
        adr = pr.normalisiere_adresse(z(r, "adresse"))
        famkey[r] = ("ADR:" + adr) if (adr and adr in haushalte) else (fam or f"@{r}")

    gruppen = collections.defaultdict(list)
    for r in zeile_nr:
        gruppen[famkey[r]].append(r)

    out = []
    for key, rows in sorted(gruppen.items()):
        spieler = [r for r in rows if z(r, "spielt") == "J" and z(r, "liz_sp")]
        sen = [r for r in spieler if z(r, "kategorie") == "SEN"]
        u25 = [r for r in spieler if z(r, "kategorie") == "U25"]
        if len(spieler) >= 2 or (sen and u25):
            tarif = 384
        elif sen:
            tarif = 300
        elif u25:
            tarif = 210
        else:
            tarif = 0
        traege = [r for r in rows
                  if werte.get(r) and not werte.get(r).startswith(("F", "XSEUL"))]

        for r in sorted(rows):
            wert = werte.get(r, "")
            if not wert:
                grund = ("Phantomzeile (kein Name, kein Geburtsdatum)"
                         if not z(r, "nom") and not z(r, "adresse")
                         else "kein tarifpflichtiger Spieler in dieser Familie")
            elif wert.startswith("F"):
                drauf = [o for o in rows if (werte.get(o) or "").startswith(str(tarif)) and tarif]
                grund = ("Rechnung traegt: " +
                         (", ".join(f"Z{o} {z(o,'vorname')}" for o in drauf) or "niemand")
                         + " – diese Zeile zeigt nur den Haushaltscode")
            elif wert == "XSEUL":
                drauf = [o for o in rows
                         if werte.get(o) not in ("", wert) and werte.get(o)]
                grund = ("nicht Traeger der Haushaltseinheit – Betrag steht auf: " +
                         ", ".join(f"Z{o}" for o in drauf)) if drauf \
                    else "Haushaltseinheit ohne eigenen Betrag"
            else:
                grund = "RECHNUNGSTRAEGER" + (" (namentliche Ausnahme)" if "Don" in wert else "")
            out.append({
                "Zeile": r,
                "Nom": z(r, "nom"),
                "Prenom": z(r, "vorname"),
                "Kategorie": z(r, "kategorie"),
                "Spieler (L)": z(r, "spielt"),
                "Spielerlizenz": z(r, "liz_sp"),
                "Haushalt": z(r, "fam"),
                "Personen": len(rows),
                "Spieler mit Lizenz": len(spieler),
                "Tarif": tarif,
                "Rechnung traegt": (f"Z{traege[0]} {z(traege[0],'nom')} {z(traege[0],'vorname')}"
                                    if traege else "niemand"),
                "Ausgabe M": wert,
                "Begruendung": grund,
            })

    with open(CSV_ZIEL, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out[0]), delimiter=";")
        w.writeheader()
        w.writerows(out)
    return out


def zusammenfassung(rows):
    print("=" * 78)
    print("COTISATION 2026/27 – ÜBERSICHT")
    print("=" * 78)
    print("Zeilen gesamt          :", len(rows))
    for titel, bed in (
            ("Betrag (echter Euro)", lambda v: v and not v.startswith(("F", "XSEUL"))),
            ("Haushaltscode Fxxxx", lambda v: bool(v) and v.startswith("F")),
            ("XSEUL (Haushalt)", lambda v: v == "XSEUL"),
            ("leer", lambda v: not v)):
        n = sum(1 for x in rows if bed(x["Ausgabe M"]))
        print(f"  {titel:<22}: {n}")

    betr = [x for x in rows
            if x["Ausgabe M"] and not x["Ausgabe M"].startswith(("F", "XSEUL"))]
    summe = 0
    for x in betr:
        for z in re.findall(r"\d+", x["Ausgabe M"]):
            summe += int(z)
    print(f"Summe aller Betraege    : {summe} EUR auf {len(betr)} Zeilen")

    print()
    print("Verteilung der Betraege:")
    for typ, n in collections.Counter(x["Ausgabe M"] for x in betr).most_common():
        print(f"   {typ:<18} {n:>4}x")

    print()
    print("-" * 78)
    print("AKTION BENOETIGT")
    print("-" * 78)

    spieler_ohne = [x for x in rows
                    if x["Spieler (L)"] == "J" and x["Spielerlizenz"]
                    and x["Ausgabe M"].startswith("F")]
    print(f"1) Spieler MIT Lizenz, aber nur Haushaltscode: {len(spieler_ohne)}")
    print(f"   (Das ist KEIN Fehler – die Rechnung traegt eine andere Person.)")
    for x in spieler_ohne[:12]:
        print(f"      Z{x['Zeile']:<5} {x['Nom']:<12} {x['Prenom']:<10} -> {x['Ausgabe M']}"
              f"   Rechnung traegt: {x['Rechnung traegt']}")
    if len(spieler_ohne) > 12:
        print(f"      ... und {len(spieler_ohne) - 12} weitere (siehe CSV)")

    # ---- ECHTE LUECKEN: Haushalt, in dem jemand mit Lizenz spielt,
    #      aber KEINE Zeile einen Betrag traegt ------------------------------
    gruppe = collections.defaultdict(list)
    for x in rows:
        if x["Haushalt"]:
            gruppe[x["Haushalt"]].append(x)

    luecken = []
    for hh, xs in gruppe.items():
        spieler = [x for x in xs if x["Spieler (L)"] == "J" and x["Spielerlizenz"]]
        betraege = [x for x in xs
                    if x["Ausgabe M"] and not x["Ausgabe M"].startswith(("F", "XSEUL"))
                    and "Ausnahme" not in x["Ausgabe M"]]
        if spieler and not betraege:
            luecken.append((hh, xs, spieler))

    print()
    print("-" * 78)
    print("ECHTE LUECKEN (Haushalt mit Spieler, aber OHNE Betrag):")
    print("-" * 78)
    if not luecken:
        print("   KEINE - jeder Haushalt mit Spieler traegt irgendwo einen Betrag.")
    else:
        print("   ", len(luecken), "Haushalte betroffen!")
        for hh, xs, spieler in luecken:
            print(f"      {hh:<10} Spieler: " +
                  ", ".join(f"{s['Nom']} {s['Prenom']} (Z{s['Zeile']})" for s in spieler))
            for x in xs:
                print(f"         Z{x['Zeile']:<5} {x['Nom']:<12} {x['Prenom']:<10} "
                      f"Ausgabe={x['Ausgabe M']!r:<12} {x['Begruendung'][:60]}")

    # ---- Zeilen, die weder Name noch Haushalt haben ----------------------
    klimm = [x for x in rows if not x["Ausgabe M"]]
    print()
    print("2) Leer OHNE Haushaltscode:", len(klimm))
    art = collections.Counter(x["Begruendung"] for x in klimm)
    for g, n in art.most_common():
        print(f"      {n:>4}x  {g}")
    for x in klimm[:6]:
        print(f"      Z{x['Zeile']:<5} {x['Nom']:<12} {x['Prenom']:<10} "
              f"Haushalt={x['Haushalt'] or '-':<8} Spieler={x['Spieler (L)'] or '-'}")

    print()
    print(f"3) Familien, in denen gar niemand mit Lizenz spielt:")
    fam_topf = collections.defaultdict(list)
    for x in rows:
        if x["Haushalt"]:
            fam_topf[x["Haushalt"]].append(x)
    ohne = [f for f, xs in fam_topf.items()
            if not any(y["Spieler mit Lizenz"] for y in xs)]
    print(f"      {len(ohne)} von {len(fam_topf)} Haushalten")
    print(f"      Beispiel: " + ", ".join(ohne[:10]))


if __name__ == "__main__":
    rows = baue()
    zusammenfassung(rows)
    print()
    print("Vollstaendige Liste mit Begruendung:", CSV_ZIEL)
