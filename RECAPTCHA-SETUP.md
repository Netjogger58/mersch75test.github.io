# reCAPTCHA-Schutz fir d'Join-Formular → Google-Sheet

**Zil:** Kee Geheimnis méi am Client (`join.html`). D'Umeldung an de Google-Sheet gëtt **server-säiteg** (am Apps Script) mat reCAPTCHA v3 ofgeséchert. Wien de Quelltext liest, fënnt **näischt Brauchbares** méi.

> ⚠️ Nëmmen **du (`M75.deisad@gmail.com`)** oder **Jeff (`deisje@hotmail.com`)** dierfen dës Astellungen änneren.

---

## Schrëtt 1 — reCAPTCHA-Schlëssel kréien (gratis)

1. Gaang op **https://www.google.com/recaptcha/admin/create**
2. **Label:** `Mersch75 Join`
3. **reCAPTCHA type:** wiel **„reCAPTCHA v3"**
4. **Domains** (all dobäisetzen, ee pro Zeil):
   - `mersch75.lu`
   - `www.mersch75.lu`
   - `netjogger58.github.io`  *(fir Test op GitHub Pages — falls do getest gëtt)*
5. Bedingunge akzeptéieren → **Submit**
6. Du kriss **zwee Schlëssel**:
   - **Site Key** (ëffentlech) → kënnt an `join.html`
   - **Secret Key** (geheim) → kënnt **NËMMEN** an de Apps Script (Schrëtt 3)

---

## Schrëtt 2 — Site Key an `join.html` setzen

An `join.html`, Zeil ~427, ersetzen:

```js
const MERSCH75_RECAPTCHA_SITE_KEY = 'PASTE_RECAPTCHA_SITE_KEY_HERE';
```

duerch däin **Site Key**, z.B.:

```js
const MERSCH75_RECAPTCHA_SITE_KEY = '6Lxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx';
```

> De Site Key **dierf** ëffentlech sinn — deen ass fir de Client geduecht.

---

## Schrëtt 3 — Apps Script: reCAPTCHA server-säiteg préiwen

1. Am Google-Sheet: **Extensions → Apps Script**
2. **Secret Key sécher späicheren** (net am Code!):
   - Lénks: **Project Settings** (Zännrad) → **Script Properties** → **Add script property**
   - Property: `RECAPTCHA_SECRET`  ·  Value: *(däin Secret Key)*
3. Am Ufank vun denger `doPost(e)`-Funktioun dës Préiwung **virum Schreiwen** asetzen:

```javascript
function doPost(e) {
  var data = JSON.parse(e.postData.contents);

  // --- reCAPTCHA v3 server-säiteg préiwen (ersetzt den ale Token) ---
  var secret = PropertiesService.getScriptProperties().getProperty('RECAPTCHA_SECRET');
  var token = data.recaptcha || '';
  if (!secret) {
    return _json({ ok: false, error: 'RECAPTCHA_SECRET net konfiguréiert' });
  }
  var verify = UrlFetchApp.fetch('https://www.google.com/recaptcha/api/siteverify', {
    method: 'post',
    payload: { secret: secret, response: token },
    muteHttpExceptions: true
  });
  var result = JSON.parse(verify.getContentText());
  // Ofleenen wann: net erfollegräich, falsch Aktioun, oder ze niddrege Score (Bot-Verdacht)
  if (!result.success || result.action !== 'join' || (typeof result.score === 'number' && result.score < 0.5)) {
    return _json({ ok: false, error: 'reCAPTCHA ofgeleent', score: result.score });
  }
  // --- Enn Préiwung ---

  // ... HEI kënnt deng bestoend Logik: fräi Zeil sichen, Felder aus data.members[] schreiwen,
  //     Random-No an Kategorie-Flag setzen. data.isTest sot ob Test- oder Produktiouns-Master.

  return _json({ ok: true });
}

// Hëllefsfunktioun fir JSON-Äntwerten
function _json(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}
```

4. **Nei deployen:** *Deploy → Manage deployments → (Edit) → New version → Deploy*.
   - Wichteg: eng **nei Version** deployen, soss leeft nach den ale Code.
   - D'Deployment-URL bleift déiselwecht (`MERSCH75_SHEET_ENDPOINT` an `join.html` muss net geännert ginn).

---

## Schrëtt 4 — Testen

1. Op `join.html` eng **Test-Umeldung** maachen (Numm mat **„TEST"**).
2. Kuck ob d'Zeil am **Adrien-Test-Master** ukomm ass.
   - ✅ Do → reCAPTCHA + Schreiwen funktionéieren.
   - ❌ Net do → am Apps Script **Executions** (lénks) kucken, ob „reCAPTCHA ofgeleent" oder „RECAPTCHA_SECRET net konfiguréiert" steet.

---

## Firwat dat sécher ass

- **Kee Geheimnis am Client:** `join.html` huet just de Site Key (ëffentlech) — kee Passwuert méi.
- **Server entscheet:** nëmmen d'Google-reCAPTCHA-Préiwung (mam Secret, deen nëmmen am Apps Script läit) entscheet ob geschriwwe gëtt.
- E Friemen dee direkt an den Endpoint POSTe wëll, huet **kee gültege reCAPTCHA-Token** → gëtt ofgeleent.

## Produktioun aktivéieren (spéider)

Wann de Secrétaire-Master prett ass:
- An `join.html`: `MERSCH75_SHEET_PRODUCTION = true` setzen.
- Da landen och **richteg** Umeldungen am Sheet (mat reCAPTCHA-Schutz).
