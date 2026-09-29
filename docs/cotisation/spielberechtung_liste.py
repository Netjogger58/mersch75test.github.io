"""Listet die Haushalte auf, die durch die Pass-/Medico-Regel weniger zahlen.

Vergleicht die alte Logik (Status J + beliebige Passnummer) mit der neuen
(Status J + echter Pass + Medico >= Jahresgrenze) und schreibt die
Spruenge auf, damit das Secretariat sie gegenpruefen kann.
"""
import collections
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import pruef_cotisation as pr

OUT = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                   "cotisation/spielberechtung-ohne-pass.md")

Q = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                 "GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv")
t = pr.lade_tarife(pathlib.Path(__file__).parent / "tarife-cotisation.csv")[0]
grenze = t["medicojahr"]

zeilen = pr.lade_csv(Q)
kopf = [c.strip() for c in zeilen[0]]


def norm(s):
    return " ".join(s.split())


def zelle(r, name):
    """Spaltenindex tolerant aufloesen - dieselbe Logik wie in
    pruef_cotisation.berechne (Leerraum im Kopf ignorieren)."""
    ziel = norm(pr.SPALTEN[name])
    # Achtung: SPALTEN_ALT ist nach dem SpaltenWERT verschluesselt,
    # nicht nach dem Kurzschluessel aus SPALTEN.
    voll = pr.SPALTEN[name]
    kandidaten = (voll,) + tuple(pr.SPALTEN_ALT.get(voll, ()))
    for i, k in enumerate(kopf):
        if any(norm(k) == norm(kn) for kn in kandidaten):
            return (r[i] or "").strip() if i < len(r) else ""
    raise KeyError(f"Spalte nicht gefunden: {name!r} "
                   f"(gesucht: {kandidaten!r}, Kopf hat {kopf[:3]!r} ...)")


haush = collections.defaultdict(list)
# enumerate statt .index(): list.index vergleicht nach WERT und wuerde bei
# identischen Zeilen (z. B. zwei gleichen Geschwistern) immer die erste
# zurueckgeben - mehrere Haushalte waeren dann faelschlich vereint.
for nr, r in enumerate(zeilen[1:], start=2):
    # Die Datei traegt hinter den echten Daten ~170 Leerzeilen, die noch ein
    # verirrtes "J" in der Statusspalte haben. Ohne Namen sind das keine
    # Mitglieder und gehoeren in keine Liste.
    if not zelle(r, "nom"):
        continue
    # Familiencode ist der stabile Haushaltsschluessel. Die Adresse fehlt bei
    # manchen Mitgliedern (z. B. ROBERT RAYNAUD) - dann taege sie nichts zur
    # Gruppierung bei und wuerde alle Adresslosen in einen Topf werfen.
    code = zelle(r, "fam")
    adr = pr.normalisiere_adresse(zelle(r, "adresse"))
    haush[code or adr or f"@Zeile{nr}"].append(r)

mitglieder = [r for r in zeilen[1:] if zelle(r, "nom")]


def spielberecht(r) -> bool:
    p = zelle(r, "liz_sp")
    if not p or p.upper().startswith("XXX"):
        return False
    m = zelle(r, "medico")
    return m.isdigit() and int(m) >= grenze


z = ["# Haushalte ohne gültigen Spielerpass / Medico",
     "",
     f"Stand: 28.09.2026 · Medico-Grenze: **{grenze}**",
     "",
     f"Mitglieder mit Status `J`: "
     f"{sum(1 for r in mitglieder if zelle(r, 'spielt') == 'J')}",
     f"davon spielberecht: "
     f"{sum(1 for r in mitglieder if zelle(r, 'spielt') == 'J' and spielberecht(r))}",
     "",
     "| Haushalt (Adresse) | Person | Pass (AO) | Medico (AX) | Status | Grund |",
     "|---|---|---|---|---|---|"]

anz = 0
for adr, rs in sorted(haush.items()):
    betroffen = [r for r in rs if zelle(r, "spielt") == "J"
                 and not spielberecht(r)]
    if not betroffen:
        continue
    anzahl_sp = sum(1 for r in rs if zelle(r, "spielt") == "J")
    anz += 1
    for r in betroffen:
        p, m_ = zelle(r, "liz_sp"), zelle(r, "medico")
        grund = ("kein Pass" if not p else
                 "Pass beantragt (XXX)" if p.upper().startswith("XXX") else
                 "kein Medico eingetragen" if not m_ else
                 f"Medico '{m_}' ist kein Jahr" if not m_.isdigit() else
                 f"Medico bis {m_} abgelaufen")
        z.append(f"| {adr} | {zelle(r,'nom')} {zelle(r,'vorname')} "
                 f"| {p or '—'} | {m_ or '—'} | {zelle(r,'spielt')} | {grund} |")
z += ["", f"**{anz} Haushalte** mit mindestens einem Spieler ohne gültigen Pass "
      "oder abgelaufenes Medico.", "",
      "> Diese Leute sind noch in der Datenbank, spielen aber vermutlich nicht. "
      "Bitte mit dem Secrétariat durchgehen, bevor die erste Zahlung rausgeht."]

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text("\n".join(z) + "\n", encoding="utf-8")
print(f"{anz} Haushalte geschrieben -> {OUT}")
