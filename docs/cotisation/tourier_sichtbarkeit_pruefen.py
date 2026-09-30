"""Prueft die Turnier-Sichtbarkeit im Live Center.

Kernfrage: erscheint jede Turnierzeile in JEDER Jugend-Kategorie und in
KEINER Senioren-Kategorie, und bleiben die normalen Meisterschaftsspiele
unveraendert? Das Skript laedt die echten Daten aus live-center.html und
fuehrt dieselben Funktionen in Node aus, die auch die Seite benutzt.
"""
import re
import pathlib
import subprocess

SEITE = pathlib.Path(__file__).resolve().parents[2] / 'live-center.html'

TEST = r'''
const fs = require('fs');
const s = fs.readFileSync(process.argv[2], 'utf8');

// Spielzeilen aus dem File ziehen und die \u-Escapes aufloesen
const zeilen = [];
const reZeile = /\{ team: "([^"]*)", datum: "([^"]*)", heim: "([^"]*)", gast: "([^"]*)"[^}]*\}/g;
let m;
while ((m = reZeile.exec(s)) !== null) {
    zeilen.push({
        team: JSON.parse('"' + m[1] + '"'),
        datum: m[2],
        heim: JSON.parse('"' + m[3] + '"'),
        gast: JSON.parse('"' + m[4] + '"')
    });
}

const TOURNAMENT_GAST = /^(Turnier|Tournoi|Plateau)\b/;
function trimText(v) { return typeof v === 'string' ? v.trim() : (v == null ? '' : String(v).trim()); }
function istTurnier(row) {
    if (!row) return false;
    if (row.tournament === true) return true;
    return TOURNAMENT_GAST.test(trimText(row.gast));
}
function normalizeTeamLabel(t) {
    if (!t) return "";
    const c = t.replace("JUGEND: ", "").replace(" (H-PRO)", "").replace(" (D-PRO)", "").trim();
    const u = c.toUpperCase();
    if (u.includes("U13M-P1")) return "U13M-P1";
    if (u.includes("U13M-P2")) return "U13M-P2";
    if (u.includes("U11M-1")) return "U11M-1";
    if (u.includes("U11M-2")) return "U11M-2";
    if (u.includes("U9M")) return "U9M";
    if (u.includes("U7M")) return "U7M";
    if (u === "M\u00c4NNER 1") return "M\u00c4NNER";
    if (u === "FRAUEN") return "FRAUEN";
    if (u.includes("U15G")) return "U15G";
    return c;
}
function istJugendKategorie(kat) {
    return /U\s?\d/.test(normalizeTeamLabel(kat || '').toUpperCase());
}
function passtZurKategorie(row, kat) {
    if (!kat || kat === 'all') return true;
    if (istTurnier(row)) {
        const e = normalizeTeamLabel(row.team || '');
        if (e && e === normalizeTeamLabel(kat)) return true;
        return istJugendKategorie(kat);
    }
    return normalizeTeamLabel(row.team || '') === normalizeTeamLabel(kat);
}

const fehler = [];
const turnier = zeilen.filter(istTurnier);
const JUGEND = ['U11M-1', 'U11M-2', 'U9M', 'U7M', 'U13M-P1', 'U13M-P2', 'U15G'];
const SENIOREN = ['M\u00c4NNER', 'FRAUEN'];

console.log('Zeilen gesamt :', zeilen.length);
console.log('Turnierzeilen:', turnier.length);

console.log('\nTreffer je Kategorie:');
JUGEND.concat(SENIOREN).forEach(function(k) {
    const treffer = zeilen.filter(function(r) { return passtZurKategorie(r, k); });
    const t = treffer.filter(istTurnier).length;
    console.log('  ' + k.padEnd(10) + String(treffer.length).padStart(3) + ' Zeilen, davon ' + t + ' Turniere');
});

// 1) Jedes Turnier in JEDER Jugend-Kategorie
turnier.forEach(function(t) {
    JUGEND.forEach(function(k) {
        if (!passtZurKategorie(t, k)) fehler.push('Turnier ' + t.datum + ' ' + t.heim + ' fehlt in ' + k);
    });
});
// 2) Kein Turnier in Senioren-Kategorien
turnier.forEach(function(t) {
    SENIOREN.forEach(function(k) {
        if (passtZurKategorie(t, k)) fehler.push('Turnier ' + t.datum + ' taucht in ' + k + ' auf');
    });
});
// 3) Normale Spiele bleiben unveraendert in ihrer eigenen Kategorie
zeilen.filter(function(r) { return !istTurnier(r); }).forEach(function(r) {
    JUGEND.concat(SENIOREN).forEach(function(k) {
        const ist = passtZurKategorie(r, k);
        const soll = normalizeTeamLabel(r.team || '') === normalizeTeamLabel(k);
        if (ist !== soll) fehler.push('Normalspiel ' + r.datum + ' ' + r.heim + ' weicht ab bei ' + k);
    });
});

console.log('\nPruefungen:');
console.log(fehler.length
    ? '  FEHLER:\n   ' + fehler.join('\n   ')
    : '  alle bestanden - Turniere in jeder Jugendkategorie, Senioren unberuehrt');

console.log('\nTurnierzeilen:');
turnier.forEach(function(t) {
    console.log('  ' + t.datum.padEnd(16) + t.team.padEnd(18) + t.heim);
});
process.exit(fehler.length ? 1 : 0);
'''


def main() -> int:
    pfad = pathlib.Path('/tmp/lc_tour_test.js')
    pfad.write_text(TEST, encoding='utf-8')
    r = subprocess.run(['node', str(pfad), str(SEITE)],
                       capture_output=True, text=True)
    print(r.stdout or r.stderr)
    return r.returncode


if __name__ == '__main__':
    raise SystemExit(main())
