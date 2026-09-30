"""Prueft die Turnier-Daten im Generator gegen ihre eigene Deduplizierung.

Der Generator laedt fuer ein Wochenende die Spiele und verwirft Duplikate
ueber den Schluessel team|datum. Zwei Turniere desselben Teams am selben
Tag wuerden damit eines verschlucken - genau die Falle, die bei mehreren
Turnieren pro Woche droht.
"""
import re
import pathlib
import subprocess

SEITE = pathlib.Path(__file__).resolve().parents[2] / 'generator.html'

TEST = r'''
const fs = require('fs');
const s = fs.readFileSync(process.argv[2], 'utf8');

const zeilen = [];
const reZeile = /\{ team: "([^"]*)", datum: "([^"]*)", heim: "([^"]*)", gast: "([^"]*)",[\s\S]*?nr: "([^"]*)", halle: "([^"]*)" \}/g;
let m;
while ((m = reZeile.exec(s)) !== null) {
    zeilen.push({
        team: JSON.parse('"' + m[1] + '"'), datum: m[2],
        heim: JSON.parse('"' + m[3] + '"'), gast: JSON.parse('"' + m[4] + '"'),
        nr: m[5], halle: m[6]
    });
}

const turnier = zeilen.filter(function(g) { return /^Tournoi$/i.test(g.gast); });
console.log('Spielzeilen im Generator:', zeilen.length);
console.log('Turnierzeilen          :', turnier.length);

// Genau die Deduplizierung, die der Generator in loadWeekendGames benutzt
const uniqueKeys = new Set();
const behalten = [];
turnier.forEach(function(g) {
    const key = g.team + '|' + g.datum + '|championship';
    if (uniqueKeys.has(key)) return;
    uniqueKeys.add(key);
    behalten.push(g);
});

const fehler = [];
console.log('\nTurnierzeilen nach der Deduplizierung:', behalten.length);
if (behalten.length !== turnier.length) {
    fehler.push('DEDUPLIZIERUNG VERWIRFT ' + (turnier.length - behalten.length) + ' Turnier(e)');
    turnier.forEach(function(g) {
        if (behalten.indexOf(g) === -1) {
            fehler.push('  verworfen: ' + g.datum + ' ' + g.team + ' ' + g.heim);
        }
    });
}

// nr muss eindeutig sein
const nr = {};
turnier.forEach(function(g) { nr[g.nr] = (nr[g.nr] || 0) + 1; });
Object.keys(nr).forEach(function(k) { if (nr[k] > 1) fehler.push('Doppelte nr: ' + k); });

// Terminfolge je Team muss chronologisch aufsteigend sein.
// Achtung: Datums-STRINGS "25.10.26" < "15.11.26" lexikografisch FALSCH -
// der Vergleich muss Tag/Monat numerisch zerlegen.
function chronologisch(a, b) {
    function teile(d) {
        const m = /^(\d{2})\.(\d{2})\.(\d{2})/.exec(d);
        return m ? [m[3], m[2], m[1]] : ['99', '99', '99'];
    }
    const x = teile(a), y = teile(b);
    for (let i = 0; i < 3; i++) {
        const d = parseInt(x[i], 10) - parseInt(y[i], 10);
        if (d) return d;
    }
    return 0;
}
const proTeam = {};
turnier.forEach(function(g) { (proTeam[g.team] = proTeam[g.team] || []).push(g); });
Object.keys(proTeam).forEach(function(t) {
    const original = proTeam[t].map(function(g) { return g.datum; });
    const sortiert = original.slice().sort(chronologisch);
    if (JSON.stringify(original) !== JSON.stringify(sortiert)) {
        fehler.push('Team ' + t + ': Daten nicht chronologisch sortiert');
    }
});

console.log('\nPruefungen:');
console.log(fehler.length ? '  FEHLER:\n   ' + fehler.join('\n   ') : '  alle bestanden');
console.log('\nTurnierzeilen:');
turnier.forEach(function(g) {
    console.log('  ' + g.datum.padEnd(16) + g.team.padEnd(22) + g.heim.padEnd(14) + 'nr=' + g.nr);
});
process.exit(fehler.length ? 1 : 0);
'''


def main() -> int:
    pfad = pathlib.Path('/tmp/gen_tour_test.js')
    pfad.write_text(TEST, encoding='utf-8')
    r = subprocess.run(['node', str(pfad), str(SEITE)], capture_output=True, text=True)
    print(r.stdout or r.stderr)
    return r.returncode


if __name__ == '__main__':
    raise SystemExit(main())
