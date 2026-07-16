(function () {
  if (typeof window.translations === 'undefined') return;
  var extra = {
    lb: {
      joinPageTitle: "Join Us | Mersch75 Handball",
      joinMetaDesc: "Matmaachen bei Mersch75: Umeldung, Training an éischt Kontaktpunkte fir nei Spiller a Familljen.",
      joinTarifTrigger: "Tariffer 2026-2027",
      joinTarifModalTitle: "Memberskaart &amp; Tariffer 2026-2027",
      joinTarifAdulte: "Adulte Tarif",
      joinTarifYouth: "Youth Tarif (≤ 25 ans)",
      joinTarifFamily: "Family Tarif",
      joinTarifOfficiels: "Officiels (mat/ouni Lizenz)",
      joinTarifOfficielsPrice: "Keng Cotisatioun · min. 50€ fir Stëmmrecht op der AG",
      joinTarifKids: "Kidssport &amp; Loisirs",
      joinTarifKidsPrice: "10 € pro Unité oder Family Tarif",
      joinMembersCards: "Memberskaarten",
      joinMembersCardHint: "D'Memberskaart mam QR-Code gëtt intern am Secretariat virbereet an eréischt no Bezuelung vum Membersbeitrag un den Antragsteller geschéckt.",
      joinWelcomeMapp: "📖 Wëllkomm-Mapp opmaachen"
    },
    fr: {
      joinPageTitle: "Join Us | Mersch75 Handball",
      joinMetaDesc: "Rejoindre Mersch75: inscription, entraînement et premiers contacts pour nouveaux joueurs et familles.",
      joinTarifTrigger: "Tarifs 2026-2027",
      joinTarifModalTitle: "Carte membre &amp; Tarifs 2026-2027",
      joinTarifAdulte: "Tarif Adulte",
      joinTarifYouth: "Tarif Jeune (≤ 25 ans)",
      joinTarifFamily: "Tarif Famille",
      joinTarifOfficiels: "Officiels (avec/sans licence)",
      joinTarifOfficielsPrice: "Pas de cotisation · min. 50€ pour droit de vote à l'AG",
      joinTarifKids: "Kidssport &amp; Loisirs",
      joinTarifKidsPrice: "10 € par unité ou Tarif Famille",
      joinMembersCards: "Cartes membre",
      joinMembersCardHint: "La carte membre avec QR-code est préparée en interne au secrétariat et envoyée après paiement de la cotisation.",
      joinWelcomeMapp: "📖 Ouvrir le pack de bienvenue"
    },
    de: {
      joinPageTitle: "Join Us | Mersch75 Handball",
      joinMetaDesc: "Mitmachen bei Mersch75: Anmeldung, Training und erste Kontaktpunkte für neue Spieler und Familien.",
      joinTarifTrigger: "Tarife 2026-2027",
      joinTarifModalTitle: "Mitgliederkarte &amp; Tarife 2026-2027",
      joinTarifAdulte: "Erwachsenen-Tarif",
      joinTarifYouth: "Jugend-Tarif (≤ 25 J.)",
      joinTarifFamily: "Familien-Tarif",
      joinTarifOfficiels: "Offizielle (mit/ohne Lizenz)",
      joinTarifOfficielsPrice: "Kein Beitrag · min. 50€ für Stimmrecht auf der GV",
      joinTarifKids: "Kidssport &amp; Loisirs",
      joinTarifKidsPrice: "10 € pro Einheit oder Familien-Tarif",
      joinMembersCards: "Mitgliederkarten",
      joinMembersCardHint: "Die Mitgliederkarte mit QR-Code wird intern im Sekretariat vorbereitet und erst nach Zahlung des Mitgliedsbeitrags an den Antragsteller geschickt.",
      joinWelcomeMapp: "📖 Willkommens-Mappe öffnen"
    },
    en: {
      joinPageTitle: "Join Us | Mersch75 Handball",
      joinMetaDesc: "Join Mersch75: registration, training and first contact points for new players and families.",
      joinTarifTrigger: "Fees 2026-2027",
      joinTarifModalTitle: "Membership card &amp; Fees 2026-2027",
      joinTarifAdulte: "Adult fee",
      joinTarifYouth: "Youth fee (≤ 25 yrs)",
      joinTarifFamily: "Family fee",
      joinTarifOfficiels: "Officials (with/without licence)",
      joinTarifOfficielsPrice: "No fee · min. 50€ for voting rights at the GA",
      joinTarifKids: "Kidssport &amp; Leisure",
      joinTarifKidsPrice: "10 € per session or Family fee",
      joinMembersCards: "Membership cards",
      joinMembersCardHint: "The membership card with QR code is prepared internally by the secretariat and sent to the applicant after payment of the membership fee.",
      joinWelcomeMapp: "📖 Open welcome pack"
    },
    pt: {
      joinPageTitle: "Join Us | Mersch75 Handball",
      joinMetaDesc: "Juntar-se ao Mersch75: inscrição, treino e primeiros contactos para novos jogadores e famílias.",
      joinTarifTrigger: "Quotas 2026-2027",
      joinTarifModalTitle: "Cartão de membro &amp; Quotas 2026-2027",
      joinTarifAdulte: "Quota Adulto",
      joinTarifYouth: "Quota Jovem (≤ 25 anos)",
      joinTarifFamily: "Quota Família",
      joinTarifOfficiels: "Oficiais (com/sem licença)",
      joinTarifOfficielsPrice: "Sem quota · min. 50€ para direito de voto na AG",
      joinTarifKids: "Kidssport &amp; Lazer",
      joinTarifKidsPrice: "10 € por sessão ou Quota Família",
      joinMembersCards: "Cartões de membro",
      joinMembersCardHint: "O cartão de membro com código QR é preparado internamente pela secretaria e enviado após o pagamento da quota.",
      joinWelcomeMapp: "📖 Abrir pack de boas-vindas"
    }
  };
  Object.keys(extra).forEach(function (lang) {
    if (window.translations[lang]) Object.assign(window.translations[lang], extra[lang]);
  });

  if (typeof window.Mersch75I18n !== 'undefined' && typeof window.Mersch75I18n.setLanguage === 'function') {
    window.Mersch75I18n.setLanguage(window.Mersch75I18n.getLanguage());
  }
})();
