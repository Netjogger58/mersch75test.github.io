# GitHub Actions CI Workflow

> **Hinweis:** Diese Datei konnte nicht über `git push` deployed werden, weil der
> Git-OAuth-Token keine `workflow`-Berechtigung hat. Sie muss **manuell** über die
> GitHub-Web-UI oder per Token mit `workflow`-Scope hinzugefügt werden.

## Anleitung

### Option A: Über GitHub Web-UI
1. Gehe zu https://github.com/Netjogger58/mersch75test.github.io
2. Klicke "Add file" → "Create new file"
3. Dateiname: `.github/workflows/ci.yml`
4. Inhalt einfügen (siehe `ci.yml.template` weiter unten)
5. Committen

### Option B: Lokal mit workflow-Scope
```bash
# Token muss workflow scope haben
git remote set-url origin https://<TOKEN>@github.com/Netjogger58/mersch75test.github.io.git
cp .github/workflows/ci.yml.template .github/workflows/ci.yml
git add .github/workflows/ci.yml
git commit -m "ci: add GitHub Actions workflow"
git push
```

## Workflow-Inhalt (`ci.yml.template`)

```yaml
name: Lint & Validate

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  js-syntax:
    name: JS Syntax Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '22'
      - run: node tools/lint-js.cjs
```
