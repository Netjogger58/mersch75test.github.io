"""Wer zahlt bei den Jugendlichen? Traeger je Jugend-Haushalt + Alter."""
import csv
import datetime
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).parent))
import mappe                     # noqa: E402
import pruef_cotisation as pr     # noqa: E402
import pruefe_stripe_export as pse  # noqa: E402
import baut_arbeitsmappe as ba

HEUTE = datetime.date(2026, 9, 29)
JUGEND = ["AG", "AH", "AI", "AJ", "AK", "AL", "AM"]   # U11F U9H U9F U7H U7F U4H U4F

z = zipfile.ZipFile(mappe.datenquelle())
t = {n: z.read(n) for n in z.namelist()}
roh = [list(r) for r in ba.liese_blatt(t, ba.finde_blatt(t, ba.BLATT))]
kopf = [c.strip() for c in roh[0]]


def cp(s):
    n = 0
    for c in s:
        n = n * 26 + (ord(c) - 64)
    return n - 1


def sp(n):
    for cand in (n,) + tuple(pr.SPALTEN_ALT.get(n, ())):
        for i, k in enumerate(kopf):
            if " ".join(k.split()) == " ".join(cand.split()):
                return i
    return -1


I = {k: sp(v) for k, v in pr.SPALTEN.items()}
JUG_I = {c: cp(c) - 1 for c in JUGEND}
JUG_I = dict(zip(JUGEND, (cp(c) - 1 for c in JUGEND)))
daten = roh[1:]
ergebnis, _ = pse.lade_modell()
modell = {e["excel_zeile"]: e for e in ergebnis}


def g(z2, k):
    i = I[k]
    return z2[i].strip() if 0 <= i < len(z2) else ""


def geb(z2):
    v = g(z2, "naissance")
    try:
        n = float(v)
    except ValueError:
        return None
    if n >= 73415:
        return None
    return datetime.date(1899, 12, 30) + datetime.timedelta(days=int(n))


def alter(z2):
    d = geb(z2)
    return (HEUTE - d).days // 365 if d else None


def ist_jugend(z2):
    return any((z2[i].strip() if i < len(z2) else "") for i in JUG_I.values())


fam_map = {}
for nr, z2 in enumerate(daten, start=pr.ERSTE_DATENZEILE):
    fam_map.setdefault(g(z2, "fam"), []).append((nr, z2))

zeilen_out = []
n_fam = 0
for fam, mit in fam_map.items():
    if not fam:
        continue
    jug = [(n, z2) for n, z2 in mit if ist_jugend(z2)]
    if not jug:
        continue
    n_fam += 1
    traeger = [(n, z2) for n, z2 in mit if modell.get(n, {}).get("ist_traeger")]
    tn, tz = traeger[0] if traeger else (None, None)
    ta = alter(tz) if tz is not None else None
    kinder = [alter(z2) for _, z2 in jug]
    for n, z2 in jug:
        betrag = pse.betrag_zahl(modell.get(n, {}).get("neu")) or 0
        zeilen_out.append({
            "jugend_z": n,
            "jugend_name": f'{g(z2,"nom")} {g(z2,"vorname")}'.strip(),
            "jugend_alter": alter(z2) if alter(z2) is not None else "",
            "jugend_lizenz": ",".join(
                k for k, i in JUG_I.items()
                if i < len(z2) and z2[i].strip()),
            "jugend_status": g(z2, "spielt"),
            "haushalt": fam,
            "traeger_z": tn if tn else "KEINER",
            "traeger_name": (f'{g(tz,"nom")} {g(tz,"vorname")}'.strip()
                             if tz is not None else ""),
            "traeger_geboren": str(geb(tz)) if tz is not None
                               and geb(tz) else "KEIN DATUM",
            "traeger_alter": ta if ta is not None else "unbekannt",
            "traeger_minderjaehrig": "JA" if (ta is not None and ta < 18) else "nein",
            "haushalt_betrag": betrag,
            "erwachsene_im_haushalt": sum(
                1 for _, z2b in mit
                if alter(z2b) is not None and alter(z2b) >= 18),
        })

kopf_csv = ["jugend_z", "jugend_name", "jugend_alter", "jugend_lizenz",
            "jugend_status", "haushalt", "traeger_z", "traeger_name",
            "traeger_geboren", "traeger_alter", "traeger_minderjaehrig",
            "haushalt_betrag", "erwachsene_im_haushalt"]
ziel = pathlib.Path(__file__).resolve().parent / "Jugend-Zahler.csv"
with open(ziel, "w", encoding="utf-8-sig", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=kopf_csv)
    w.writeheader()
    w.writerows(zeilen_out)

print(f"Haushalte mit mindestens einem Jugendlichen: {n_fam}")
print(f"Zeilen in der Liste: {len(zeilen_out)}")
print(f"Geschrieben: {ziel.name}\n")

kinder_tr = [r for r in zeilen_out if r["traeger_minderjaehrig"] == "JA"]
print(f"Traeger ist ein Minderjaehriger: {len(kinder_tr)} Zeilen")
print(f"Traeger hat gar kein Geburtsdatum: "
      f"{sum(1 for r in zeilen_out if r['traeger_alter'] == 'unbekannt')} Zeilen")
print(f"Traeger ist ein Erwachsener:     "
      f"{sum(1 for r in zeilen_out if r['traeger_minderjaehrig'] == 'nein' and r['traeger_alter'] != 'unbekannt')} Zeilen")
print(f"\nSumme Haushaltsbetraege in der Liste: "
      f"{sum(r['haushalt_betrag'] for r in zeilen_out if r['haushalt_betrag'])} EUR")

print("\n--- Beispiel: Traeger ist ein Minderjaehriger ---")
for r in kinder_tr[:12]:
    print(f"  {r['jugend_name'][:24]:<26}({r['jugend_alter']} J) "
          f"-> Traeger {r['traeger_name'][:22]:<24}({r['traeger_alter']}) "
          f"betrag={r['haushalt_betrag']}")
print("\n--- Beispiel: Traeger hat kein Geburtsdatum, Erwachsene im Haus ---")
for r in zeilen_out:
    if r["traeger_alter"] == "unbekannt" and r["erwachsene_im_haushalt"] > 0:
        print(f"  {r['jugend_name'][:24]:<26}({r['jugend_alter']} J) "
              f"-> Traeger {r['traeger_name'][:22]:<24}ohne Datum, "
              f"Erwachsene im Haus: {r['erwachsene_im_haushalt']} "
              f"betrag={r['haushalt_betrag']}")
