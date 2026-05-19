function syncCurrentYear() {
    document.querySelectorAll('#current-year').forEach((target) => {
        target.textContent = new Date().getFullYear();
    });
}

function initializeSiteMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');

    if (!navToggle || !siteNav) {
        return;
    }

    const labelDefault = 'Menü';
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navItems = [
        { href: 'index.html', label: 'Startseite', primary: true },
        { href: 'live-center.html', label: 'Spielplan', primary: true },
        { href: 'training.html', label: 'Training', primary: true },
        { href: 'trainerstaff.html', label: 'Trainerstaff', primary: true },
        { href: 'news.html', label: 'News', primary: true },
        { href: 'join.html', label: 'Join Us', primary: true },
        { href: 'comite.html', label: 'Comité', primary: true },
        { href: 'gallery.html', label: 'Galerie', primary: false },
        { href: 'historie.html', label: 'Historie', primary: false },
        { href: 'links.html', label: 'Links', primary: false },
        { href: 'contact.html', label: 'Contact', primary: false }
    ];

    const primaryGroup = document.createElement('div');
    primaryGroup.className = 'site-menu-primary';

    const secondaryGroup = document.createElement('div');
    secondaryGroup.className = 'site-menu-secondary';

    navItems.forEach(({ href, label, primary }) => {
        const link = document.createElement('a');
        const targetGroup = primary ? primaryGroup : secondaryGroup;

        link.href = href;
        link.textContent = label;

        if (currentPath === href) {
            link.classList.add('is-active');
        }

        targetGroup.append(link);
    });

    const footer = document.createElement('div');
    footer.className = 'site-menu-footer';

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'site-menu-close';
    closeButton.setAttribute('aria-label', 'Menü schließen');
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
    backdrop.setAttribute('aria-label', 'Menü schließen');
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
}

function initializeTrainingSchedule() {
    const scheduleContainer = document.querySelector('#schedule-container');
    const fullscreenButton = document.querySelector('#btn-schedule-fs');
    const hotspotLayer = document.querySelector('.training-schedule-hotspots');
    const tooltip = document.querySelector('#schedule-tooltip');

    if (!scheduleContainer || !fullscreenButton) {
        return;
    }

    const hotspotGroups = [
        {
            group: 'u4',
            label: 'Kidssports U4',
            title: 'Kidssports U4',
            trainers: 'TRAINER Grégory Redavid, Christophe Kremer, Marc Jungels, Max Blanc (LUXQF3)',
            slots: [
                { day: 'Mëttwochs', time: '16:30 - 17:30', location: 'Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Samschdes', time: '10:00 - 11:00', location: "SportHal, 4, rue de l'Ecole, Lëntgen" }
            ],
            areas: [
                { left: 43.1, top: 47.3, width: 11.4, height: 8.4 },
                { left: 87.4, top: 30.6, width: 10.8, height: 8.3 }
            ]
        },
        {
            group: 'u7',
            label: 'U7',
            title: 'U7',
            trainers: 'TRAINER Max Blanc (LUXQF3), Anne Holm (LUXQF3)',
            slots: [
                { day: 'Dënschdes', time: '17:30 - 18:30', location: 'Sportshal Lëntgen, 50, rue de la Gare' },
                { day: 'Freides', time: '16:30 - 17:30', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 20.2, top: 55.6, width: 10.8, height: 8.1 },
                { left: 76.1, top: 47.3, width: 11.3, height: 8.4 }
            ]
        },
        {
            group: 'u9',
            label: 'U9',
            title: 'U9',
            trainers: 'TRAINER Max Blanc (LUXQF3), Louis Van der Weken (LUXQF2Bis)',
            slots: [
                { day: 'Dënschdes', time: '17:30 - 19:00', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' },
                { day: 'Donneschdes', time: '17:30 - 19:00', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 32.3, top: 55.6, width: 10.8, height: 12.2 },
                { left: 54.4, top: 55.6, width: 10.9, height: 12.4 }
            ]
        },
        {
            group: 'u11',
            label: 'U11',
            title: 'U11',
            trainers: 'TRAINER Max Blanc (LUXQF3), Elie Schuster',
            slots: [
                { day: 'Mëttwochs', time: '17:30 - 19:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Freides', time: '17:30 - 19:00', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 43.1, top: 55.7, width: 11.4, height: 12.3 },
                { left: 76.1, top: 55.6, width: 11.3, height: 12.4 }
            ]
        },
        {
            group: 'u13u15',
            label: 'U13 + U15',
            title: 'U13 & U15',
            trainers: 'TRAINER Max Blanc (LUXQF3), Mathis Derneden',
            slots: [
                { day: 'Méindes', time: '17:30 - 19:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Mëttwochs', time: '18:30 - 20:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Freides', time: '19:00 - 20:30', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 10.1, top: 55.6, width: 11.3, height: 12.2 },
                { left: 43.1, top: 67.9, width: 11.4, height: 8.3 },
                { left: 76.1, top: 68.0, width: 11.3, height: 8.3 }
            ]
        },
        {
            group: 'filles',
            label: 'Filles',
            title: 'Groupe Filles U9 / U11 / U13',
            trainers: 'TRAINER Anne Bisenius Holm (LUXQF3), Katarzyna Pietrasik',
            slots: [
                { day: 'Freides', time: '17:30 - 19:00', location: 'Hall Omnisports, 21, rue des Prés, Mersch' }
            ],
            areas: [
                { left: 65.3, top: 55.6, width: 10.8, height: 12.4 }
            ]
        },
        {
            group: 'fraen',
            label: 'Fraen',
            title: 'Fraen',
            trainers: 'TRAINER Katarzyna Pietrasik',
            slots: [
                { day: 'Méindes', time: '19:00 - 20:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Freides', time: '19:00 - 20:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' }
            ],
            areas: [
                { left: 10.1, top: 67.9, width: 11.3, height: 12.2 },
                { left: 65.3, top: 68.0, width: 10.8, height: 12.2 }
            ]
        },
        {
            group: 'haeren',
            label: 'Hären S1 / S2 / U21 - U17',
            title: 'Hären S1 / S2 / U21 - U17',
            trainers: 'TRAINER Laurent Metzler',
            slots: [
                { day: 'Méindes', time: '20:30 - 21:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Mëttwochs', time: '20:30 - 21:30', location: 'Hall Omnisports, 21, rue des Prés, Mersch' },
                { day: 'Freides', time: '20:30 - 21:30', location: 'Hall Omnisports Krounebierg, 11, rue de la Piscine, Mersch' }
            ],
            areas: [
                { left: 10.1, top: 80.2, width: 11.3, height: 8.5 },
                { left: 43.1, top: 76.2, width: 11.4, height: 12.4 },
                { left: 76.1, top: 76.3, width: 11.3, height: 12.3 }
            ]
        }
    ];

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

    if (hotspotLayer && tooltip && hotspotGroups.length) {
        hotspotGroups.forEach(({ group, label, areas }) => {
            const groupHotspots = [];

            areas.forEach((area, index) => {
                const hotspot = document.createElement('button');

                hotspot.type = 'button';
                hotspot.className = 'training-schedule-hotspot';
                hotspot.setAttribute('aria-label', `${label} anzeigen`);
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
    }

    const getFullscreenElement = () => (
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.msFullscreenElement
    );

    const syncButton = () => {
        const isActive = Boolean(getFullscreenElement());
        fullscreenButton.textContent = isActive
            ? 'Vollbild schließen'
            : 'Trainingsplan im Vollbild öffnen';
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
        { href: 'gallery.html', label: 'Galerie' },
        { href: 'community.html', label: 'Community' },
        { href: 'links.html', label: 'Links' },
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

initializeSiteMenu();
initializeTrainingSchedule();
initializeJoinUsForm();
initializeSharedFooters();
syncCurrentYear();