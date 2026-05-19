<?php
if (!defined('ABSPATH')) {
	exit;
}

function mersch75_join_us_shortcode() {
	ob_start();
	?>
	<div class="mersch75-join-us">
		<style>
			.mersch75-join-us {
				--mersch75-blue: #005f8e;
				--mersch75-blue-dark: #003d6b;
				--mersch75-blue-soft: #edf6fb;
				--mersch75-border: #d4e7f2;
				--mersch75-text: #20313f;
				--mersch75-muted: #607383;
				max-width: 980px;
				margin: 0 auto;
				font-family: Outfit, "Segoe UI", sans-serif;
				color: var(--mersch75-text);
			}

			.mersch75-join-card {
				background: linear-gradient(180deg, #ffffff 0%, #f8fbfd 100%);
				border: 1px solid var(--mersch75-border);
				border-radius: 24px;
				box-shadow: 0 28px 64px rgba(0, 61, 107, 0.12);
				overflow: hidden;
			}

			.mersch75-join-card-header {
				padding: 28px 30px 18px;
				background: radial-gradient(circle at top right, rgba(0, 115, 170, 0.16), transparent 44%), linear-gradient(135deg, #ffffff, #f1f8fc);
				border-bottom: 1px solid var(--mersch75-border);
			}

			.mersch75-join-card-header h2 {
				margin: 0;
				font-size: 30px;
				line-height: 1.05;
				color: var(--mersch75-blue-dark);
			}

			.mersch75-join-card-header p {
				margin: 10px 0 0;
				color: var(--mersch75-muted);
				font-size: 15px;
				line-height: 1.6;
			}

			.mersch75-join-form {
				padding: 28px 30px 30px;
			}

			.mersch75-language-switcher {
				display: flex;
				justify-content: center;
				gap: 10px;
				flex-wrap: wrap;
				margin: 0 0 24px;
				padding: 12px;
				border: 1px solid var(--mersch75-border);
				border-radius: 18px;
				background: #ffffff;
			}

			.mersch75-language-switcher button {
				min-width: 92px;
				min-height: 44px;
				padding: 8px 12px;
				border: 1.5px solid var(--mersch75-border);
				border-radius: 14px;
				background: #ffffff;
				color: var(--mersch75-blue-dark);
				font-size: 14px;
				font-weight: 800;
				line-height: 1.2;
				text-align: center;
				white-space: nowrap;
				cursor: pointer;
				transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
			}

			.mersch75-language-switcher button:hover,
			.mersch75-language-switcher button.is-active {
				border-color: var(--mersch75-blue);
				box-shadow: 0 0 0 4px rgba(0, 115, 170, 0.12);
				transform: translateY(-1px);
			}

			.mersch75-join-grid {
				display: grid;
				grid-template-columns: minmax(0, 1fr);
				gap: 18px;
			}

			.mersch75-join-row {
				display: grid;
				grid-template-columns: repeat(2, minmax(0, 1fr));
				gap: 16px;
			}

			.mersch75-join-group {
				display: flex;
				flex-direction: column;
				gap: 7px;
			}

			.mersch75-join-group label,
			.mersch75-join-meta label,
			#u7-section label {
				font-size: 12px;
				font-weight: 800;
				letter-spacing: 0.08em;
				text-transform: uppercase;
				color: var(--mersch75-blue-dark);
			}

			.mersch75-join-form input[type="text"],
			.mersch75-join-form input[type="email"],
			.mersch75-join-form select {
				width: 100%;
				min-height: 50px;
				padding: 13px 15px;
				border: 1.5px solid var(--mersch75-border);
				border-radius: 14px;
				background: #ffffff;
				color: var(--mersch75-text);
				font-size: 15px;
				line-height: 1.35;
				box-sizing: border-box;
				transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease;
			}

			.mersch75-join-form input:focus,
			.mersch75-join-form select:focus {
				outline: none;
				border-color: var(--mersch75-blue);
				box-shadow: 0 0 0 4px rgba(0, 115, 170, 0.12);
				transform: translateY(-1px);
			}

			.mersch75-join-form select[disabled] {
				color: #6f8493;
				background: #f3f7fa;
			}

			.mersch75-join-meta,
			#parent-section,
			#u7-section {
				padding: 18px;
				border: 1px solid var(--mersch75-border);
				border-radius: 18px;
				background: var(--mersch75-blue-soft);
			}

			.mersch75-join-meta {
				display: grid;
				gap: 8px;
			}

			#cat-display {
				font-size: 22px;
				font-weight: 800;
				color: var(--mersch75-blue-dark);
			}

			#parent-section,
			#u7-section {
				display: none;
			}

			#u7-section {
				gap: 12px;
				align-items: flex-start;
			}

			#u7-section input {
				margin-top: 3px;
			}

			#cns-prefix-display {
				font-size: 13px;
				color: var(--mersch75-muted);
			}

			.mersch75-join-submit {
				margin-top: 8px;
			}

			.mersch75-join-legal {
				display: flex;
				gap: 12px;
				align-items: flex-start;
				padding: 16px 18px;
				border: 1px solid var(--mersch75-border);
				border-radius: 18px;
				background: #ffffff;
				color: var(--mersch75-muted);
				font-size: 13px;
				line-height: 1.55;
			}

			.mersch75-join-legal.is-info {
				background: linear-gradient(180deg, #fff9d8 0%, #f8fbfd 100%);
			}

			.mersch75-join-legal input {
				margin-top: 3px;
				flex: 0 0 auto;
			}

			.mersch75-join-legal a {
				color: var(--mersch75-blue);
				font-weight: 800;
				text-decoration: none;
			}

			.mersch75-join-legal a:hover {
				text-decoration: underline;
			}

			#submitBtn {
				width: 100%;
				min-height: 56px;
				border: 0;
				border-radius: 16px;
				background: linear-gradient(135deg, var(--mersch75-blue) 0%, var(--mersch75-blue-dark) 100%);
				color: #ffffff;
				font-size: 15px;
				font-weight: 800;
				letter-spacing: 0.08em;
				text-transform: uppercase;
				cursor: pointer;
				box-shadow: 0 16px 32px rgba(0, 95, 142, 0.22);
				transition: transform 0.2s ease, box-shadow 0.2s ease, opacity 0.2s ease;
			}

			#submitBtn:hover {
				transform: translateY(-1px);
				box-shadow: 0 18px 34px rgba(0, 95, 142, 0.28);
			}

			#submitBtn:disabled {
				opacity: 0.75;
				cursor: not-allowed;
				transform: none;
			}

			#success-box {
				display: none;
				margin: 24px 30px 30px;
				padding: 20px 22px;
				border-radius: 18px;
				border: 1px solid #b7dec2;
				background: #edf9f1;
				color: #20592f;
				font-size: 15px;
				font-weight: 600;
			}

			@media (max-width: 720px) {
				.mersch75-join-card-header,
				.mersch75-join-form {
					padding-left: 18px;
					padding-right: 18px;
				}

				.mersch75-join-row {
					grid-template-columns: minmax(0, 1fr);
				}

				#success-box {
					margin-left: 18px;
					margin-right: 18px;
				}
			}
		</style>

		<div class="mersch75-join-card">
			<div class="mersch75-join-card-header">
				<h2>Join Us</h2>
				<p data-ui-key="intro">Interne Voranmeldung für neue Spielerinnen, Spieler und Offizielle bei Mersch75.</p>
			</div>

			<form id="registrationForm" class="join-registration-form mersch75-join-form" action="https://api.web3forms.com/submit" method="POST" novalidate>
				<input type="hidden" name="access_key" value="15e3cc53-6864-47dd-bfaf-332cb4ca45e5">
				<input type="hidden" name="subject" value="Nouvelle inscription Mersch 75">
				<input type="hidden" name="from_name" value="Mersch75 E-JOIN-US">
				<input type="hidden" id="Langue" name="Langue" value="lu">
				<input type="hidden" id="name" name="name" value="">
				<input type="hidden" id="email" name="email" value="">
				<div hidden aria-hidden="true">
					<input type="text" id="honeypot" name="website" autocomplete="off" tabindex="-1">
				</div>

				<div class="mersch75-language-switcher" aria-label="Language selection">
					<button type="button" data-language-button="lu" title="Lëtzebuergesch">&#x1F1F1;&#x1F1FA; Lux</button>
					<button type="button" data-language-button="fr" title="Français">&#x1F1EB;&#x1F1F7; FR</button>
					<button type="button" data-language-button="de" title="Deutsch">&#x1F1E9;&#x1F1EA; D</button>
					<button type="button" data-language-button="en" title="English">&#x1F1EC;&#x1F1E7; EN</button>
					<button type="button" data-language-button="pt" title="Português">&#x1F1F5;&#x1F1F9; PT</button>
				</div>

				<div class="mersch75-join-grid">
					<div class="mersch75-join-group">
						<label for="Nom" data-ui-key="lastName">Nom *</label>
						<input type="text" id="Nom" name="Nom" required>
					</div>

					<div class="mersch75-join-group">
						<label for="Prenom" data-ui-key="firstName">Prenom *</label>
						<input type="text" id="Prenom" name="Prenom" required>
					</div>

					<div class="mersch75-join-row">
						<div class="mersch75-join-group">
							<label for="DateNaissance" data-ui-key="birthDate">Date de naissance *</label>
							<input type="text" id="DateNaissance" name="DateNaissance" placeholder="01.01.2010" pattern="[0-9]{2}\.[0-9]{2}\.[0-9]{4}" required>
						</div>

						<div class="mersch75-join-group">
							<label for="Mineur" data-ui-key="minor">Mineur</label>
							<select id="Mineur" disabled>
								<option value="NON" data-ui-key="no">NON</option>
								<option value="OUI" data-ui-key="yes">OUI</option>
							</select>
						</div>
					</div>

					<div id="cat-section" class="mersch75-join-meta">
						<label for="Categorie" data-ui-key="category">Categorie FLH</label>
						<strong id="cat-display">-</strong>
						<input type="hidden" id="Categorie" name="Categorie" value="">
					</div>

					<div class="mersch75-join-group">
						<label for="Role" data-ui-key="role">Role / Funktion *</label>
						<select id="Role" name="Role" required>
							<option value="Joueur / Joueuse" data-ui-key="player">Joueur / Joueuse</option>
							<option value="Officiel(le)" data-ui-key="official">Officiel(le)</option>
							<option value="Arbitre" data-ui-key="referee">Arbitre</option>
						</select>
					</div>

					<div id="parent-section">
						<div class="mersch75-join-grid">
							<div class="mersch75-join-group">
								<label for="ParentIsole" data-ui-key="singleParent">Parent isole *</label>
								<select id="ParentIsole" name="ParentIsole">
									<option value="NON" data-ui-key="twoGuardians">NON (2 Tuteurs)</option>
									<option value="OUI" data-ui-key="oneGuardian">OUI (1 Tuteur)</option>
								</select>
							</div>

							<div class="mersch75-join-row">
								<div class="mersch75-join-group">
									<label for="Tuteur1" data-ui-key="guardianOne">Tuteur 1 *</label>
									<input type="text" id="Tuteur1" name="Tuteur1">
								</div>

								<div class="mersch75-join-group" id="tuteur2-wrap">
									<label for="Tuteur2" data-ui-key="guardianTwo">Tuteur 2 *</label>
									<input type="text" id="Tuteur2" name="Tuteur2">
								</div>
							</div>
						</div>
					</div>

					<div class="mersch75-join-group">
						<label for="Nationalite" data-ui-key="nationality">Nationalite *</label>
						<input type="text" id="Nationalite" name="Nationalite" required>
					</div>

					<div class="mersch75-join-group">
						<label for="CNS" data-ui-key="cns">Matricule CNS *</label>
						<input type="text" id="CNS" name="CNS" maxlength="5" pattern="[0-9]{5}" required>
						<span id="cns-prefix-display"></span>
					</div>

					<div class="mersch75-join-row">
						<div class="mersch75-join-group">
							<label for="Medico" data-ui-key="medico">Medico *</label>
							<select id="Medico" name="Medico" required>
								<option value="Non" data-ui-key="no">Non</option>
								<option value="Oui" data-ui-key="yes">Oui</option>
							</select>
						</div>

						<div class="mersch75-join-group">
							<label for="Licence" data-ui-key="license">Licence *</label>
							<select id="Licence" name="Licence" required>
								<option value="Non" data-ui-key="no">Non</option>
								<option value="Oui" data-ui-key="yes">Oui</option>
							</select>
						</div>
					</div>

					<div class="mersch75-join-group">
						<label for="AncienClub" data-ui-key="formerClub">Ancien club *</label>
						<input type="text" id="AncienClub" name="AncienClub" required>
					</div>

					<div id="u7-section">
						<input type="checkbox" id="U7Cert" name="U7Cert" value="Oui">
						<label for="U7Cert" data-ui-key="u7Cert">U7 certificat medical obligatoire</label>
					</div>

					<div class="mersch75-join-group">
						<label for="Adresse" data-ui-key="address">Adresse *</label>
						<input type="text" id="Adresse" name="Adresse" required>
					</div>

					<div class="mersch75-join-group">
						<label for="Email" data-ui-key="emailLabel">Email *</label>
						<input type="email" id="Email" name="Email" required>
					</div>

					<div class="mersch75-join-row">
						<div class="mersch75-join-group">
							<label for="GSM1" data-ui-key="gsmOne">GSM 1 *</label>
							<input type="text" id="GSM1" name="GSM1" required>
						</div>

						<div class="mersch75-join-group">
							<label for="GSM2" data-ui-key="gsmTwo">GSM 2</label>
							<input type="text" id="GSM2" name="GSM2">
						</div>
					</div>

					<label class="mersch75-join-legal" for="LegalConsent">
						<input type="checkbox" id="LegalConsent" name="LegalConsent" value="Oui" required>
						<span>
							<span data-legal-key="legalPrefix">Ech hu gelies an akzeptéieren d' </span><a href="<?php echo esc_url(site_url('/x2-terms-and-conditions/')); ?>" target="_blank" rel="noopener noreferrer" data-legal-key="termsLink">Allgemeng Bedéngungen</a><span data-legal-key="legalMiddle"> an Reglementatioun iwwert den </span><a href="<?php echo esc_url(site_url('/datenschutzerklaerung/')); ?>" target="_blank" rel="noopener noreferrer" data-legal-key="dataLink">Dateschutz</a><span data-legal-key="sentenceEnd">.</span>
						</span>
					</label>

					<label class="mersch75-join-legal is-info" for="FlhPortalConsent">
						<input type="checkbox" id="FlhPortalConsent" name="FlhPortalConsent" value="Oui" required>
						<span data-legal-key="flhInfo">Info: Ech hu verstaan dat meng Umeldung mat dësen Daten un d' flh.lu geschéckt ginn fir eng Lizenz auszestellen.</span>
					</label>

					<label class="mersch75-join-legal" for="AccuracyConsent">
						<input type="checkbox" id="AccuracyConsent" name="AccuracyConsent" value="Oui" required>
						<span data-legal-key="accuracy">Bestätegung: Ech confirméiere d'Richtegkeet vun menge Donnéeën.</span>
					</label>

					<div class="mersch75-join-submit">
						<button type="submit" id="submitBtn" data-ui-key="send">Envoyer</button>
					</div>
				</div>
			</form>

			<div id="success-box" data-ui-key="success">Inscription envoyee.</div>
		</div>
	</div>

	<script>
	const MERSCH75_WEB3FORMS_MAIN_KEY = '15e3cc53-6864-47dd-bfaf-332cb4ca45e5';
	const MERSCH75_WEB3FORMS_MAX_KEY = 'f748489b-abc6-4e37-bb82-860a82c91f4e';
	const MERSCH75_LICENSE_LINK = 'https://submit.paperless.io/f/s4zaWnzHBwxcPK8jAkkbjPpVC1giUfr7';
	const MERSCH75_LICENSE_PASSWORD = 'FIhNvLi26';
	const MERSCH75_UI_TEXTS = {
		lu: {
			intro: 'Intern Virumeldung fir nei Spillerinnen, Spiller an Offizieller bei Mersch75.',
			lastName: 'Numm *',
			firstName: 'Virnumm *',
			birthDate: 'Gebuertsdatum *',
			minor: 'Mannerjäreg',
			no: 'NEE',
			yes: 'JO',
			category: 'FLH Kategorie',
			role: 'Roll / Funktioun *',
			player: 'Spiller / Spillerin',
			official: 'Offiziell Persoun',
			referee: 'Arbitter',
			singleParent: 'Elengerzéiend *',
			twoGuardians: 'NEE (2 Erzéiungsberechtegter)',
			oneGuardian: 'JO (1 Erzéiungsberechtegten)',
			guardianOne: 'Erzéiungsberechtegten 1 *',
			guardianTwo: 'Erzéiungsberechtegten 2 *',
			nationality: 'Nationalitéit *',
			cns: 'Matricule CNS *',
			medico: 'Medico *',
			license: 'Lizenz *',
			formerClub: 'Ale Veräin *',
			u7Cert: 'U7 medezineschen Zertifikat obligatoresch',
			address: 'Adress *',
			emailLabel: 'E-Mail *',
			gsmOne: 'GSM 1 *',
			gsmTwo: 'GSM 2',
			send: 'Schécken',
			sending: 'Gëtt geschéckt...',
			success: 'Umeldung geschéckt.',
			legalRequired: 'Liest an akzeptéiert w.e.g. déi allgemeng Bedéngungen an den Dateschutz.',
			flhRequired: 'Bestätegt w.e.g. d\'Iwwermëttlung un flh.lu fir d\'Lizenz.',
			accuracyRequired: 'Bestätegt w.e.g. d\'Richtegkeet vun den Donnéeën.'
		},
		fr: {
			intro: 'Préinscription interne pour nouvelles joueuses, nouveaux joueurs et officiels chez Mersch75.',
			lastName: 'Nom *',
			firstName: 'Prénom *',
			birthDate: 'Date de naissance *',
			minor: 'Mineur',
			no: 'NON',
			yes: 'OUI',
			category: 'Catégorie FLH',
			role: 'Rôle / Fonction *',
			player: 'Joueur / Joueuse',
			official: 'Officiel(le)',
			referee: 'Arbitre',
			singleParent: 'Parent isolé *',
			twoGuardians: 'NON (2 tuteurs)',
			oneGuardian: 'OUI (1 tuteur)',
			guardianOne: 'Tuteur 1 *',
			guardianTwo: 'Tuteur 2 *',
			nationality: 'Nationalité *',
			cns: 'Matricule CNS *',
			medico: 'Médico *',
			license: 'Licence *',
			formerClub: 'Ancien club *',
			u7Cert: 'U7 certificat médical obligatoire',
			address: 'Adresse *',
			emailLabel: 'E-mail *',
			gsmOne: 'GSM 1 *',
			gsmTwo: 'GSM 2',
			send: 'Envoyer',
			sending: 'Envoi...',
			success: 'Inscription envoyée.',
			legalRequired: 'Veuillez lire et accepter les conditions générales et la protection des données.',
			flhRequired: 'Veuillez confirmer la transmission à flh.lu pour la licence.',
			accuracyRequired: 'Veuillez confirmer l\'exactitude des données.'
		},
		de: {
			intro: 'Interne Voranmeldung für neue Spielerinnen, Spieler und Offizielle bei Mersch75.',
			lastName: 'Name *',
			firstName: 'Vorname *',
			birthDate: 'Geburtsdatum *',
			minor: 'Minderjährig',
			no: 'NEIN',
			yes: 'JA',
			category: 'FLH Kategorie',
			role: 'Rolle / Funktion *',
			player: 'Spieler / Spielerin',
			official: 'Offizielle Person',
			referee: 'Schiedsrichter',
			singleParent: 'Alleinerziehend *',
			twoGuardians: 'NEIN (2 Erziehungsberechtigte)',
			oneGuardian: 'JA (1 Erziehungsberechtigter)',
			guardianOne: 'Erziehungsberechtigter 1 *',
			guardianTwo: 'Erziehungsberechtigter 2 *',
			nationality: 'Nationalität *',
			cns: 'CNS-Matrikelnummer *',
			medico: 'Medico *',
			license: 'Lizenz *',
			formerClub: 'Ehemaliger Verein *',
			u7Cert: 'U7 ärztliches Attest obligatorisch',
			address: 'Adresse *',
			emailLabel: 'E-Mail *',
			gsmOne: 'GSM 1 *',
			gsmTwo: 'GSM 2',
			send: 'Senden',
			sending: 'Senden...',
			success: 'Anmeldung gesendet.',
			legalRequired: 'Bitte die allgemeinen Bedingungen und den Datenschutz lesen und akzeptieren.',
			flhRequired: 'Bitte die Übermittlung an flh.lu für die Lizenz bestätigen.',
			accuracyRequired: 'Bitte die Richtigkeit der Angaben bestätigen.'
		},
		en: {
			intro: 'Internal pre-registration for new players and officials at Mersch75.',
			lastName: 'Last name *',
			firstName: 'First name *',
			birthDate: 'Date of birth *',
			minor: 'Minor',
			no: 'NO',
			yes: 'YES',
			category: 'FLH category',
			role: 'Role / Function *',
			player: 'Player',
			official: 'Official',
			referee: 'Referee',
			singleParent: 'Single parent *',
			twoGuardians: 'NO (2 guardians)',
			oneGuardian: 'YES (1 guardian)',
			guardianOne: 'Guardian 1 *',
			guardianTwo: 'Guardian 2 *',
			nationality: 'Nationality *',
			cns: 'CNS number *',
			medico: 'Medical check *',
			license: 'Licence *',
			formerClub: 'Former club *',
			u7Cert: 'U7 medical certificate required',
			address: 'Address *',
			emailLabel: 'Email *',
			gsmOne: 'Mobile 1 *',
			gsmTwo: 'Mobile 2',
			send: 'Submit',
			sending: 'Sending...',
			success: 'Registration sent.',
			legalRequired: 'Please read and accept the terms and conditions and data protection.',
			flhRequired: 'Please confirm the transfer to flh.lu for the licence.',
			accuracyRequired: 'Please confirm the accuracy of the data.'
		},
		pt: {
			intro: 'Pré-inscrição interna para novas jogadoras, jogadores e oficiais no Mersch75.',
			lastName: 'Apelido *',
			firstName: 'Nome próprio *',
			birthDate: 'Data de nascimento *',
			minor: 'Menor',
			no: 'NÃO',
			yes: 'SIM',
			category: 'Categoria FLH',
			role: 'Função *',
			player: 'Jogador / Jogadora',
			official: 'Oficial',
			referee: 'Árbitro',
			singleParent: 'Encarregado isolado *',
			twoGuardians: 'NÃO (2 encarregados)',
			oneGuardian: 'SIM (1 encarregado)',
			guardianOne: 'Encarregado 1 *',
			guardianTwo: 'Encarregado 2 *',
			nationality: 'Nacionalidade *',
			cns: 'Número CNS *',
			medico: 'Exame médico *',
			license: 'Licença *',
			formerClub: 'Clube anterior *',
			u7Cert: 'U7 certificado médico obrigatório',
			address: 'Morada *',
			emailLabel: 'E-mail *',
			gsmOne: 'Telemóvel 1 *',
			gsmTwo: 'Telemóvel 2',
			send: 'Enviar',
			sending: 'A enviar...',
			success: 'Inscrição enviada.',
			legalRequired: 'Por favor, leia e aceite os termos e condições e a proteção de dados.',
			flhRequired: 'Por favor, confirme o envio para flh.lu para a licença.',
			accuracyRequired: 'Por favor, confirme a exatidão dos dados.'
		}
	};
	const MERSCH75_LEGAL_TEXTS = {
		lu: {
			legalPrefix: "Ech hu gelies an akzeptéieren d' ",
			termsLink: 'Allgemeng Bedéngungen',
			legalMiddle: ' an Reglementatioun iwwert den ',
			dataLink: 'Dateschutz',
			flhInfo: "Info: Ech hu verstaan dat meng Umeldung mat dësen Daten un d' flh.lu geschéckt ginn fir eng Lizenz auszestellen.",
			accuracy: "Bestätegung: Ech confirméiere d'Richtegkeet vun menge Donnéeën.",
			sentenceEnd: '.'
		},
		de: {
			legalPrefix: 'Ich habe die ',
			termsLink: 'Allgemeinen Bedingungen',
			legalMiddle: ' und die Regelung zum ',
			dataLink: 'Datenschutz',
			flhInfo: 'Info: Ich habe verstanden, dass meine Anmeldung mit diesen Daten an flh.lu gesendet wird, um eine Lizenz auszustellen.',
			accuracy: 'Bestätigung: Ich bestätige die Richtigkeit meiner Angaben.',
			sentenceEnd: ' gelesen und akzeptiert.'
		},
		fr: {
			legalPrefix: "J'ai lu et j'accepte les ",
			termsLink: 'conditions générales',
			legalMiddle: ' et le règlement relatif à la ',
			dataLink: 'protection des données',
			flhInfo: "Info: J'ai compris que mon inscription sera envoyée avec ces données à flh.lu afin d'établir une licence.",
			accuracy: "Confirmation: je confirme l'exactitude de mes données.",
			sentenceEnd: '.'
		},
		en: {
			legalPrefix: 'I have read and accept the ',
			termsLink: 'terms and conditions',
			legalMiddle: ' and the regulation concerning ',
			dataLink: 'data protection',
			flhInfo: 'Info: I understand that my registration will be sent with this data to flh.lu in order to issue a licence.',
			accuracy: 'Confirmation: I confirm the accuracy of my information.',
			sentenceEnd: '.'
		},
		pt: {
			legalPrefix: 'Li e aceito os ',
			termsLink: 'termos e condições gerais',
			legalMiddle: ' e o regulamento relativo à ',
			dataLink: 'proteção de dados',
			flhInfo: 'Info: Compreendi que a minha inscrição será enviada com estes dados para flh.lu para emitir uma licença.',
			accuracy: 'Confirmação: confirmo a exatidão dos meus dados.',
			sentenceEnd: '.'
		}
	};

	function detectLegalLanguage(form) {
		const languageField = form ? form.querySelector('[name="Langue"]') : document.getElementById('Langue');
		const language = languageField ? languageField.value : 'lu';

		if (language === 'lb') {
			return 'lu';
		}

		return MERSCH75_LEGAL_TEXTS[language] ? language : 'lu';
	}

	function applyLegalLanguage(form) {
		form = form || document.getElementById('registrationForm');
		const language = detectLegalLanguage(form);
		const labels = MERSCH75_LEGAL_TEXTS[language];
		const uiLabels = MERSCH75_UI_TEXTS[language];
		const languageField = form ? form.querySelector('[name="Langue"]') : document.getElementById('Langue');

		if (languageField) {
			languageField.value = language;
		}

		form.querySelectorAll('[data-legal-key]').forEach(function(element) {
			const key = element.getAttribute('data-legal-key');

			if (labels[key]) {
				element.innerText = labels[key];
			}
		});

		document.querySelectorAll('[data-ui-key]').forEach(function(element) {
			const key = element.getAttribute('data-ui-key');

			if (uiLabels[key]) {
				element.innerText = uiLabels[key];
			}
		});

		form.querySelectorAll('[data-language-button]').forEach(function(button) {
			button.classList.toggle('is-active', button.getAttribute('data-language-button') === language);
		});
	}

	function setLegalLanguage(language, form) {
		form = form || document.getElementById('registrationForm');
		const languageField = form ? form.querySelector('[name="Langue"]') : document.getElementById('Langue');

		if (language === 'lb') {
			language = 'lu';
		}

		if (!MERSCH75_LEGAL_TEXTS[language]) {
			language = 'lu';
		}

		if (languageField) {
			languageField.value = language;
		}

		applyLegalLanguage(form);
	}

	function updateConsentValidationMessages(form) {
		form = form || document.getElementById('registrationForm');
		const language = detectLegalLanguage(form);
		const uiLabels = MERSCH75_UI_TEXTS[language];
		const validationMessages = {
			LegalConsent: uiLabels.legalRequired,
			FlhPortalConsent: uiLabels.flhRequired,
			AccuracyConsent: uiLabels.accuracyRequired
		};

		Object.keys(validationMessages).forEach(function(id) {
			const checkbox = form.querySelector('#' + id);

			if (!checkbox) {
				return;
			}

			checkbox.setCustomValidity(checkbox.checked ? '' : validationMessages[id]);
		});
	}

	function initLanguageSwitcher() {
		document.addEventListener('click', function(event) {
			const button = event.target.closest('[data-language-button]');

			if (!button) {
				return;
			}

			const form = button.closest('form');

			if (!form) {
				return;
			}

			event.preventDefault();
			setLegalLanguage(button.getAttribute('data-language-button'), form);
			updateConsentValidationMessages(form);
		});
	}

	function initConsentValidation() {
		document.querySelectorAll('.join-registration-form').forEach(function(form) {
			updateConsentValidationMessages(form);

			['LegalConsent', 'FlhPortalConsent', 'AccuracyConsent'].forEach(function(id) {
				const checkbox = form.querySelector('#' + id);

				if (!checkbox) {
					return;
				}

				checkbox.addEventListener('change', function() {
					updateConsentValidationMessages(form);
				});
			});
		});
	}

	function getValue(id) {
		return document.getElementById(id).value.trim();
	}

	function getCheckedValue(id) {
		return document.getElementById(id).checked ? 'Oui' : 'Non';
	}

	function getFullName() {
		return (getValue('Nom') + ' ' + getValue('Prenom')).trim();
	}

	function getCategoryValue() {
		return document.getElementById('Categorie').value || document.getElementById('cat-display').innerText;
	}

	function getCnsComplete() {
		const dob = getValue('DateNaissance');
		const cnsManual = getValue('CNS');

		if (dob.length !== 10) {
			return '';
		}

		const parts = dob.split('.');
		return parts[2] + '.' + parts[1] + '.' + parts[0] + '.' + cnsManual;
	}

	function getGuardianText() {
		const guardianOne = getValue('Tuteur1');
		const guardianTwo = document.getElementById('ParentIsole').value === 'OUI' ? '' : getValue('Tuteur2');
		const guardians = [guardianOne, guardianTwo].filter(Boolean).join(' / ');
		return guardians || '-';
	}

	function setRequiredState(isMinor, category) {
		const tuteur1 = document.getElementById('Tuteur1');
		const tuteur2 = document.getElementById('Tuteur2');
		const parentIsole = document.getElementById('ParentIsole');
		const u7Cert = document.getElementById('U7Cert');

		tuteur1.required = isMinor;
		tuteur2.required = isMinor && parentIsole.value !== 'OUI';
		u7Cert.required = category === 'U7';

		document.getElementById('parent-section').style.display = isMinor ? 'block' : 'none';
		document.getElementById('u7-section').style.display = category === 'U7' ? 'block' : 'none';
		document.getElementById('tuteur2-wrap').style.display = parentIsole.value === 'OUI' ? 'none' : 'block';

		if (!isMinor) {
			tuteur1.value = '';
			tuteur2.value = '';
			parentIsole.value = 'NON';
		}

		if (parentIsole.value === 'OUI') {
			tuteur2.value = '';
		}
	}

	function updateCnsDisplay() {
		const dob = document.getElementById('DateNaissance').value;
		const cns = document.getElementById('CNS').value.trim();

		if (dob.length === 10) {
			const parts = dob.split('.');
			const formattedDob = parts[2] + '.' + parts[1] + '.' + parts[0];
			document.getElementById('cns-prefix-display').innerText = 'Format CNS: ' + formattedDob + '.' + (cns !== '' ? cns : 'xxxxx');
		} else {
			document.getElementById('cns-prefix-display').innerText = 'Format CNS: yyyy.mm.dd.xxxxx';
		}
	}

	function buildJoinMessage(includeLicenseLines, messageLanguage) {
		const lines = [];
		const isFrenchMessage = messageLanguage === 'fr';
		const text = isFrenchMessage ? {
			licenseLink: 'LIEN LICENCE',
			password: 'MOT DE PASSE',
			applicant: 'DEMANDEUR',
			role: 'ROLE / FONCTION',
			category: 'CATEGORIE FLH',
			cnsDigits: 'CNS (5 chiffres)',
			birthDate: 'DATE DE NAISSANCE',
			email: 'E-MAIL',
			address: 'ADRESSE',
			minor: 'MINEUR',
			singleParent: 'PARENT ISOLE',
			guardians: 'TUTEUR(S)',
			club: 'ANCIEN CLUB',
			medLicense: 'MED/LIC',
			nationality: 'NATIONALITE',
			legalAccepted: 'CONDITIONS GENERALES ET PROTECTION DES DONNEES ACCEPTEES',
			flhAccepted: 'TRANSMISSION DES DONNEES A FLH.LU POUR LICENCE COMPRISE',
			accuracyAccepted: 'EXACTITUDE DES DONNEES CONFIRMEE',
			cnsComplete: 'MATRICULE CNS COMPLET'
		} : {
			licenseLink: 'LIZENZ-LINK',
			password: 'PASSWORT',
			applicant: 'ANTRAGSTELLER',
			role: 'ROLLE / FUNKTION',
			category: 'FLH KATEGORIE',
			cnsDigits: 'CNS (5 Ziffern)',
			birthDate: 'GEBURTSDATUM',
			email: 'E-MAIL',
			address: 'ADRESSE',
			minor: 'MINDERJAEHRIG',
			singleParent: 'ALLEINERZIEHEND',
			guardians: 'ERZIEHUNGSBERECHTIGTE(R)',
			club: 'EHEMALIGER VEREIN',
			medLicense: 'MED/LIZ',
			nationality: 'NATIONALITAET',
			legalAccepted: 'ALLGEMEINE BEDINGUNGEN UND DATENSCHUTZ AKZEPTIERT',
			flhAccepted: 'DATENUEBERMITTLUNG AN FLH.LU FUER LIZENZ VERSTANDEN',
			accuracyAccepted: 'RICHTIGKEIT DER ANGABEN BESTAETIGT',
			cnsComplete: 'MATRICULE CNS KOMPLETT'
		};

		if (includeLicenseLines) {
			lines.push('========================================');
			lines.push(text.licenseLink + ': ' + MERSCH75_LICENSE_LINK);
			lines.push(text.password + ': ' + MERSCH75_LICENSE_PASSWORD);
			lines.push('========================================');
			lines.push('');
		}

		lines.push('========================================');
		lines.push(text.applicant + ': ' + getFullName());
		lines.push(text.role + ': ' + getValue('Role'));
		lines.push(text.category + ': ' + getCategoryValue());
		lines.push('========================================');
		lines.push('');
		lines.push(text.cnsDigits + ': ' + getValue('CNS'));
		lines.push(text.birthDate + ': ' + getValue('DateNaissance'));
		lines.push('----------------------------------------');
		lines.push(text.email + ': ' + getValue('Email'));
		lines.push('GSM 1: ' + getValue('GSM1'));

		if (getValue('GSM2')) {
			lines.push('GSM 2: ' + getValue('GSM2'));
		}

		lines.push('----------------------------------------');
		lines.push(text.address + ': ' + getValue('Adresse'));
		lines.push('----------------------------------------');
		lines.push(text.minor + ': ' + document.getElementById('Mineur').value);

		if (document.getElementById('Mineur').value === 'OUI') {
			lines.push(text.singleParent + ': ' + document.getElementById('ParentIsole').value);
			lines.push(text.guardians + ': ' + getGuardianText());
		}

		lines.push('U7: ' + getCheckedValue('U7Cert'));
		lines.push(text.club + ': ' + getValue('AncienClub'));
		lines.push(text.medLicense + ': Med: ' + getValue('Medico') + ' / Liz: ' + getValue('Licence'));
		lines.push(text.nationality + ': ' + getValue('Nationalite'));
		lines.push(text.legalAccepted + ': ' + getCheckedValue('LegalConsent'));
		lines.push(text.flhAccepted + ': ' + getCheckedValue('FlhPortalConsent'));
		lines.push(text.accuracyAccepted + ': ' + getCheckedValue('AccuracyConsent'));

		const cnsComplete = getCnsComplete();
		if (cnsComplete) {
			lines.push(text.cnsComplete + ': ' + cnsComplete);
		}

		lines.push('========================================');

		return lines.join('\n');
	}

	function createCleanWeb3FormsData(accessKey, subjectPrefix, message) {
		const category = getCategoryValue();
		const fullName = getFullName();
		const formData = new FormData();

		formData.append('access_key', accessKey);
		formData.append('from_name', 'Mersch75 E-JOIN-US');
		formData.append('name', fullName);
		formData.append('email', getValue('Email'));
		formData.append('subject', subjectPrefix + ' - ' + fullName + ' - ' + category);
		formData.append('message', message);

		return formData;
	}

	async function sendToWeb3Forms(formData) {
		const response = await fetch('https://api.web3forms.com/submit', {
			method: 'POST',
			body: formData
		});

		const data = await response.json();

		if (data.success === true || data.status === 'success') {
			return data;
		}

		throw new Error(data.message || 'Web3Forms konnte die Anfrage nicht senden.');
	}

	function calcCategorie(dob) {
		const parts = dob.split('.');
		if (parts.length !== 3) return;

		const day = parseInt(parts[0], 10);
		const month = parseInt(parts[1], 10);
		const year = parseInt(parts[2], 10);

		if (isNaN(day) || isNaN(month) || isNaN(year) || year < 1900 || month < 1 || month > 12 || day < 1 || day > 31) {
			document.getElementById('Categorie').value = '';
			document.getElementById('Mineur').value = 'NON';
			document.getElementById('cat-display').innerText = '-';
			setRequiredState(false, '');
			return;
		}

		const today = new Date();
		let age = today.getFullYear() - year;

		if (today.getMonth() + 1 < month || (today.getMonth() + 1 === month && today.getDate() < day)) {
			age--;
		}

		let cat = '';

		if (age <= 6) cat = 'U7';
		else if (age <= 8) cat = 'U9';
		else if (age <= 10) cat = 'U11';
		else if (age <= 12) cat = 'U13';
		else if (age <= 14) cat = 'U15';
		else if (age <= 16) cat = 'U17';
		else if (age <= 18) cat = 'U19';
		else if (age <= 23) cat = 'Espoirs';
		else if (age <= 40) cat = 'Seniors';
		else cat = 'Veterans';

		const isMinor = age < 18;

		document.getElementById('Categorie').value = cat;
		document.getElementById('cat-display').innerText = cat;
		document.getElementById('Mineur').value = isMinor ? 'OUI' : 'NON';
		setRequiredState(isMinor, cat);
	}

	document.getElementById('DateNaissance').addEventListener('input', function() {
		let val = this.value.replace(/\D/g, '').slice(0, 8);

		if (val.length > 2 && val.length <= 4) {
			val = val.slice(0, 2) + '.' + val.slice(2);
		} else if (val.length > 4) {
			val = val.slice(0, 2) + '.' + val.slice(2, 4) + '.' + val.slice(4, 8);
		}

		this.value = val;

		if (val.length === 10) {
			calcCategorie(val);
		} else {
			document.getElementById('Categorie').value = '';
			document.getElementById('Mineur').value = 'NON';
			document.getElementById('cat-display').innerText = '-';
			setRequiredState(false, '');
		}

		updateCnsDisplay();
	});

	document.getElementById('ParentIsole').addEventListener('change', function() {
		const isMinor = document.getElementById('Mineur').value === 'OUI';
		const category = document.getElementById('Categorie').value;
		setRequiredState(isMinor, category);
	});

	document.getElementById('CNS').addEventListener('input', function() {
		this.value = this.value.slice(0, 5);
		updateCnsDisplay();
	});

	document.getElementById('registrationForm').addEventListener('submit', async function(event) {
		event.preventDefault();

		const form = document.getElementById('registrationForm');
		const submitBtn = document.getElementById('submitBtn');
		const originalText = submitBtn.innerText;

		if (!form.checkValidity()) {
			form.reportValidity();
			return;
		}

		if (document.getElementById('honeypot').value.trim() !== '') {
			return;
		}

		updateConsentValidationMessages(form);

		if (!form.checkValidity()) {
			form.reportValidity();
			return;
		}

		submitBtn.disabled = true;
		submitBtn.innerText = MERSCH75_UI_TEXTS[detectLegalLanguage(form)].sending;

		const isMinor = document.getElementById('Mineur').value === 'OUI';

		try {
			await sendToWeb3Forms(createCleanWeb3FormsData(
				MERSCH75_WEB3FORMS_MAIN_KEY,
				'Nouvelle inscription Mersch 75',
				buildJoinMessage(true, 'fr')
			));

			await sendToWeb3Forms(createCleanWeb3FormsData(
				MERSCH75_WEB3FORMS_MAX_KEY,
				(isMinor ? 'MINDERJAEHRIG - ' : '') + 'Neue Anmeldung Mersch 75',
				buildJoinMessage(false, 'de')
			));

			form.style.display = 'none';
			document.getElementById('success-box').style.display = 'block';
		} catch (error) {
			alert('Fehler: ' + error.message);
			submitBtn.disabled = false;
			submitBtn.innerText = originalText;
		}
	});

	updateCnsDisplay();
	initLanguageSwitcher();
	initConsentValidation();
	document.querySelectorAll('.join-registration-form').forEach(function(form) {
		applyLegalLanguage(form);
		updateConsentValidationMessages(form);
	});
	</script>
	<?php
	return ob_get_clean();
}

add_shortcode('mersch75_join_us', 'mersch75_join_us_shortcode');
