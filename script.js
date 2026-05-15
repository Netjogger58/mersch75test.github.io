const yearTarget = document.querySelector('#current-year');

function initializeSiteMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const siteNav = document.querySelector('.site-nav');

    if (!navToggle || !siteNav) {
        return;
    }

    const labelDefault = 'Menü';
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    const navItems = [
        { href: 'matchcenter.html', label: 'Matchcenter', primary: true },
        { href: 'matchday.html', label: 'Matchday', primary: true },
        { href: 'training.html', label: 'Training', primary: true },
        { href: 'trainerstaff.html', label: 'Trainerstaff', primary: true },
        { href: 'news.html', label: 'News', primary: true },
        { href: 'join.html', label: 'Join Us', primary: true },
        { href: 'inside.html', label: 'Inside', primary: true },
        { href: 'gallery.html', label: 'Galerie', primary: false },
        { href: 'community.html', label: 'Community', primary: false },
        { href: 'links.html', label: 'Links', primary: false },
        { href: 'contact.html', label: 'Contact', primary: false }
    ];

    const intro = document.createElement('div');
    intro.className = 'site-menu-intro';
    intro.innerHTML = [
        '<p class="site-menu-kicker">Navigation</p>',
        '<h2>Alles Wichtegt fir Mersch75 op enger Plaz.</h2>',
        '<p>Matchday, Matchcenter, Training, Trainerstaff a Club-Liewen ginn hei wéi an engem richtege Menü-Hub gebündelt, amplaz als klassesch Header-Leescht.</p>'
    ].join('');

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
    footer.innerHTML = [
        '<a class="site-menu-cta" href="matchday.html">',
        '<span>Live Fokus</span>',
        '<strong>Aktueller Spieltag</strong>',
        '</a>',
        '<a class="site-menu-cta" href="join.html">',
        '<span>Club</span>',
        '<strong>Mitmachen & Kontakt</strong>',
        '</a>'
    ].join('');

    const closeButton = document.createElement('button');
    closeButton.type = 'button';
    closeButton.className = 'site-menu-close';
    closeButton.setAttribute('aria-label', 'Menü schließen');
    closeButton.textContent = 'X';

    const shell = document.createElement('div');
    shell.className = 'site-menu-shell';
    shell.append(closeButton, intro, primaryGroup, secondaryGroup, footer);

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

initializeSiteMenu();
initializeTrainingSchedule();

if (yearTarget) {
    yearTarget.textContent = new Date().getFullYear();
}