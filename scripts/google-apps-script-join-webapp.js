const SHEET_ID = '1SnJgdW0MEv9mgQIdDi5nOO-ws6nmGhqX5eBrvQgmj2o';
const SHEET_GID = 134466781;
const SHARED_TOKEN = 'm75-join-9f36-secure-2026';
const ALPHABET = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
const LAST_COL = 56; // BD

function doPost(e) {
  try {
    const body = JSON.parse(e.postData.contents);
    if (body.token !== SHARED_TOKEN) {
      return json({ ok: false, error: 'unauthorized' });
    }

    const members = (Array.isArray(body.members) && body.members.length) ? body.members : [body];
    if (members.length > 10) {
      return json({ ok: false, error: 'too_many_members', maxMembers: 10 });
    }
    const ss = SpreadsheetApp.openById(SHEET_ID);
    const sheet = getSheetByGid(ss, SHEET_GID) || ss.getSheets()[0];
    ensureJoinHeaders(sheet);
    const isTest = body.isTest === true;

    const results = [];
    members.forEach(function (member) {
      const randomNo = ensureUniqueRandomNo(sheet, member.cardInternalId || member.randomNo || '');
      const row = buildRow(member, randomNo, isTest);
      sheet.appendRow(row);
      const rowIndex = sheet.getLastRow();
      markRow(sheet, rowIndex, isTest, member);
      results.push({ row: rowIndex, randomNo: randomNo });
    });

    return json({ ok: true, results: results });
  } catch (err) {
    return json({ ok: false, error: String(err) });
  }
}

function buildRow(member, randomNo, isTest) {
  const arr = new Array(LAST_COL).fill('');
  const set = function (col, val) { arr[col - 1] = (val == null ? '' : val); };

  set(1, member.nom || '');
  set(2, member.prenom || '');
  set(3, randomNo);
  set(4, (member.language || 'lu') + ' / ' + (member.nationality || ''));
  set(5, member.street || '');
  set(6, member.postcode || '');
  set(7, member.city || '');
  set(8, '');
  set(9, member.role || '');
  set(10, member.categorie || '');
  set(11, '');
  set(12, '');
  set(13, member.categorie || '');
  set(14, '');
  set(15, '');
  set(16, '');
  set(17, '');
  set(18, '');
  set(19, '');
  set(20, '');
  set(21, '');
  set(22, '');
  set(23, '');
  set(24, '');
  set(25, '');
  set(26, '');
  set(27, '');
  set(28, '');
  set(29, '');
  set(30, '');
  set(31, '');
  set(32, '');
  set(33, '');
  set(34, '');
  set(35, '');
  set(36, '');
  set(37, '');
  set(38, '');
  set(39, '');
  set(40, '');
  set(41, '');
  set(42, '');
  set(43, '');
  set(44, '');
  set(45, '');
  set(46, '');
  set(47, '');
  set(48, '');
  set(49, '');
  set(50, '');
  set(51, '');
  set(52, '');

  set(37, member.dateNaissance || '');
  set(38, member.cnsComplete || member.cns || '');
  set(39, member.gsm1 || '');
  set(40, member.email || '');
  set(41, member.gsm2 || '');
  set(42, member.gsm3 || '');
  set(43, member.gsm4 || '');
  set(44, member.familyParent1 || '');
  set(45, member.familyParent2 || '');
  set(46, member.tarifValue || '');
  set(47, member.consentSummary || '');
  set(48, member.legalConsent || '');
  set(49, member.flhPortalConsent || '');
  set(50, member.accuracyConsent || '');
  set(51, member.source || '');
  set(52, member.cardInternalId || randomNo || '');
  set(53, member.officialRole || '');
  set(54, member.trainerQualifications || '');
  set(55, member.officialQualificationDescription || '');
  set(56, member.qualificationDocumentLink || member.qualificationDocumentId || '');

  return arr;
}

function ensureJoinHeaders(sheet) {
  const headers = ['Funktioun Umeldung', 'Trainer Qualifikatioun', 'Qualifikatioun / Erfarung', 'Qualifikatioun Dokument'];
  sheet.getRange(1, 53, 1, headers.length).setValues([headers]);
}

function markRow(sheet, rowIndex, isTest, member) {
  const color = isTest ? '#fef3c7' : '#dcfce7';
  sheet.getRange(rowIndex, 1, 1, sheet.getLastColumn()).setBackground(color);
  sheet.getRange(rowIndex, 51).setValue(isTest ? 'TEST - join.html' : 'NEU - join.html');
  sheet.getRange(rowIndex, 51).setNote('Importé via join.html le ' + new Date().toISOString());
  if (member && member.cardInternalId) {
    sheet.getRange(rowIndex, 3).setValue(member.cardInternalId);
  }
}

function ensureUniqueRandomNo(sheet, seed) {
  let candidate = seed;
  if (!candidate) {
    candidate = generateRandomNo();
  }

  let existing = readColumnValues(sheet, 3);
  while (existing.indexOf(candidate) !== -1) {
    candidate = generateRandomNo();
  }

  return candidate;
}

function generateRandomNo() {
  let value = '';
  for (let i = 0; i < 8; i += 1) {
    value += ALPHABET.charAt(Math.floor(Math.random() * ALPHABET.length));
  }
  return value;
}

function readColumnValues(sheet, column) {
  const values = sheet.getRange(1, column, sheet.getLastRow(), 1).getValues();
  return values.map(function (row) { return row[0] || ''; }).filter(Boolean);
}

function getSheetByGid(ss, gid) {
  const sheets = ss.getSheets();
  for (let i = 0; i < sheets.length; i += 1) {
    if (sheets[i].getSheetId() === gid) {
      return sheets[i];
    }
  }
  return null;
}

function json(payload) {
  return ContentService.createTextOutput(JSON.stringify(payload)).setMimeType(ContentService.MimeType.JSON);
}
