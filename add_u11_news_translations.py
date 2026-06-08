from pathlib import Path

p = Path('script.js')
s = p.read_text(encoding='utf-8')

replacements = [
    (
        "            newsU13Body: 'Mat enger staarker Leeschtung huet eis U13 d\\'Halleronn 2025/2026 an der Mixte Poule Espoir ofgeschloss: géint den Tabellenzweeten HB Esch gouf et eng kloer 39:26-Victoire. D\\'Ekipp ass konzentréiert bliwwen, huet als Team zesumme gekämpft a bleift domat ongeschloen un der Spëtzt. Eng immens flott Saisonronn fir eis jonk Mierscher! 💛💙 🏆',",
        "            newsU13Body: 'Mat enger staarker Leeschtung huet eis U13 d\\'Halleronn 2025/2026 an der Mixte Poule Espoir ofgeschloss: géint den Tabellenzweeten HB Esch gouf et eng kloer 39:26-Victoire. D\\'Ekipp ass konzentréiert bliwwen, huet als Team zesumme gekämpft a bleift domat ongeschloen un der Spëtzt. Eng immens flott Saisonronn fir eis jonk Mierscher! 💛💙 🏆',\n            newsU11Eyebrow: 'U11 Elite · Saisonofschloss',\n            newsU11Title: 'U11 Elite schléisst d\\'Saison staark of',\n            newsU11Body: 'Eis U11 Elite huet och um Enn vun der Saison nach eemol gewisen, wat an der Ekipp stécht. Am Duell ëm Plaz 5 géint HC Standard konnt Mersch75 béid Matcher gewannen: doheem mat 23:16 an auswäerts mat 22:18. Eng flott Belounung fir eng engagéiert Saison an e staarke Schlussakkord fir eis jonk Mierscher. 💛💙',"
    ),
    (
        "            newsU13Body: 'Avec une très belle prestation, nos U13 ont terminé le tour en salle 2025/2026 de la Poule Espoir Mixte par une nette victoire 39:26 contre HB Esch, deuxième du classement. L\\'équipe est restée concentrée, a combattu ensemble et reste invaincue en tête. Une superbe phase de saison pour nos jeunes de Mersch ! 💛💙 🏆',",
        "            newsU13Body: 'Avec une très belle prestation, nos U13 ont terminé le tour en salle 2025/2026 de la Poule Espoir Mixte par une nette victoire 39:26 contre HB Esch, deuxième du classement. L\\'équipe est restée concentrée, a combattu ensemble et reste invaincue en tête. Une superbe phase de saison pour nos jeunes de Mersch ! 💛💙 🏆',\n            newsU11Eyebrow: 'U11 Elite · Fin de saison',\n            newsU11Title: 'Les U11 Elite terminent la saison en force',\n            newsU11Body: 'Nos U11 Elite ont encore montré en fin de saison tout le potentiel de cette équipe. Dans le duel pour la 5e place contre HC Standard, Mersch75 a remporté les deux matchs : 23:16 à domicile et 22:18 à l\\'extérieur. Une belle récompense pour une saison engagée et une très belle conclusion pour nos jeunes de Mersch. 💛💙',"
    ),
    (
        "            newsU13Body: 'Mit einer starken Leistung hat unsere U13 die Hallenrunde 2025/2026 in der Mixte Poule Espoir abgeschlossen: Gegen den Tabellenzweiten HB Esch gab es einen klaren 39:26-Sieg. Die Mannschaft blieb konzentriert, kämpfte als Team zusammen und bleibt damit ungeschlagen an der Spitze. Eine richtig starke Saisonrunde für unsere jungen Merscher! 💛💙 🏆',",
        "            newsU13Body: 'Mit einer starken Leistung hat unsere U13 die Hallenrunde 2025/2026 in der Mixte Poule Espoir abgeschlossen: Gegen den Tabellenzweiten HB Esch gab es einen klaren 39:26-Sieg. Die Mannschaft blieb konzentriert, kämpfte als Team zusammen und bleibt damit ungeschlagen an der Spitze. Eine richtig starke Saisonrunde für unsere jungen Merscher! 💛💙 🏆',\n            newsU11Eyebrow: 'U11 Elite · Saisonabschluss',\n            newsU11Title: 'U11 Elite schließt die Saison stark ab',\n            newsU11Body: 'Unsere U11 Elite hat auch am Ende der Saison noch einmal gezeigt, was in dieser Mannschaft steckt. Im Duell um Platz 5 gegen HC Standard konnte Mersch75 beide Spiele gewinnen: zuhause mit 23:16 und auswärts mit 22:18. Eine schöne Belohnung für eine engagierte Saison und ein starker Schlussakkord für unsere jungen Merscher. 💛💙',"
    ),
    (
        "            newsU13Body: 'With a strong performance, our U13 completed the 2025/2026 indoor round in the Mixed Poule Espoir with a clear 39:26 win against second-placed HB Esch. The team stayed focused, fought together and remains unbeaten at the top. A fantastic round for our young Mersch players! 💛💙 🏆',",
        "            newsU13Body: 'With a strong performance, our U13 completed the 2025/2026 indoor round in the Mixed Poule Espoir with a clear 39:26 win against second-placed HB Esch. The team stayed focused, fought together and remains unbeaten at the top. A fantastic round for our young Mersch players! 💛💙 🏆',\n            newsU11Eyebrow: 'U11 Elite · Season finale',\n            newsU11Title: 'U11 Elite finish the season strongly',\n            newsU11Body: 'Our U11 Elite once again showed at the end of the season what this team is capable of. In the duel for 5th place against HC Standard, Mersch75 won both matches: 23:16 at home and 22:18 away. A fine reward for a committed season and a strong final note for our young Mersch players. 💛💙',"
    ),
    (
        "            newsU13Body: 'Com uma grande prestação, a nossa U13 terminou a ronda indoor 2025/2026 na Poule Espoir Mixte com uma clara vitória por 39:26 frente ao HB Esch, segundo classificado. A equipa manteve-se concentrada, lutou em conjunto e continua invicta no topo. Uma fase fantástica para os nossos jovens de Mersch! 💛💙 🏆',",
        "            newsU13Body: 'Com uma grande prestação, a nossa U13 terminou a ronda indoor 2025/2026 na Poule Espoir Mixte com uma clara vitória por 39:26 frente ao HB Esch, segundo classificado. A equipa manteve-se concentrada, lutou em conjunto e continua invicta no topo. Uma fase fantástica para os nossos jovens de Mersch! 💛💙 🏆',\n            newsU11Eyebrow: 'U11 Elite · Final da época',\n            newsU11Title: 'U11 Elite termina a época em força',\n            newsU11Body: 'A nossa U11 Elite voltou a mostrar no fim da época todo o potencial desta equipa. No duelo pelo 5.º lugar contra o HC Standard, o Mersch75 venceu os dois jogos: 23:16 em casa e 22:18 fora. Uma bela recompensa por uma época empenhada e um final forte para os nossos jovens de Mersch. 💛💙',"
    ),
]

for old, new in replacements:
    if old not in s:
        print('missing marker:', old[:80])
    elif 'newsU11Eyebrow' not in s[s.find(old)-300:s.find(old)+300]:
        s = s.replace(old, new, 1)

p.write_text(s, encoding='utf-8')
