# Project Rules for Agents

## Non-Negotiable
- Keep the site working first. Do not rename, move, or delete files unless the references are updated in the same change.
- Never perform large structural changes without a validation pass.
- Prefer small, reversible commits over broad rewrites.

## Asset Policy
- Use `assets/shared/` for files used on multiple pages.
- Use `assets/pages/<page>/` for page-specific files.
- Do not recreate duplicate copies of the same image or logo.
- Do not edit or remove archived assets unless explicitly asked.

## Media Policy
- Treat `Media/` as legacy input unless a file is still required by the live site.
- If a file is migrated, update every reference before deleting the old copy.
- Ignore macOS metadata files such as `.DS_Store`.

## HTML and Link Policy
- After changing paths, verify all `src`, `href`, and `url()` references.
- Do not leave broken links, missing images, or orphaned references behind.
- Preserve existing page behavior and layout unless a visual change is requested.

## Validation
- Before finishing, check `git status` and verify that all changed references resolve on disk.
- If the change touches files that are deployed publicly, ensure the final commit is pushed.

## Agent Behavior
- Ask before making destructive cleanup outside the current migration plan.
- Do not “tidy” unrelated files.
- Prefer repository conventions over inventing new ones.

## Join → Google Sheet Automation (join.html)
- `join.html` posts new registrations to a Google Apps Script Web App that writes rows into a Google-Sheet master; column **C** = `Random-No` (from `generateCardInternalId`, alphabet `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`), with a server-side uniqueness/collision check.
- Config constants in `join.html`: `MERSCH75_SHEET_ENDPOINT` (Apps Script deploy URL), `MERSCH75_SHEET_TOKEN` (`m75-join-9f36-secure-2026`), `MERSCH75_WEB3FORMS_TEST_KEY`, `MERSCH75_SHEET_PRODUCTION` (false during test phase).
- **Test mode:** if the surname (`Nom`) contains `TEST`, all Web3Forms mails go only to `m75.deisad@gmail.com` (never Secrétaire/Max); minors trigger 2 mails. Sheet writes go only to the Adrien test master and rows are marked `TEST`.
- Real Web3Forms mail flow (main FR key + Max DE copy) is unchanged; FLH licence form stays manual.
- **Roles & CAT-code (column J):** multi-role via checkboxes (e.g. player + referee). Player = FLH category code; Officiel H=`1`/D=`11`; referee=`10`; player+referee = `10`+category code (e.g. `102`, `109`, `1019`); pure Bénévole=`50`; Contact Famille=`214`/`215`. Referee only from U13+. `roles` array drives sheet markers AK (Off) / AM (SR). Logic in `buildCatCode` / `getRoleFlags` / `suggestTarif`.
- **Fee (`suggestTarif`):** Officiel/referee or Bénévole-with-licence → €50 even if also a player; family (2+) → €250; otherwise age-based player fee. Tarif label + hint are i18n (`tarif`/`tarifHint`).
- Full details + Apps Script code: `.windsurf/plans/join-to-sheet-automation-f4cdcc.md`.
