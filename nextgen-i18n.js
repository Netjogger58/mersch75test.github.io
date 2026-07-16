(function () {
  if (typeof window.translations === 'undefined') return;
  var extra = {
    lb: {
      nextgenPageTitle: "NEXTGEN | Mersch75 Handball",
      nextgenMetaDesc: "NEXTGEN vum Mersch75: Ënnerstëtz eis Jugend mat engem Don vun 100 €.",
      nextgenEyebrow: "Ënnerstëtz eis Jugend",
      nextgenTitle: "NEXTGEN: Däin Numm fir eis nächst Generatioun",
      nextgenIntro: "Mat NEXTGEN investéiere mir an dat, wat Mersch75 staark mécht: eis Kanner, eis Jugend an eng nohalteg sportlech Zukunft.",
      nextgenContact: "Fir Sponsoring a Partnersuche këmmert sech de Max Blanc (<a href=\"mailto:max.hbm75@gmail.com\">max.hbm75@gmail.com</a>) am Veräin ëm NEXTGEN.",
      nextgenPanelName: "Däin Numm um Spillfeld",
      nextgenPanelDesc: "Mat <strong style=\"color:#f9d611;\">250 €</strong> gëtt Däin Numm op engem grousse Panel um Terräin veréiwegt – siichtbar bei all Match an all Training, fir déi ganz Saison laang. Du gëss e fixe Bestanddeel vun eiser Aréna an hëllefs direkt mat, datt eis jonk Spiller dat bescht Material, Formatioun a Betreiung kréien.",
      nextgenPanelSlogan: "Ee Feld. Ee Numm. Eng grouss Ënnerstëtzung. 💛💙",
      nextgenDonation: "All Don hëlleft eis, Material, Formatioun, Jugendaarbecht an Aktivitéite fir eis jonk Spiller weider auszebauen.",
      nextgenCtaSupport: "Ech wëll NEXTGEN ënnerstëtzen",
      nextgenCtaClub: "Méi iwwer de Club"
    },
    fr: {
      nextgenPageTitle: "NEXTGEN | Mersch75 Handball",
      nextgenMetaDesc: "NEXTGEN de Mersch75: soutenez notre jeunesse avec un don de 100 €.",
      nextgenEyebrow: "Soutenez notre jeunesse",
      nextgenTitle: "NEXTGEN: Votre nom pour notre prochaine génération",
      nextgenIntro: "Avec NEXTGEN, nous investissons dans ce qui rend Mersch75 fort: nos enfants, notre jeunesse et un avenir sportif durable.",
      nextgenContact: "Pour le sponsoring et les partenariats, Max Blanc (<a href=\"mailto:max.hbm75@gmail.com\">max.hbm75@gmail.com</a>) s'occupe de NEXTGEN au sein du club.",
      nextgenPanelName: "Votre nom sur le terrain",
      nextgenPanelDesc: "Avec <strong style=\"color:#f9d611;\">250 €</strong>, votre nom est affiché sur un grand panneau au terrain – visible à chaque match et entraînement, pour toute la saison. Vous devenez un élément fixe de notre arène et aidez directement nos jeunes joueurs à obtenir le meilleur matériel, la meilleure formation et le meilleur encadrement.",
      nextgenPanelSlogan: "Un terrain. Un nom. Un grand soutien. 💛💙",
      nextgenDonation: "Chaque don nous aide à développer le matériel, la formation, le travail avec les jeunes et les activités pour nos jeunes joueurs.",
      nextgenCtaSupport: "Je veux soutenir NEXTGEN",
      nextgenCtaClub: "En savoir plus sur le club"
    },
    de: {
      nextgenPageTitle: "NEXTGEN | Mersch75 Handball",
      nextgenMetaDesc: "NEXTGEN von Mersch75: Unterstütze unsere Jugend mit einer Spende von 100 €.",
      nextgenEyebrow: "Unterstütze unsere Jugend",
      nextgenTitle: "NEXTGEN: Dein Name für unsere nächste Generation",
      nextgenIntro: "Mit NEXTGEN investieren wir in das, was Mersch75 stark macht: unsere Kinder, unsere Jugend und eine nachhaltige sportliche Zukunft.",
      nextgenContact: "Für Sponsoring und Partnerschaften kümmert sich Max Blanc (<a href=\"mailto:max.hbm75@gmail.com\">max.hbm75@gmail.com</a>) im Verein um NEXTGEN.",
      nextgenPanelName: "Dein Name auf dem Spielfeld",
      nextgenPanelDesc: "Mit <strong style=\"color:#f9d611;\">250 €</strong> wird dein Name auf einem großen Panel am Platz präsentiert – sichtbar bei jedem Match und jedem Training, die ganze Saison lang. Du wirst ein fester Bestandteil unserer Arena und hilfst direkt mit, dass unsere jungen Spieler das beste Material, die beste Ausbildung und Betreuung erhalten.",
      nextgenPanelSlogan: "Ein Feld. Ein Name. Eine große Unterstützung. 💛💙",
      nextgenDonation: "Jede Spende hilft uns, Material, Ausbildung, Jugendarbeit und Aktivitäten für unsere jungen Spieler weiter auszubauen.",
      nextgenCtaSupport: "Ich möchte NEXTGEN unterstützen",
      nextgenCtaClub: "Mehr über den Verein"
    },
    en: {
      nextgenPageTitle: "NEXTGEN | Mersch75 Handball",
      nextgenMetaDesc: "NEXTGEN by Mersch75: support our youth with a donation of €100.",
      nextgenEyebrow: "Support our youth",
      nextgenTitle: "NEXTGEN: Your name for our next generation",
      nextgenIntro: "With NEXTGEN we invest in what makes Mersch75 strong: our children, our youth and a sustainable sporting future.",
      nextgenContact: "For sponsoring and partnerships, Max Blanc (<a href=\"mailto:max.hbm75@gmail.com\">max.hbm75@gmail.com</a>) is responsible for NEXTGEN at the club.",
      nextgenPanelName: "Your name on the pitch",
      nextgenPanelDesc: "With <strong style=\"color:#f9d611;\">€250</strong>, your name is displayed on a large panel at the pitch – visible at every match and every training session, for the entire season. You become a permanent part of our arena and directly help our young players get the best equipment, training and support.",
      nextgenPanelSlogan: "One pitch. One name. One big support. 💛💙",
      nextgenDonation: "Every donation helps us to further develop equipment, training, youth work and activities for our young players.",
      nextgenCtaSupport: "I want to support NEXTGEN",
      nextgenCtaClub: "More about the club"
    },
    pt: {
      nextgenPageTitle: "NEXTGEN | Mersch75 Handball",
      nextgenMetaDesc: "NEXTGEN do Mersch75: apoia a nossa juventude com um donativo de 100 €.",
      nextgenEyebrow: "Apoia a nossa juventude",
      nextgenTitle: "NEXTGEN: O teu nome para a nossa próxima geração",
      nextgenIntro: "Com o NEXTGEN investimos no que torna o Mersch75 forte: as nossas crianças, a nossa juventude e um futuro desportivo sustentável.",
      nextgenContact: "Para patrocínios e parcerias, o Max Blanc (<a href=\"mailto:max.hbm75@gmail.com\">max.hbm75@gmail.com</a>) é o responsável pelo NEXTGEN no clube.",
      nextgenPanelName: "O teu nome no campo",
      nextgenPanelDesc: "Com <strong style=\"color:#f9d611;\">250 €</strong>, o teu nome é exibido num grande painel no campo – visível em todos os jogos e treinos, durante toda a época. Tornas-te uma parte fixa da nossa arena e ajudas diretamente os nossos jovens jogadores a obter o melhor material, formação e acompanhamento.",
      nextgenPanelSlogan: "Um campo. Um nome. Um grande apoio. 💛💙",
      nextgenDonation: "Cada donativo ajuda a desenvolver material, formação, trabalho com jovens e atividades para os nossos jovens jogadores.",
      nextgenCtaSupport: "Quero apoiar o NEXTGEN",
      nextgenCtaClub: "Saber mais sobre o clube"
    }
  };
  Object.keys(extra).forEach(function (lang) {
    if (window.translations[lang]) Object.assign(window.translations[lang], extra[lang]);
  });

  if (typeof window.Mersch75I18n !== 'undefined' && typeof window.Mersch75I18n.setLanguage === 'function') {
    window.Mersch75I18n.setLanguage(window.Mersch75I18n.getLanguage());
  }
})();
