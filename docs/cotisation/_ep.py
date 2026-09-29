"""EPPS: Spieler in einem Haushalt, der 384 zahlt - soll F0039 zeigen."""
import pathlib
import sys

D = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(D))
import pruef_cotisation as pr  # noqa: E402

Q = pathlib.Path("/Users/netjogger58/CascadeProjects/Vereins-OS/docs/"
                 "GC 2026-09-24 MEMBERSLESCHT 2026-2027.csv")
T, ZB, REG, OF, RES = pr.lade_tarife(D / "tarife-cotisation.csv")
A, H = pr.lade_ausnahmen(D / "ausnahmen-cotisation.csv")
zl = pr.lade_csv(Q)
erg = pr.berechne(zl, A, T, ZB, REG, OF, RES, H)
by = {e["excel_zeile"]: e for e in erg}

kopf = [c.strip() for c in zl[0]]


def sp(k):
    n = pr.SPALTEN[k]
    if n in kopf:
        return kopf.index(n)
    for alt in pr.SPALTEN_ALT.get(n, ()):
        if alt in kopf:
            return kopf.index(alt)
    raise SystemExit(k)


i_fam, i_st, i_liz, i_adr = sp("fam"), sp("spielt"), sp("liz_sp"), sp("adresse")

print("Haushalt F0039:")
for i, r in enumerate(zl[1:]):
    if r[i_fam].strip() == "F0039":
        nr = 2 + i
        e = by[nr]
        print(f"  Z{nr:>3} {r[0][:16]:<16} {r[1][:13]:<13} St={r[i_st]:<2} "
              f"Lizenz={'ja' if r[i_liz].strip() else 'nein':<4} "
              f"Tr={'J' if e['ist_traeger'] else '-'} -> {e['neu'] or '(leer)':<8} "
              f"{e['grund'][:38]}")
        print(f"        Adresse: {r[i_adr][:40]!r} | famkey={e['famkey'][:30]}")

print("\nAlle Comite-Leute mit Status:")
for i, r in enumerate(zl[1:]):
    nr = 2 + i
    e = by[nr]
    if e["nom"].upper() in ("EPPS", "METZLER", "CASTELLANO", "DEISCHTER",
                            "DIDELOT", "VAN DER WEKEN", "BISENIUS",
                            "MAQUIL", "SCHUSTER", "DA CONCEICAO"):
        print(f"  {e['nom'][:16]:<16} {e['vorname'][:12]:<12} St={e['spielt'] or '-':<2} "
              f"Tr={'J' if e['ist_traeger'] else '-'} -> {e['neu'] or '(leer)':<8} "
              f"| {e['grund'][:36]}")
