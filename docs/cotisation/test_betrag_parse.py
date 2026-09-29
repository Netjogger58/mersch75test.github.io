"""Testet die Betrags-Parser-Formel aus Stripe_Export Spalte C gegen alle
real vorkommenden L-Werte.

VALUE() allein scheitert an Texten wie "(0+50)" und liess 34 von 234
Rechnungen ohne Betrag. Der Parser liest:
  "384"            -> 384
  "210 (+0+50)"    -> 210   (+50 ist Bestandteil, nicht extra)
  "(0+50)"         -> 50    (0 Basis + 50 Zuschlag = 50 zu zahlen)
  "Don ? +(0 +50)" -> ""    (unbekannt -> bleibt manuell)
"""
import re
import sys


def excel_value(s: str):
    """VALUE(): Zahl, wenn der Text eine Zahl ist, sonst Fehler."""
    try:
        return float(s.strip())
    except ValueError:
        return None


def parser(L: str):
    """Entspricht der Excel-Formel in baue_stripe_sheet (Spalte C)."""
    L = (L or "").strip()
    if L == "":
        return ""
    v = excel_value(L)
    if v is not None:                       # ISNUMBER(VALUE(L))
        return int(v) if v == int(v) else v
    if L[0] == "(":                         # LEFT(L,1)="(" -> Teil nach "+"
        k = L.find("+")
        e = L.find(")")
        if k == -1 or e == -1:
            return ""
        return excel_value(L[k + 1:e]) or ""
    k = L.find("(")                         # Zahl vor "("
    if k == -1:
        return ""
    # NUR die Zahl vor "(" - der Zusatz wird nicht addiert (siehe
    # pruefe_stripe_export.betrag_zahl).
    return excel_value(L[:k]) or ""


def main() -> int:
    faelle = [
        ("384", 384),
        ("210", 210),
        ("300", 300),
        ("(0+50)", 50),
        ("210 (+0+50)", 210),
        ("384 (+0+50)", 384),
        ("Don ? +(0 +50)", ""),
        ("F0001", ""),
        ("XSEUL", ""),
        ("", ""),
    ]
    fehler = 0
    for L, soll in faelle:
        ist = parser(L)
        ok = ist == soll
        fehler += not ok
        print(f"  {'ok ' if ok else 'FEHLER'}  L={L!r:<18} -> C={ist!r:<8} (erwartet {soll!r})")
    print()
    print("ERGEBNIS:", "Parser verhaelt sich wie die Excel-Formel" if not fehler
          else f"{fehler} Abweichungen")
    return 1 if fehler else 0


if __name__ == "__main__":
    raise SystemExit(main())
