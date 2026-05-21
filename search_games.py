import json
import os

feeds = [
    {"cl": "153713", "label": "HERREN 1 (H-PRO)"},
    {"cl": "152653", "label": "FRAUEN (D-PRO)"},
    {"cl": "156341", "label": "JUGEND: U15G"},
    {"cl": "152106", "label": "JUGEND: U13M-PE"},
    {"cl": "152529", "label": "JUGEND: U11 Elite"},
    {"cl": "153409", "label": "JUGEND: U11 Espoirs"},
    {"cl": "151356", "label": "JUGEND: U9M"},
    {"cl": "152096", "label": "JUGEND: U7M"}
]

keywords = ['Forfait', 'RBD2']

def search_game(game, label):
    gComment = str(game.get('gComment', ''))
    gHomeTeam = str(game.get('gHomeTeam', ''))
    gGuestTeam = str(game.get('gGuestTeam', ''))
    gHomeGoals = str(game.get('gHomeGoals', ''))
    gGuestGoals = str(game.get('gGuestGoals', ''))
    
    found = False
    for kw in keywords:
        if kw in gComment:
            found = True
            break
            
    if not found:
        is_mersch = "Mersch75" in gHomeTeam or "Mersch 75" in gHomeTeam or "Mersch75" in gGuestTeam or "Mersch 75" in gGuestTeam
        if is_mersch:
            if (gHomeGoals == "20" and gGuestGoals == "0") or (gHomeGoals == "0" and gGuestGoals == "20"):
                found = True
                
    if found:
        result = {
            "config_label": label,
            "gDate": game.get("gDate"),
            "gTime": game.get("gTime"),
            "gHomeTeam": gHomeTeam,
            "gGuestTeam": gGuestTeam,
            "gComment": gComment,
            "gGroupsortTxt": game.get("gGroupsortTxt"),
            "gNo": game.get("gNo"),
            "sGID": game.get("sGID"),
            "gHomeGoals": game.get("gHomeGoals"),
            "gGuestGoals": game.get("gGuestGoals")
        }
        print(json.dumps(result))

def process_data(data, label):
    if not data: return
    actual = data.get('actualGames', {}).get('games', [])
    future = data.get('futureGames', {}).get('games', [])
    for g in actual: search_game(g, label)
    for g in future: search_game(g, label)

# Based on previous observation, one file contains one feed.
# Let's assume the files are named flh_data_<cl>.json or similar if we can find them.
# If they are not present, I'll check flh_data.json and flh_herren1.json.

for feed in feeds:
    cl = feed['cl']
    # Check common naming patterns
    files_to_check = [f"flh_data_{cl}.json", f"flh_{cl}.json", f"flh_data.json" if cl == "153713" else None]
    for fname in files_to_check:
        if fname and os.path.exists(fname):
            with open(fname, 'r') as f:
                try:
                    data = json.load(f)
                    # If it's a list, it might be multiple feeds, if object, it's one.
                    if isinstance(data, list):
                        for item in data:
                             # Check if cl matches
                             if str(item.get('cl')) == cl:
                                 process_data(item, feed['label'])
                    elif isinstance(data, dict):
                         # If it's flh_data.json, check if cl matches or it's Heron1
                         if fname == "flh_data.json" and cl == "153713":
                             process_data(data, feed['label'])
                         elif str(data.get('cl')) == cl:
                             process_data(data, feed['label'])
                         elif 'actualGames' in data: # Generic check
                             process_data(data, feed['label'])
                except:
                    pass

