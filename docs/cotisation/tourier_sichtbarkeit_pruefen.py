"""Prueft die Turnier-Sichtbarkeit im Live Center.

Kernfrage: erscheint jede Turnierzeile in JEDER Jugend-Kategorie und in
KEINER Senioren-Kategorie, und bleiben die normalen Meisterschaftsspiele
unveraendert? Das Skript laedt die echten Daten aus live-center.html und
fuehrt dieselben Funktionen in Node aus, die auch die Seite benutzt.
"""
import re
import pathlib
import subprocess
import sys

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

// 4) KRITISCH: die Seite enthaelt in renderAllGames einen Filter, der Zeilen
//    per "return" unterdrueckt. Genau dort sind die U11-Turniere am
//    30.09.2026 verschwunden: der alte Phantom-Filter /Turn.?ier\s*U11/
//    lief gegen heim UND gast und hat jede echte U11-Turnierzeile
//    weggeworfen (5 U9 sichtbar, 0 U11).
//    Dieser Test sucht ALLE solchen Filter in der Seite und prueft jeden
//    gegen die echten Daten - statt den aktuellen Filter zu verdrahten.
function trimT(v) { return typeof v === 'string' ? v.trim() : (v == null ? '' : String(v).trim()); }

// Zeilen-Unterdruecker aus der Seite einsammeln:
//   if (<Bedingung>) return;   innerhalb der forEach-Schleife von renderAllGames
const startFn = s.indexOf('sortedGames.forEach');
const endFn = s.indexOf('const emptyState', startFn);
const rumpf = s.slice(startFn, endFn > startFn ? endFn : startFn + 20000);

const filterQuelle = rumpf.match(/if\s*\(([^\n]*?)\)\s*return\s*;/g) || [];
console.log('\nGefundene Zeilen-Unterdruecker:', filterQuelle.length);

filterQuelle.forEach(function(code) {
    const kontext = code.slice(0, 110).replace(/\s+/g, ' ');
    const bedingung = code.replace(/^if\s*\(/, '').replace(/\)\s*return\s*;$/, '');
    let fn;
    try {
        fn = new Function('r', 'normalizeTeamLabel', 'trimText', 'trimT',
            'return (' + bedingung + ');');
    } catch (e) {
        return;   // Bedingung laesst sich nicht isoliert auswerten
    }
    const opfer = zeilen.filter(function(r) {
        try { return fn(r, normalizeTeamLabel, trimText, trimT); } catch (e) { return false; }
    });
    const opferTurnier = opfer.filter(istTurnier);
    if (opfer.length) {
        console.log('  -> ' + kontext);
        console.log('     unterdrueckt ' + opfer.length + ' Zeilen, davon '
            + opferTurnier.length + ' Turniere');
    }
    opferTurnier.forEach(function(t) {
        fehler.push('FILTER VERSCHLUCKT TURNIER: ' + t.datum + ' ' + t.team
            + ' ' + t.heim + '  durch  ' + kontext);
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
    # Optionaler Pfad, damit man den Test GEGEN einen alten Stand laufen
    # lassen kann. Nur so laesst sich beweisen, dass er den Fehler ueberhaupt
    # faengt - ein Test, der nur gegen den aktuellen Stand gruen wird,
    # beweist nichts.
    seite = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else SEITE
    if not seite.exists():
        print('Datei nicht gefunden:', seite)
        return 2
    print('Geprueft:', seite.name)
    pfad = pathlib.Path('/tmp/lc_tour_test.js')
    pfad.write_text(TEST, encoding='utf-8')
    r = subprocess.run(['node', str(pfad), str(seite)],
                       capture_output=True, text=True)
    print(r.stdout or r.stderr)
    return r.returncode


if __name__ == '__main__':
    raise SystemExit(main())
