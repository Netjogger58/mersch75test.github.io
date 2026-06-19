# Asset Structure (Safe Migration)

This folder is the new, structured home for website assets.

## Target Layout

- `assets/shared/images/` -> images used on multiple pages
- `assets/shared/icons/` -> icons used on multiple pages
- `assets/shared/logos/` -> logos used on multiple pages
- `assets/pages/<page>/images/` -> images used only on one page

## Migration Rules

1. Do not break existing URLs during migration.
2. Copy first, then switch references, then verify, then delete old files later.
3. Shared assets must exist only once in final state.
4. Page-specific assets must be placed under `assets/pages/<page>/images/`.
5. Avoid spaces in new file names; use lowercase with dashes.

## Rollout Strategy

1. Build an asset usage map from HTML/CSS/JS.
2. Classify files:
   - used by 2+ pages -> shared
   - used by 1 page -> page-local
3. Copy files to new destinations.
4. Rewrite references automatically.
5. Validate links and missing files.
6. Deploy.
7. Remove old duplicates in a separate cleanup pass.
