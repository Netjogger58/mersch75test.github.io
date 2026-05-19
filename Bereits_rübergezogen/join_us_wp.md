<style>
	/* --- Das Fundament: Apple-Style Card --- */
	.wp-form-wrapper { padding: 15px; font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; }
	#join-us-form {
		background-color: #ffffff; width: 100%; max-width: 800px; margin: auto;
		padding: 40px 30px; border-radius: 24px; box-shadow: 0 10px 30px rgba(0,0,0,0.03); 
		box-sizing: border-box; border: 1px solid rgba(202, 202, 204, 0.4); 
	}
	.lang-selector {
		background: #ffffff; padding: 10px; border-radius: 16px; margin-bottom: 25px;
		text-align: center; border: 1px solid rgba(202, 202, 204, 0.3);
	}
	.flag-picker { display: flex; justify-content: center; gap: 15px; padding: 5px; flex-wrap: wrap; }
	.flag {
		font-size: 34px; cursor: pointer; opacity: 0.4;
		transition: transform 0.3s ease, opacity 0.3s; border-radius: 8px; padding: 4px;
	}
	.flag:hover { transform: scale(1.1); opacity: 0.8; }
	.active-flag { opacity: 1; transform: scale(1.1); box-shadow: 0 4px 10px rgba(0,0,0,0.08); border-radius: 12px; background: #F5F5F7; }
	.lang-text { display: none; line-height: 1.5; font-size: 14px; margin-bottom: 30px; color: #1d1d1f; }
	.active-lang { display: block !important; }
	.lang-text strong { color: #002F65; font-size: 22px; display: block; margin-bottom: 10px; font-weight: 700; letter-spacing: -0.5px; }
	.form-group { margin-bottom: 20px; width: 100%; text-align: left; }
	.row { display: flex; gap: 15px; margin-bottom: 20px; }
	.row .form-group { flex: 1; margin-bottom: 0; }
	@media (max-width: 600px) { .row { flex-direction: column; gap: 20px; } }
	.wp-form-wrapper label {
		display: block; font-weight: 600; font-size: 11px; margin-bottom: 6px;
		color: #86868b; letter-spacing: 0.5px; text-transform: uppercase; 
	}
	.wp-form-wrapper input[type="text"], .wp-form-wrapper input[type="email"], .wp-form-wrapper select {
		width: 100%; padding: 14px; border: 1px solid transparent; 
		background-color: #F5F5F7; box-sizing: border-box; border-radius: 10px;
		font-size: 15px; outline: none; color: #1d1d1f; transition: all 0.3s ease; font-family: inherit;
	}
	.wp-form-wrapper input[type="text"]:focus, .wp-form-wrapper input[type="email"]:focus, .wp-form-wrapper select:focus {
		background-color: #ffffff; border: 1px solid #002F65; box-shadow: 0 0 0 3px rgba(0, 47, 101, 0.1);
	}
	.wp-form-wrapper input:disabled, .wp-form-wrapper select:disabled { opacity: 0.6; cursor: not-allowed; }
	.error-border { border: 1px solid #d93025 !important; background-color: #fce8e6; }
	.info-text-small { font-size: 11px; color: #86868b; margin-top: 5px; display: block; }
	#cat-section {
		border: none; padding: 15px; border-radius: 12px;
		margin-bottom: 20px; display: none; background: #e8f0fe; text-align: left;
	}
	#cat-section strong { color: #002F65; font-size: 16px; text-transform: none; }
	#parent-section {
		background: #F5F5F7; padding: 25px; border-radius: 12px;
		border: none; margin-bottom: 20px; display: none; text-align: left;
	}
	#u7-section { display: none; align-items: flex-start; gap: 12px; margin-bottom: 20px; text-align: left; }
	.checkbox-row { display: flex; align-items: flex-start; gap: 12px; margin-bottom: 15px; text-align: left; }
	.checkbox-row input[type="checkbox"], #u7-section input { width: 18px; height: 18px; margin-top: 2px; cursor: pointer; flex-shrink: 0; accent-color: #002F65; }
	.checkbox-row label, #u7-section label {
		font-size: 13px; color: #1d1d1f; font-weight: 500; cursor: pointer; line-height: 1.4; margin: 0; text-transform: none;
	}
	.checkbox-row label a { color: #002F65; text-decoration: underline; font-weight: 600; }
	.info-checkbox-box { background-color: #F5F5F7; padding: 15px; border-radius: 10px; margin: 20px 0; }
	.submit-btn {
		background-color: #002F65; color: white; padding: 16px; border: none;
		width: 100%; font-size: 16px; font-weight: 600; cursor: pointer;
		border-radius: 12px; margin-top: 15px; transition: transform 0.2s ease, background-color 0.2s ease;
	}
	.submit-btn:hover { background-color: #001f45; transform: translateY(-2px); box-shadow: 0 8px 15px rgba(0, 47, 101, 0.2); }
	#success-box {
		display: none; background-color: #ffffff; border: 1px solid rgba(202, 202, 204, 0.3);
		color: #1d1d1f; padding: 30px; border-radius: 16px; text-align: center;
		margin-top: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); max-width: 800px; margin-left: auto; margin-right: auto;
	}
	#website-field { display: none; }
</style>

<div class="wp-form-wrapper">

<div id="join-us-form">
	<div class="lang-selector">
		<div class="flag-picker">
			<span class="flag active-flag" onclick="updateLang('lu')" title="Lëtzebuergesch">🇱🇺</span>
			<span class="flag" onclick="updateLang('fr')" title="Français">🇫🇷</span>
			<span class="flag" onclick="updateLang('de')" title="Deutsch">🇩🇪</span>
			<span class="flag" onclick="updateLang('en')" title="English">🇬🇧</span>
			<span class="flag" onclick="updateLang('pt')" title="Português">🇵🇹</span>
		</div>
	</div>

	<div id="lu" class="lang-text active-lang">
		<strong>Wëllkomm am Veräin!</strong>
		Super, datt du Loscht hues eist Team ze verstäerken. Fëll w.e.g. de Formulaire aus fir d'intern Umeldung ze starten. Nodeems de Veräin deng Donnéeën kritt huet, gëtt den offizielle Lizenzantrag vum Veräinsresponsabel gestart.
	</div>
	<div id="fr" class="lang-text">
		<strong>Bienvenue au club !</strong>
		Ravis que vous souhaitiez renforcer notre équipe. Veuillez remplir ce formulaire pour lancer l'inscription interne. Une fois les données reçues, la demande officielle de licence sera initiée par le responsable du club.
	</div>
	<div id="de" class="lang-text">
		<strong>Willkommen im Verein!</strong>
		Toll, dass du unser Team verstärken möchtest. Bitte fülle das Formular aus, um die interne Anmeldung zu starten. Sobald der Verein deine Daten erhalten hat, wird der offizielle Lizenzantrag vom Vereinsverantwortlichen gestartet.
	</div>
	<div id="en" class="lang-text">
		<strong>Welcome to the club!</strong>
		Great to have you on board. Please fill out the form to start the internal registration. Once the club receives your data, the official licence request will be initiated by the club manager.
	</div>
	<div id="pt" class="lang-text">
		<strong>Bem-vindo ao clube!</strong>
		É ótimo que queiras reforçar a nossa equipa. Por favor, preenche o formulário para iniciar o registo interno. Assim que o clube receber os teus dados, o pedido oficial de licença será iniciado pelo responsável do clube.
	</div>

	<form id="registrationForm" onkeypress="return event.keyCode != 13">
		<div id="website-field">
			<input type="text" id="honeypot" name="website" autocomplete="off">
		</div>

		<div class="form-group">
			<label id="lbl-nom">NOM(S) SUR CARTE D'IDENTITÉ *</label>
			<input type="text" id="Nom" name="Nom" required>
		</div>
		<div class="form-group">
			<label id="lbl-prenom">PRÉNOM *</label>
			<input type="text" id="Prenom" name="Prenom" required>
		</div>

		<div class="row">
			<div class="form-group">
				<label id="lbl-dob">DATE DE NAISSANCE (JJ.MM.AAAA) *</label>
				<input type="text" id="DateNaissance" name="DateNaissance" placeholder="01.01.2010" required>
			</div>
			<div class="form-group">
				<label id="lbl-mineur">MINEUR? *</label>
				<select id="Mineur" disabled>
					<option value="NON">NON</option>
					<option value="OUI">OUI</option>
				</select>
			</div>
		</div>

		<div id="cat-section">
			<label id="lbl-cat">CATÉGORIE FLH (AUTO)</label>
			<strong id="cat-display">-</strong>
			<input type="hidden" id="Categorie" name="Categorie" value="">
		</div>

		<div class="form-group">
			<label id="lbl-role">RÔLE / FUNKTION *</label>
			<select id="Role" name="Role" required>
				<option value="Joueur / Joueuse">Joueur / Joueuse</option>
				<option value="Officiel(le)">Officiel(le)</option>
				<option value="Arbitre">Arbitre</option>
			</select>
		</div>

		<div id="parent-section">
			<div class="form-group" style="max-width: 50%;">
				<label id="lbl-parent">PARENT ISOLÉ / ALLEINERZIEHEND? *</label>
				<select id="ParentIsole">
					<option value="NON">NON (2 Tuteurs)</option>
					<option value="OUI">OUI (1 Tuteur)</option>
				</select>
			</div>
			<div class="row">
				<div class="form-group">
					<label id="lbl-tuteur1">TUTEUR 1 (NOM ET PRÉNOM) *</label>
					<input type="text" id="Tuteur1" name="Tuteur1">
				</div>
				<div class="form-group" id="tuteur2-wrap">
					<label id="lbl-tuteur2">TUTEUR 2 (NOM ET PRÉNOM) *</label>
					<input type="text" id="Tuteur2" name="Tuteur2">
				</div>
			</div>
		</div>

		<div class="form-group">
			<label id="lbl-nat">NATIONALITÉ *</label>
			<input type="text" id="Nationalite" name="Nationalite" required>
		</div>
		<div class="form-group">
			<label id="lbl-cns">MATRICULE CNS (5 CHIFFRES) *</label>
			<input type="text" id="CNS" name="CNS" maxlength="5" pattern="\d{5}" required>
			<span id="cns-prefix-display" class="info-text-small"></span>
		</div>

		<div class="row">
			<div class="form-group">
				<label id="lbl-medico">MEDICO? *</label>
				<select id="Medico" name="Medico" required>
					<option value="Non">Non</option>
					<option value="Oui">Oui</option>
				</select>
			</div>
			<div class="form-group">
				<label id="lbl-licence">LICENCE? *</label>
				<select id="Licence" name="Licence" required>
					<option value="Non">Non</option>
					<option value="Oui">Oui</option>
				</select>
			</div>
		</div>

		<div class="form-group">
			<label id="lbl-club">ANCIEN CLUB (OU "NÉANT") *</label>
			<input type="text" id="AncienClub" name="AncienClub" required>
		</div>

		<div id="u7-section">
			<input type="checkbox" id="U7Cert">
			<label for="U7Cert" id="lbl-u7">U7 : CERTIFICAT MÉDICAL D'APTITUDE SPORTIVE OBLIGATOIRE (ÉTABLI PAR LE MÉDECIN TRAITANT).</label>
		</div>

		<div class="form-group">
			<label id="lbl-adresse">ADRESSE (NO, RUE, CODE POSTAL, LOCALITÉ) *</label>
			<input type="text" id="Adresse" name="Adresse" required>
		</div>
		<div class="form-group">
			<label id="lbl-email">EMAIL *</label>
			<input type="email" id="Email" name="Email" required>
		</div>

		<div class="row">
			<div class="form-group">
				<label id="lbl-gsm1">TEL MOBILE / GSM 1 *</label>
				<input type="text" id="GSM1" name="GSM1" required>
			</div>
			<div class="form-group">
				<label id="lbl-gsm2">TEL MOBILE / GSM 2 (OPTIONNEL)</label>
				<input type="text" id="GSM2" name="GSM2">
			</div>
		</div>

		<div class="checkbox-row">
			<input type="checkbox" id="chk1" required>
			<label for="chk1" id="lbl-chk1">J'AI LU ET J'ACCEPTE LES ALLGEMEINEN BEDINGUNGEN.</label>
		</div>
		<div class="checkbox-row">
			<input type="checkbox" id="chk2" required>
			<label for="chk2" id="lbl-chk2">J'AI LU ET J'ACCEPTE LE DATESCHUTZ.</label>
		</div>
		<div class="checkbox-row info-checkbox-box">
			<input type="checkbox" id="chk3" required>
			<label for="chk3" id="lbl-chk3">INFO: J'AI COMPRIS QUE MA DEMANDE D'AFFILIATION SERA FINALISÉE VIA LE PORTAIL DE LA FLH.</label>
		</div>
		<div class="checkbox-row">
			<input type="checkbox" id="chk4" required>
			<label for="chk4" id="lbl-chk4">CONFIRMATION: JE CONFIRME L'EXACTITUDE DE MES DONNÉES.</label>
		</div>

		<button type="button" id="submitBtn" class="submit-btn">SEND / ABSCHICKEN</button>
	</form>
</div>

<div id="success-box">
	<strong style="color: #002F65; font-size: 20px; margin-bottom: 10px; display: block;">✅ Merci / Danke / Thank you / Obrigado!</strong>
	<span style="font-weight: 600;">Deng Umeldung gouf erfollegräich iwwermëttelt.</span><br>
	<small style="color: #86868b; margin-top: 8px; display: block;">Du kriss eng Bestätegung per E-Mail.</small>
</div>

</div>

<script>
const CGurl = "https://www.mersch75.lu/x2-terms-and-conditions/";
const DPurl = "https://www.mersch75.lu/x3-dataprotection/";

const T = {
    lu: {
        nom: "NIMM (WÉI AUM PERSONALAUSWEIS) *", prenom: "VIRNUMM *",
        dob: "GEBUERTSDATUM (DD.MM.JJJJ) *", mineur: "MANNERJÄREG? *",
        cat: "FLH KATEGORIE (AUTO)", role: "FUNKTIOUN *",
        parent: "ELENDERZÉIEND? *", tuteur1: "TUTEUR 1 (NUMM A VIRNUMM) *",
        tuteur2: "TUTEUR 2 (NUMM A VIRNUMM) *", nat: "NATIONALITÉIT *",
        cns: "CNS NUMMER (5 ZIFFEREN) *", medico: "MEDICO? *", licence: "LIZENZ? *",
        club: "FRÉIERE VERÄIN (ODER \"NÉANT\") *",
        u7: "U7: SPORTMEDIZINESCHT ATTEST OBLIGATORESCH (VUM HAUSARZT).",
        adresse: "ADRESS (NR., STROOSS, PLZ, UERT) *", email: "EMAIL *",
        gsm1: "TEL MOBILE / GSM 1 *", gsm2: "TEL MOBILE / GSM 2 (OPTIONAL)",
        chk1: "ECH HUN GELIES AN AKZEPTÉIEREN D'<a href='" + CGurl + "' target='_blank'>ALLGEMENG BEDÉNGUNGEN</a>.",
        chk2: "ECH HUN GELIES AN AKZEPTÉIEREN DE <a href='" + DPurl + "' target='_blank'>DATESCHUTZ</a>.",
        chk3: "INFO: ECH HUN VERSTANEN DATT MENG UMELDUNG IWWERT DAT FLH PORTAL OFGESCHLOSS GËTT.",
        chk4: "BESTÄTEGUNG: ECH CONFIRMÉIEREN D'RICHTEGKEET VUN MENGE DONNÉEËN.",
        send: "WEIDERLEEDEN",
        oui: "Jo", non: "Nee",
        joueur: "Spiller / Spillerin", officiel: "Offiziell(e)", arbitre: "Schiedsriichter(in)",
        parent_non: "NEE (2 Tuteure)", parent_oui: "Jo (1 Tuteur)"
    },
    fr: {
        nom: "NOM(S) SUR CARTE D'IDENTITÉ *", prenom: "PRÉNOM *",
        dob: "DATE DE NAISSANCE (JJ.MM.AAAA) *", mineur: "MINEUR? *",
        cat: "CATÉGORIE FLH (AUTO)", role: "RÔLE / FONCTION *",
        parent: "PARENT ISOLÉ? *", tuteur1: "TUTEUR 1 (NOM ET PRÉNOM) *",
        tuteur2: "TUTEUR 2 (NOM ET PRÉNOM) *", nat: "NATIONALITÉ *",
        cns: "MATRICULE CNS (5 CHIFFRES) *", medico: "MEDICO? *", licence: "LICENCE? *",
        club: "ANCIEN CLUB (OU \"NÉANT\") *",
        u7: "U7 : CERTIFICAT MÉDICAL D'APTITUDE SPORTIVE OBLIGATOIRE (ÉTABLI PAR LE MÉDECIN TRAITANT).",
        adresse: "ADRESSE (NO, RUE, CODE POSTAL, LOCALITÉ) *", email: "EMAIL *",
        gsm1: "TEL MOBILE / GSM 1 *", gsm2: "TEL MOBILE / GSM 2 (OPTIONNEL)",
        chk1: "J'AI LU ET J'ACCEPTE LES <a href='" + CGurl + "' target='_blank'>CONDITIONS GÉNÉRALES</a>.",
        chk2: "J'AI LU ET J'ACCEPTE LA <a href='" + DPurl + "' target='_blank'>PROTECTION DES DONNÉES</a>.",
        chk3: "INFO: J'AI COMPRIS QUE MA DEMANDE D'AFFILIATION SERA FINALISÉE VIA LE PORTAIL DE LA FLH.",
        chk4: "CONFIRMATION: JE CONFIRME L'EXACTITUDE DE MES DONNÉES.",
        send: "ENVOYER",
        oui: "Oui", non: "Non",
        joueur: "Joueur / Joueuse", officiel: "Officiel(le)", arbitre: "Arbitre",
        parent_non: "NON (2 Tuteurs)", parent_oui: "OUI (1 Tuteur)"
    },
    de: {
        nom: "NAME(N) LAUT PERSONALAUSWEIS *", prenom: "VORNAME *",
        dob: "GEBURTSDATUM (TT.MM.JJJJ) *", mineur: "MINDERJÄHRIG? *",
        cat: "FLH KATEGORIE (AUTO)", role: "ROLLE / FUNKTION *",
        parent: "ALLEINERZIEHEND? *", tuteur1: "ERZIEHUNGSBERECHTIGTER 1 (NAME UND VORNAME) *",
        tuteur2: "ERZIEHUNGSBERECHTIGTER 2 (NAME UND VORNAME) *", nat: "NATIONALITÄT *",
        cns: "CNS NUMMER (5 ZIFFERN) *", medico: "ÄRZTLICHES ATTEST? *", licence: "LIZENZ? *",
        club: "FRÜHERER VEREIN (ODER \"KEINER\") *",
        u7: "U7: SPORTÄRZTLICHES ATTEST PFLICHT (VOM HAUSARZT AUSGESTELLT).",
        adresse: "ADRESSE (NR., STRASSE, PLZ, ORT) *", email: "E-MAIL *",
        gsm1: "MOBILNUMMER / GSM 1 *", gsm2: "MOBILNUMMER / GSM 2 (OPTIONAL)",
        chk1: "ICH HABE GELESEN UND AKZEPTIERE DIE <a href='" + CGurl + "' target='_blank'>ALLGEMEINEN BEDINGUNGEN</a>.",
        chk2: "ICH HABE GELESEN UND AKZEPTIERE DEN <a href='" + DPurl + "' target='_blank'>DATENSCHUTZ</a>.",
        chk3: "INFO: ICH HABE VERSTANDEN, DASS MEIN ANTRAG ÜBER DAS FLH-PORTAL ABGESCHLOSSEN WIRD.",
        chk4: "BESTÄTIGUNG: ICH BESTÄTIGE DIE RICHTIGKEIT MEINER ANGABEN.",
        send: "ABSCHICKEN",
        oui: "Ja", non: "Nein",
        joueur: "Spieler/in", officiel: "Funktionär/in", arbitre: "Schiedsrichter/in",
        parent_non: "NEIN (2 Erziehungsberechtigte)", parent_oui: "JA (1 Erziehungsberechtigter)"
    },
    en: {
        nom: "LAST NAME(S) AS ON ID CARD *", prenom: "FIRST NAME *",
        dob: "DATE OF BIRTH (DD.MM.YYYY) *", mineur: "MINOR? *",
        cat: "FLH CATEGORY (AUTO)", role: "ROLE / FUNCTION *",
        parent: "SINGLE PARENT? *", tuteur1: "GUARDIAN 1 (LAST & FIRST NAME) *",
        tuteur2: "GUARDIAN 2 (LAST & FIRST NAME) *", nat: "NATIONALITY *",
        cns: "CNS NUMBER (5 DIGITS) *", medico: "MEDICAL CERTIFICATE? *", licence: "LICENCE? *",
        club: "PREVIOUS CLUB (OR \"NONE\") *",
        u7: "U7: MEDICAL FITNESS CERTIFICATE MANDATORY (ISSUED BY FAMILY DOCTOR).",
        adresse: "ADDRESS (NO., STREET, POSTCODE, CITY) *", email: "EMAIL *",
        gsm1: "MOBILE / GSM 1 *", gsm2: "MOBILE / GSM 2 (OPTIONAL)",
        chk1: "I HAVE READ AND ACCEPT THE <a href='" + CGurl + "' target='_blank'>GENERAL TERMS AND CONDITIONS</a>.",
        chk2: "I HAVE READ AND ACCEPT THE <a href='" + DPurl + "' target='_blank'>DATA PROTECTION POLICY</a>.",
        chk3: "INFO: I UNDERSTAND THAT MY MEMBERSHIP REQUEST WILL BE FINALISED VIA THE FLH PORTAL.",
        chk4: "CONFIRMATION: I CONFIRM THE ACCURACY OF MY DATA.",
        send: "SUBMIT",
        oui: "Yes", non: "No",
        joueur: "Player", officiel: "Official", arbitre: "Referee",
        parent_non: "NO (2 Guardians)", parent_oui: "YES (1 Guardian)"
    },
    pt: {
        nom: "APELIDO(S) CONFORME BILHETE DE IDENTIDADE *", prenom: "PRIMEIRO NOME *",
        dob: "DATA DE NASCIMENTO (DD.MM.AAAA) *", mineur: "MENOR? *",
        cat: "CATEGORIA FLH (AUTO)", role: "FUNÇÃO *",
        parent: "PROGENITOR ÚNICO? *", tuteur1: "TUTOR 1 (APELIDO E NOME) *",
        tuteur2: "TUTOR 2 (APELIDO E NOME) *", nat: "NACIONALIDADE *",
        cns: "NÚMERO CNS (5 DÍGITOS) *", medico: "ATESTADO MÉDICO? *", licence: "LICENÇA? *",
        club: "CLUBE ANTERIOR (OU \"NENHUM\") *",
        u7: "U7: CERTIFICADO MÉDICO DE APTIDÃO DESPORTIVA OBRIGATÓRIO (EMITIDO PELO MÉDICO DE FAMÍLIA).",
        adresse: "MORADA (Nº, RUA, CÓDIGO POSTAL, LOCALIDADE) *", email: "EMAIL *",
        gsm1: "TEL MÓVEL / GSM 1 *", gsm2: "TEL MÓVEL / GSM 2 (OPCIONAL)",
        chk1: "LI E ACEITO OS <a href='" + CGurl + "' target='_blank'>TERMOS E CONDIÇÕES GERAIS</a>.",
        chk2: "LI E ACEITO A <a href='" + DPurl + "' target='_blank'>POLÍTICA DE PROTEÇÃO DE DADOS</a>.",
        chk3: "INFO: COMPREENDO QUE O MEU PEDIDO DE FILIAÇÃO SERÁ FINALIZADO VIA O PORTAL FLH.",
        chk4: "CONFIRMAÇÃO: CONFIRMO A EXATIDÃO DOS MEUS DADOS.",
        send: "ENVIAR",
        oui: "Sim", non: "Não",
        joueur: "Jogador/a", officiel: "Oficial", arbitre: "Árbitro/a",
        parent_non: "NÃO (2 Tutores)", parent_oui: "SIM (1 Tutor)"
    }
};

let currentLang = 'lu';

window.updateLang = function(lang) {
    currentLang = lang;
    const t = T[lang];

    document.querySelectorAll('.lang-text').forEach(el => el.classList.remove('active-lang'));
    const active = document.getElementById(lang);
    if (active) active.classList.add('active-lang');
    document.querySelectorAll('.flag').forEach(el => el.classList.remove('active-flag'));
    const flagEl = document.querySelector('.flag[onclick="updateLang(\'' + lang + '\')"]');
    if (flagEl) flagEl.classList.add('active-flag');

    document.getElementById('lbl-nom').innerText     = t.nom;
    document.getElementById('lbl-prenom').innerText  = t.prenom;
    document.getElementById('lbl-dob').innerText     = t.dob;
    document.getElementById('lbl-mineur').innerText  = t.mineur;
    document.getElementById('lbl-cat').innerText     = t.cat;
    document.getElementById('lbl-role').innerText    = t.role;
    document.getElementById('lbl-parent').innerText  = t.parent;
    document.getElementById('lbl-tuteur1').innerText = t.tuteur1;
    document.getElementById('lbl-tuteur2').innerText = t.tuteur2;
    document.getElementById('lbl-nat').innerText     = t.nat;
    document.getElementById('lbl-cns').innerText     = t.cns;
    document.getElementById('lbl-medico').innerText  = t.medico;
    document.getElementById('lbl-licence').innerText = t.licence;
    document.getElementById('lbl-club').innerText    = t.club;
    document.getElementById('lbl-u7').innerText      = t.u7;
    document.getElementById('lbl-adresse').innerText = t.adresse;
    document.getElementById('lbl-email').innerText   = t.email;
    document.getElementById('lbl-gsm1').innerText    = t.gsm1;
    document.getElementById('lbl-gsm2').innerText    = t.gsm2;
    document.getElementById('lbl-chk1').innerHTML    = t.chk1;
    document.getElementById('lbl-chk2').innerHTML    = t.chk2;
    document.getElementById('lbl-chk3').innerText    = t.chk3;
    document.getElementById('lbl-chk4').innerText    = t.chk4;
    document.getElementById('submitBtn').innerText   = t.send;

    const mineur = document.getElementById('Mineur');
    mineur.options[0].text = t.non;
    mineur.options[1].text = t.oui;
    const role = document.getElementById('Role');
    role.options[0].text = t.joueur;
    role.options[1].text = t.officiel;
    role.options[2].text = t.arbitre;
    const parent = document.getElementById('ParentIsole');
    parent.options[0].text = t.parent_non;
    parent.options[1].text = t.parent_oui;
}

document.getElementById('DateNaissance').addEventListener('input', function() {
    let val = this.value.replace(/\D/g, '');
    if (val.length > 2 && val.length <= 4) val = val.slice(0,2) + '.' + val.slice(2);
    else if (val.length > 4) val = val.slice(0,2) + '.' + val.slice(2,4) + '.' + val.slice(4,8);
    this.value = val;
    if (val.length === 10) calcCategorie(val);
    else {
        document.getElementById('cat-section').style.display = 'none';
        document.getElementById('Mineur').value = 'NON';
        document.getElementById('parent-section').style.display = 'none';
        document.getElementById('u7-section').style.display = 'none';
    }
});

function calcCategorie(dob) {
    const parts = dob.split('.');
    if (parts.length !== 3) return;
    const year = parseInt(parts[2]);
    const month = parseInt(parts[1]);
    const day = parseInt(parts[0]);
    if (isNaN(year) || year < 1900) return;

    const today = new Date();
    let age = today.getFullYear() - year;
    if (today.getMonth() + 1 < month || (today.getMonth() + 1 === month && today.getDate() < day)) age--;

    let cat = '';
    if (age <= 6)       cat = 'U7';
    else if (age <= 8)  cat = 'U9';
    else if (age <= 10) cat = 'U11';
    else if (age <= 12) cat = 'U13';
    else if (age <= 14) cat = 'U15';
    else if (age <= 16) cat = 'U17';
    else if (age <= 18) cat = 'U19';
    else if (age <= 23) cat = 'Espoirs';
    else if (age <= 40) cat = 'Seniors';
    else cat = 'Vétérans';

    document.getElementById('Categorie').value = cat;
    document.getElementById('cat-display').innerText = cat;
    document.getElementById('cat-section').style.display = 'block';
    document.getElementById('Mineur').value = age < 18 ? 'OUI' : 'NON';
    document.getElementById('parent-section').style.display = age < 18 ? 'block' : 'none';
    document.getElementById('u7-section').style.display = cat === 'U7' ? 'flex' : 'none';
}

document.getElementById('ParentIsole').addEventListener('change', function() {
    document.getElementById('tuteur2-wrap').style.display = this.value === 'OUI' ? 'none' : 'block';
});

document.getElementById('CNS').addEventListener('input', function() {
    const val = this.value.replace(/\D/g, '').slice(0, 5);
    this.value = val;
    const dob = document.getElementById('DateNaissance').value;
    if (dob.length === 10 && val.length >= 1) {
        const parts = dob.split('.');
        const expected = parts[2].slice(-2) + parts[1] + parts[0];
        document.getElementById('cns-prefix-display').innerText =
            expected.startsWith(val) ? '✅ Préfixe OK' : '⚠️ Préfixe attendu: ' + expected;
    }
});

document.getElementById('submitBtn').addEventListener('click', function(e) {
    e.preventDefault();
    const form = document.getElementById('registrationForm');

    if (!form.checkValidity()) { form.reportValidity(); return; }

    if (!document.getElementById('chk1').checked || !document.getElementById('chk2').checked ||
        !document.getElementById('chk3').checked || !document.getElementById('chk4').checked) {
        alert('❌ Veuillez accepter toutes les cases / Bitte alle Checkboxen akzeptieren!');
        return;
    }

    const submitBtn = document.getElementById('submitBtn');
    const originalText = submitBtn.innerText;
    submitBtn.innerText = '⏳ ...';
    submitBtn.disabled = true; submitBtn.style.opacity = "0.7";

    const formData = new FormData(form);
    const mineurSelect = document.getElementById('Mineur');
    if (mineurSelect && mineurSelect.disabled) { formData.append('Mineur', mineurSelect.value); }
    const catDisplay = document.getElementById('cat-display').innerText;
    formData.append('Categorie', catDisplay);
    if (document.getElementById('ParentIsole').value === 'OUI') { formData.set('Tuteur2', '-'); }

    fetch('https://www.mersch75.lu/send_registration.php', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            form.style.display = 'none';
            document.querySelector('.lang-selector').style.display = 'none';
            document.querySelectorAll('.lang-text').forEach(el => el.style.display = 'none');
            
            const successBox = document.getElementById('success-box');
            successBox.style.display = 'block';
            successBox.animate([ { opacity: 0, transform: 'translateY(20px)' }, { opacity: 1, transform: 'translateY(0)' } ], { duration: 400, easing: 'ease-out' });
            
            window.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
            alert('❌ Fehler: ' + data.message);
            submitBtn.innerText = originalText; submitBtn.disabled = false; submitBtn.style.opacity = "1";
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('❌ Connexion erreur. Réessayez. (Technisches Problem)');
        submitBtn.innerText = originalText; submitBtn.disabled = false; submitBtn.style.opacity = "1";
    });
});

updateLang('lu');
</script>