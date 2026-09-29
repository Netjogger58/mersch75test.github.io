"""Excel -> Stripe, ohne Google Sheets.

Der Weg braucht KEIN Google-Konto: Dieses Skript liest die fertige Arbeitsmappe,
rechnet die Rechnungen nach (identische Logik wie pruef_cotisation, also wie
die Excel-Formeln), legt bei Stripe Payment Links an.

SICHER: Ohne --apply passiert NICHTS, es wird nur angezeigt. Der Secret Key
kommt aus der Umgebungsvariable STRIPE_SECRET_KEY, niemals aus dem Repo.

  # 1) ansehen, was passieren wuerde (ohne Key, ohne Aktion)
  python3 docs/cotisation/stripe_sync.py

  # 2) erst mit Test-Keys buchen (max. 5 Links)
  STRIPE_SECRET_KEY=sk_test_... python3 docs/cotisation/stripe_sync.py --apply --limit 5

  # 3) Produktiv (bestaetigt sich zusaetzlich selbst)
  M75_LIVE_OK=1 STRIPE_SECRET_KEY=sk_live_... python3 docs/cotisation/stripe_sync.py --apply
"""
import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.parse
import urllib.request
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe                  # noqa: E402
import pruef_cotisation as pr  # noqa: E402
import pruefe_stripe_export as pse  # noqa: E402

API = "https://api.stripe.com/v1/payment_links"
SAISON = "2026/27"


def lade_zeilen():
    """Modell + Excel-Werte (E-Mail, Adresse, Bezahlt) fuer die Rechnungen."""
    import build_perfect_workbook as bp
    import baut_arbeitsmappe as ba
    cfg = lambda n: pr.liese_config(bp.CONFIG / n)  # noqa: E731
    tarife = pr.lade_tarife(bp.CONFIG / "tarife-cotisation.csv")
    ausnahmen = {(n.strip().upper(), p.strip().upper()): a.strip()
                 for n, p, a in cfg("ausnahmen-cotisation.csv")}
    haushalte = {pr.normalisiere_adresse(a.strip())
                 for a, _b, *_r in ((r + ["", ""])[:3]
                                    for r in cfg("haushalte-cotisation.csv"))
                 if a.strip()}
    with zipfile.ZipFile(mappe.datenquelle()) as z:
        teile = {n: z.read(n) for n in z.namelist()}
    roh = ba.liese_blatt(teile, "xl/worksheets/sheet1.xml")
    modell = {x["excel_zeile"]: x
              for x in pr.berechne(roh, ausnahmen, *tarife, haushalte)}
    kopf = [h.strip() for h in roh[0]]

    def idx(*namen):
        for n in namen:
            if n in kopf:
                return kopf.index(n)
        return -1

    return (modell, roh, idx("Email"), idx("Adresse"),
            idx("BEZAHLT J/N", "Bezahlt J/N"))


def sammle_rechnungen():
    """Genau die Zeilen, die eine Rechnung ergeben - wie das Tor in Spalte A."""
    modell, roh, i_email, i_adr, i_bez = lade_zeilen()
    raus = []
    for zeile, x in sorted(modell.items()):
        v = x["neu"]
        if not pse.echter_betrag(v) or x["fam"] == "GAJGL":
            continue
        betrag = pse.betrag_zahl(v)
        if betrag is None:
            continue
        daten = roh[zeile - 1]

        def hol(i, daten=daten):
            return ((daten[i] if 0 <= i < len(daten) else "") or "").strip()

        raus.append({"zeile": zeile, "famid": x["famkey"],
                     "name": f"{x['nom']} {x['vorname']}".strip(),
                     "email": hol(i_email), "betrag": betrag,
                     "text": str(v), "bezahlt": hol(i_bez)})
    return raus


def stripe_post(key: str, payload: dict) -> dict:
    body = urllib.parse.urlencode(payload).encode()
    req = urllib.request.Request(
        API, data=body, method="post",
        headers={"Authorization": "Bearer " + key,
                 "Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=45) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"Stripe-Fehler {e.code}: {e.read().decode()[:400]}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true",
                    help="Links wirklich anlegen (sonst nur ansehen)")
    ap.add_argument("--limit", type=int, default=0, help="max. Anzahl Links")
    ap.add_argument("--status", action="store_true",
                    help="nur anzeigen, was schon angelegt wurde")
    ap.add_argument("--key", default=os.environ.get("STRIPE_SECRET_KEY", ""))
    ap.add_argument("--datei", default="",
                    help="Arbeitsdatei (z. B. die aus Google Drive geladene "
                         "Kopie) - bestimmt, wo die Statusdatei liegt")
    args = ap.parse_args()
    if args.datei:
        print(f"Arbeitsdatei: {mappe.set_ziel(args.datei)}")

    posten = sammle_rechnungen()
    offen = [p for p in posten if p["bezahlt"].upper() != "J"]
    summe = sum(p["betrag"] for p in offen)
    pfad = mappe.ziel().with_suffix(".stripe-status.json")
    erledigt = {e["zeile"] for e in json.loads(pfad.read_text())} if pfad.exists() else set()
    todo = [p for p in offen if p["zeile"] not in erledigt]

    print(f"Rechnungen gesamt : {len(posten)}")
    print(f"davon offen (N)   : {len(offen)}")
    print(f"bereits bezahlt J : {len(posten) - len(offen)}")
    print(f"Summe offen       : {summe:,.2f} EUR".replace(",", "."))
    print(f"ohne E-Mail       : {sum(1 for p in offen if not p['email'])}"
          "  (Payment Link geht, Invoice nicht)")
    print(f"schon bei Stripe  : {len(erledigt)}")

    if args.status:
        print("\nBereits angelegt:")
        for e in json.loads(pfad.read_text()) if pfad.exists() else []:
            print(f"   Z{e['zeile']:<4} {e['betrag']:>7.2f}  {e['link']}")
        return 0

    print("\nVorschau (erste 12 offene Posten):")
    for p in todo[:12]:
        print(f"   Z{p['zeile']:<4} {p['famid'][:22]:<22} {p['betrag']:>7.2f}  "
              f"L={p['text']:<12} {p['name'][:24]}")

    if not args.apply:
        print(f"\nNichts getan. {len(todo)} Links wuerden angelegt. "
              "Mit --apply wirklich buchen.")
        return 0
    if not args.key:
        raise SystemExit("STRIPE_SECRET_KEY fehlt - es wurde nichts gebucht.")
    if args.key.startswith("sk_live") and os.environ.get("M75_LIVE_OK") != "1":
        raise SystemExit("Live-Key erkannt. Mit M75_LIVE_OK=1 bestaetigen.")

    menge = min(args.limit, len(todo)) if args.limit else len(todo)
    print(f"\nLege {menge} Payment Links bei Stripe an …")
    neu = []
    for p in todo[:menge]:
        o = stripe_post(args.key, {
            "line_items[0][price_data][currency]": "eur",
            "line_items[0][price_data][unit_amount]":
                str(int(round(p["betrag"] * 100))),
            "line_items[0][price_data][product_data][name]":
                f"Cotisation {SAISON} – Haushalt {p['famid']} ({p['name']})",
            "line_items[0][quantity]": "1",
            "metadata[famid]": p["famid"],
            "metadata[excel_zeile]": str(p["zeile"]),
            "metadata[saison]": SAISON,
        })
        print(f"   Z{p['zeile']:<4} {p['betrag']:>7.2f} -> {o.get('url')}")
        p["status"] = "link_created"
        p["link"] = o.get("url", "")
        neu.append(p)
    alt = json.loads(pfad.read_text()) if pfad.exists() else []
    pfad.write_text(json.dumps(alt + neu, ensure_ascii=False, indent=1))
    print(f"\nStatus geschrieben: {pfad}")
    print("In der Excel bitte Spalte N auf J setzen, damit der Posten nicht")
    print("erneut angelegt wird.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

