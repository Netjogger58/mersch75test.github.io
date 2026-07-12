function syncCurrentYear() {
    document.querySelectorAll('#current-year').forEach((target) => {
        target.textContent = new Date().getFullYear();
    });
}

function ensureSiteLanguageSwitcher() {
    // Wenn die Seite bereits einen Sprachumschalter mitbringt, nichts tun.
    if (document.querySelector('.site-language-switcher')) return;

    const header = document.querySelector('.site-header');
    if (!header) return;

    const navToggle = header.querySelector('.nav-toggle');

    const nav = document.createElement('nav');
    nav.className = 'site-language-switcher legal-lang-switcher';
    nav.setAttribute('aria-label', 'Sprache auswählen');
    nav.innerHTML = [
        '<button type="button" class="is-active" data-site-lang-button="lb" aria-pressed="true"><span class="lang-flag flag-lu" aria-hidden="true"></span><span>LU</span></button>',
        '<button type="button" data-site-lang-button="fr" aria-pressed="false"><span class="lang-flag flag-fr" aria-hidden="true"></span><span>FR</span></button>',
        '<button type="button" data-site-lang-button="de" aria-pressed="false"><span class="lang-flag flag-de" aria-hidden="true"></span><span>DE</span></button>',
        '<button type="button" data-site-lang-button="en" aria-pressed="false"><span class="lang-flag flag-en" aria-hidden="true"></span><span>EN</span></button>',
        '<button type="button" data-site-lang-button="pt" aria-pressed="false"><span class="lang-flag flag-pt" aria-hidden="true"></span><span>PT</span></button>'
    ].join('');

    if (navToggle) {
        header.insertBefore(nav, navToggle);
    } else {
        header.append(nav);
    }
}

function initializeSiteLanguage() {
    const languageButtons = Array.from(document.querySelectorAll('[data-site-lang-button]'));
    const storageKey = 'mersch75-language';
    const fallbackLanguage = 'lb';
    const supportedLanguages = ['lb', 'fr', 'de', 'en', 'pt'];
    const textTargets = Array.from(document.querySelectorAll('[data-i18n]'));
    const htmlTargets = Array.from(document.querySelectorAll('[data-i18n-html]'));
    const attributeTargets = Array.from(document.querySelectorAll('[data-i18n-attr]'));

    const translations = {
        lb: {
            pageTitle: 'Mersch75 Handball',
            pageDescription: 'Mersch75 Handball: Veräinsiwwerbléck, Spillplang, Training, News, Galerie a Matmaachen.',
            brandHomeAria: 'Mersch75 Startsäit',
            brandTagline: 'Zesumme staark',
            compassEyebrow: 'Zesumme Staark',
            compassTitle: 'ZESUMME STAARK – Eise Kompass',
            compassBody: '<h2>Wien mir sinn</h2><p>Den Handball Club Mersch75 ass zënter 1975 eng fest Gréisst am Lëtzebuerger Sport. No enger beweegter Geschicht hu mir eis 2023 nei erfonnt: Mir setzen zu 100% op eis eege Jugend an eis lokal Identitéit.</p><h2>Eis DNA: S.T.A.A.R.K.</h2><p>Eist Motto ass Programm. Jidderee Buschtaf steet fir e Wäert, dee mir um Terrain an donieft liewen:</p><ul><li><strong>Solidaritéit</strong> – Ee fir all, all fir een.</li><li><strong>Toleranz</strong> – Villfalt ass eis Stäerkt.</li><li><strong>Akzeptanz</strong> – Jiddereen ass wëllkomm.</li><li><strong>Anescht</strong> – Perséinlechkeet gëtt gefërdert.</li><li><strong>Respekt</strong> – Fairplay ass Gesetz.</li><li><strong>Kommunikatioun</strong> – Mir schwätze mateneen, net iwwereneen.</li></ul><h2>Eise Wee: Kuerz &amp; Kompakt</h2><p><strong>1975:</strong> Grënnung duerch de Michel Goergen.<br><strong>1978–1985:</strong> Déi éischt gëllen Ära an der héchster Divisioun.<br><strong>2014:</strong> De groussen Opstig no 30 Joer Gedold an Opbauaarbecht.<br><strong>2015–2023:</strong> D’Léierjoren. Versuch vum Erfolleg duerch deier Investitiounen an extern Spiller. Resultat: Sportlech Top (Axa-League), awer finanziell a mënschlech schwiereg.<br><strong>Zënter 2023:</strong> Den Neistart. Strategesch Ëmorientéierung ewech vum Semi-Professionalismus, hin zu enger professioneller Jugendaarbecht.</p><h2>Firwat Mersch75?</h2><p>Well mir méi si wéi e Sportveräin. Mir sinn eng Erliewensschoul. Mir investéieren eis Ressourcen net an deier Transferte, mä an d’Ausbildung vun eise Kanner. Mat eisem Jugendkoordinator Max Blanc (Tel: 661 406 836) garantéiere mir Top-Training a perséinlech Betreiung.</p><p><strong>Eist Zil:</strong> Nohaltegen Erfolleg mat Spiller aus eiser eegener Rei.</p><p><strong>Deng Plaz:</strong> Ass bei eis – ob als Spiller, Fan oder Benevollen.</p><p>#ZesummeStaark #HBMersch75 #MatHäerzaSéil</p>',
            compassBackHome: 'Zréck op d\'Homepage',
            newsRefEyebrow: 'FLH · Cycle inférieur',
            newsRefTitle: 'Jonk Schidsrichter: Aschreiwunge sinn op',
            newsRefBody: 'D\'Formatioun fir jonk Schidsrichter am FLH Cycle inférieur ass online. Eng flott Geleeënheet fir déi nächst Generatioun, Verantwortung ze iwwerhuelen.',
            newsRefCta: 'Info & Aschreiwung',
            trainingPageTitle: 'Training | Mersch75 Handball',
            trainingPageDescription: 'Training beim Mersch75: Trainingsplang, Gruppen, Halen a Jugendkoordinatioun op ee Bléck.',
            trainingHeroLogoAlt: 'Team Training Logo',
            trainingTrainerstaff: 'Trainerteam',
            trainingTrialRequest: 'Probetraining ufroen',
            trainingScheduleOpen: 'Trainingsplang am Vollbild opmaachen',
            trainingScheduleClose: 'Vollbild zoumaachen',
            trainingYouthCoord: 'JUGENDKOORDINATIOUN:',
            trainingYouthCoordBody: 'Fir de Jugendberäich si de Max Blanc (LUXQF4) an de Louis Van der Weken (LUXQF2Bis) zoustänneg.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Tel.: Max Blanc 661 406 836',
            navMenu: 'Menü',
            navClose: 'Menü zoumaachen',
            navHome: 'Startsäit',
            navLiveCenter: 'Spillplang',
            navTraining: 'Training',
            navTrainerstaff: 'Trainerteam',
            navNews: 'News',
            navStatistics: 'Statistik',
            navStatisticsArchive: 'Statistik 25/26',
            navJoin: 'Join Us',
            navSponsors: 'Sponsoren / Partner',
            navComite: 'Comité',
            navInside: 'Inside',
            navGallery: 'Galerie',
            navHistory: 'Geschicht',
            navLinks: 'Nëtzlech Linken',
            usefulFanshopTitle: 'Mersch75 Fanshop',
            usefulFanshopMeta: 'Hoodies, T-Shirts & Fanartikelen',
            navHallenkarte: 'Hallekaart',
            navContact: 'Kontakt',
            posterAlt: 'Mersch75 Matchposter',
            posterLandscapeTitle: 'Querformat eroflueden',
            posterPortraitTitle: 'Portraitformat eroflueden',
            posterShareTitle: 'Poster deelen',
            posterLandscapeLabel: 'Querformat',
            posterPortraitLabel: 'Portraitformat',
            posterShareLabel: 'Deelen',
            ballJumpAria: 'Zum Spillplang',
            ballJumpSchedule: 'Zum Spillplang',
            ballJumpNews: 'Bei d\'Noriichten',
            eventsEyebrow: 'Evenementer & Jugend',
            eventsTitle: 'Weekender, Aktivitéiten an Ulafplaze fir nei Spiller.',
            eventsBody: 'Dës Rubrik verbënnt d\'Kommunikatioun vun Evenementer, den Entrée an d\'Veräinsliewen an e kloeren Opruff zum Handelen.',
            eventsPillYouth: 'U4 & Jugend',
            eventsPillJoin: 'Join Us',
            eventsPillCommunity: 'Communautéit',
            eventsPrimary: 'Matmaachen',
            eventsSecondary: 'Zesumme staark',
            eventsImageAlt: 'U4 Events',
            newsKicker: 'News',
            newsHeading: 'Aktuelles vum Mersch75',
            newsFanshopEyebrow: 'Fanshop · Mersch75',
            newsFanshopTitle: 'Dro eis Faarwen och nieft dem Terrain',
            newsFanshopBody: 'Am Mersch75-Fanshop fënns du Hoodies, T-Shirten an aner Fanartikelen am Look vum Club. Weis däi Support, stäerk d’Mierscher Gemeinschaft a dro eis blo-giel Faarwe mat Stolz.',
            newsFanshopPillClub: '💛💙 Mersch75',
            newsFanshopPillHoodies: 'Hoodies',
            newsFanshopPillShirts: 'T-Shirts',
            newsFanshopCta: 'Zum Fanshop',
            newsGirlsDayEyebrow: 'Girls Handball Day',
            newsGirlsDayTitle: 'Schnupper-Training fir Meedercher',
            newsGirlsDayBody: 'Den 20.06. invitéiert Mersch75 Meedercher vu 7 bis 12 Joer op e flotten Handball-Schnupper-Training. Vun 10h00 bis 12h00 kanns du an der Hall Omnisports zu Miersch de Sport ausprobéieren, Spaass hunn an eis blo-giel Gemeinschaft kenneléieren.',
            newsGirlsDayPillDate: '📅 20.06',
            newsGirlsDayPillTime: '⏱ 10h00-12h00',
            newsGirlsDayPillAge: '7-12 Joer',
            newsGirlsDayCta: 'Elo umellen',
            newsU13Eyebrow: 'U13 Mixte · Poule Espoir',
            newsU13Title: 'Eis U13 bleift ongeschloen!',
            newsU13Body: 'Mat enger staarker Leeschtung huet eis U13 d\'Halleronn 2025/2026 an der Mixte Poule Espoir ofgeschloss: géint den Tabellenzweeten HB Esch gouf et eng kloer 39:26-Victoire. D\'Ekipp ass konzentréiert bliwwen, huet als Team zesumme gekämpft a bleift domat ongeschloen un der Spëtzt. Eng immens flott Saisonronn fir eis jonk Mierscher! 💛💙 🏆',
            newsMenEyebrow: 'Männer · Saison 25/26',
            newsMenTitle: 'Eis Männer ginn als Team virun',
            newsMenBody: 'Mat vill Asaz, Tempo a Charakter weisen eis Männer och dës Saison, wat Mersch75 ausmécht: zesumme schaffen, Verantwortung iwwerhuelen an all Match mat voller Energie ugoen. D\'Ekipp bleift e wichtege Pilier vum Club a gëtt de jonke Spiller e staarkt Beispill. 💛💙',
            newsWomenEyebrow: 'Fraen · Saison 25/26',
            newsWomenTitle: 'Eis Fraen stinn fir Kampfgeescht a Gemeinschaft',
            newsWomenBody: 'Eis Fraen droen d\'Mersch75-Faarwen mat Häerz, Disziplin a vill Teamspirit. All Training an all Match weisen, wéi vill Energie an dëser Ekipp stécht. Eng staark Grupp, déi mat Freed, Courage a Solidaritéit fir de Club um Terrain steet. 💛💙',
            newsU11Eyebrow: 'U11 Elite · Saisonofschloss',
            newsU11Title: 'U11 Elite schléisst d\'Saison staark of',
            newsU11Body: 'Eis U11 Elite huet och um Enn vun der Saison nach eemol gewisen, wat an der Ekipp stécht. Am Duell ëm Plaz 5 géint HC Standard konnt Mersch75 béid Matcher gewannen: doheem mat 23:16 an auswäerts mat 22:18. Eng flott Belounung fir eng engagéiert Saison an e staarke Schlussakkord fir eis jonk Mierscher. 💛💙',
            newsStatsEyebrow: 'Saisonstatistik 25/26',
            newsStatsTitle: 'STATISTIKEN VUN EISEN EKIPPEN OP ENGER PLAZ',
            newsStatsBody: 'D\'Saisonstatistik 2025/2026 ass live: Tabellen, Resultater an Torschützenlëschten fir Männer, Fraen, U15, U13 an U11 – iwwersiichtlech an aktuell.',
            newsStatsPillMen: 'Männer',
            newsStatsPillWomen: 'Fraen',
            newsStatsPillLive: 'Live',
            newsStatsCta: 'Statistik kucken',
            newsStatsImageAlt: 'Saisonstatistik',
            newsSiteEyebrow: 'Neie Look',
            newsSiteTitle: 'D\'Websäit erstrahlt an engem neie Liicht.',
            newsSiteBody: 'Frësch Optik, méi kloer Struktur a séier Navigatioun: déi nei Mersch75-Säit bréngt Spillplang, Statistiken an Infoen iwwersiichtlech zesummen.',
            newsSitePillDesign: 'Neit Design',
            newsSitePillFast: 'Méi séier',
            newsSitePillClear: 'Méi kloer',
            newsSiteCta: 'Entdecken',
            newsSiteImageAlt: 'Mersch75',
            infoTitle: 'National an international Informatiounen',
            infoAxaAria: 'AXA League Links',
            infoWomen: 'AXA League Fraen',
            infoMen: 'AXA League Männer',
            sponsorsTitle: 'D\' finanziell Hëllef vun eise Partner bedeit d\'Realisatioun vun eise Visiounen',
            sponsorsAlt: 'Mersch75 Sponsoren',
            footerBrandBody: 'Handball zu Miersch mat engem méi kloeren digitalen Optrëtt: séier Informatiounen, e méi rouegt Layout an eng Struktur, déi fir GitHub Pages gebaut ass.',
            footerQuick: 'Schnellzougrëff',
            footerContact: 'Kontakt',
            footerClub: 'Veräin',
            footerTrainerstaff: 'Trainerteam',
            footerUsefulLinks: 'Nëtzlech Linken',
            footerLegalHint: 'Impressum an Dateschutz kommen als nächst statesch Servicessäiten derbäi.',
            footerAdmin: 'Admin Login'
        },
        fr: {
            pageTitle: 'Mersch75 Handball',
            pageDescription: 'Mersch75 Handball : aperçu du club, calendrier, entraînement, actualités, galerie et participation.',
            brandHomeAria: 'Accueil Mersch75',
            brandTagline: 'Ensemble plus forts',
            compassEyebrow: 'Zesumme Staark',
            compassTitle: 'ZESUMME STAARK – Notre boussole',
            compassBody: '<h2>Qui sommes-nous ?</h2><p>Le Handball Club Mersch75 est une référence du sport luxembourgeois depuis 1975. Après une histoire mouvementée, nous nous sommes réinventés en 2023 : nous misons à 100% sur notre propre jeunesse et notre identité locale.</p><h2>Notre ADN : S.T.A.A.R.K.</h2><p>Notre devise est un programme. Chaque lettre représente une valeur que nous vivons sur le terrain et en dehors :</p><ul><li><strong>Solidarité</strong> – Un pour tous, tous pour un.</li><li><strong>Tolérance</strong> – La diversité est notre force.</li><li><strong>Acceptation</strong> – Tout le monde est bienvenu.</li><li><strong>Différence</strong> – La personnalité est encouragée.</li><li><strong>Respect</strong> – Le fair-play est la règle.</li><li><strong>Communication</strong> – Nous parlons ensemble, pas les uns sur les autres.</li></ul><h2>Notre chemin : bref &amp; compact</h2><p><strong>1975 :</strong> Fondation par Michel Goergen.<br><strong>1978–1985 :</strong> La première grande époque dans la plus haute division.<br><strong>2014 :</strong> La grande montée après 30 ans de patience et de travail de construction.<br><strong>2015–2023 :</strong> Les années d’apprentissage. Tentative de réussite par des investissements coûteux et des joueurs externes. Résultat : sportivement au top (Axa-League), mais financièrement et humainement difficile.<br><strong>Depuis 2023 :</strong> Le nouveau départ. Réorientation stratégique loin du semi-professionnalisme, vers un travail de formation des jeunes professionnel.</p><h2>Pourquoi Mersch75 ?</h2><p>Parce que nous sommes plus qu’un club sportif. Nous sommes une école de vie. Nous n’investissons pas nos ressources dans des transferts coûteux, mais dans la formation de nos enfants. Avec notre coordinateur jeunes Max Blanc (Tél. : 661 406 836), nous garantissons un entraînement de qualité et un accompagnement personnel.</p><p><strong>Notre objectif :</strong> Un succès durable avec des joueurs issus de nos propres rangs.</p><p><strong>Ta place :</strong> Elle est chez nous – comme joueur, supporter ou bénévole.</p><p>#ZesummeStaark #HBMersch75 #MatHäerzaSéil</p>',
            compassBackHome: 'Retour à l\'accueil',
            newsRefEyebrow: 'FLH · Cycle inférieur',
            newsRefTitle: 'Jeunes arbitres : inscriptions ouvertes',
            newsRefBody: 'La formation pour jeunes arbitres du FLH Cycle inférieur est en ligne. Une belle occasion pour la prochaine génération de prendre des responsabilités.',
            newsRefCta: 'Infos & inscription',
            trainingPageTitle: 'Entraînement | Mersch75 Handball',
            trainingPageDescription: 'Entraînement au Mersch75 : planning, groupes, salles et coordination des jeunes en un coup d\'oeil.',
            trainingHeroLogoAlt: 'Logo team training',
            trainingTrainerstaff: 'Encadrement',
            trainingTrialRequest: 'Demander un entraînement d\'essai',
            trainingScheduleOpen: 'Ouvrir le planning en plein écran',
            trainingScheduleClose: 'Fermer le plein écran',
            trainingYouthCoord: 'COORDINATION JEUNES:',
            trainingYouthCoordBody: 'Le secteur des jeunes est coordonné par Max Blanc (LUXQF4) et Louis Van der Weken (LUXQF2Bis).',
            trainingInfoLabel: 'Info :',
            trainingPhoneLabel: 'Tél. : Max Blanc 661 406 836',
            navMenu: 'Menu',
            navClose: 'Fermer le menu',
            navHome: 'Accueil',
            navLiveCenter: 'Calendrier',
            navTraining: 'Entraînement',
            navTrainerstaff: 'Encadrement',
            navNews: 'Actualités',
            navStatistics: 'Statistiques',
            navStatisticsArchive: 'Statistiques 25/26',
            navJoin: 'Join Us',
            navSponsors: 'Sponsors / Partenaires',
            navComite: 'Comité',
            navInside: 'Inside',
            navGallery: 'Galerie',
            navHistory: 'Histoire',
            navLinks: 'Liens utiles',
            usefulFanshopTitle: 'Fanshop Mersch75',
            usefulFanshopMeta: 'Hoodies, T-shirts & articles supporters',
            navHallenkarte: 'Carte des salles',
            navContact: 'Contact',
            posterAlt: 'Affiche du match Mersch75',
            posterLandscapeTitle: 'Télécharger en paysage',
            posterPortraitTitle: 'Télécharger en portrait',
            posterShareTitle: 'Partager l\'affiche',
            posterLandscapeLabel: 'Paysage',
            posterPortraitLabel: 'Portrait',
            posterShareLabel: 'Partager',
            ballJumpAria: 'Vers le calendrier',
            ballJumpSchedule: 'Vers le calendrier',
            ballJumpNews: 'Vers les actualités',
            eventsEyebrow: 'Événements & relève',
            eventsTitle: 'Week-ends, activités et points d\'entrée pour les nouveaux joueurs.',
            eventsBody: 'Cette zone relie la communication des événements, l\'entrée dans la vie du club et un appel à l\'action clair.',
            eventsPillYouth: 'U4 & relève',
            eventsPillJoin: 'Join Us',
            eventsPillCommunity: 'Communauté',
            eventsPrimary: 'Participer',
            eventsSecondary: 'Ensemble plus forts',
            eventsImageAlt: 'Événements U4',
            newsKicker: 'Actualités',
            newsHeading: 'L\'actualité du Mersch75',
            newsFanshopEyebrow: 'Fanshop · Mersch75',
            newsFanshopTitle: 'Porte nos couleurs aussi en dehors du terrain',
            newsFanshopBody: 'Dans le Fanshop Mersch75, tu peux commander des hoodies, des T-shirts et d’autres articles aux couleurs du club. Montre ton soutien, renforce la communauté de Mersch et porte fièrement le bleu et le jaune.',
            newsFanshopPillClub: '💛💙 Mersch75',
            newsFanshopPillHoodies: 'Hoodies',
            newsFanshopPillShirts: 'T-shirts',
            newsFanshopCta: 'Vers le Fanshop',
            newsU13Eyebrow: 'U13 Mixte · Poule Espoir',
            newsGirlsDayEyebrow: 'Girls Handball Day',
            newsGirlsDayTitle: 'Séance découverte pour filles',
            newsGirlsDayBody: 'Le 20.06, Mersch75 invite les filles de 7 à 12 ans à une séance découverte de handball. De 10h00 à 12h00, viens essayer le handball à la Hall Omnisports de Mersch, t’amuser et découvrir notre communauté bleue et jaune.',
            newsGirlsDayPillDate: '📅 20.06',
            newsGirlsDayPillTime: '⏱ 10h00-12h00',
            newsGirlsDayPillAge: '7-12 ans',
            newsGirlsDayCta: 'S’inscrire',
            newsU13Title: 'Nos U13 restent invaincus !',
            newsU13Body: 'Avec une très belle prestation, nos U13 ont terminé le tour en salle 2025/2026 de la Poule Espoir Mixte par une nette victoire 39:26 contre HB Esch, deuxième du classement. L\'équipe est restée concentrée, a combattu ensemble et reste invaincue en tête. Une superbe phase de saison pour nos jeunes de Mersch ! 💛💙 🏆',
            newsMenEyebrow: 'Hommes · Saison 25/26',
            newsMenTitle: 'Nos hommes avancent en équipe',
            newsMenBody: 'Avec engagement, rythme et caractère, nos hommes montrent une nouvelle fois ce qui fait la force du Mersch75 : travailler ensemble, prendre des responsabilités et aborder chaque match avec énergie. L’équipe reste un pilier important du club et un bel exemple pour les jeunes joueurs. 💛💙',
            newsWomenEyebrow: 'Femmes · Saison 25/26',
            newsWomenTitle: 'Nos femmes incarnent l’esprit d’équipe et le combat',
            newsWomenBody: 'Nos femmes portent les couleurs du Mersch75 avec cœur, discipline et beaucoup d’esprit d’équipe. À chaque entraînement et à chaque match, elles montrent l’énergie de ce groupe. Une équipe forte, courageuse et solidaire sur le terrain. 💛💙',
            newsU11Eyebrow: 'U11 Elite · Fin de saison',
            newsU11Title: 'Les U11 Elite terminent la saison en force',
            newsU11Body: 'Nos U11 Elite ont encore montré en fin de saison tout le potentiel de cette équipe. Dans le duel pour la 5e place contre HC Standard, Mersch75 a remporté les deux matchs : 23:16 à domicile et 22:18 à l\'extérieur. Une belle récompense pour une saison engagée et une très belle conclusion pour nos jeunes de Mersch. 💛💙',
            newsStatsEyebrow: 'Statistiques de saison 25/26',
            newsStatsTitle: 'STATISTIQUES DE NOS ÉQUIPES AU MÊME ENDROIT',
            newsStatsBody: 'Les statistiques de la saison 2025/2026 sont en ligne : classements, résultats et meilleurs buteurs pour les hommes, les femmes, U15, U13 et U11 – clairs et à jour.',
            newsStatsPillMen: 'Hommes',
            newsStatsPillWomen: 'Femmes',
            newsStatsPillLive: 'Live',
            newsStatsCta: 'Voir les statistiques',
            newsStatsImageAlt: 'Statistiques de saison',
            newsSiteEyebrow: 'Nouveau look',
            newsSiteTitle: 'Le site rayonne sous un nouveau jour.',
            newsSiteBody: 'Nouveau design, structure plus claire et navigation rapide : le nouveau site Mersch75 réunit calendrier, statistiques et infos en un coup d\'oeil.',
            newsSitePillDesign: 'Nouveau design',
            newsSitePillFast: 'Plus rapide',
            newsSitePillClear: 'Plus clair',
            newsSiteCta: 'Découvrir',
            newsSiteImageAlt: 'Mersch75',
            infoTitle: 'Infos nationales et internationales',
            infoAxaAria: 'Liens AXA League',
            infoWomen: 'AXA League Femmes',
            infoMen: 'AXA League Hommes',
            sponsorsTitle: 'Nos sponsors',
            sponsorsAlt: 'Sponsors Mersch75',
            footerBrandBody: 'Le handball à Mersch avec une présence numérique plus claire : informations rapides, mise en page plus calme et structure pensée pour GitHub Pages.',
            footerQuick: 'Accès rapide',
            footerContact: 'Contact',
            footerClub: 'Club',
            footerTrainerstaff: 'Encadrement',
            footerUsefulLinks: 'Liens utiles',
            footerLegalHint: 'Mentions légales et protection des données seront ajoutées comme pages de service statiques.',
            footerAdmin: 'Connexion admin'
        },
        de: {
            pageTitle: 'Mersch75 Handball',
            pageDescription: 'Mersch75 Handball: Vereinsübersicht, Spielplan, Training, News, Galerie und Mitmachen.',
            brandHomeAria: 'Mersch75 Startseite',
            brandTagline: 'Zusammen stark',
            compassEyebrow: 'Zesumme Staark',
            compassTitle: 'ZESUMME STAARK – Unser Kompass',
            compassBody: '<h2>Wer wir sind</h2><p>Der Handball Club Mersch75 ist seit 1975 eine feste Größe im Luxemburger Sport. Nach einer bewegten Geschichte haben wir uns 2023 neu erfunden: Wir setzen zu 100% auf unsere eigene Jugend und unsere lokale Identität.</p><h2>Unsere DNA: S.T.A.A.R.K.</h2><p>Unser Motto ist Programm. Jeder Buchstabe steht für einen Wert, den wir auf dem Feld und daneben leben:</p><ul><li><strong>Solidarität</strong> – Einer für alle, alle für einen.</li><li><strong>Toleranz</strong> – Vielfalt ist unsere Stärke.</li><li><strong>Akzeptanz</strong> – Jeder ist willkommen.</li><li><strong>Anders</strong> – Persönlichkeit wird gefördert.</li><li><strong>Respekt</strong> – Fairplay ist Gesetz.</li><li><strong>Kommunikation</strong> – Wir reden miteinander, nicht übereinander.</li></ul><h2>Unser Weg: kurz &amp; kompakt</h2><p><strong>1975:</strong> Gründung durch Michel Goergen.<br><strong>1978–1985:</strong> Die erste goldene Ära in der höchsten Division.<br><strong>2014:</strong> Der große Aufstieg nach 30 Jahren Geduld und Aufbauarbeit.<br><strong>2015–2023:</strong> Die Lehrjahre. Versuch des Erfolgs durch teure Investitionen und externe Spieler. Ergebnis: sportlich top (Axa-League), aber finanziell und menschlich schwierig.<br><strong>Seit 2023:</strong> Der Neustart. Strategische Neuausrichtung weg vom Semi-Professionalismus, hin zu professioneller Jugendarbeit.</p><h2>Warum Mersch75?</h2><p>Weil wir mehr sind als ein Sportverein. Wir sind eine Erlebnisschule. Wir investieren unsere Ressourcen nicht in teure Transfers, sondern in die Ausbildung unserer Kinder. Mit unserem Jugendkoordinator Max Blanc (Tel.: 661 406 836) garantieren wir Top-Training und persönliche Betreuung.</p><p><strong>Unser Ziel:</strong> Nachhaltiger Erfolg mit Spielern aus den eigenen Reihen.</p><p><strong>Dein Platz:</strong> Ist bei uns – ob als Spieler, Fan oder Ehrenamtlicher.</p><p>#ZesummeStaark #HBMersch75 #MatHäerzaSéil</p>',
            compassBackHome: 'Zurück zur Homepage',
            newsRefEyebrow: 'FLH · Cycle inférieur',
            newsRefTitle: 'Junge Schiedsrichter: Anmeldungen offen',
            newsRefBody: 'Die Ausbildung für junge Schiedsrichter im FLH Cycle inférieur ist online. Eine gute Gelegenheit für die nächste Generation, Verantwortung zu übernehmen.',
            newsRefCta: 'Info & Anmeldung',
            trainingPageTitle: 'Training | Mersch75 Handball',
            trainingPageDescription: 'Training bei Mersch75: Trainingsplan, Gruppen, Hallen und Jugendkoordination auf einen Blick.',
            trainingHeroLogoAlt: 'Team-Training Logo',
            trainingTrainerstaff: 'Trainerstaff',
            trainingTrialRequest: 'Probetraining anfragen',
            trainingScheduleOpen: 'Trainingsplan im Vollbild öffnen',
            trainingScheduleClose: 'Vollbild schließen',
            trainingYouthCoord: 'JUGENDKOORDINATION:',
            trainingYouthCoordBody: 'Für den Jugendbereich sind Max Blanc (LUXQF4) und Louis Van der Weken (LUXQF2Bis) zuständig.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Tel.: Max Blanc 661 406 836',
            navMenu: 'Menü',
            navClose: 'Menü schließen',
            navHome: 'Startseite',
            navLiveCenter: 'Spielplan',
            navTraining: 'Training',
            navTrainerstaff: 'Trainerstaff',
            navNews: 'News',
            navStatistics: 'Statistik',
            navStatisticsArchive: 'Statistik 25/26',
            navJoin: 'Join Us',
            navSponsors: 'Sponsoren / Partner',
            navComite: 'Comité',
            navInside: 'Inside',
            navGallery: 'Galerie',
            navHistory: 'Geschicht',
            navLinks: 'Nützliche Links',
            usefulFanshopTitle: 'Mersch75 Fanshop',
            usefulFanshopMeta: 'Hoodies, T-Shirts & Fanartikel',
            navHallenkarte: 'Hallenkarte',
            navContact: 'Kontakt',
            posterAlt: 'Mersch75 Matchposter',
            posterLandscapeTitle: 'Landscape herunterladen',
            posterPortraitTitle: 'Portrait herunterladen',
            posterShareTitle: 'Poster teilen',
            posterLandscapeLabel: 'Landscape',
            posterPortraitLabel: 'Portrait',
            posterShareLabel: 'Teilen',
            ballJumpAria: 'Zum Spielplan',
            ballJumpSchedule: 'Zum Spielplan',
            ballJumpNews: 'Zu den News',
            eventsEyebrow: 'Events & Nachwuchs',
            eventsTitle: 'Wochenenden, Aktivitäten und Einstiegspunkte für neue Spieler.',
            eventsBody: 'Diese Fläche verbindet Event-Kommunikation, Einstieg ins Vereinsleben und einen klaren Call-to-Action.',
            eventsPillYouth: 'U4 & Nachwuchs',
            eventsPillJoin: 'Join Us',
            eventsPillCommunity: 'Community',
            eventsPrimary: 'Mitmachen',
            eventsSecondary: 'Zusammen stark',
            eventsImageAlt: 'U4 Events',
            newsKicker: 'News',
            newsHeading: 'Aktuelles vom Mersch75',
            newsFanshopEyebrow: 'Fanshop · Mersch75',
            newsFanshopTitle: 'Trage unsere Farben auch neben dem Spielfeld',
            newsFanshopBody: 'Im Mersch75-Fanshop kannst du Hoodies, T-Shirts und weitere Fanartikel im Vereins-Look bestellen. Zeig deinen Support, stärke die Merscher Gemeinschaft und trage Blau-Gelb mit Stolz.',
            newsFanshopPillClub: '💛💙 Mersch75',
            newsFanshopPillHoodies: 'Hoodies',
            newsFanshopPillShirts: 'T-Shirts',
            newsFanshopCta: 'Zum Fanshop',
            newsU13Eyebrow: 'U13 Mixte · Poule Espoir',
            newsGirlsDayEyebrow: 'Girls Handball Day',
            newsGirlsDayTitle: 'Schnupper-Training für Mädchen',
            newsGirlsDayBody: 'Am 20.06. lädt Mersch75 Mädchen von 7 bis 12 Jahren zu einem Handball-Schnupper-Training ein. Von 10:00 bis 12:00 Uhr kannst du in der Hall Omnisports in Mersch den Sport ausprobieren, Spaß haben und unsere blau-gelbe Gemeinschaft kennen lernen.',
            newsGirlsDayPillDate: '📅 20.06',
            newsGirlsDayPillTime: '⏱ 10:00-12:00',
            newsGirlsDayPillAge: '7-12 Jahre',
            newsGirlsDayCta: 'Jetzt anmelden',
            newsU13Title: 'Unsere U13 bleibt ungeschlagen!',
            newsU13Body: 'Mit einer starken Leistung hat unsere U13 die Hallenrunde 2025/2026 in der Mixte Poule Espoir abgeschlossen: Gegen den Tabellenzweiten HB Esch gab es einen klaren 39:26-Sieg. Die Mannschaft blieb konzentriert, kämpfte als Team zusammen und bleibt damit ungeschlagen an der Spitze. Eine richtig starke Saisonrunde für unsere jungen Merscher! 💛💙 🏆',
            newsMenEyebrow: 'Männer · Saison 25/26',
            newsMenTitle: 'Unsere Männer gehen als Team voran',
            newsMenBody: 'Mit Einsatz, Tempo und Charakter zeigen unsere Männer auch in dieser Saison, wofür Mersch75 steht: gemeinsam arbeiten, Verantwortung übernehmen und jedes Spiel mit voller Energie angehen. Die Mannschaft bleibt ein wichtiger Pfeiler des Clubs und ein starkes Vorbild für die jungen Spieler. 💛💙',
            newsWomenEyebrow: 'Frauen · Saison 25/26',
            newsWomenTitle: 'Unsere Frauen stehen für Kampfgeist und Gemeinschaft',
            newsWomenBody: 'Unsere Frauen tragen die Mersch75-Farben mit Herz, Disziplin und viel Teamgeist. In jedem Training und jedem Spiel zeigen sie, wie viel Energie in dieser Mannschaft steckt. Eine starke Gruppe, die mit Freude, Mut und Zusammenhalt für den Club auf dem Feld steht. 💛💙',
            newsU11Eyebrow: 'U11 Elite · Saisonabschluss',
            newsU11Title: 'U11 Elite schließt die Saison stark ab',
            newsU11Body: 'Unsere U11 Elite hat auch am Ende der Saison noch einmal gezeigt, was in dieser Mannschaft steckt. Im Duell um Platz 5 gegen HC Standard konnte Mersch75 beide Spiele gewinnen: zuhause mit 23:16 und auswärts mit 22:18. Eine schöne Belohnung für eine engagierte Saison und ein starker Schlussakkord für unsere jungen Merscher. 💛💙',
            newsStatsEyebrow: 'Saisonstatistik 25/26',
            newsStatsTitle: 'STATISTIKEN UNSERER TEAMS AN EINEM ORT',
            newsStatsBody: 'Die Saisonstatistik 2025/2026 ist live: Tabellen, Ergebnisse und Torschützenlisten für Männer, Frauen, U15, U13 und U11 – übersichtlich und aktuell.',
            newsStatsPillMen: 'Männer',
            newsStatsPillWomen: 'Frauen',
            newsStatsPillLive: 'Live',
            newsStatsCta: 'Statistik ansehen',
            newsStatsImageAlt: 'Saisonstatistik',
            newsSiteEyebrow: 'Neuer Look',
            newsSiteTitle: 'Die Website erstrahlt in neuem Licht.',
            newsSiteBody: 'Frische Optik, klarere Struktur und schnelle Navigation: Die neue Mersch75-Seite bringt Spielplan, Statistiken und Infos übersichtlich zusammen.',
            newsSitePillDesign: 'Neues Design',
            newsSitePillFast: 'Schneller',
            newsSitePillClear: 'Klarer',
            newsSiteCta: 'Entdecken',
            newsSiteImageAlt: 'Mersch75',
            infoTitle: 'Nationale und internationale Infos',
            infoAxaAria: 'AXA League Links',
            infoWomen: 'AXA League Frauen',
            infoMen: 'AXA League Männer',
            sponsorsTitle: 'Unsere Sponsoren',
            sponsorsAlt: 'Mersch75 Sponsoren',
            footerBrandBody: 'Handball in Mersch mit einem klareren digitalen Auftritt: schnelle Informationen, ruhigeres Layout und eine Struktur, die für GitHub Pages gebaut ist.',
            footerQuick: 'Schnellzugriff',
            footerContact: 'Kontakt',
            footerClub: 'Verein',
            footerTrainerstaff: 'Trainerstaff',
            footerUsefulLinks: 'Nützliche Links',
            footerLegalHint: 'Impressum und Datenschutz werden als nächste statische Service-Seiten ergänzt.',
            footerAdmin: 'Admin Login'
        },
        en: {
            pageTitle: 'Mersch75 Handball',
            pageDescription: 'Mersch75 Handball: club overview, schedule, training, news, gallery and joining information.',
            brandHomeAria: 'Mersch75 home',
            brandTagline: 'Stronger together',
            compassEyebrow: 'Zesumme Staark',
            compassTitle: 'ZESUMME STAARK – Our compass',
            compassBody: '<h2>Who we are</h2><p>Handball Club Mersch75 has been a fixture in Luxembourg sport since 1975. After an eventful history, we reinvented ourselves in 2023: we focus 100% on our own youth and our local identity.</p><h2>Our DNA: S.T.A.A.R.K.</h2><p>Our motto is our programme. Each letter stands for a value we live on and off the court:</p><ul><li><strong>Solidarity</strong> – One for all, all for one.</li><li><strong>Tolerance</strong> – Diversity is our strength.</li><li><strong>Acceptance</strong> – Everyone is welcome.</li><li><strong>Different</strong> – Personality is encouraged.</li><li><strong>Respect</strong> – Fair play is the rule.</li><li><strong>Communication</strong> – We talk with each other, not about each other.</li></ul><h2>Our path: short &amp; compact</h2><p><strong>1975:</strong> Founded by Michel Goergen.<br><strong>1978–1985:</strong> The first golden era in the top division.<br><strong>2014:</strong> The big promotion after 30 years of patience and development work.<br><strong>2015–2023:</strong> The learning years. An attempt to achieve success through expensive investments and external players. Result: strong sporting level (Axa-League), but financially and humanly difficult.<br><strong>Since 2023:</strong> The restart. A strategic shift away from semi-professionalism towards professional youth development.</p><h2>Why Mersch75?</h2><p>Because we are more than a sports club. We are a school of life. We do not invest our resources in expensive transfers, but in the education of our children. With our youth coordinator Max Blanc (Tel.: 661 406 836), we guarantee top training and personal support.</p><p><strong>Our goal:</strong> Sustainable success with players from our own ranks.</p><p><strong>Your place:</strong> Is with us – whether as a player, fan or volunteer.</p><p>#ZesummeStaark #HBMersch75 #MatHäerzaSéil</p>',
            compassBackHome: 'Back to homepage',
            newsRefEyebrow: 'FLH · Lower cycle',
            newsRefTitle: 'Young referees: registration is open',
            newsRefBody: 'The FLH lower-cycle training for young referees is online. A great opportunity for the next generation to take responsibility.',
            newsRefCta: 'Info & registration',
            trainingPageTitle: 'Training | Mersch75 Handball',
            trainingPageDescription: 'Training at Mersch75: schedule, groups, halls and youth coordination at a glance.',
            trainingHeroLogoAlt: 'Team training logo',
            trainingTrainerstaff: 'Coaching Staff',
            trainingTrialRequest: 'Request a trial session',
            trainingScheduleOpen: 'Open training schedule fullscreen',
            trainingScheduleClose: 'Close fullscreen',
            trainingYouthCoord: 'YOUTH COORDINATION:',
            trainingYouthCoordBody: 'Max Blanc (LUXQF4) and Louis Van der Weken (LUXQF2Bis) are responsible for the youth section.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Phone: Max Blanc 661 406 836',
            navMenu: 'Menu',
            navClose: 'Close menu',
            navHome: 'Home',
            navLiveCenter: 'Schedule',
            navTraining: 'Training',
            navTrainerstaff: 'Coaching Staff',
            navNews: 'News',
            navStatistics: 'Statistics',
            navStatisticsArchive: 'Statistics 25/26',
            navJoin: 'Join Us',
            navSponsors: 'Sponsors / Partners',
            navComite: 'Committee',
            navInside: 'Inside',
            navGallery: 'Gallery',
            navHistory: 'History',
            navLinks: 'Useful Links',
            usefulFanshopTitle: 'Mersch75 Fanshop',
            usefulFanshopMeta: 'Hoodies, T-shirts & fan items',
            navHallenkarte: 'Venue Map',
            navContact: 'Contact',
            posterAlt: 'Mersch75 match poster',
            posterLandscapeTitle: 'Download landscape version',
            posterPortraitTitle: 'Download portrait version',
            posterShareTitle: 'Share poster',
            posterLandscapeLabel: 'Landscape',
            posterPortraitLabel: 'Portrait',
            posterShareLabel: 'Share',
            ballJumpAria: 'Go to schedule',
            ballJumpSchedule: 'Go to schedule',
            ballJumpNews: 'Go to news',
            eventsEyebrow: 'Events & youth',
            eventsTitle: 'Weekends, activities and entry points for new players.',
            eventsBody: 'This section ties event communication, club onboarding and a clear call to action together.',
            eventsPillYouth: 'U4 & youth',
            eventsPillJoin: 'Join Us',
            eventsPillCommunity: 'Community',
            eventsPrimary: 'Join in',
            eventsSecondary: 'Stronger together',
            eventsImageAlt: 'U4 events',
            newsKicker: 'News',
            newsHeading: 'Latest from Mersch75',
            newsFanshopEyebrow: 'Fanshop · Mersch75',
            newsFanshopTitle: 'Wear our colours beyond the court',
            newsFanshopBody: 'In the Mersch75 Fanshop, you can order hoodies, T-shirts and other fan items in the club look. Show your support, strengthen the Mersch community and wear blue and yellow with pride.',
            newsFanshopPillClub: '💛💙 Mersch75',
            newsFanshopPillHoodies: 'Hoodies',
            newsFanshopPillShirts: 'T-shirts',
            newsFanshopCta: 'Go to Fanshop',
            newsU13Eyebrow: 'U13 Mixed · Poule Espoir',
            newsGirlsDayEyebrow: 'Girls Handball Day',
            newsGirlsDayTitle: 'Try-out training for girls',
            newsGirlsDayBody: 'On 20.06, Mersch75 invites girls aged 7 to 12 to a fun handball try-out session. From 10:00 to 12:00 at the Hall Omnisports in Mersch, you can discover the sport, have fun and get to know our blue and yellow community.',
            newsGirlsDayPillDate: '📅 20.06',
            newsGirlsDayPillTime: '⏱ 10:00-12:00',
            newsGirlsDayPillAge: 'Ages 7-12',
            newsGirlsDayCta: 'Register now',
            newsU13Title: 'Our U13 stay unbeaten!',
            newsU13Body: 'With a strong performance, our U13 completed the 2025/2026 indoor round in the Mixed Poule Espoir with a clear 39:26 win against second-placed HB Esch. The team stayed focused, fought together and remains unbeaten at the top. A fantastic round for our young Mersch players! 💛💙 🏆',
            newsMenEyebrow: 'Men · Season 25/26',
            newsMenTitle: 'Our men lead the way as a team',
            newsMenBody: 'With commitment, pace and character, our men once again show what Mersch75 stands for: working together, taking responsibility and approaching every match with full energy. The team remains an important pillar of the club and a strong example for the young players. 💛💙',
            newsWomenEyebrow: 'Women · Season 25/26',
            newsWomenTitle: 'Our women stand for fighting spirit and togetherness',
            newsWomenBody: 'Our women wear the Mersch75 colours with heart, discipline and strong team spirit. In every training session and every match, they show how much energy this team has. A strong group representing the club with joy, courage and solidarity. 💛💙',
            newsU11Eyebrow: 'U11 Elite · Season finale',
            newsU11Title: 'U11 Elite finish the season strongly',
            newsU11Body: 'Our U11 Elite once again showed at the end of the season what this team is capable of. In the duel for 5th place against HC Standard, Mersch75 won both matches: 23:16 at home and 22:18 away. A fine reward for a committed season and a strong final note for our young Mersch players. 💛💙',
            newsStatsEyebrow: 'Season stats 25/26',
            newsStatsTitle: 'STATS FOR OUR TEAMS IN ONE PLACE',
            newsStatsBody: 'The 2025/2026 season statistics are live: tables, results and top scorers for men, women, U15, U13 and U11 – clear and up to date.',
            newsStatsPillMen: 'Men',
            newsStatsPillWomen: 'Women',
            newsStatsPillLive: 'Live',
            newsStatsCta: 'View statistics',
            newsStatsImageAlt: 'Season statistics',
            newsSiteEyebrow: 'New look',
            newsSiteTitle: 'The website shines in a new light.',
            newsSiteBody: 'Fresh design, clearer structure and fast navigation: the new Mersch75 site brings schedule, statistics and info together at a glance.',
            newsSitePillDesign: 'New design',
            newsSitePillFast: 'Faster',
            newsSitePillClear: 'Clearer',
            newsSiteCta: 'Explore',
            newsSiteImageAlt: 'Mersch75',
            infoTitle: 'National and international info',
            infoAxaAria: 'AXA League links',
            infoWomen: 'AXA League Women',
            infoMen: 'AXA League Men',
            sponsorsTitle: 'Our sponsors',
            sponsorsAlt: 'Mersch75 sponsors',
            footerBrandBody: 'Handball in Mersch with a clearer digital presence: quick information, calmer layout and a structure built for GitHub Pages.',
            footerQuick: 'Quick access',
            footerContact: 'Contact',
            footerClub: 'Club',
            footerTrainerstaff: 'Coaching Staff',
            footerUsefulLinks: 'Useful Links',
            footerLegalHint: 'Legal notice and data protection will be added next as static service pages.',
            footerAdmin: 'Admin Login'
        },
        pt: {
            pageTitle: 'Mersch75 Handball',
            pageDescription: 'Mersch75 Handball: visão geral do clube, calendário, treino, notícias, galeria e participação.',
            brandHomeAria: 'Página inicial Mersch75',
            brandTagline: 'Mais fortes juntos',
            compassEyebrow: 'Zesumme Staark',
            compassTitle: 'ZESUMME STAARK – A nossa bússola',
            compassBody: '<h2>Quem somos</h2><p>O Handball Club Mersch75 faz parte do desporto luxemburguês desde 1975. Depois de uma história movimentada, reinventámo-nos em 2023: apostamos a 100% na nossa própria juventude e na nossa identidade local.</p><h2>O nosso ADN: S.T.A.A.R.K.</h2><p>O nosso lema é o nosso programa. Cada letra representa um valor que vivemos dentro e fora do campo:</p><ul><li><strong>Solidariedade</strong> – Um por todos, todos por um.</li><li><strong>Tolerância</strong> – A diversidade é a nossa força.</li><li><strong>Aceitação</strong> – Todos são bem-vindos.</li><li><strong>Diferente</strong> – A personalidade é incentivada.</li><li><strong>Respeito</strong> – Fair-play é regra.</li><li><strong>Comunicação</strong> – Falamos uns com os outros, não uns sobre os outros.</li></ul><h2>O nosso caminho: curto &amp; compacto</h2><p><strong>1975:</strong> Fundação por Michel Goergen.<br><strong>1978–1985:</strong> A primeira era dourada na divisão principal.<br><strong>2014:</strong> A grande subida após 30 anos de paciência e trabalho de construção.<br><strong>2015–2023:</strong> Os anos de aprendizagem. Tentativa de sucesso através de investimentos caros e jogadores externos. Resultado: forte a nível desportivo (Axa-League), mas difícil financeira e humanamente.<br><strong>Desde 2023:</strong> O recomeço. Reorientação estratégica, afastando-nos do semiprofissionalismo e aproximando-nos de um trabalho profissional com os jovens.</p><h2>Porquê Mersch75?</h2><p>Porque somos mais do que um clube desportivo. Somos uma escola de vida. Não investimos os nossos recursos em transferências caras, mas na formação das nossas crianças. Com o nosso coordenador jovem Max Blanc (Tel.: 661 406 836), garantimos treino de qualidade e acompanhamento pessoal.</p><p><strong>O nosso objetivo:</strong> Sucesso sustentável com jogadores da nossa própria formação.</p><p><strong>O teu lugar:</strong> É connosco – seja como jogador, adepto ou voluntário.</p><p>#ZesummeStaark #HBMersch75 #MatHäerzaSéil</p>',
            compassBackHome: 'Voltar à página inicial',
            newsRefEyebrow: 'FLH · Ciclo inferior',
            newsRefTitle: 'Jovens árbitros: inscrições abertas',
            newsRefBody: 'A formação para jovens árbitros do FLH Ciclo inferior está online. Uma boa oportunidade para a próxima geração assumir responsabilidade.',
            newsRefCta: 'Info & inscrição',
            trainingPageTitle: 'Treino | Mersch75 Handball',
            trainingPageDescription: 'Treino no Mersch75: horários, grupos, pavilhões e coordenação jovem num relance.',
            trainingHeroLogoAlt: 'Logótipo team training',
            trainingTrainerstaff: 'Equipa técnica',
            trainingTrialRequest: 'Pedir treino experimental',
            trainingScheduleOpen: 'Abrir plano de treino em ecrã inteiro',
            trainingScheduleClose: 'Fechar ecrã inteiro',
            trainingYouthCoord: 'COORDENAÇÃO JOVEM:',
            trainingYouthCoordBody: 'Max Blanc (LUXQF4) e Louis Van der Weken (LUXQF2Bis) são responsáveis pela secção jovem.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Tel.: Max Blanc 661 406 836',
            navMenu: 'Menu',
            navClose: 'Fechar menu',
            navHome: 'Início',
            navLiveCenter: 'Calendário',
            navTraining: 'Treino',
            navTrainerstaff: 'Equipa técnica',
            navNews: 'Notícias',
            navStatistics: 'Estatísticas',
            navStatisticsArchive: 'Estatísticas 25/26',
            navJoin: 'Join Us',
            navSponsors: 'Patrocinadores / Parceiros',
            navComite: 'Comité',
            navInside: 'Inside',
            navGallery: 'Galeria',
            navHistory: 'História',
            navLinks: 'Links úteis',
            usefulFanshopTitle: 'Fanshop Mersch75',
            usefulFanshopMeta: 'Hoodies, T-shirts & artigos de adepto',
            navHallenkarte: 'Mapa dos pavilhões',
            navContact: 'Contacto',
            posterAlt: 'Cartaz do jogo Mersch75',
            posterLandscapeTitle: 'Transferir em paisagem',
            posterPortraitTitle: 'Transferir em retrato',
            posterShareTitle: 'Partilhar cartaz',
            posterLandscapeLabel: 'Paisagem',
            posterPortraitLabel: 'Retrato',
            posterShareLabel: 'Partilhar',
            ballJumpAria: 'Ir para o calendário',
            ballJumpSchedule: 'Ir para o calendário',
            ballJumpNews: 'Ir para as notícias',
            eventsEyebrow: 'Eventos & formação',
            eventsTitle: 'Fins de semana, atividades e pontos de entrada para novos jogadores.',
            eventsBody: 'Esta área liga a comunicação dos eventos, a entrada na vida do clube e um apelo à ação claro.',
            eventsPillYouth: 'U4 & formação',
            eventsPillJoin: 'Join Us',
            eventsPillCommunity: 'Comunidade',
            eventsPrimary: 'Participar',
            eventsSecondary: 'Mais fortes juntos',
            eventsImageAlt: 'Eventos U4',
            newsKicker: 'Notícias',
            newsHeading: 'Novidades do Mersch75',
            newsFanshopEyebrow: 'Fanshop · Mersch75',
            newsFanshopTitle: 'Usa as nossas cores também fora do campo',
            newsFanshopBody: 'No Fanshop Mersch75, podes encomendar hoodies, T-shirts e outros artigos de adepto com o visual do clube. Mostra o teu apoio, fortalece a comunidade de Mersch e usa o azul e amarelo com orgulho.',
            newsFanshopPillClub: '💛💙 Mersch75',
            newsFanshopPillHoodies: 'Hoodies',
            newsFanshopPillShirts: 'T-shirts',
            newsFanshopCta: 'Ir para o Fanshop',
            newsU13Eyebrow: 'U13 Mista · Poule Espoir',
            newsGirlsDayEyebrow: 'Girls Handball Day',
            newsGirlsDayTitle: 'Treino experimental para raparigas',
            newsGirlsDayBody: 'No dia 20.06, o Mersch75 convida raparigas dos 7 aos 12 anos para um treino experimental de andebol. Das 10h00 às 12h00, na Hall Omnisports em Mersch, podes experimentar o desporto, divertir-te e conhecer a nossa comunidade azul e amarela.',
            newsGirlsDayPillDate: '📅 20.06',
            newsGirlsDayPillTime: '⏱ 10h00-12h00',
            newsGirlsDayPillAge: '7-12 anos',
            newsGirlsDayCta: 'Inscrever-se',
            newsU13Title: 'A nossa U13 continua invicta!',
            newsU13Body: 'Com uma grande exibição, a nossa U13 terminou a ronda de pavilhão 2025/2026 na Poule Espoir Mista com uma vitória clara por 39:26 frente ao HB Esch, segundo classificado. A equipa manteve-se concentrada, lutou em conjunto e continua invicta no topo. Uma excelente fase da época para os nossos jovens de Mersch! 💛💙 🏆',
            newsMenEyebrow: 'Homens · Época 25/26',
            newsMenTitle: 'Os nossos homens avançam como equipa',
            newsMenBody: 'Com empenho, ritmo e carácter, os nossos homens mostram mais uma vez o que representa o Mersch75: trabalhar juntos, assumir responsabilidade e entrar em cada jogo com máxima energia. A equipa continua a ser um pilar importante do clube e um forte exemplo para os jovens jogadores. 💛💙',
            newsWomenEyebrow: 'Mulheres · Época 25/26',
            newsWomenTitle: 'As nossas mulheres representam espírito de luta e união',
            newsWomenBody: 'As nossas mulheres vestem as cores do Mersch75 com coração, disciplina e muito espírito de equipa. Em cada treino e em cada jogo mostram a energia deste grupo. Uma equipa forte, corajosa e solidária em campo. 💛💙',
            newsU11Eyebrow: 'U11 Elite · Final da época',
            newsU11Title: 'U11 Elite termina a época em força',
            newsU11Body: 'A nossa U11 Elite voltou a mostrar no fim da época todo o potencial desta equipa. No duelo pelo 5.º lugar contra o HC Standard, o Mersch75 venceu os dois jogos: 23:16 em casa e 22:18 fora. Uma bela recompensa por uma época empenhada e um final forte para os nossos jovens de Mersch. 💛💙',
            newsStatsEyebrow: 'Estatísticas da época 25/26',
            newsStatsTitle: 'ESTATÍSTICAS DAS NOSSAS EQUIPAS NUM SÓ LUGAR',
            newsStatsBody: 'As estatísticas da época 2025/2026 estão online: classificações, resultados e melhores marcadores para homens, mulheres, U15, U13 e U11 – claras e atualizadas.',
            newsStatsPillMen: 'Homens',
            newsStatsPillWomen: 'Mulheres',
            newsStatsPillLive: 'Live',
            newsStatsCta: 'Ver estatísticas',
            newsStatsImageAlt: 'Estatísticas da época',
            newsSiteEyebrow: 'Novo visual',
            newsSiteTitle: 'O site brilha sob uma nova luz.',
            newsSiteBody: 'Novo design, estrutura mais clara e navegação rápida: o novo site Mersch75 reúne calendário, estatísticas e informações de forma clara.',
            newsSitePillDesign: 'Novo design',
            newsSitePillFast: 'Mais rápido',
            newsSitePillClear: 'Mais claro',
            newsSiteCta: 'Descobrir',
            newsSiteImageAlt: 'Mersch75',
            infoTitle: 'Informações nacionais e internacionais',
            infoAxaAria: 'Ligações AXA League',
            infoWomen: 'AXA League Feminina',
            infoMen: 'AXA League Masculina',
            sponsorsTitle: 'Os nossos patrocinadores',
            sponsorsAlt: 'Patrocinadores Mersch75',
            footerBrandBody: 'Andebol em Mersch com uma presença digital mais clara: informação rápida, layout mais calmo e uma estrutura pensada para GitHub Pages.',
            footerQuick: 'Acesso rápido',
            footerContact: 'Contacto',
            footerClub: 'Clube',
            footerTrainerstaff: 'Equipa técnica',
            footerUsefulLinks: 'Links úteis',
            footerLegalHint: 'Aviso legal e proteção de dados serão adicionados em seguida como páginas estáticas de serviço.',
            footerAdmin: 'Admin Login'
        }
    };

    const resolveLanguage = (lang) => {
        return supportedLanguages.includes(lang) ? lang : fallbackLanguage;
    };

    const getTranslation = (lang, key) => {
        const resolvedLanguage = resolveLanguage(lang);
        return (translations[resolvedLanguage] && translations[resolvedLanguage][key])
            || (translations[fallbackLanguage] && translations[fallbackLanguage][key])
            || '';
    };

    const applyLanguage = (lang) => {
        const resolvedLanguage = resolveLanguage(lang);

        document.documentElement.lang = resolvedLanguage === 'lb' ? 'lb-LU' : resolvedLanguage;
        document.body.dataset.siteLanguage = resolvedLanguage;

        textTargets.forEach((target) => {
            const key = target.dataset.i18n;
            const value = getTranslation(resolvedLanguage, key);

            if (value) {
                target.textContent = value;
            }
        });

        htmlTargets.forEach((target) => {
            const key = target.dataset.i18nHtml;
            const value = getTranslation(resolvedLanguage, key);

            if (value) {
                target.innerHTML = value;
            }
        });

        attributeTargets.forEach((target) => {
            const bindings = (target.dataset.i18nAttr || '').split(';');

            bindings.forEach((binding) => {
                const parts = binding.split(':');
                const attributeName = parts[0] ? parts[0].trim() : '';
                const key = parts[1] ? parts[1].trim() : '';
                const value = getTranslation(resolvedLanguage, key);

                if (attributeName && key && value) {
                    target.setAttribute(attributeName, value);
                }
            });
        });

        languageButtons.forEach((button) => {
            const isActive = button.dataset.siteLangButton === resolvedLanguage;
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', String(isActive));
        });

        window.localStorage.setItem(storageKey, resolvedLanguage);
        document.dispatchEvent(new CustomEvent('mersch75:languagechange', {
            detail: { language: resolvedLanguage, t: (key) => getTranslation(resolvedLanguage, key) }
        }));
    };

    const initialLanguage = resolveLanguage(window.localStorage.getItem(storageKey) || fallbackLanguage);

    languageButtons.forEach((button) => {
        button.addEventListener('click', () => {
            applyLanguage(button.dataset.siteLangButton);
        });
    });

    window.Mersch75I18n = {
        getLanguage() {
            return resolveLanguage(window.localStorage.getItem(storageKey) || fallbackLanguage);
        },
        setLanguage: applyLanguage,
        t(key) {
            return getTranslation(this.getLanguage(), key);
        }
    };

    applyLanguage(initialLanguage);
}

function initializeLanguageSelectionHint() {
    const storageKey = 'mersch75-language-hint-dismissed';
    const switcher = document.querySelector('.site-language-switcher, .legal-lang-switcher');

    if (!switcher) {
        return;
    }

    try {
        if (window.localStorage.getItem(storageKey) === 'true') {
            return;
        }
    } catch (error) {
        /* ignore storage access issues */
    }

    const hintTexts = {
        lb: 'Wielt hei Är Sprooch.',
        fr: 'Choisissez votre langue ici.',
        de: 'Wählen Sie hier Ihre Sprache.',
        en: 'Choose your language here.',
        pt: 'Escolha aqui o seu idioma.'
    };

    const dismissTexts = {
        lb: 'Verstanen',
        fr: 'Compris',
        de: 'Verstanden',
        en: 'Got it',
        pt: 'Percebi'
    };

    const resolveLanguage = () => {
        if (window.Mersch75I18n && typeof window.Mersch75I18n.getLanguage === 'function') {
            return window.Mersch75I18n.getLanguage();
        }

        const activeButton = switcher.querySelector('.is-active');
        if (activeButton && activeButton.dataset.siteLangButton) {
            return activeButton.dataset.siteLangButton;
        }

        if (activeButton && activeButton.dataset.legalLangButton) {
            return activeButton.dataset.legalLangButton;
        }

        if (activeButton && activeButton.dataset.privacyLangButton) {
            return activeButton.dataset.privacyLangButton;
        }

        return 'lb';
    };

    const hint = document.createElement('div');
    hint.className = 'language-selection-hint';
    hint.setAttribute('role', 'status');
    hint.innerHTML = [
        '<span class="language-selection-hint-copy"></span>',
        '<button type="button" class="language-selection-hint-close"></button>'
    ].join('');

    const copy = hint.querySelector('.language-selection-hint-copy');
    const close = hint.querySelector('.language-selection-hint-close');

    const updateHintText = () => {
        const language = resolveLanguage();
        copy.textContent = hintTexts[language] || hintTexts.lb;
        close.textContent = dismissTexts[language] || dismissTexts.lb;
    };

    const dismiss = () => {
        hint.remove();

        try {
            window.localStorage.setItem(storageKey, 'true');
        } catch (error) {
            /* ignore storage access issues */
        }
    };

    updateHintText();
    close.addEventListener('click', dismiss);

    switcher.insertAdjacentElement('afterend', hint);

    switcher.querySelectorAll('button').forEach((button) => {
        button.addEventListener('click', () => {
            updateHintText();
            dismiss();
        }, { once: true });
    });

    document.addEventListener('mersch75:languagechange', updateHintText);
}

function initializeSiteMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');

    if (!navToggle || !siteNav) {
        return;
    }

    const getI18nText = (key, fallback) => {
        if (window.Mersch75I18n && typeof window.Mersch75I18n.t === 'function') {
            return window.Mersch75I18n.t(key) || fallback;
        }

        return fallback;
    };

    const labelDefault = getI18nText('navMenu', 'Menü');
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navItems = [
        { href: 'index.html', labelKey: 'navHome', fallback: 'Startseite', primary: true },
        { href: 'live-center.html', labelKey: 'navLiveCenter', fallback: 'Spielplan', primary: true },
        { href: 'training.html', labelKey: 'navTraining', fallback: 'Training', primary: true },
        { href: 'trainerstaff.html', labelKey: 'navTrainerstaff', fallback: 'Trainerstaff', primary: true },
        { href: 'news.html', labelKey: 'navNews', fallback: 'News', primary: true },
        { href: 'join.html', labelKey: 'navJoin', fallback: 'Join Us', primary: true },
        { href: 'nextgen.html', labelKey: 'navNextgen', fallback: 'NEXTGEN', primary: true },
        { href: 'inside.html', labelKey: 'navInside', fallback: 'Inside', primary: true },
        { href: 'statistics-25-26.html', labelKey: 'navStatistics', fallback: 'Statistik', primary: true },
        { href: 'sponsors.html', labelKey: 'navSponsors', fallback: 'Sponsoren / Partner', primary: true },
        { href: 'gallery.html', labelKey: 'navGallery', fallback: 'Galerie', primary: false },
        { href: 'memories.html', labelKey: 'navMemories', fallback: 'Memories', primary: false },
        { href: 'statistics-25-26.html', labelKey: 'navStatisticsArchive', fallback: 'Statistik 25/26', primary: false },
        { href: 'inside.html#history', labelKey: 'navHistory', fallback: 'Geschicht', primary: false },
        { href: 'links.html', labelKey: 'navLinks', fallback: 'Useful Links', primary: false },
        { href: 'hallenkarte.html', labelKey: 'navHallenkarte', fallback: 'Hallenkarte', primary: false },
        { href: 'contact.html', labelKey: 'navContact', fallback: 'Contact', primary: false }
    ];

    const primaryGroup = document.createElement('div');
    primaryGroup.className = 'site-menu-primary';

    const secondaryGroup = document.createElement('div');
    secondaryGroup.className = 'site-menu-secondary';

    const trainingPair = document.createElement('div');
    trainingPair.className = 'site-menu-pair site-menu-pair-training';

    navItems.forEach(({ href, labelKey, fallback, primary }) => {
        const link = document.createElement('a');
        let targetGroup = primary ? primaryGroup : secondaryGroup;

        link.href = href;
        link.textContent = getI18nText(labelKey, fallback);
        link.dataset.labelKey = labelKey;
        link.dataset.fallback = fallback;

        if (currentPath === href) {
            link.classList.add('is-active');
        }

        if (href === 'training.html' || href === 'trainerstaff.html') {
            targetGroup = trainingPair;
        }

        targetGroup.append(link);

        if (href === 'trainerstaff.html') {
            primaryGroup.append(trainingPair);
        }
    });

    const footer = document.createElement('div');
    footer.className = 'site-menu-footer';

    // Sprachumschalter (nur auf Smartphones sichtbar) als Klon in das Burger-Menü übernehmen.
    const headerSwitcher = document.querySelector('.site-language-switcher');
    let menuLangWrap = null;
    if (headerSwitcher) {
        menuLangWrap = document.createElement('div');
        menuLangWrap.className = 'site-menu-language';

        const menuSwitcher = headerSwitcher.cloneNode(true);
        menuSwitcher.classList.add('site-menu-language-switcher');
        menuSwitcher.removeAttribute('id');

        menuSwitcher.querySelectorAll('[data-site-lang-button]').forEach((btn) => {
            btn.addEventListener('click', () => {
                const lang = btn.dataset.siteLangButton;
                if (window.Mersch75I18n && typeof window.Mersch75I18n.setLanguage === 'function') {
                    window.Mersch75I18n.setLanguage(lang);
                }
            });
        });

        document.addEventListener('mersch75:languagechange', (event) => {
            const lang = event && event.detail ? event.detail.language : null;
            if (!lang) return;
            menuSwitcher.querySelectorAll('[data-site-lang-button]').forEach((btn) => {
                const isActive = btn.dataset.siteLangButton === lang;
                btn.classList.toggle('is-active', isActive);
                btn.setAttribute('aria-pressed', String(isActive));
            });
        });

        menuLangWrap.append(menuSwitcher);
    }

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'site-menu-close';
    closeButton.setAttribute('aria-label', getI18nText('navClose', 'Menü schließen'));
    closeButton.textContent = 'X';

    const shell = document.createElement('div');
    shell.className = 'site-menu-shell';
    shell.append(closeButton);
    if (menuLangWrap) {
        shell.append(menuLangWrap);
    }
    shell.append(primaryGroup, secondaryGroup, footer);

    siteNav.innerHTML = '';
    siteNav.append(shell);
    document.body.append(siteNav);

    const backdrop = document.createElement('button');
    backdrop.type = 'button';
    backdrop.className = 'site-menu-backdrop';
    backdrop.setAttribute('aria-label', getI18nText('navClose', 'Menü schließen'));
    document.body.append(backdrop);

    const closeMenu = () => {
        document.body.classList.remove('menu-open');
        siteNav.classList.remove('is-open');
        backdrop.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
        navToggle.textContent = labelDefault;
    };

    const openMenu = () => {
        document.body.classList.add('menu-open');
        siteNav.classList.add('is-open');
        backdrop.classList.add('is-open');
        navToggle.setAttribute('aria-expanded', 'true');
    };

    navToggle.textContent = labelDefault;
    navToggle.addEventListener('click', () => {
        if (siteNav.classList.contains('is-open')) {
            closeMenu();
            return;
        }

        openMenu();
    });

    backdrop.addEventListener('click', closeMenu);
    closeButton.addEventListener('click', closeMenu);
    siteNav.addEventListener('click', (event) => {
        if (event.target instanceof HTMLAnchorElement) {
            closeMenu();
        }
    });

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape' && siteNav.classList.contains('is-open')) {
            closeMenu();
        }
    });

    document.addEventListener('mersch75:languagechange', (event) => {
        const language = event && event.detail ? event.detail.language : null;
        const translator = event && event.detail ? event.detail.t : null;

        navToggle.textContent = (translator && translator('navMenu')) || getI18nText('navMenu', 'Menü');
        closeButton.setAttribute('aria-label', (translator && translator('navClose')) || getI18nText('navClose', 'Menü schließen'));
        backdrop.setAttribute('aria-label', (translator && translator('navClose')) || getI18nText('navClose', 'Menü schließen'));

        siteNav.querySelectorAll('a[data-label-key]').forEach((link) => {
            const labelKey = link.dataset.labelKey;
            const fallback = link.dataset.fallback || '';
            const text = translator ? translator(labelKey) : getI18nText(labelKey, fallback);
            if (text) {
                link.textContent = text;
            }
        });

        if (language) {
            document.documentElement.lang = language === 'lb' ? 'lb' : language;
        }
    });
}

function initializeTrainingSchedule() {
    const scheduleContainer = document.querySelector('#schedule-container');
    const fullscreenButton = document.querySelector('#btn-schedule-fs');
    const hotspotLayer = document.querySelector('.training-schedule-hotspots');
    const tooltip = document.querySelector('#schedule-tooltip');

    if (!scheduleContainer || !fullscreenButton) {
        return;
    }

    const getI18nText = (key, fallback) => {
        if (window.Mersch75I18n && typeof window.Mersch75I18n.t === 'function') {
            return window.Mersch75I18n.t(key) || fallback;
        }

        return fallback;
    };

    const scheduleTranslations = {
        lb: {
            showSuffix: 'weisen',
            trainerPrefix: 'TRAINER',
            days: { mon: 'Méindes', tue: 'Dënschdes', wed: 'Mëttwochs', thu: 'Donneschdes', fri: 'Freides', sat: 'Samschdes' },
            groups: {
                u4: { label: 'Kidssports U4', title: 'Kidssports U4' },
                u7: { label: 'U7', title: 'U7' },
                u9: { label: 'U9', title: 'U9' },
                u11: { label: 'U11', title: 'U11 (débutants confirmés)' },
                u13f: { label: 'U13F', title: 'U13 Meedercher' },
                u13g: { label: 'U13G', title: 'U13 Jongen' },
                u15: { label: 'U15', title: 'U15' },
                filles: { label: 'Filles', title: 'Meedercher (Ufänger)' },
                femmes: { label: 'Fraen', title: 'Fraen' },
                hommes: { label: 'Männer', title: 'Männer' },
                loisir: { label: 'Loisir', title: 'Loisir' }
            }
        },
        fr: {
            showSuffix: 'afficher',
            trainerPrefix: 'ENTRAÎNEURS',
            days: { mon: 'Lundi', tue: 'Mardi', wed: 'Mercredi', thu: 'Jeudi', fri: 'Vendredi', sat: 'Samedi' },
            groups: {
                u4: { label: 'Kidssports U4', title: 'Kidssports U4' },
                u7: { label: 'U7', title: 'U7' },
                u9: { label: 'U9', title: 'U9' },
                u11: { label: 'U11', title: 'U11 (débutants confirmés)' },
                u13f: { label: 'U13F', title: 'U13 Filles' },
                u13g: { label: 'U13G', title: 'U13 Garçons' },
                u15: { label: 'U15', title: 'U15' },
                filles: { label: 'Filles', title: 'Filles (débutantes)' },
                femmes: { label: 'Dames', title: 'Dames' },
                hommes: { label: 'Hommes', title: 'Hommes' },
                loisir: { label: 'Loisir', title: 'Loisir' }
            }
        },
        de: {
            showSuffix: 'anzeigen',
            trainerPrefix: 'TRAINER',
            days: { mon: 'Montag', tue: 'Dienstag', wed: 'Mittwoch', thu: 'Donnerstag', fri: 'Freitag', sat: 'Samstag' },
            groups: {
                u4: { label: 'Kidssports U4', title: 'Kidssports U4' },
                u7: { label: 'U7', title: 'U7' },
                u9: { label: 'U9', title: 'U9' },
                u11: { label: 'U11', title: 'U11 (débutants confirmés)' },
                u13f: { label: 'U13F', title: 'U13 Mädchen' },
                u13g: { label: 'U13G', title: 'U13 Jungen' },
                u15: { label: 'U15', title: 'U15' },
                filles: { label: 'Mädchen', title: 'Mädchen (Anfänger)' },
                femmes: { label: 'Frauen', title: 'Frauen' },
                hommes: { label: 'Männer', title: 'Männer' },
                loisir: { label: 'Loisir', title: 'Freizeit / Loisir' }
            }
        },
        en: {
            showSuffix: 'show',
            trainerPrefix: 'COACHES',
            days: { mon: 'Monday', tue: 'Tuesday', wed: 'Wednesday', thu: 'Thursday', fri: 'Friday', sat: 'Saturday' },
            groups: {
                u4: { label: 'Kidssports U4', title: 'Kidssports U4' },
                u7: { label: 'U7', title: 'U7' },
                u9: { label: 'U9', title: 'U9' },
                u11: { label: 'U11', title: 'U11 (débutants confirmés)' },
                u13f: { label: 'U13F', title: 'U13 Girls' },
                u13g: { label: 'U13G', title: 'U13 Boys' },
                u15: { label: 'U15', title: 'U15' },
                filles: { label: 'Girls', title: 'Girls (beginners)' },
                femmes: { label: 'Women', title: 'Women' },
                hommes: { label: 'Men', title: 'Men' },
                loisir: { label: 'Loisir', title: 'Recreational' }
            }
        },
        pt: {
            showSuffix: 'mostrar',
            trainerPrefix: 'TREINADORES',
            days: { mon: 'Segunda-feira', tue: 'Terça-feira', wed: 'Quarta-feira', thu: 'Quinta-feira', fri: 'Sexta-feira', sat: 'Sábado' },
            groups: {
                u4: { label: 'Kidssports U4', title: 'Kidssports U4' },
                u7: { label: 'U7', title: 'U7' },
                u9: { label: 'U9', title: 'U9' },
                u11: { label: 'U11', title: 'U11 (débutants confirmés)' },
                u13f: { label: 'U13F', title: 'U13 Raparigas' },
                u13g: { label: 'U13G', title: 'U13 Rapazes' },
                u15: { label: 'U15', title: 'U15' },
                filles: { label: 'Raparigas', title: 'Raparigas (iniciantes)' },
                femmes: { label: 'Seniores femininas', title: 'Seniores femininas' },
                hommes: { label: 'Seniores masculinos', title: 'Seniores masculinos' },
                loisir: { label: 'Loisir', title: 'Lazer' }
            }
        }
    };

    // Halen
    const LOC_OMNI = 'Hall Omnisports, 21, rue des Prés, Mersch';
    const LOC_KROU = 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch';
    const LOC_GARE = 'Sporthal Lëntgen (Gare), 50, rue de la Gare, Lëntgen';
    const LOC_ECOLE = "Schoulsporthal Lintgen (École), 4, rue de l'Ecole, Lintgen";

    // Positiounen op der Tabell 2026-2027 (Prozent, aus dem Gitter gemooss).
    // Kolonnen: A Lun/Omni 7.34 · B Lun/Gare 18.86 · C Mar/Krounebierg 30.38 · D Mer/Omni 41.90
    //           E Jeu/Krounebierg 53.41 · F Ven/Omni 64.93 · G Ven/Krounebierg 76.45 · H Sam/École 87.97
    // Zäit-Reihen: 09:00 = 23.92 %, all 30 Min = 3.77 %.
    const hotspotGroupBase = [
        {
            group: 'u4',
            trainers: 'Grégory Redavid, Marc Jungels, Max Blanc (LUXQF4)',
            slots: [
                { dayKey: 'sat', time: '10:00 - 11:00', location: LOC_ECOLE }
            ],
            areas: [
                { left: 87.97, top: 31.46, width: 11.52, height: 7.54 }
            ]
        },
        {
            group: 'u7',
            trainers: 'Max Blanc (LUXQF4), Anne Holm (LUXQF3)',
            slots: [
                { dayKey: 'tue', time: '17:30 - 18:30', location: LOC_KROU },
                { dayKey: 'fri', time: '16:30 - 17:30', location: LOC_KROU }
            ],
            areas: [
                { left: 30.38, top: 57.85, width: 11.52, height: 7.54 },
                { left: 76.45, top: 50.31, width: 11.52, height: 7.54 }
            ]
        },
        {
            group: 'u9',
            trainers: 'Max Blanc (LUXQF4), Louis Van der Weken (LUXQF2Bis)',
            slots: [
                { dayKey: 'mon', time: '17:30 - 19:00', location: LOC_GARE },
                { dayKey: 'thu', time: '17:30 - 19:00', location: LOC_KROU }
            ],
            areas: [
                { left: 18.86, top: 57.85, width: 11.52, height: 11.31 },
                { left: 53.41, top: 57.85, width: 11.52, height: 11.31 }
            ]
        },
        {
            group: 'u11',
            trainers: 'Max Blanc (LUXQF4), Elie Schuster',
            slots: [
                { dayKey: 'wed', time: '17:00 - 18:30', location: LOC_OMNI },
                { dayKey: 'fri', time: '17:30 - 19:00', location: LOC_KROU }
            ],
            areas: [
                { left: 41.90, top: 50.31, width: 11.52, height: 15.08 },
                { left: 76.45, top: 57.85, width: 11.52, height: 7.54 }
            ]
        },
        {
            group: 'u13f',
            trainers: 'Max Blanc (LUXQF4), Mathis Derneden',
            slots: [
                { dayKey: 'mon', time: '17:30 - 19:00', location: LOC_OMNI },
                { dayKey: 'fri', time: '17:30 - 19:00', location: LOC_OMNI }
            ],
            areas: [
                { left: 7.34, top: 54.08, width: 11.52, height: 11.31 },
                { left: 64.93, top: 57.85, width: 11.52, height: 7.54 }
            ]
        },
        {
            group: 'u13g',
            trainers: 'Max Blanc (LUXQF4), Mathis Derneden',
            slots: [
                { dayKey: 'mon', time: '19:00 - 20:30', location: LOC_OMNI },
                { dayKey: 'wed', time: '18:30 - 20:00', location: LOC_OMNI }
            ],
            areas: [
                { left: 7.34, top: 69.16, width: 11.52, height: 7.54 },
                { left: 41.90, top: 65.39, width: 11.52, height: 11.31 }
            ]
        },
        {
            group: 'u15',
            trainers: 'Max Blanc (LUXQF4), Mathis Derneden',
            slots: [
                { dayKey: 'wed', time: '20:00 - 21:30', location: LOC_OMNI },
                { dayKey: 'fri', time: '19:00 - 20:30', location: LOC_KROU }
            ],
            areas: [
                { left: 41.90, top: 76.70, width: 5.76, height: 7.54 },
                { left: 76.45, top: 69.16, width: 11.52, height: 11.31 }
            ]
        },
        {
            group: 'filles',
            trainers: 'Anne Bisenius Holm (LUXQF3), Katarzyna Pietrasik',
            slots: [
                { dayKey: 'fri', time: '16:30 - 17:30', location: LOC_OMNI }
            ],
            areas: [
                { left: 64.93, top: 50.31, width: 11.52, height: 3.77 }
            ]
        },
        {
            group: 'femmes',
            trainers: 'Katarzyna Pietrasik',
            slots: [
                { dayKey: 'mon', time: '19:00 - 20:30', location: LOC_GARE },
                { dayKey: 'fri', time: '19:00 - 20:30', location: LOC_OMNI }
            ],
            areas: [
                { left: 18.86, top: 69.16, width: 11.52, height: 11.31 },
                { left: 64.93, top: 69.16, width: 11.52, height: 11.31 }
            ]
        },
        {
            group: 'hommes',
            trainers: '',
            slots: [
                { dayKey: 'mon', time: '20:00 - 21:30', location: LOC_OMNI },
                { dayKey: 'wed', time: '20:00 - 21:30', location: LOC_OMNI },
                { dayKey: 'fri', time: '20:00 - 21:30', location: LOC_KROU }
            ],
            areas: [
                { left: 7.34, top: 76.70, width: 11.52, height: 7.54 },
                { left: 47.66, top: 76.70, width: 5.76, height: 7.54 },
                { left: 76.45, top: 76.70, width: 11.52, height: 7.54 }
            ]
        },
        {
            group: 'loisir',
            trainers: 'Mersch75',
            slots: [
                { dayKey: 'mon', time: '20:30 - 22:00', location: LOC_GARE }
            ],
            areas: [
                { left: 18.86, top: 80.47, width: 11.52, height: 11.31 }
            ]
        }
    ];

    let currentOpenGroup = null;

    const getScheduleLanguage = () => {
        if (window.Mersch75I18n && typeof window.Mersch75I18n.getLanguage === 'function') {
            return window.Mersch75I18n.getLanguage();
        }

        return 'lb';
    };

    const getLocalizedGroups = () => {
        const lang = scheduleTranslations[getScheduleLanguage()] ? getScheduleLanguage() : 'lb';
        const translation = scheduleTranslations[lang];

        return hotspotGroupBase.map((group) => {
            const translatedGroup = translation.groups[group.group] || scheduleTranslations.lb.groups[group.group];

            return {
                group: group.group,
                label: translatedGroup.label,
                title: translatedGroup.title,
                trainers: group.trainers ? `${translation.trainerPrefix} ${group.trainers}` : '',
                slots: group.slots.map((slot) => ({
                    day: translation.days[slot.dayKey] || scheduleTranslations.lb.days[slot.dayKey],
                    time: slot.time,
                    location: slot.location
                })),
                areas: group.areas
            };
        });
    };

    let hotspotGroups = getLocalizedGroups();

    const hotspotsByGroup = new Map();

    const resetScheduleHover = () => {
        document.querySelectorAll('.training-schedule-hotspot.is-active').forEach((hotspot) => {
            hotspot.classList.remove('is-active');
        });

        if (tooltip) {
            tooltip.classList.remove('is-visible');
            tooltip.innerHTML = '';
        }
    };

    const showGroupInfo = (group) => {
        const groupInfo = hotspotGroups.find((entry) => entry.group === group);

        if (!groupInfo) {
            return;
        }

        currentOpenGroup = group;

        resetScheduleHover();

        (hotspotsByGroup.get(group) || []).forEach((hotspot) => {
            hotspot.classList.add('is-active');
        });

        if (!tooltip) {
            return;
        }

        const slots = groupInfo.slots.map(({ day, time, location }) => {
            return [
                '<li>',
                '<div class="training-schedule-tooltip-row">',
                `<strong>${day}</strong>`,
                `<span>${time}</span>`,
                '</div>',
                `<small>${location}</small>`,
                '</li>'
            ].join('');
        }).join('');

        tooltip.innerHTML = [
            `<h3>${groupInfo.title}</h3>`,
            groupInfo.trainers ? `<p>${groupInfo.trainers}</p>` : '',
            `<ul>${slots}</ul>`
        ].join('');
        tooltip.classList.add('is-visible');
    };

    const renderHotspots = () => {
        if (!hotspotLayer || !tooltip || !hotspotGroups.length) {
            return;
        }

        hotspotLayer.innerHTML = '';
        hotspotsByGroup.clear();

        hotspotGroups.forEach(({ group, label, areas }) => {
            const groupHotspots = [];

            areas.forEach((area, index) => {
                const hotspot = document.createElement('button');

                hotspot.type = 'button';
                hotspot.className = 'training-schedule-hotspot';
                hotspot.setAttribute('aria-label', `${label} ${scheduleTranslations[getScheduleLanguage()]?.showSuffix || scheduleTranslations.lb.showSuffix}`);
                hotspot.dataset.group = group;
                hotspot.style.left = `${area.left}%`;
                hotspot.style.top = `${area.top}%`;
                hotspot.style.width = `${area.width}%`;
                hotspot.style.height = `${area.height}%`;

                hotspot.addEventListener('mouseenter', () => showGroupInfo(group));
                hotspot.addEventListener('focus', () => showGroupInfo(group));
                hotspot.addEventListener('click', () => showGroupInfo(group));
                hotspot.addEventListener('mouseleave', () => {
                    if (index === areas.length - 1) {
                        resetScheduleHover();
                    }
                });
                hotspot.addEventListener('blur', () => {
                    if (!scheduleContainer.contains(document.activeElement)) {
                        resetScheduleHover();
                    }
                });

                hotspotLayer.append(hotspot);
                groupHotspots.push(hotspot);
            });

            hotspotsByGroup.set(group, groupHotspots);
        });

        scheduleContainer.addEventListener('mouseleave', resetScheduleHover);
    };

    renderHotspots();

    const getFullscreenElement = () => (
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.msFullscreenElement
    );

    const syncButton = () => {
        const isActive = Boolean(getFullscreenElement());
        fullscreenButton.textContent = isActive
            ? getI18nText('trainingScheduleClose', 'Vollbild schließen')
            : getI18nText('trainingScheduleOpen', 'Trainingsplan im Vollbild öffnen');
        fullscreenButton.classList.toggle('is-active', isActive);
    };

    const requestFullscreen = () => {
        if (scheduleContainer.requestFullscreen) {
            return scheduleContainer.requestFullscreen();
        }

        if (scheduleContainer.webkitRequestFullscreen) {
            scheduleContainer.webkitRequestFullscreen();
            return Promise.resolve();
        }

        if (scheduleContainer.msRequestFullscreen) {
            scheduleContainer.msRequestFullscreen();
            return Promise.resolve();
        }

        return Promise.reject(new Error('fullscreen-not-supported'));
    };

    const exitFullscreen = () => {
        if (document.exitFullscreen) {
            return document.exitFullscreen();
        }

        if (document.webkitExitFullscreen) {
            document.webkitExitFullscreen();
            return Promise.resolve();
        }

        if (document.msExitFullscreen) {
            document.msExitFullscreen();
            return Promise.resolve();
        }

        return Promise.reject(new Error('fullscreen-not-supported'));
    };

    fullscreenButton.addEventListener('click', async () => {
        try {
            if (getFullscreenElement()) {
                await exitFullscreen();
            } else {
                await requestFullscreen();
            }
        } catch {
            const scheduleImage = scheduleContainer.querySelector('img');

            if (scheduleImage) {
                window.open(scheduleImage.src, '_blank', 'noopener');
            }
        }
    });

    document.addEventListener('fullscreenchange', syncButton);
    document.addEventListener('webkitfullscreenchange', syncButton);
    document.addEventListener('msfullscreenchange', syncButton);
    document.addEventListener('mersch75:languagechange', () => {
        hotspotGroups = getLocalizedGroups();
        renderHotspots();
        syncButton();

        if (currentOpenGroup) {
            showGroupInfo(currentOpenGroup);
        }
    });

    syncButton();
}

function initializeSharedFooters() {
    const socialLinks = [
        {
            href: 'https://www.facebook.com/mersch75',
            label: 'Facebook'
        },
        {
            href: 'https://www.youtube.com/Netjogger58',
            label: 'YouTube'
        },
        {
            href: 'https://www.instagram.com/hbmersch75/',
            label: 'Instagram'
        }
    ];
    const pageLinks = [
        { href: 'matchday.html', label: 'Matchday' },
        { href: 'matchcenter.html', label: 'Matchcenter' },
        { href: 'training.html', label: 'Training' },
        { href: 'trainerstaff.html', label: 'Trainerstaff' },
        { href: 'news.html', label: 'News' },
        { href: 'statistics-25-26.html', label: 'Statistik 25/26' },
        { href: 'gallery.html', label: 'Galerie' },
        { href: 'community.html', label: 'Community' },
        { href: 'links.html', label: 'Useful Links' },
        { href: 'hallenkarte.html', label: 'Hallenkarte' },
        { href: 'comite.html', label: 'Comité' },
        { href: 'history.html', label: 'Geschicht' },
        { href: 'contact.html', label: 'Contact' }
    ];
    const landingQuickLinks = [
        { href: 'matchday.html', label: 'Matchday' },
        { href: 'matchcenter.html', label: 'Matchcenter' },
        { href: 'training.html', label: 'Training' },
        { href: 'statistics-25-26.html', label: 'Statistik' },
        { href: 'sponsors.html', label: 'Sponsoren / Partner' },
        { href: 'join.html', label: 'Join Us' },
        { href: 'contact.html', label: 'Contact' }
    ];
    const serviceLinks = [
        { href: 'join.html', label: 'Join Us' },
        { href: 'impressum.html', label: 'Impressum' },
        { href: 'terms.html', label: 'Terms & Conditions' },
        { href: 'dataprotection.html', label: 'Data Protection' }
    ];

    const renderLinkGroup = (links) => links.map(({ href, label }) => {
        return `<a href="${href}">${label}</a>`;
    }).join('');

    const renderExternalLinkGroup = (links, className) => links.map(({ href, label }) => {
        return `<a class="${className}" href="${href}" target="_blank" rel="noreferrer">${label}</a>`;
    }).join('');

    const pageFooter = document.querySelector('.site-page-footer');

    if (pageFooter) {
        const yearEl = pageFooter.querySelector('#current-year');
        if (yearEl) {
            yearEl.textContent = new Date().getFullYear();
        }
    }

    const landingFooter = document.querySelector('.landing-footer');

    if (landingFooter) {
        if (landingFooter.querySelector('[data-i18n], [data-i18n-attr]')) {
            const yearEls = landingFooter.querySelectorAll('#current-year');

            yearEls.forEach((yearEl) => {
                yearEl.textContent = new Date().getFullYear();
            });

            return;
        }

        const brandCopy = landingFooter.querySelector('.footer-brand p');
        const columns = landingFooter.querySelector('.footer-columns');
        const bottom = landingFooter.querySelector('.footer-bottom');

        if (brandCopy) {
            brandCopy.textContent = 'Handball zu Miersch mat enger kloerer digitaler Struktur: séier Informatiounen, propper Service-Weeër an en Optrëtt, deen op allen Säiten zesummegehéiert.';
        }

        if (columns) {
            columns.innerHTML = [
                '<div class="footer-column">',
                '<h3>Schnellzugriff</h3>',
                `<div class="footer-link-list">${renderLinkGroup(landingQuickLinks)}</div>`,
                '</div>',
                '<div class="footer-column">',
                '<h3>Kontakt</h3>',
                '<p>21 rue des Pres<br>L-7561 Mersch</p>',
                '<p><a href="mailto:info@mersch75.lu">info@mersch75.lu</a></p>',
                '<p>Tel.: 288 00 399</p>',
                '<p>RCS: F2345<br>BCEELULL: LU730019220008607000</p>',
                '</div>',
                '<div class="footer-column">',
                '<h3>Service</h3>',
                `<div class="footer-link-list">${renderLinkGroup(serviceLinks)}</div>`,
                '</div>'
            ].join('');
        }

        if (bottom) {
            bottom.innerHTML = [
                '<p>RCS: F2345 · BCEELULL: LU730019220008607000</p>',
                `<div class="footer-social">${renderExternalLinkGroup(socialLinks, 'footer-social-link')}</div>`,
                '<p>© <span id="current-year"></span> by Mersch75, Handball Club</p>'
            ].join('');
        }
    }
}

function initializeJoinUsForm() {
    const form = document.querySelector('#registrationForm');

    if (!form) {
        return;
    }

    const conditionsUrl = 'https://www.mersch75.lu/x2-terms-and-conditions/';
    const dataProtectionUrl = 'https://www.mersch75.lu/x3-dataprotection/';
    const registrationEndpoint = 'https://api.web3forms.com/submit';
    const registrationAccessKey = '15e3cc53-6864-47dd-bfaf-332cb4ca45e5';
    const registrationMailbox = 'hbmersch75secretariat@gmail.com';

    const elements = {
        langButtons: Array.from(document.querySelectorAll('.join-lang-button')),
        langTexts: Array.from(document.querySelectorAll('.join-lang-text')),
        nomLabel: document.getElementById('lbl-nom'),
        prenomLabel: document.getElementById('lbl-prenom'),
        dobLabel: document.getElementById('lbl-dob'),
        mineurLabel: document.getElementById('lbl-mineur'),
        catLabel: document.getElementById('lbl-cat'),
        roleLabel: document.getElementById('lbl-role'),
        parentLabel: document.getElementById('lbl-parent'),
        tuteur1Label: document.getElementById('lbl-tuteur1'),
        tuteur2Label: document.getElementById('lbl-tuteur2'),
        natLabel: document.getElementById('lbl-nat'),
        cnsLabel: document.getElementById('lbl-cns'),
        medicoLabel: document.getElementById('lbl-medico'),
        licenceLabel: document.getElementById('lbl-licence'),
        clubLabel: document.getElementById('lbl-club'),
        u7Label: document.getElementById('lbl-u7'),
        adresseLabel: document.getElementById('lbl-adresse'),
        emailLabel: document.getElementById('lbl-email'),
        gsm1Label: document.getElementById('lbl-gsm1'),
        gsm2Label: document.getElementById('lbl-gsm2'),
        chk1Label: document.getElementById('lbl-chk1'),
        chk2Label: document.getElementById('lbl-chk2'),
        chk3Label: document.getElementById('lbl-chk3'),
        chk4Label: document.getElementById('lbl-chk4'),
        dateNaissance: document.getElementById('DateNaissance'),
        mineur: document.getElementById('Mineur'),
        categorie: document.getElementById('Categorie'),
        catDisplay: document.getElementById('cat-display'),
        catSection: document.getElementById('cat-section'),
        role: document.getElementById('Role'),
        parentSection: document.getElementById('parent-section'),
        parentIsole: document.getElementById('ParentIsole'),
        tuteur1: document.getElementById('Tuteur1'),
        tuteur2: document.getElementById('Tuteur2'),
        tuteur2Wrap: document.getElementById('tuteur2-wrap'),
        cnsInput: document.getElementById('CNS'),
        cnsPrefix: document.getElementById('cns-prefix-display'),
        u7Section: document.getElementById('u7-section'),
        u7Cert: document.getElementById('U7Cert'),
        submitButton: document.getElementById('submitBtn'),
        successBox: document.getElementById('success-box'),
        langSelector: document.querySelector('.join-lang-selector'),
        honeypot: document.getElementById('honeypot')
    };

    let currentLang = 'lu';

    const translations = {
        lu: {
            nom: 'NIMM (WEI AUM PERSONALAUSWEIS) *',
            prenom: 'VIRNUMM *',
            dob: 'GEBUERTSDATUM (DD.MM.JJJJ) *',
            mineur: 'MANNERJAREG? *',
            cat: 'FLH KATEGORIE (AUTO)',
            role: 'FUNKTIOUN *',
            parent: 'ELENDERZEIEND? *',
            tuteur1: 'TUTEUR 1 (NUMM A VIRNUMM) *',
            tuteur2: 'TUTEUR 2 (NUMM A VIRNUMM) *',
            nat: 'NATIONALITEIT *',
            cns: 'CNS NUMMER (5 ZIFFEREN) *',
            medico: 'MEDICO? *',
            licence: 'LIZENZ? *',
            club: 'FREIERE VERAIN (ODER "NEANT") *',
            u7: 'U7: SPORTMEDIZINESCHT ATTEST OBLIGATORESCH (VUM HAUSARZT).',
            adresse: 'ADRESS (NR., STROOSS, PLZ, UERT) *',
            email: 'EMAIL *',
            gsm1: 'TEL MOBILE / GSM 1 *',
            gsm2: 'TEL MOBILE / GSM 2 (OPTIONAL)',
            chk1: `ECH HUN GELIES AN AKZEPTEIEREN D'<a href="${conditionsUrl}" target="_blank" rel="noopener noreferrer">ALLGEMENG BEDENGUNGEN</a>.`,
            chk2: `ECH HUN GELIES AN AKZEPTEIEREN DE <a href="${dataProtectionUrl}" target="_blank" rel="noopener noreferrer">DATESCHUTZ</a>.`,
            chk3: 'INFO: ECH HUN VERSTANEN DATT MENG UMELDUNG IWWERT DAT FLH PORTAL OFGESCHLOSS GETT.',
            chk4: 'BESTATEGUNG: ECH CONFIRMEIEREN D\'RICHTEGKEET VUN MENGE DONNEEEN.',
            send: 'WEIDERLEEDEN',
            yes: 'Jo',
            no: 'Nee',
            player: 'Spiller / Spillerin',
            official: 'Offiziell(e)',
            referee: 'Schiedsriichter(in)',
            parentNo: 'NEE (2 Tuteure)',
            parentYes: 'Jo (1 Tuteur)'
        },
        fr: {
            nom: 'NOM(S) SUR CARTE D\'IDENTITE *',
            prenom: 'PRENOM *',
            dob: 'DATE DE NAISSANCE (JJ.MM.AAAA) *',
            mineur: 'MINEUR? *',
            cat: 'CATEGORIE FLH (AUTO)',
            role: 'ROLE / FONCTION *',
            parent: 'PARENT ISOLE? *',
            tuteur1: 'TUTEUR 1 (NOM ET PRENOM) *',
            tuteur2: 'TUTEUR 2 (NOM ET PRENOM) *',
            nat: 'NATIONALITE *',
            cns: 'MATRICULE CNS (5 CHIFFRES) *',
            medico: 'MEDICO? *',
            licence: 'LICENCE? *',
            club: 'ANCIEN CLUB (OU "NEANT") *',
            u7: 'U7 : CERTIFICAT MEDICAL D\'APTITUDE SPORTIVE OBLIGATOIRE (ETABLI PAR LE MEDECIN TRAITANT).',
            adresse: 'ADRESSE (NO, RUE, CODE POSTAL, LOCALITE) *',
            email: 'EMAIL *',
            gsm1: 'TEL MOBILE / GSM 1 *',
            gsm2: 'TEL MOBILE / GSM 2 (OPTIONNEL)',
            chk1: `J'AI LU ET J'ACCEPTE LES <a href="${conditionsUrl}" target="_blank" rel="noopener noreferrer">CONDITIONS GENERALES</a>.`,
            chk2: `J'AI LU ET J'ACCEPTE LA <a href="${dataProtectionUrl}" target="_blank" rel="noopener noreferrer">PROTECTION DES DONNEES</a>.`,
            chk3: 'INFO: J\'AI COMPRIS QUE MA DEMANDE D\'AFFILIATION SERA FINALISEE VIA LE PORTAIL DE LA FLH.',
            chk4: 'CONFIRMATION: JE CONFIRME L\'EXACTITUDE DE MES DONNEES.',
            send: 'ENVOYER',
            yes: 'Oui',
            no: 'Non',
            player: 'Joueur / Joueuse',
            official: 'Officiel(le)',
            referee: 'Arbitre',
            parentNo: 'NON (2 Tuteurs)',
            parentYes: 'OUI (1 Tuteur)'
        },
        de: {
            nom: 'NAME(N) LAUT PERSONALAUSWEIS *',
            prenom: 'VORNAME *',
            dob: 'GEBURTSDATUM (TT.MM.JJJJ) *',
            mineur: 'MINDERJAEHRIG? *',
            cat: 'FLH KATEGORIE (AUTO)',
            role: 'ROLLE / FUNKTION *',
            parent: 'ALLEINERZIEHEND? *',
            tuteur1: 'ERZIEHUNGSBERECHTIGTER 1 (NAME UND VORNAME) *',
            tuteur2: 'ERZIEHUNGSBERECHTIGTER 2 (NAME UND VORNAME) *',
            nat: 'NATIONALITAET *',
            cns: 'CNS NUMMER (5 ZIFFERN) *',
            medico: 'AERZTLICHES ATTEST? *',
            licence: 'LIZENZ? *',
            club: 'FRUEHERER VEREIN (ODER "KEINER") *',
            u7: 'U7: SPORTAERZTLICHES ATTEST PFLICHT (VOM HAUSARZT AUSGESTELLT).',
            adresse: 'ADRESSE (NR., STRASSE, PLZ, ORT) *',
            email: 'E-MAIL *',
            gsm1: 'MOBILNUMMER / GSM 1 *',
            gsm2: 'MOBILNUMMER / GSM 2 (OPTIONAL)',
            chk1: `ICH HABE GELESEN UND AKZEPTIERE DIE <a href="${conditionsUrl}" target="_blank" rel="noopener noreferrer">ALLGEMEINEN BEDINGUNGEN</a>.`,
            chk2: `ICH HABE GELESEN UND AKZEPTIERE DEN <a href="${dataProtectionUrl}" target="_blank" rel="noopener noreferrer">DATENSCHUTZ</a>.`,
            chk3: 'INFO: ICH HABE VERSTANDEN, DASS MEIN ANTRAG UEBER DAS FLH-PORTAL ABGESCHLOSSEN WIRD.',
            chk4: 'BESTAETIGUNG: ICH BESTAETIGE DIE RICHTIGKEIT MEINER ANGABEN.',
            send: 'ABSCHICKEN',
            yes: 'Ja',
            no: 'Nein',
            player: 'Spieler/in',
            official: 'Funktionaer/in',
            referee: 'Schiedsrichter/in',
            parentNo: 'NEIN (2 Erziehungsberechtigte)',
            parentYes: 'JA (1 Erziehungsberechtigter)'
        },
        en: {
            nom: 'LAST NAME(S) AS ON ID CARD *',
            prenom: 'FIRST NAME *',
            dob: 'DATE OF BIRTH (DD.MM.YYYY) *',
            mineur: 'MINOR? *',
            cat: 'FLH CATEGORY (AUTO)',
            role: 'ROLE / FUNCTION *',
            parent: 'SINGLE PARENT? *',
            tuteur1: 'GUARDIAN 1 (LAST AND FIRST NAME) *',
            tuteur2: 'GUARDIAN 2 (LAST AND FIRST NAME) *',
            nat: 'NATIONALITY *',
            cns: 'CNS NUMBER (5 DIGITS) *',
            medico: 'MEDICAL CERTIFICATE? *',
            licence: 'LICENCE? *',
            club: 'PREVIOUS CLUB (OR "NONE") *',
            u7: 'U7: MEDICAL FITNESS CERTIFICATE MANDATORY (ISSUED BY FAMILY DOCTOR).',
            adresse: 'ADDRESS (NO., STREET, POSTCODE, CITY) *',
            email: 'EMAIL *',
            gsm1: 'MOBILE / GSM 1 *',
            gsm2: 'MOBILE / GSM 2 (OPTIONAL)',
            chk1: `I HAVE READ AND ACCEPT THE <a href="${conditionsUrl}" target="_blank" rel="noopener noreferrer">GENERAL TERMS AND CONDITIONS</a>.`,
            chk2: `I HAVE READ AND ACCEPT THE <a href="${dataProtectionUrl}" target="_blank" rel="noopener noreferrer">DATA PROTECTION POLICY</a>.`,
            chk3: 'INFO: I UNDERSTAND THAT MY MEMBERSHIP REQUEST WILL BE FINALISED VIA THE FLH PORTAL.',
            chk4: 'CONFIRMATION: I CONFIRM THE ACCURACY OF MY DATA.',
            send: 'SUBMIT',
            yes: 'Yes',
            no: 'No',
            player: 'Player',
            official: 'Official',
            referee: 'Referee',
            parentNo: 'NO (2 Guardians)',
            parentYes: 'YES (1 Guardian)'
        },
        pt: {
            nom: 'APELIDO(S) CONFORME BILHETE DE IDENTIDADE *',
            prenom: 'PRIMEIRO NOME *',
            dob: 'DATA DE NASCIMENTO (DD.MM.AAAA) *',
            mineur: 'MENOR? *',
            cat: 'CATEGORIA FLH (AUTO)',
            role: 'FUNCAO *',
            parent: 'PROGENITOR UNICO? *',
            tuteur1: 'TUTOR 1 (APELIDO E NOME) *',
            tuteur2: 'TUTOR 2 (APELIDO E NOME) *',
            nat: 'NACIONALIDADE *',
            cns: 'NUMERO CNS (5 DIGITOS) *',
            medico: 'ATESTADO MEDICO? *',
            licence: 'LICENCA? *',
            club: 'CLUBE ANTERIOR (OU "NENHUM") *',
            u7: 'U7: CERTIFICADO MEDICO DE APTIDAO DESPORTIVA OBRIGATORIO (EMITIDO PELO MEDICO DE FAMILIA).',
            adresse: 'MORADA (N, RUA, CODIGO POSTAL, LOCALIDADE) *',
            email: 'EMAIL *',
            gsm1: 'TEL MOVEL / GSM 1 *',
            gsm2: 'TEL MOVEL / GSM 2 (OPCIONAL)',
            chk1: `LI E ACEITO OS <a href="${conditionsUrl}" target="_blank" rel="noopener noreferrer">TERMOS E CONDICOES GERAIS</a>.`,
            chk2: `LI E ACEITO A <a href="${dataProtectionUrl}" target="_blank" rel="noopener noreferrer">POLITICA DE PROTECAO DE DADOS</a>.`,
            chk3: 'INFO: COMPREENDO QUE O MEU PEDIDO DE FILIACAO SERA FINALIZADO VIA O PORTAL FLH.',
            chk4: 'CONFIRMACAO: CONFIRMO A EXATIDAO DOS MEUS DADOS.',
            send: 'ENVIAR',
            yes: 'Sim',
            no: 'Nao',
            player: 'Jogador/a',
            official: 'Oficial',
            referee: 'Arbitro/a',
            parentNo: 'NAO (2 Tutores)',
            parentYes: 'SIM (1 Tutor)'
        }
    };

    const parseBirthDate = (value) => {
        const parts = value.split('.');

        if (parts.length !== 3) {
            return null;
        }

        const day = Number.parseInt(parts[0], 10);
        const month = Number.parseInt(parts[1], 10);
        const year = Number.parseInt(parts[2], 10);

        if (
            Number.isNaN(day) ||
            Number.isNaN(month) ||
            Number.isNaN(year) ||
            year < 1900 ||
            month < 1 ||
            month > 12 ||
            day < 1 ||
            day > 31
        ) {
            return null;
        }

        return { day, month, year };
    };

    const determineCategory = (age) => {
        if (age <= 6) return 'U7';
        if (age <= 8) return 'U9';
        if (age <= 10) return 'U11';
        if (age <= 12) return 'U13';
        if (age <= 14) return 'U15';
        if (age <= 16) return 'U17';
        if (age <= 18) return 'U19';
        if (age <= 23) return 'Espoirs';
        if (age <= 40) return 'Seniors';

        return 'Veterans';
    };

    const syncParentRequirements = () => {
        const isMinor = elements.mineur.value === 'OUI';
        const isSingleParent = elements.parentIsole.value === 'OUI';

        elements.parentSection.style.display = isMinor ? 'grid' : 'none';
        elements.tuteur1.required = isMinor;
        elements.tuteur2.required = isMinor && !isSingleParent;
        elements.tuteur2Wrap.style.display = isMinor && !isSingleParent ? 'grid' : 'none';

        if (!isMinor) {
            elements.parentIsole.value = 'NON';
            elements.tuteur1.value = '';
            elements.tuteur2.value = '';
        }

        if (isSingleParent) {
            elements.tuteur2.value = '';
        }
    };

    const syncU7Requirement = (category) => {
        const isU7 = category === 'U7';

        elements.u7Section.style.display = isU7 ? 'flex' : 'none';
        elements.u7Cert.required = isU7;

        if (!isU7) {
            elements.u7Cert.checked = false;
        }
    };

    const updateLanguage = (lang) => {
        const text = translations[lang];

        if (!text) {
            return;
        }

        currentLang = lang;

        elements.langTexts.forEach((entry) => {
            entry.classList.toggle('is-active', entry.id === lang);
        });
        elements.langButtons.forEach((button) => {
            const isActive = button.dataset.lang === lang;
            button.classList.toggle('is-active', isActive);
            button.setAttribute('aria-pressed', isActive ? 'true' : 'false');
        });

        elements.nomLabel.textContent = text.nom;
        elements.prenomLabel.textContent = text.prenom;
        elements.dobLabel.textContent = text.dob;
        elements.mineurLabel.textContent = text.mineur;
        elements.catLabel.textContent = text.cat;
        elements.roleLabel.textContent = text.role;
        elements.parentLabel.textContent = text.parent;
        elements.tuteur1Label.textContent = text.tuteur1;
        elements.tuteur2Label.textContent = text.tuteur2;
        elements.natLabel.textContent = text.nat;
        elements.cnsLabel.textContent = text.cns;
        elements.medicoLabel.textContent = text.medico;
        elements.licenceLabel.textContent = text.licence;
        elements.clubLabel.textContent = text.club;
        elements.u7Label.textContent = text.u7;
        elements.adresseLabel.textContent = text.adresse;
        elements.emailLabel.textContent = text.email;
        elements.gsm1Label.textContent = text.gsm1;
        elements.gsm2Label.textContent = text.gsm2;
        elements.chk1Label.innerHTML = text.chk1;
        elements.chk2Label.innerHTML = text.chk2;
        elements.chk3Label.textContent = text.chk3;
        elements.chk4Label.textContent = text.chk4;
        elements.submitButton.textContent = text.send;

        elements.mineur.options[0].text = text.no;
        elements.mineur.options[1].text = text.yes;
        elements.role.options[0].text = text.player;
        elements.role.options[1].text = text.official;
        elements.role.options[2].text = text.referee;
        elements.parentIsole.options[0].text = text.parentNo;
        elements.parentIsole.options[1].text = text.parentYes;
    };

    const buildRegistrationMessage = (formData) => {
        const details = [
            ['Language', currentLang.toUpperCase()],
            ['Last name', formData.get('Nom') || '-'],
            ['First name', formData.get('Prenom') || '-'],
            ['Date of birth', formData.get('DateNaissance') || '-'],
            ['Minor', elements.mineur.value || '-'],
            ['FLH category', elements.catDisplay.textContent.trim() || '-'],
            ['Role', formData.get('Role') || '-'],
            ['Nationality', formData.get('Nationalite') || '-'],
            ['CNS', formData.get('CNS') || '-'],
            ['Medical certificate', formData.get('Medico') || '-'],
            ['Existing licence', formData.get('Licence') || '-'],
            ['Previous club', formData.get('AncienClub') || '-'],
            ['Address', formData.get('Adresse') || '-'],
            ['Email', formData.get('Email') || '-'],
            ['Mobile 1', formData.get('GSM1') || '-'],
            ['Mobile 2', formData.get('GSM2') || '-']
        ];

        if (elements.mineur.value === 'OUI') {
            details.push(['Single parent', elements.parentIsole.value || '-']);
            details.push(['Guardian 1', formData.get('Tuteur1') || '-']);
            details.push(['Guardian 2', formData.get('Tuteur2') || '-']);
        }

        if (elements.catDisplay.textContent.trim() === 'U7') {
            details.push(['U7 medical certificate confirmed', elements.u7Cert.checked ? 'Yes' : 'No']);
        }

        details.push(['Conditions accepted', document.getElementById('chk1').checked ? 'Yes' : 'No']);
        details.push(['Data protection accepted', document.getElementById('chk2').checked ? 'Yes' : 'No']);
        details.push(['FLH portal info accepted', document.getElementById('chk3').checked ? 'Yes' : 'No']);
        details.push(['Data accuracy confirmed', document.getElementById('chk4').checked ? 'Yes' : 'No']);

        return details.map(([label, value]) => `${label}: ${value || '-'}`).join('\n');
    };

    const updateCategoryFromBirthDate = (value) => {
        const birthDate = parseBirthDate(value);

        if (!birthDate) {
            elements.catSection.style.display = 'none';
            elements.catDisplay.textContent = '-';
            elements.categorie.value = '';
            elements.mineur.value = 'NON';
            syncParentRequirements();
            syncU7Requirement('');
            return;
        }

        const today = new Date();
        let age = today.getFullYear() - birthDate.year;

        if (
            today.getMonth() + 1 < birthDate.month ||
            (today.getMonth() + 1 === birthDate.month && today.getDate() < birthDate.day)
        ) {
            age -= 1;
        }

        const category = determineCategory(age);

        elements.categorie.value = category;
        elements.catDisplay.textContent = category;
        elements.catSection.style.display = 'grid';
        elements.mineur.value = age < 18 ? 'OUI' : 'NON';
        syncParentRequirements();
        syncU7Requirement(category);
    };

    elements.langButtons.forEach((button) => {
        button.addEventListener('click', () => {
            updateLanguage(button.dataset.lang || 'lu');
        });
    });

    elements.dateNaissance.addEventListener('input', (event) => {
        const input = event.currentTarget;
        let value = input.value.replace(/\D/g, '').slice(0, 8);

        if (value.length > 2 && value.length <= 4) {
            value = `${value.slice(0, 2)}.${value.slice(2)}`;
        } else if (value.length > 4) {
            value = `${value.slice(0, 2)}.${value.slice(2, 4)}.${value.slice(4)}`;
        }

        input.value = value;
        updateCategoryFromBirthDate(value);
    });

    elements.parentIsole.addEventListener('change', syncParentRequirements);

    elements.cnsInput.addEventListener('input', (event) => {
        const input = event.currentTarget;
        const numericValue = input.value.replace(/\D/g, '').slice(0, 5);
        const birthDate = parseBirthDate(elements.dateNaissance.value);

        input.value = numericValue;

        if (!birthDate || !numericValue.length) {
            elements.cnsPrefix.textContent = '';
            return;
        }

        const expectedPrefix = `${String(birthDate.year).slice(-2)}${String(birthDate.month).padStart(2, '0')}${String(birthDate.day).padStart(2, '0')}`.slice(0, 5);

        elements.cnsPrefix.textContent = expectedPrefix.startsWith(numericValue)
            ? 'Prefix CNS OK'
            : `Expected prefix: ${expectedPrefix}`;
    });

    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        if (elements.honeypot.value.trim() !== '') {
            return;
        }

        if (!form.checkValidity()) {
            form.reportValidity();
            return;
        }

        const formData = new FormData(form);
        const originalLabel = elements.submitButton.textContent;
        const fullName = `${formData.get('Prenom') || ''} ${formData.get('Nom') || ''}`.trim() || 'Join Us Registration';

        formData.append('Mineur', elements.mineur.value);
        formData.set('Categorie', elements.catDisplay.textContent.trim());

        if (elements.parentIsole.value === 'OUI') {
            formData.set('Tuteur2', '-');
        }

        formData.set('access_key', registrationAccessKey);
        formData.set('subject', `[Mersch75 Join Us] ${fullName}`);
        formData.set('from_name', 'Mersch75 Join Us');
        formData.set('name', fullName);
        formData.set('email', String(formData.get('Email') || ''));
        formData.set('replyto', String(formData.get('Email') || ''));
        formData.set('redirect', 'false');
        formData.set('botcheck', elements.honeypot.value.trim());
        formData.set('message', buildRegistrationMessage(formData));

        elements.submitButton.textContent = 'Sending...';
        elements.submitButton.disabled = true;

        try {
            const response = await fetch(registrationEndpoint, {
                method: 'POST',
                headers: {
                    Accept: 'application/json'
                },
                body: formData
            });
            const payload = await response.json();

            if (!response.ok || payload.success !== true) {
                throw new Error(payload.message || 'submission-failed');
            }

            form.style.display = 'none';
            elements.langSelector.style.display = 'none';
            elements.langTexts.forEach((entry) => {
                entry.style.display = 'none';
            });
            elements.successBox.style.display = 'block';
            window.scrollTo({ top: form.offsetTop - 40, behavior: 'smooth' });
        } catch (error) {
            console.error(error);
            alert(`The registration could not be sent. Please try again or contact ${registrationMailbox}.`);
            elements.submitButton.textContent = originalLabel;
            elements.submitButton.disabled = false;
        }
    });

    updateLanguage('lu');
    syncParentRequirements();
    syncU7Requirement('');
}

function initializeNewsCarousel() {
    const carousel = document.querySelector('[data-news-carousel]');
    if (!carousel) return;

    const track = carousel.querySelector('[data-news-track]');
    let slides = Array.from(carousel.querySelectorAll('[data-news-slide]'));
    if (track) {
        const agSlide = track.querySelector('.news-slide-ag[data-news-slide]');
        if (agSlide && track.firstElementChild !== agSlide) {
            track.prepend(agSlide);
            slides = Array.from(carousel.querySelectorAll('[data-news-slide]'));
        }
    }
    const prevButton = carousel.querySelector('[data-news-prev]');
    const nextButton = carousel.querySelector('[data-news-next]');
    const dotsContainer = carousel.querySelector('[data-news-dots]');

    // Zeitgesteuerte Slides: noch nicht gestartete (data-news-starts) oder
    // abgelaufene (data-news-expires) Meldungen automatisch entfernen.
    // Format: "YYYY-MM-DD" oder "YYYY-MM-DDTHH:MM". Ohne Uhrzeit gilt der Slide
    // bis zum Tagesende des angegebenen Datums.
    const nowTs = new Date();
    slides.forEach((slide) => {
        const starts = slide.getAttribute('data-news-starts');
        const expires = slide.getAttribute('data-news-expires');
        if (starts) {
            const start = new Date(starts);
            if (!isNaN(start) && nowTs < start) {
                slide.remove();
                return;
            }
        }
        if (expires) {
            const end = new Date(expires);
            if (!expires.includes('T')) end.setHours(23, 59, 59, 999);
            if (!isNaN(end) && nowTs > end) {
                slide.remove();
            }
        }
    });

    carousel.querySelectorAll('[data-news-expires]:not([data-news-slide])').forEach((item) => {
        const expires = item.getAttribute('data-news-expires');
        const end = new Date(expires);
        if (!expires.includes('T')) end.setHours(23, 59, 59, 999);
        if (!isNaN(end) && nowTs > end) {
            item.remove();
        }
    });

    slides = Array.from(carousel.querySelectorAll('[data-news-slide]'));

    if (!track || slides.length === 0) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const allowAutoplay = false;

    // Bilder ausserhalb des ersten Slides erst bei Bedarf laden.
    slides.forEach((slide, i) => {
        if (i === 0) return;
        slide.querySelectorAll('img').forEach((img) => {
            if (!img.getAttribute('loading')) img.setAttribute('loading', 'lazy');
        });
    });

    let index = 0;
    let autoplayTimer = null;
    const autoplayDelay = 12000;

    const dots = slides.map((_, i) => {
        const dot = document.createElement('button');
        dot.type = 'button';
        dot.className = 'news-dot';
        dot.setAttribute('role', 'tab');
        dot.setAttribute('aria-label', `News ${i + 1}`);
        dot.addEventListener('click', () => {
            goTo(i);
            restartAutoplay();
        });
        if (dotsContainer) dotsContainer.append(dot);
        return dot;
    });

    function goTo(target) {
        index = (target + slides.length) % slides.length;
        const offset = slides[index].offsetLeft - slides[0].offsetLeft;
        track.style.transform = `translateX(-${offset}px)`;
        dots.forEach((dot, i) => {
            const active = i === index;
            dot.classList.toggle('is-active', active);
            dot.setAttribute('aria-selected', active ? 'true' : 'false');
        });
        slides.forEach((slide, i) => {
            slide.classList.toggle('is-current', i === index);
            slide.setAttribute('aria-hidden', i === index ? 'false' : 'true');
        });
    }

    function next() {
        goTo(index + 1);
    }

    function prev() {
        goTo(index - 1);
    }

    function startAutoplay() {
        if (!allowAutoplay || autoplayTimer) return;
        carousel.classList.add('is-autoplaying');
        autoplayTimer = window.setInterval(next, autoplayDelay);
    }

    function stopAutoplay() {
        carousel.classList.remove('is-autoplaying');
        if (autoplayTimer) {
            window.clearInterval(autoplayTimer);
            autoplayTimer = null;
        }
    }

    function restartAutoplay() {
        stopAutoplay();
        startAutoplay();
    }

    if (nextButton) {
        nextButton.addEventListener('click', () => {
            next();
            restartAutoplay();
        });
    }

    if (prevButton) {
        prevButton.addEventListener('click', () => {
            prev();
            restartAutoplay();
        });
    }

    carousel.addEventListener('mouseenter', stopAutoplay);
    carousel.addEventListener('mouseleave', startAutoplay);
    carousel.addEventListener('focusin', stopAutoplay);
    carousel.addEventListener('focusout', (event) => {
        if (!carousel.contains(event.relatedTarget)) startAutoplay();
    });

    // Tastatur-Navigation
    carousel.setAttribute('tabindex', '0');
    carousel.addEventListener('keydown', (event) => {
        if (event.key === 'ArrowRight') {
            event.preventDefault();
            next();
            restartAutoplay();
        } else if (event.key === 'ArrowLeft') {
            event.preventDefault();
            prev();
            restartAutoplay();
        }
    });

    let touchStartX = null;
    track.addEventListener('touchstart', (event) => {
        touchStartX = event.touches[0].clientX;
        stopAutoplay();
    }, { passive: true });
    track.addEventListener('touchend', (event) => {
        if (touchStartX === null) return;
        const delta = event.changedTouches[0].clientX - touchStartX;
        if (Math.abs(delta) > 40) {
            if (delta < 0) {
                next();
            } else {
                prev();
            }
        }
        touchStartX = null;
        restartAutoplay();
    }, { passive: true });

    let resizeTimer = null;
    window.addEventListener('resize', () => {
        if (resizeTimer) window.clearTimeout(resizeTimer);
        resizeTimer = window.setTimeout(() => goTo(index), 150);
    });

    goTo(0);
}

function initializeAgModal() {
    const modal = document.getElementById('agModal');
    if (!modal) return;
    const triggers = document.querySelectorAll('.news-ag-link');
    const closeEls = modal.querySelectorAll('[data-ag-close]');
    const copyBtn = modal.querySelector('[data-ag-copy]');
    const mailBtn = modal.querySelector('.ag-modal-btn');
    const hint = modal.querySelector('[data-ag-hint]');
    const mailText = 'An: info@mersch75.lu\n'
        + 'Betreff: Umeldung Generalversammlung 10.07.2026\n\n'
        + 'Moien,\n\n'
        + 'Ech melle mech mat ____ Persoun(en) un fir op d\'Generalversammlung & Ofschloss-Party de 10. Juli 2026 ze kommen.\n\n'
        + 'Numm(en):\n\n'
        + 'Merci a bis geschwënn!';
    function showHint(message) {
        if (!hint) return;
        hint.textContent = message;
        hint.hidden = false;
        window.setTimeout(() => { hint.hidden = true; }, 4000);
    }
    let lastFocus = null;
    function openModal(event) {
        if (event) event.preventDefault();
        lastFocus = document.activeElement;
        modal.hidden = false;
        document.body.style.overflow = 'hidden';
        const closeBtn = modal.querySelector('.ag-modal-close');
        if (closeBtn) closeBtn.focus();
    }
    function closeModal() {
        modal.hidden = true;
        document.body.style.overflow = '';
        if (lastFocus && typeof lastFocus.focus === 'function') lastFocus.focus();
    }
    triggers.forEach((t) => t.addEventListener('click', openModal));
    closeEls.forEach((el) => el.addEventListener('click', closeModal));
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.hidden) closeModal();
    });
    async function copyText(value) {
        try {
            await navigator.clipboard.writeText(value);
            return true;
        } catch (_) {
            try {
                const ta = document.createElement('textarea');
                ta.value = value;
                ta.style.position = 'fixed';
                ta.style.opacity = '0';
                document.body.appendChild(ta);
                ta.focus();
                ta.select();
                const ok = document.execCommand('copy');
                document.body.removeChild(ta);
                return ok;
            } catch (_e) {
                return false;
            }
        }
    }
    if (copyBtn) {
        copyBtn.addEventListener('click', async () => {
            const ok = await copyText(copyBtn.getAttribute('data-ag-copy'));
            showHint(ok ? 'Adress kopéiert ✓' : 'info@mersch75.lu');
        });
    }
    if (mailBtn) {
        mailBtn.addEventListener('click', async () => {
            const ok = await copyText(mailText);
            showHint(ok
                ? 'E-Mail-Text kopéiert ✓ — fügt en an ären Mailprogramm oder Webmail (Gmail, Outlook...) an a schéckt en un info@mersch75.lu'
                : 'Schéckt eng Mail un info@mersch75.lu');
        });
    }
}

ensureSiteLanguageSwitcher();
initializeSiteLanguage();
// initializeLanguageSelectionHint();  // Hinweisbanner "Wielt hei Är Sprooch." deaktiviert – Sprachumschalter ist dezent in der Kopfzeile sichtbar.
initializeSiteMenu();
initializeTrainingSchedule();
initializeJoinUsForm();
initializeSharedFooters();
initializeNewsCarousel();
initializeAgModal();
syncCurrentYear();

// Passwuert Modal fir Wëllkomm Mapp
(function() {
    document.addEventListener('DOMContentLoaded', function() {
        document.querySelectorAll('a[data-password]').forEach(function(link) {
            link.addEventListener('click', function(e) {
                e.preventDefault();
                var password = link.getAttribute('data-password');
                var userPass = prompt('Passwuert fir Wëllkomm Mapp:');
                if (userPass === password) {
                    window.location.href = link.href;
                } else if (userPass !== null) {
                    alert('Falscht Passwuert!');
                }
            });
        });
    });
})();
