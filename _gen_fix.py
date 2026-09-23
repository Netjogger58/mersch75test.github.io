import re, sys

with open('generator.html', 'r') as f:
    content = f.read()

start_marker = 'function updateLandscapePreview() {'
start_idx = content.find(start_marker)
if start_idx == -1:
    print("ERROR: Could not find updateLandscapePreview")
    sys.exit(1)

next_func = content.find('\nfunction renderLandscapeGame(', start_idx + 1)
if next_func == -1:
    print("ERROR: Could not find renderLandscapeGame")
    sys.exit(1)

new_func = """function updateLandscapePreview() {
    const smLEl = document.getElementById('l-scale-mixvoip-l'); const smL = smLEl ? smLEl.value : 280;
    const sdEl = document.getElementById('l-scale-matchday'); const sd = sdEl ? sdEl.value : 90;
    const smREl = document.getElementById('l-scale-mixvoip-r'); const smR = smREl ? smREl.value : 280;
    const s50El = document.getElementById('l-scale-50years'); const s50 = s50El ? s50El.value : 82;

    const imgMixL = document.querySelector('.mixvoip-left img'); if (imgMixL) imgMixL.style.width = smL + 'px';
    const imgMixR = document.querySelector('.mixvoip-right img'); if (imgMixR) imgMixR.style.width = smR + 'px';
    const imgMatch = document.querySelector('.matchday-text img'); if (imgMatch) imgMatch.style.height = sd + 'px';
    const layer50L = document.querySelector('.layer-50years-left'); if (layer50L) { layer50L.style.width = s50 + 'px'; layer50L.style.height = s50 + 'px'; layer50L.style.display = 'flex'; }
    const layer50R = document.querySelector('.layer-50years-right'); if (layer50R) { layer50R.style.width = s50 + 'px'; layer50R.style.height = s50 + 'px'; layer50R.style.display = 'flex'; }

    const cont = document.getElementById('l-dynamic-main');
    if (!cont) return;
    cont.innerHTML = '';

    const ymEl = document.getElementById('toggle-youth-mode');
    const ym = ymEl ? ymEl.checked : false;

    const seniorIds = ['s1', 'fe', 's2'];
    const youthIds = ['u15', 'u13p1', 'u13p2', 'u11MEL', 'u9M', 'u7M', 'u4M'];
    const tournoiIds = ['u11MES'];

    const seniorTeams = [];
    const youthTeams = [];
    const tournoiTeams = [];

    for (let i = 0; i < TEAM_CONFIGS.length; i++) {
        const id = TEAM_CONFIGS[i].id;
        if (teamHasConfiguredGame(id) || teamHasUploadedPhoto(id)) {
            if (seniorIds.includes(id)) seniorTeams.push(id);
            else if (tournoiIds.includes(id)) tournoiTeams.push(id);
            else if (youthIds.includes(id)) youthTeams.push(id);
        }
    }

    if (ym) {
        const youthSlots = [
            { type: 'big', top: 350, left: 36 },
            { type: 'big', top: 350, left: 400 },
            { type: 'big', top: 350, left: 780 },
            { type: 'big', top: 350, left: 1160 }
        ];
        for (let i = 0; i < youthTeams.length && i < youthSlots.length; i++) {
            renderLandscapeGame(youthTeams[i], youthSlots[i], cont, teamHasConfiguredGame(youthTeams[i]));
        }
        const tc = document.getElementById('l-dynamic-tournoi');
        if (tc) tc.innerHTML = '';
        return;
    }

    const seniorSlots = [
        { type: 'big', top: 350, left: 20 },
        { type: 'big', top: 350, left: 570 },
        { type: 'big', top: 350, left: 1120 }
    ];
    for (let i = 0; i < seniorTeams.length && i < seniorSlots.length; i++) {
        renderLandscapeGame(seniorTeams[i], seniorSlots[i], cont, teamHasConfiguredGame(seniorTeams[i]));
    }

    const tournoiPanel = document.getElementById('l-dynamic-tournoi');
    if (tournoiPanel && tournoiTeams.length > 0) {
        tournoiPanel.innerHTML = '';
        const tTop = 350;
        const tLeft = 1120;
        let html = '<div style="position:absolute;top:' + tTop + 'px;left:' + tLeft + 'px;width:240px;">';
        html += '<div style="font-size:14px;font-weight:600;color:#1E1E1E;text-align:center;margin-bottom:8px;">Tournoi</div>';
        for (let i = 0; i < tournoiTeams.length; i++) {
            const id = tournoiTeams[i];
            const hasGame = teamHasConfiguredGame(id);
            const oppEl = document.getElementById(id + '-opp');
            const opp = oppEl ? oppEl.value : '';
            html += '<div style="display:flex;align-items:center;gap:6px;margin-bottom:6px;padding:6px;background:#F5F5F5;border-radius:8px;">';
            html += '<div style="width:28px;height:28px;border-radius:50%;background:#E07856;display:flex;align-items:center;justify-content:center;color:#FFFFFF;font-size:11px;font-weight:700;">' + id.toUpperCase().charAt(0) + '</div>';
            html += '<div style="flex:1;font-size:11px;color:#1E1E1E;"><div style="font-weight:600;">' + (opp || 'Tournoi') + '</div></div>';
            html += '<div style="font-size:11px;color:' + (hasGame ? '#1E7E34' : '#666666') + ';">' + (hasGame ? 'Teilgenommen' : 'Ausstehend') + '</div>';
            html += '</div>';
        }
        html += '</div>';
        tournoiPanel.innerHTML = html;
    } else if (tournoiPanel) {
        tournoiPanel.innerHTML = '';
    }

    const youthCols = [40, 380, 720, 1060];
    for (let i = 0; i < youthTeams.length && i < youthCols.length; i++) {
        renderLandscapeGame(youthTeams[i], { type: 'small', top: 500, left: youthCols[i] }, cont, teamHasConfiguredGame(youthTeams[i]));
    }
    if (youthTeams.length > 4) {
        for (let i = 4; i < youthTeams.length && (i - 4) < youthCols.length; i++) {
            renderLandscapeGame(youthTeams[i], { type: 'small', top: 660, left: youthCols[i - 4] }, cont, teamHasConfiguredGame(youthTeams[i]));
        }
    }

    scalePoster();
}"""

new_content = content[:start_idx] + new_func + content[next_func:]

with open('generator.html', 'w') as f:
    f.write(new_content)

print("SUCCESS: function replaced.")
print(f"New length: {len(new_content)} chars (was {len(content)})")
