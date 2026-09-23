import json
import urllib.request
import time

def fetch_and_analyze(cl, label):
    url = f'https://spo.handball4all.de/service/if_g_json.php?cmd=ps&og=95&p=137&cl={cl}&ca=1&_{int(time.time())}'
    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
            
            # Navigate the nested structure
            content = data
            if isinstance(data, list):
                content = data[0] if data else {}
            if isinstance(content, dict) and 'content' in content:
                content = content['content']
            
            if not isinstance(content, dict):
                print(f'{label}: Could not parse content')
                return
            
            games = []
            for key in ['actualGames', 'futureGames']:
                if key in content and isinstance(content[key], dict) and 'games' in content[key]:
                    games.extend(content[key]['games'])
            
            print(f'\n=== {label} (cl={cl}) ===')
            print(f'Total games: {len(games)}')
            
            found = False
            for g in games:
                home = str(g.get('gHomeTeam', ''))
                guest = str(g.get('gGuestTeam', ''))
                if 'Mersch75' in home or 'Mersch75' in guest:
                    sgid = g.get('sGID', '')
                    home_goals = g.get('gHomeGoals', '')
                    guest_goals = g.get('gGuestGoals', '')
                    found = True
                    print(f'  MERSCH75: sGID={sgid} | {home} vs {guest} | score={home_goals}:{guest_goals}')
            
            if not found:
                print('  No Mersch75 games found!')
                
    except Exception as e:
        print(f'{label}: Error: {e}')

fetch_and_analyze('153713', 'Men')
fetch_and_analyze('152653', 'Women')
fetch_and_analyze('156341', 'U15G')
