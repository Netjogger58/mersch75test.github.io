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
    const attributeTargets = Array.from(document.querySelectorAll('[data-i18n-attr]'));

    const translations = {
        lb: {
            pageTitle: 'Mersch75 Handball',
            pageDescription: 'Mersch75 Handball: Veräinsiwwerbléck, Spillplang, Training, News, Galerie a Matmaachen.',
            brandHomeAria: 'Mersch75 Startsäit',
            brandTagline: 'Zesumme staark',
            trainingPageTitle: 'Training | Mersch75 Handball',
            trainingPageDescription: 'Training beim Mersch75: Trainingsplang, Gruppen, Halen a Jugendkoordinatioun op ee Bléck.',
            trainingHeroLogoAlt: 'Team Training Logo',
            trainingTrainerstaff: 'Trainerteam',
            trainingTrialRequest: 'Probetraining ufroen',
            trainingScheduleOpen: 'Trainingsplang am Vollbild opmaachen',
            trainingScheduleClose: 'Vollbild zoumaachen',
            trainingYouthCoord: 'JUGENDKOORDINATIOUN:',
            trainingYouthCoordBody: 'Fir de Jugendberäich si de Max Blanc (LUXQF3) an de Louis Van der Weken (LUXQF2Bis) zoustänneg.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Tel.: Max Blanc 661 406 836',
            navMenu: 'Menü',
            navClose: 'Menü zoumaachen',
            navHome: 'Startsäit',
            navLiveCenter: 'Spillplang',
            navTraining: 'Training',
            navTrainerstaff: 'Trainerteam',
            navNews: 'News',
            navStatistics: 'Statistik 25/26',
            navJoin: 'Join Us',
            navComite: 'Comité',
            navGallery: 'Galerie',
            navHistory: 'Geschicht',
            navLinks: 'Nëtzlech Linken',
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
            newsStatsEyebrow: 'Saisonstatistik 25/26',
            newsStatsTitle: 'Statistiken vu Hären a Fraen op enger Plaz.',
            newsStatsBody: 'D\'Saisonstatistik 2025/2026 ass live: Tabellen, Resultater an Torschützenlëschten fir Hären a Fraen – iwwersiichtlech an aktuell.',
            newsStatsPillMen: 'Hären',
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
            infoMen: 'AXA League Hären',
            sponsorsTitle: 'Eis Sponsoren',
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
            trainingPageTitle: 'Entraînement | Mersch75 Handball',
            trainingPageDescription: 'Entraînement au Mersch75 : planning, groupes, salles et coordination des jeunes en un coup d\'oeil.',
            trainingHeroLogoAlt: 'Logo team training',
            trainingTrainerstaff: 'Encadrement',
            trainingTrialRequest: 'Demander un entraînement d\'essai',
            trainingScheduleOpen: 'Ouvrir le planning en plein écran',
            trainingScheduleClose: 'Fermer le plein écran',
            trainingYouthCoord: 'COORDINATION JEUNES:',
            trainingYouthCoordBody: 'Le secteur des jeunes est coordonné par Max Blanc (LUXQF3) et Louis Van der Weken (LUXQF2Bis).',
            trainingInfoLabel: 'Info :',
            trainingPhoneLabel: 'Tél. : Max Blanc 661 406 836',
            navMenu: 'Menu',
            navClose: 'Fermer le menu',
            navHome: 'Accueil',
            navLiveCenter: 'Calendrier',
            navTraining: 'Entraînement',
            navTrainerstaff: 'Encadrement',
            navNews: 'Actualités',
            navStatistics: 'Statistiques 25/26',
            navJoin: 'Join Us',
            navComite: 'Comité',
            navGallery: 'Galerie',
            navHistory: 'Historique',
            navLinks: 'Liens utiles',
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
            newsStatsEyebrow: 'Statistiques de saison 25/26',
            newsStatsTitle: 'Les statistiques hommes et femmes au même endroit.',
            newsStatsBody: 'Les statistiques de la saison 2025/2026 sont en ligne : classements, résultats et meilleurs buteurs pour les hommes et les femmes – clairs et à jour.',
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
            trainingPageTitle: 'Training | Mersch75 Handball',
            trainingPageDescription: 'Training bei Mersch75: Trainingsplan, Gruppen, Hallen und Jugendkoordination auf einen Blick.',
            trainingHeroLogoAlt: 'Team-Training Logo',
            trainingTrainerstaff: 'Trainerstaff',
            trainingTrialRequest: 'Probetraining anfragen',
            trainingScheduleOpen: 'Trainingsplan im Vollbild öffnen',
            trainingScheduleClose: 'Vollbild schließen',
            trainingYouthCoord: 'JUGENDKOORDINATION:',
            trainingYouthCoordBody: 'Für den Jugendbereich sind Max Blanc (LUXQF3) und Louis Van der Weken (LUXQF2Bis) zuständig.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Tel.: Max Blanc 661 406 836',
            navMenu: 'Menü',
            navClose: 'Menü schließen',
            navHome: 'Startseite',
            navLiveCenter: 'Spielplan',
            navTraining: 'Training',
            navTrainerstaff: 'Trainerstaff',
            navNews: 'News',
            navStatistics: 'Statistik 25/26',
            navJoin: 'Join Us',
            navComite: 'Comité',
            navGallery: 'Galerie',
            navHistory: 'Historie',
            navLinks: 'Nützliche Links',
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
            newsStatsEyebrow: 'Saisonstatistik 25/26',
            newsStatsTitle: 'Statistiken von Herren und Frauen an einem Ort.',
            newsStatsBody: 'Die Saisonstatistik 2025/2026 ist live: Tabellen, Ergebnisse und Torschützenlisten für Herren und Frauen – übersichtlich und aktuell.',
            newsStatsPillMen: 'Herren',
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
            infoMen: 'AXA League Herren',
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
            trainingPageTitle: 'Training | Mersch75 Handball',
            trainingPageDescription: 'Training at Mersch75: schedule, groups, halls and youth coordination at a glance.',
            trainingHeroLogoAlt: 'Team training logo',
            trainingTrainerstaff: 'Coaching Staff',
            trainingTrialRequest: 'Request a trial session',
            trainingScheduleOpen: 'Open training schedule fullscreen',
            trainingScheduleClose: 'Close fullscreen',
            trainingYouthCoord: 'YOUTH COORDINATION:',
            trainingYouthCoordBody: 'Max Blanc (LUXQF3) and Louis Van der Weken (LUXQF2Bis) are responsible for the youth section.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Phone: Max Blanc 661 406 836',
            navMenu: 'Menu',
            navClose: 'Close menu',
            navHome: 'Home',
            navLiveCenter: 'Schedule',
            navTraining: 'Training',
            navTrainerstaff: 'Coaching Staff',
            navNews: 'News',
            navStatistics: 'Statistics 25/26',
            navJoin: 'Join Us',
            navComite: 'Committee',
            navGallery: 'Gallery',
            navHistory: 'History',
            navLinks: 'Useful Links',
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
            newsStatsEyebrow: 'Season stats 25/26',
            newsStatsTitle: 'Men\'s and women\'s stats in one place.',
            newsStatsBody: 'The 2025/2026 season statistics are live: tables, results and top scorers for men and women – clear and up to date.',
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
            trainingPageTitle: 'Treino | Mersch75 Handball',
            trainingPageDescription: 'Treino no Mersch75: horários, grupos, pavilhões e coordenação jovem num relance.',
            trainingHeroLogoAlt: 'Logótipo team training',
            trainingTrainerstaff: 'Equipa técnica',
            trainingTrialRequest: 'Pedir treino experimental',
            trainingScheduleOpen: 'Abrir plano de treino em ecrã inteiro',
            trainingScheduleClose: 'Fechar ecrã inteiro',
            trainingYouthCoord: 'COORDENAÇÃO JOVEM:',
            trainingYouthCoordBody: 'Max Blanc (LUXQF3) e Louis Van der Weken (LUXQF2Bis) são responsáveis pela secção jovem.',
            trainingInfoLabel: 'Info:',
            trainingPhoneLabel: 'Tel.: Max Blanc 661 406 836',
            navMenu: 'Menu',
            navClose: 'Fechar menu',
            navHome: 'Início',
            navLiveCenter: 'Calendário',
            navTraining: 'Treino',
            navTrainerstaff: 'Equipa técnica',
            navNews: 'Notícias',
            navStatistics: 'Estatísticas 25/26',
            navJoin: 'Join Us',
            navComite: 'Comité',
            navGallery: 'Galeria',
            navHistory: 'História',
            navLinks: 'Links úteis',
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
            newsStatsEyebrow: 'Estatísticas da época 25/26',
            newsStatsTitle: 'Estatísticas de homens e mulheres num só lugar.',
            newsStatsBody: 'As estatísticas da época 2025/2026 estão online: classificações, resultados e melhores marcadores para homens e mulheres – claras e atualizadas.',
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

        document.documentElement.lang = resolvedLanguage === 'lb' ? 'lb' : resolvedLanguage;
        document.body.dataset.siteLanguage = resolvedLanguage;

        textTargets.forEach((target) => {
            const key = target.dataset.i18n;
            const value = getTranslation(resolvedLanguage, key);

            if (value) {
                target.textContent = value;
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
        { href: 'statistics-25-26.html', labelKey: 'navStatistics', fallback: 'Statistik 25/26', primary: true },
        { href: 'join.html', labelKey: 'navJoin', fallback: 'Join Us', primary: true },
        { href: 'comite.html', labelKey: 'navComite', fallback: 'Comité', primary: true },
        { href: 'gallery.html', labelKey: 'navGallery', fallback: 'Galerie', primary: false },
        { href: 'memories.html', labelKey: 'navMemories', fallback: 'Memories', primary: false },
        { href: 'historie.html', labelKey: 'navHistory', fallback: 'Historie', primary: false },
        { href: 'links.html', labelKey: 'navLinks', fallback: 'Useful Links', primary: false },
        { href: 'hallenkarte.html', labelKey: 'navHallenkarte', fallback: 'Hallenkarte', primary: false },
        { href: 'contact.html', labelKey: 'navContact', fallback: 'Contact', primary: false }
    ];

    const primaryGroup = document.createElement('div');
    primaryGroup.className = 'site-menu-primary';

    const secondaryGroup = document.createElement('div');
    secondaryGroup.className = 'site-menu-secondary';

    navItems.forEach(({ href, labelKey, fallback, primary }) => {
        const link = document.createElement('a');
        const targetGroup = primary ? primaryGroup : secondaryGroup;

        link.href = href;
        link.textContent = getI18nText(labelKey, fallback);

        if (currentPath === href) {
            link.classList.add('is-active');
        }

        targetGroup.append(link);
    });

    const footer = document.createElement('div');
    footer.className = 'site-menu-footer';

    // Sprachumschalter (nur auf Smartphones sichtbar) als Klon in das Burger-Menü übernehmen.
    const headerSwitcher = document.querySelector('.site-language-switcher');
    if (headerSwitcher) {
        const menuLangWrap = document.createElement('div');
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
        footer.append(menuLangWrap);
    }

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'site-menu-close';
    closeButton.setAttribute('aria-label', getI18nText('navClose', 'Menü schließen'));
    closeButton.textContent = 'X';

    const shell = document.createElement('div');
    shell.className = 'site-menu-shell';
    shell.append(closeButton, primaryGroup, secondaryGroup, footer);

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

        siteNav.querySelectorAll('a').forEach((link, index) => {
            const item = navItems[index];

            if (!item) {
                return;
            }

            const text = translator ? translator(item.labelKey) : getI18nText(item.labelKey, item.fallback);
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
                u11: { label: 'U11', title: 'U11' },
                u13u15: { label: 'U13 + U15', title: 'U13 & U15' },
                filles: { label: 'Filles', title: 'Filles U9 / U11 / U13' },
                fraen: { label: 'Fraen', title: 'Fraen' },
                haeren: { label: 'Hären S1 / S2 / U21 - U17', title: 'Hären S1 / S2 / U21 - U17' }
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
                u11: { label: 'U11', title: 'U11' },
                u13u15: { label: 'U13 + U15', title: 'U13 & U15' },
                filles: { label: 'Filles', title: 'Groupe Filles U9 / U11 / U13' },
                fraen: { label: 'Dames', title: 'Dames' },
                haeren: { label: 'Hommes S1 / S2 / U21 - U17', title: 'Hommes S1 / S2 / U21 - U17' }
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
                u11: { label: 'U11', title: 'U11' },
                u13u15: { label: 'U13 + U15', title: 'U13 & U15' },
                filles: { label: 'Mädchen', title: 'Mädchengruppe U9 / U11 / U13' },
                fraen: { label: 'Frauen', title: 'Frauen' },
                haeren: { label: 'Herren S1 / S2 / U21 - U17', title: 'Herren S1 / S2 / U21 - U17' }
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
                u11: { label: 'U11', title: 'U11' },
                u13u15: { label: 'U13 + U15', title: 'U13 & U15' },
                filles: { label: 'Girls', title: 'Girls Group U9 / U11 / U13' },
                fraen: { label: 'Women', title: 'Women' },
                haeren: { label: 'Men S1 / S2 / U21 - U17', title: 'Men S1 / S2 / U21 - U17' }
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
                u11: { label: 'U11', title: 'U11' },
                u13u15: { label: 'U13 + U15', title: 'U13 & U15' },
                filles: { label: 'Raparigas', title: 'Grupo Feminino U9 / U11 / U13' },
                fraen: { label: 'Seniores femininas', title: 'Seniores femininas' },
                haeren: { label: 'Seniores masculinos S1 / S2 / U21 - U17', title: 'Seniores masculinos S1 / S2 / U21 - U17' }
            }
        }
    };

    const hotspotGroupBase = [
        {
            group: 'u4',
            trainers: 'Grégory Redavid, Christophe Kremer, Marc Jungels, Max Blanc (LUXQF3)',
            slots: [
                { dayKey: 'wed', time: '16:30 - 17:30', location: 'Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'sat', time: '10:00 - 11:00', location: "Sportshal Lëntgen, 4, rue de l'Ecole, Lëntgen" }
            ],
            areas: [
                { left: 43.1, top: 47.3, width: 11.4, height: 8.4 },
                { left: 87.4, top: 30.6, width: 10.8, height: 8.3 }
            ]
        },
        {
            group: 'u7',
            trainers: 'Max Blanc (LUXQF3), Anne Holm (LUXQF3)',
            slots: [
                { dayKey: 'tue', time: '17:30 - 18:30', location: 'Sportshal Lëntgen, 50, rue de la Gare' },
                { dayKey: 'fri', time: '16:30 - 17:30', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 20.2, top: 55.6, width: 10.8, height: 8.1 },
                { left: 76.1, top: 47.3, width: 11.3, height: 8.4 }
            ]
        },
        {
            group: 'u9',
            trainers: 'Max Blanc (LUXQF3), Louis Van der Weken (LUXQF2Bis)',
            slots: [
                { dayKey: 'tue', time: '17:30 - 19:00', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' },
                { dayKey: 'thu', time: '17:30 - 19:00', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 32.3, top: 55.6, width: 10.8, height: 12.2 },
                { left: 54.4, top: 55.6, width: 10.9, height: 12.4 }
            ]
        },
        {
            group: 'u11',
            trainers: 'Max Blanc (LUXQF3), Elie Schuster',
            slots: [
                { dayKey: 'wed', time: '17:30 - 19:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'fri', time: '17:30 - 19:00', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 43.1, top: 55.7, width: 11.4, height: 12.3 },
                { left: 76.1, top: 55.6, width: 11.3, height: 12.4 }
            ]
        },
        {
            group: 'u13u15',
            trainers: 'Max Blanc (LUXQF3), Mathis Derneden',
            slots: [
                { dayKey: 'mon', time: '17:30 - 19:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'wed', time: '18:30 - 20:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'fri', time: '19:00 - 20:30', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 10.1, top: 55.6, width: 11.3, height: 12.2 },
                { left: 43.1, top: 67.9, width: 11.4, height: 8.3 },
                { left: 76.1, top: 68.0, width: 11.3, height: 8.3 }
            ]
        },
        {
            group: 'filles',
            trainers: 'Anne Bisenius Holm (LUXQF3), Katarzyna Pietrasik',
            slots: [
                { dayKey: 'fri', time: '17:30 - 19:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' }
            ],
            areas: [
                { left: 65.3, top: 55.6, width: 10.8, height: 12.4 }
            ]
        },
        {
            group: 'fraen',
            trainers: 'Katarzyna Pietrasik',
            slots: [
                { dayKey: 'mon', time: '19:00 - 20:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'fri', time: '19:00 - 20:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' }
            ],
            areas: [
                { left: 10.1, top: 67.9, width: 11.3, height: 12.2 },
                { left: 65.3, top: 68.0, width: 10.8, height: 12.2 }
            ]
        },
        {
            group: 'haeren',
            trainers: 'Laurent Metzler',
            slots: [
                { dayKey: 'mon', time: '20:30 - 21:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'wed', time: '20:30 - 21:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { dayKey: 'fri', time: '20:30 - 21:30', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 10.1, top: 80.2, width: 11.3, height: 8.5 },
                { left: 43.1, top: 76.2, width: 11.4, height: 12.4 },
                { left: 76.1, top: 76.3, width: 11.3, height: 12.3 }
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
                trainers: `${translation.trainerPrefix} ${group.trainers}`,
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
            `<p>${groupInfo.trainers}</p>`,
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
        { href: 'historie.html', label: 'Historie' },
        { href: 'contact.html', label: 'Contact' }
    ];
    const landingQuickLinks = [
        { href: 'matchday.html', label: 'Matchday' },
        { href: 'matchcenter.html', label: 'Matchcenter' },
        { href: 'training.html', label: 'Training' },
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
    const slides = Array.from(carousel.querySelectorAll('[data-news-slide]'));
    const prevButton = carousel.querySelector('[data-news-prev]');
    const nextButton = carousel.querySelector('[data-news-next]');
    const dotsContainer = carousel.querySelector('[data-news-dots]');
    if (!track || slides.length === 0) return;

    const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const allowAutoplay = !reduceMotion && slides.length > 1;

    // Bilder ausserhalb des ersten Slides erst bei Bedarf laden.
    slides.forEach((slide, i) => {
        if (i === 0) return;
        slide.querySelectorAll('img').forEach((img) => {
            if (!img.getAttribute('loading')) img.setAttribute('loading', 'lazy');
        });
    });

    let index = 0;
    let autoplayTimer = null;
    const autoplayDelay = 7000;

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
        if (!allowAutoplay) return;
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
    startAutoplay();
}

ensureSiteLanguageSwitcher();
initializeSiteLanguage();
// initializeLanguageSelectionHint();  // Hinweisbanner "Wielt hei Är Sprooch." deaktiviert – Sprachumschalter ist dezent in der Kopfzeile sichtbar.
initializeSiteMenu();
initializeTrainingSchedule();
initializeJoinUsForm();
initializeSharedFooters();
initializeNewsCarousel();
syncCurrentYear();