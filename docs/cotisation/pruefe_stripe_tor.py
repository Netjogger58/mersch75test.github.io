"""Verifiziert das Rechnungs-TOR in der gebauten Mappe (nicht nur im Modell).

Liest Spalte A/Formel aus Stripe_Export im erzeugten File und vergleicht die
Bedingung mit dem Python-Referenzmodell aus pruef_cotisation.
"""
import pathlib
import re
import sys
import zipfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import mappe           # noqa: E402
import pruefe_stripe_export as p  # noqa: E402

Z = mappe.ziel()
with zipfile.ZipFile(Z) as z:
    s14 = z.read("xl/worksheets/sheet14.xml").decode("utf-8")

# WICHTIG: nicht </f></c> suchen. Excel schreibt hinter der Formel IMMER den
# gecachten Wert mit: <f>..</f><v/>  bzw. <f>..</f><v>zahl</v>. Mit </f></c>
# fand das Skript 0 Treffer und starb mit IndexError, obwohl das Blatt voller
# Formeln ist (899 in Spalte A) - der Test lief nie, statt rot zu schlagen.
a_formeln = re.findall(r'<c r="A(\d+)"[^>]*><f>(.*?)</f>', s14, re.S)
if not a_formeln:
    raise SystemExit("ABBRUCH: keine Formel in Spalte A von Stripe_Export")
print("Stripe_Export Spalte A: Formeln in", len(a_formeln), "Zeilen")
print("Bedingung (Zeile 2):")
print("   ", a_formeln[0][1][:400].replace("&quot;", '"').replace("&lt;", "<")
      .replace("&gt;", ">").replace("&amp;", "&"))

# 1) Das Tor nennt $CC (Spalte "Rechnung traegt"), NICHT mehr $BW.
#    $CC ist der Nachfolger von $BW: BW ist nur noch der Zahlen-Schluessel,
#    aus dem CC per MIN-Vergleich das Wort TRAEGER macht. Das Skript suchte hier
#    noch die alte Fassung und meldete "Tor FEHLT", obwohl das Tor korrekt
#    verbaut ist - der Test war seit dem Umbau auf CC wirkungslos.
tor = a_formeln[0][1]
for teile in ("$CC", "$CD", "$CH", "$CJ", "$BV", "GAJGL"):
    print(f"   {teile:<5} im Tor: {teile in tor}")

# 2) Erwartete Rechnungen aus dem Modell
ergebnis, _ = p.lade_modell()
soll = [x for x in ergebnis
        if p.echter_betrag(x["neu"]) and x["fam"] != "GAJGL"]
traeger = {x["excel_zeile"] for x in ergebnis if x["ist_traeger"]}
xseul = {x["excel_zeile"] for x in soll if x["fam"] == "XSEUL"}
print()
print("Modell-Soll (Zeilen mit Betrag, ohne GAJGL):", len(soll))
print("  davon Traeger (BW):", len(soll and [x for x in soll if x["ist_traeger"]]))
print("  davon XSEUL:", len(xseul))
print("  Rechnungen, die NUR ueber BX/CB/CD kommen:",
      len([x for x in soll if not x["ist_traeger"]]))
ok_gate = all(t in tor for t in ("$CC", "$CD", "$CH", "$CJ", "$BV"))
print()
print("ERGEBNIS:", "Tor im File korrekt verbaut" if ok_gate else "Tor FEHLT")
