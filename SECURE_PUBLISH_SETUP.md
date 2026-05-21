# Secure Publish Setup

## Ziel

Der Generator soll Poster auf die Homepage veroeffentlichen koennen, ohne dass ein GitHub-Secret im Browser gespeichert wird.

## Empfohlene Architektur

1. Der Browser erzeugt Landscape- und Portrait-Poster wie bisher lokal.
2. Der Generator sendet die Base64-Bilder an einen HTTPS-Proxy-Endpoint.
3. Nur dieser Proxy besitzt das echte GitHub-Secret.
4. Der Proxy schreibt die Dateien ins Repo:
   - `Media/Hauptseite/current-matchposter.jpg`
   - `Media/Hauptseite/current-matchposter-portrait.jpg`
   - optionale Archivdateien unter `Media/Hauptseite/archive/`
5. GitHub Pages deployed wie bisher aus `main`.

## Geeignete Umsetzungen

### Option A: Cloudflare Worker

- Vorteil: klein, guenstig, schnell aufzusetzen
- Secret liegt in `wrangler secret`
- Endpoint validiert Request und ruft danach die GitHub Contents API auf

### Option B: Serverless Function

- Vercel Function, Netlify Function oder eigener kleiner API-Endpoint
- Secret liegt in Umgebungsvariablen des Hosters

### Option C: GitHub Actions Dispatch

- Browser ruft einen schmalen Endpoint auf
- Endpoint startet `workflow_dispatch`
- Das eigentliche GitHub-Secret bleibt nur in GitHub Actions Secrets

## Mindest-Sicherheitsregeln

1. Nur `https://`-Endpoint verwenden.
2. Im Browser kein GitHub PAT mehr speichern, sobald der Proxy produktiv ist.
3. Proxy auf genau dieses Repo begrenzen.
4. Nur die benoetigten Zielpfade erlauben.
5. Request-Groesse begrenzen.
6. Einfache Protokollierung pro Publish speichern.

## Request-Format des aktuellen Generators

Der Generator sendet im Proxy-Modus ein JSON mit diesem Aufbau:

```json
{
  "stamp": "230526",
  "landscapeBase64": "...",
  "portraitBase64": "...",
  "targets": {
    "landscape": "Media/Hauptseite/current-matchposter.jpg",
    "portrait": "Media/Hauptseite/current-matchposter-portrait.jpg",
    "archiveLandscape": "Media/Hauptseite/archive/matchposter-230526.jpg",
    "archivePortrait": "Media/Hauptseite/archive/matchposter-230526-portrait.jpg"
  }
}
```

## Empfohlener naechster Schritt

1. Cloudflare Worker oder Serverless Function anlegen.
2. GitHub PAT nur serverseitig als Secret hinterlegen.
3. Proxy-URL im Generator unter `Veroeffentlichungs-Einstellungen` eintragen.
4. Browser-Token-Modus danach nur noch als Notfall-Fallback verwenden.