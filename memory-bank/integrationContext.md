# Integration Context - mersch75.lu

## 1. Verknüpfung zu Vereins-OS
- mersch75.lu ist das Frontend (gehostet auf GitHub Pages).
- Es ruft dynamische Daten (REST/GraphQL) vom Hetzner-Server (Vereins-OS) ab.
- Base-URL für API-Aufrufe in Produktion: `https://api.mersch75.lu`
- Base-URL für lokale Entwicklung: `http://localhost:8080`

## 2. Verknüpfung zu M75-VideoStudio
- Konsumiert finale Media-Assets (Videos, Overlays), die im Repository `M75-VideoStudio` gerendert und exportiert wurden.
- Speicherort für importierte Assets: `/assets/media/`

## 3. GitHub Pages Deployment
- Der Code in diesem Repository wird aus dem Root-Verzeichnis auf mersch75.lu bereitgestellt.
- DNS-Routing für mersch75.lu ist auf GitHub Pages konfiguriert.
- Das Hetzner-Backend muss stets erreichbar sein, damit dynamische Inhalte der Homepage laden.
