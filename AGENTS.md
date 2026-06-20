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
