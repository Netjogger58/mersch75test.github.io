/** M75 Stripe-Brücke: Google-Sheet-Spiegel <-> Stripe Payment Links/Invoices.
 *  Einmal täglich (Zeit-Trigger) oder per Menü "M75 Stripe" ausführen.
 *  Liest das Blatt Stripe_Export (Spiegel der Excel-Mappe), erzeugt für jede
 *  offene Zeile (Betrag>0, Bezahlt <> "J", Status leer) einen Stripe Payment Link
 *  und schreibt Status + Link zurück. Optional Rechnung per Stripe-Invoice.
 *
 *  Setup:
 *  1. Dieses Sheet ist der Spiegel des Excel-Blatts Stripe_Export
 *     (Excel: Blatt als CSV/Google-Sheet importieren oder per Drive-Sync).
 *  2. Script-Eigenschaften setzen: STRIPE_SECRET_KEY (sk_test_.../sk_live_...),
 *     STRIPE_MODE ("payment_link" oder "invoice").
 *  3. Zeit-Trigger: syncStripe() täglich, z.B. 06:00.
 */
const SHEET = 'Stripe_Export';
// NEUE MITGLIEDER: syncStripe() liest bis zur LETZTEN Zeile des Spiegels
// (getLastRow) - keine festen Zeilennummern noetig, neu synchronisierte
// Zeilen laufen automatisch mit. Der Spiegel muss nach neuen Mitgliedern
// aktualisiert werden, sonst fehlen sie hier (im Excel passiert durch
// Neuzugaenge nichts).
// UMBENENNUNGEN: SHEET ist der Name des SPIEGEL-Blatts. Wird das
// Excel-Datenblatt umbenannt, aendert das hier nichts - die Formeln im
// Excel-Blatt passen sich selbst an. Nur wenn das Spiegel-Blatt selbst
// umbenannt wird, muss SHEET hier angepasst werden.
const COL = { fam: 1, name: 2, betrag: 3, betragText: 4, email: 5, nom: 6, pre: 7,
              adr: 8, mitgl: 9, bezahlt: 10, status: 11, link: 12, bemerk: 13 };

function syncStripe() {
  const props = PropertiesService.getScriptProperties();
  const key = props.getProperty('STRIPE_SECRET_KEY');
  if (!key) throw new Error('STRIPE_SECRET_KEY fehlt (Datei > Projekteinstellungen > Script-Eigenschaften).');
  const mode = props.getProperty('STRIPE_MODE') || 'payment_link';
  const sh = SpreadsheetApp.getActive().getSheetByName(SHEET);
  if (!sh) {
    throw new Error('Blatt "' + SHEET + '" gibt es in dieser Datei nicht.\n' +
      'Anlegen: Blatt + -> "Stripe_Export" benennen, dann die Kopfzeile A1:M1 ' +
      'einfügen: FamID, Rechnung_traegt, Betrag_EUR, Betrag_Text, Email, Nom, ' +
      'Prenom, Haushalt_Adress, Mitglieder, Bezahlt_JN, Stripe_Status, ' +
      'Stripe_Link, Bemerkung.');
  }
  const last = sh.getLastRow();
  if (last < 2) {
    throw new Error('Blatt "' + SHEET + '" ist leer - erst die Daten aus dem ' +
      'Excel-Blatt Stripe_Export dorthin kopieren.');
  }
  const rows = sh.getRange(2, 1, last - 1, 13).getValues();
  let neu = 0;
  const manuell = [];   // offene Posten OHNE reinen Zahlenbetrag, z. B. "Don ?"
  rows.forEach((r, i) => {
    const fam = String(r[0] || '').trim();
    const betrag = Number(r[2] || 0);
    const email = String(r[4] || '').trim();
    const bezahlt = String(r[9] || '').trim().toUpperCase();
    const status = String(r[10] || '').trim();
    if (!fam || bezahlt === 'J' || status) return;
    if (!(betrag > 0)) {
      // Spalte C ist leer, wenn L ein Text wie "(0+50)" ist. Das ist kein
      // Fehler, aber es darf nicht ungeprueft durchrutschen: Betrag in der
      // Spalte D (Betrag_Text) nachsehen und in Stripe manuell anlegen.
      manuell.push('Z' + (i + 2) + ' ' + fam + ' (' + r[3] + ')');
      return;
    }
    const descr = 'Cotisation 2026/27 – Haushalt ' + fam + ' (' + r[1] + ')';
    const url = (mode === 'invoice' && email)
      ? stripeInvoice(key, email, r[5] + ' ' + r[6], betrag, descr)
      : stripePaymentLink(key, betrag, descr);
    sh.getRange(i + 2, COL.status).setValue(mode === 'invoice' ? 'invoice_sent' : 'link_created');
    sh.getRange(i + 2, COL.link).setValue(url);
    neu++;
  });
  Logger.log(neu + ' Stripe-Links/Rechnungen erzeugt.');
  if (manuell.length) {
    Logger.log('ACHTUNG - ' + manuell.length +
               ' offene Posten ohne Zahlenbetrag, manuell in Stripe anlegen: ' +
               manuell.join(' | '));
  }
}

function stripePaymentLink(key, betragEur, descr) {
  const res = UrlFetchApp.fetch('https://api.stripe.com/v1/payment_links', {
    method: 'post',
    headers: { Authorization: 'Bearer ' + key },
    payload: {
      'line_items[0][price_data][currency]': 'eur',
      'line_items[0][price_data][unit_amount]': String(Math.round(betragEur * 100)),
      'line_items[0][price_data][product_data][name]': descr,
      'line_items[0][quantity]': '1'
    },
    muteHttpExceptions: true
  });
  const o = JSON.parse(res.getContentText());
  if (!o.url) throw new Error('Stripe-Fehler: ' + res.getContentText());
  return o.url;
}

function stripeInvoice(key, email, name, betragEur, descr) {
  const hdr = { Authorization: 'Bearer ' + key };
  const c = JSON.parse(UrlFetchApp.fetch('https://api.stripe.com/v1/customers', {
    method: 'post', headers: hdr,
    payload: { email: email, name: name }, muteHttpExceptions: true
  }).getContentText());
  UrlFetchApp.fetch('https://api.stripe.com/v1/invoiceitems', {
    method: 'post', headers: hdr,
    payload: { customer: c.id, currency: 'eur',
      unit_amount: String(Math.round(betragEur * 100)), description: descr },
    muteHttpExceptions: true
  });
  const inv = JSON.parse(UrlFetchApp.fetch('https://api.stripe.com/v1/invoices', {
    method: 'post', headers: hdr,
    payload: { customer: c.id, auto_advance: 'true' }, muteHttpExceptions: true
  }).getContentText());
  const fin = JSON.parse(UrlFetchApp.fetch(
    'https://api.stripe.com/v1/invoices/' + inv.id + '/finalize', {
    method: 'post', headers: hdr, muteHttpExceptions: true
  }).getContentText());
  UrlFetchApp.fetch('https://api.stripe.com/v1/invoices/' + inv.id + '/send', {
    method: 'post', headers: hdr, muteHttpExceptions: true
  });
  return fin.hosted_invoice_url || fin.id;
}

/** Menü beim Öffnen */
function onOpen() {
  SpreadsheetApp.getUi().createMenu('M75 Stripe')
    .addItem('Jetzt synchronisieren', 'syncStripe').addToUi();
}
