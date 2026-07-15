(function () {
  if (typeof translations === 'undefined') return;
  const extra = {
    lb: {
      sponsorsPageTitle: "Sponsoren / Partner | Mersch75 Handball",
      sponsorsMetaDescription: "Sponsoren a Partner vu Mersch75 Handball: Firmen an Institutiounen, déi eise Veräin ënnerstëtzen. Gitt Partner!",
      sponsorsKicker: "Zesumme Staark",
      sponsorsHeroTitle: "Sponsoren & Partner",
      sponsorsHeroBody: "Mersch75 Handball lieft vum Engagement vu Firmen, Institutiounen a Partner, déi eise Veräin a seng Jugend ënnerstëtzen. Merci fir äre Support — Dir maacht den Handball zu Miersch méiglech.",
      sponsorsMainHeading: "Hauptsponsoren",
      sponsorsMainMeta: "Eis Haaptpartner, déi de Veräin laangfristeg begleeden.",
      sponsorsPartnerHeading: "Partner",
      sponsorsPartnerMeta: "Firmen a Servicer, déi eis bei Eventer an Aktioune ënnerstëtzen.",
      sponsorsEquipmentHeading: "Ausstatter & Institutiounen",
      sponsorsEquipmentMeta: "Equipementer, Gemeng a Federatioun.",
      sponsorsCtaTitle: "Gitt Partner vu Mersch75",
      sponsorsCtaBody: "Dir wëllt de Veräin ënnerstëtzen a gläichzäiteg är Firma sichtbar maachen — um Trikot, an der Hal an um Site? Mir fannen zesummen dat passend Partnerpaket.",
      sponsorsCtaContact: "Kontaktéiert eis",
      sponsorsCtaMore: "Méi iwwer de Veräin"
    },
    fr: {
      sponsorsPageTitle: "Sponsors / Partenaires | Mersch75 Handball",
      sponsorsMetaDescription: "Sponsors et partenaires du Mersch75 Handball : entreprises et institutions qui soutiennent notre club. Devenez partenaire !",
      sponsorsKicker: "Ensemble Forts",
      sponsorsHeroTitle: "Sponsors & Partenaires",
      sponsorsHeroBody: "Mersch75 Handball vit de l'engagement d'entreprises, d'institutions et de partenaires qui soutiennent notre club et sa jeunesse. Merci pour votre soutien — vous rendez le handball à Mersch possible.",
      sponsorsMainHeading: "Sponsors principaux",
      sponsorsMainMeta: "Nos partenaires principaux qui accompagnent le club à long terme.",
      sponsorsPartnerHeading: "Partenaires",
      sponsorsPartnerMeta: "Entreprises et services qui nous soutiennent lors d'événements et d'actions.",
      sponsorsEquipmentHeading: "Équipementiers & Institutions",
      sponsorsEquipmentMeta: "Équipementiers, commune et fédération.",
      sponsorsCtaTitle: "Devenez partenaire de Mersch75",
      sponsorsCtaBody: "Vous souhaitez soutenir le club et donner de la visibilité à votre entreprise — sur le maillot, dans la halle et sur le site ? Nous trouverons ensemble le package partenaire adapté.",
      sponsorsCtaContact: "Contactez-nous",
      sponsorsCtaMore: "En savoir plus sur le club"
    },
    de: {
      sponsorsPageTitle: "Sponsoren / Partner | Mersch75 Handball",
      sponsorsMetaDescription: "Sponsoren und Partner von Mersch75 Handball: Firmen und Institutionen, die unseren Verein unterstützen. Werden Sie Partner!",
      sponsorsKicker: "Gemeinsam Stark",
      sponsorsHeroTitle: "Sponsoren & Partner",
      sponsorsHeroBody: "Mersch75 Handball lebt vom Engagement von Firmen, Institutionen und Partnern, die unseren Verein und seine Jugend unterstützen. Danke für Ihre Unterstützung — Sie machen Handball in Mersch möglich.",
      sponsorsMainHeading: "Hauptsponsoren",
      sponsorsMainMeta: "Unsere Hauptpartner, die den Verein langfristig begleiten.",
      sponsorsPartnerHeading: "Partner",
      sponsorsPartnerMeta: "Firmen und Services, die uns bei Events und Aktionen unterstützen.",
      sponsorsEquipmentHeading: "Ausrüster & Institutionen",
      sponsorsEquipmentMeta: "Ausrüster, Gemeinde und Verband.",
      sponsorsCtaTitle: "Werden Sie Partner von Mersch75",
      sponsorsCtaBody: "Sie möchten den Verein unterstützen und gleichzeitig Ihr Unternehmen sichtbar machen — am Trikot, in der Halle und auf der Website? Gemeinsam finden wir das passende Partnerpaket.",
      sponsorsCtaContact: "Kontaktieren Sie uns",
      sponsorsCtaMore: "Mehr über den Verein"
    },
    en: {
      sponsorsPageTitle: "Sponsors / Partners | Mersch75 Handball",
      sponsorsMetaDescription: "Sponsors and partners of Mersch75 Handball: companies and institutions supporting our club. Become a partner!",
      sponsorsKicker: "Strong Together",
      sponsorsHeroTitle: "Sponsors & Partners",
      sponsorsHeroBody: "Mersch75 Handball relies on the commitment of companies, institutions and partners that support our club and its youth. Thank you for your support — you make handball in Mersch possible.",
      sponsorsMainHeading: "Main Sponsors",
      sponsorsMainMeta: "Our main partners supporting the club in the long run.",
      sponsorsPartnerHeading: "Partners",
      sponsorsPartnerMeta: "Companies and services that support us at events and activities.",
      sponsorsEquipmentHeading: "Suppliers & Institutions",
      sponsorsEquipmentMeta: "Equipment suppliers, municipality and federation.",
      sponsorsCtaTitle: "Become a Mersch75 Partner",
      sponsorsCtaBody: "Do you want to support the club and make your company visible — on the jersey, in the hall and on the website? Together we will find the right partner package.",
      sponsorsCtaContact: "Contact us",
      sponsorsCtaMore: "More about the club"
    },
    pt: {
      sponsorsPageTitle: "Patrocinadores / Parceiros | Mersch75 Handball",
      sponsorsMetaDescription: "Patrocinadores e parceiros do Mersch75 Handball: empresas e instituições que apoiam o nosso clube. Torne-se parceiro!",
      sponsorsKicker: "Juntos Somos Mais Fortes",
      sponsorsHeroTitle: "Patrocinadores & Parceiros",
      sponsorsHeroBody: "O Mersch75 Handball vive do empenho de empresas, instituições e parceiros que apoiam o nosso clube e a sua juventude. Obrigado pelo vosso apoio — vocês fazem o andebol em Mersch possível.",
      sponsorsMainHeading: "Patrocinadores principais",
      sponsorsMainMeta: "Os nossos parceiros principais que acompanham o clube a longo prazo.",
      sponsorsPartnerHeading: "Parceiros",
      sponsorsPartnerMeta: "Empresas e serviços que nos apoiam em eventos e atividades.",
      sponsorsEquipmentHeading: "Fornecedores & Instituições",
      sponsorsEquipmentMeta: "Fornecedores de equipamento, município e federação.",
      sponsorsCtaTitle: "Torne-se parceiro do Mersch75",
      sponsorsCtaBody: "Quer apoiar o clube e dar visibilidade à sua empresa — no equipamento, no pavilhão e no site? Juntos encontramos o pacote de parceria adequado.",
      sponsorsCtaContact: "Contacte-nos",
      sponsorsCtaMore: "Mais sobre o clube"
    }
  };
  Object.keys(extra).forEach(function (lang) {
    if (translations[lang]) Object.assign(translations[lang], extra[lang]);
  });
})();
