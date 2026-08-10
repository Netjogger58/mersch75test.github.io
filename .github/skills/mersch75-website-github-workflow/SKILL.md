---
name: mersch75-website-github-workflow
description: Safely inspect and process GitHub tasks, recovery pull requests, assets, links, and deployments for the mersch75test.github.io website.
---

# Mersch75 Website GitHub Workflow

Use this skill for GitHub issues, pull requests, recovery branches, public website changes, assets, or deployment work in `Netjogger58/mersch75test.github.io`.

## Safety Rules

- Start read-only: inspect `git status`, the branch, the requested PR, and its diff.
- Do not push, merge, close, rebase, or create a PR unless the user explicitly requests that exact action.
- Preserve the static site's layout and behavior unless a visual or behavioral change is requested.
- Never rename, move, or delete a file without updating every `src`, `href`, and `url()` reference in the same change.
- Do not modify Google Sheets, external forms, or production endpoints while reviewing website code.
- Do not tidy unrelated files or archived assets.

## Recovery Pull Requests

For a recovery PR such as PR #13:

1. Compare the PR with `main` and identify all recovered changes.
2. Separate intended work from stale, generated, or accidental changes.
3. Validate links, assets, language switching, and affected forms locally.
4. Report findings before merging.
5. Merge or close only after explicit user approval.

## Validation

- Check `git status`.
- Verify all changed local references resolve on disk.
- Test the smallest affected page or script.
- For `join.html`, preserve test-mode mail routing, role/CAT-code rules, tariffs, and the disabled production Sheet switch unless explicitly requested otherwise.
- Because the site deploys publicly through GitHub Pages, push only when the user explicitly requests publication.

## Completion

- Report changed files, validation results, and unresolved risks.
- Show the exact GitHub action awaiting approval.
- Keep changes local unless the user explicitly asks to commit, push, update a PR, or merge.
