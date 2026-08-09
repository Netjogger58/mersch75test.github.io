# Working model for safe continuation

This repository now uses a safety-first flow so work from different tools/agents stays recoverable.

## 1) Branch model
- Keep one long-lived integration branch (for example `recovery/...`).
- Create short topic branches from that integration branch.
- Merge topic branches back frequently in small increments.
- Create/update integration branch from remote main when needed:
  - `scripts/start_integration_branch.sh main`

## 2) Draft PR early
- Open a draft PR as soon as a branch has meaningful work:
  - `scripts/open_draft_pr.sh main "WIP: <title>"`

## 3) Required preflight before push/merge
- Run:
  - `scripts/preflight_check.sh`
- This checks:
  - broken local `href/src` references
  - new live-page dependencies on legacy `Media/`

## 4) Asset/source policy
- Keep live assets under `assets/shared/` and `assets/pages/<page>/`.
- Treat `Media/` as legacy/archive input only.

## 5) API endpoint standard
- Shared config lives in [js/site-config.js](/Volumes/Prog+Daten/Project%20HP%20M75.worktrees/github-pages-setup/js/site-config.js).
- Web form submissions should use `window.M75_CONFIG.WEB3FORMS_ENDPOINT`.
- Backend calls should use absolute URLs based on `window.M75_CONFIG.API_BASE`.

## 6) Recovery snapshot before risky operations
- Before heavy merge/rebase:
  - `scripts/create_recovery_snapshot.sh`
- This creates and pushes a backup branch under `backup/<timestamp>-<branch>`.
