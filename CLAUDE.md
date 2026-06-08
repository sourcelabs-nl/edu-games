# CLAUDE.md

Richtlijnen voor het werken in deze repository.

## Wat dit is

Een statische verzameling educatieve browsergames, gehost op GitHub Pages
(https://sourcelabs-nl.github.io/edu-games/). Geen build-stap, geen dependencies,
geen package manager. Elke game is één op zichzelf staand `index.html`-bestand met
inline CSS en JavaScript.

## Structuur

- `index.html` — landingspagina. Genereert de game-tegels uit een games-lijst
  bovenin het `<script>`-blok.
- `<categorie>/<game>/index.html` — één game per submap (bijv. `topo/eu/`).

## Conventies

- Alle UI-teksten en documentatie zijn in het Nederlands.
- Game-pagina's zijn zelfstandig: inline CSS/JS, geen gedeelde assets of bundler.
- Gebruik relatieve paden (bijv. `topo/eu/`) zodat het werkt onder het
  `/edu-games/`-subpad van GitHub Pages.
- Houd elke game in zijn eigen map; meng geen games in één bestand.

## Een game toevoegen

1. Nieuwe submap met `index.html`.
2. Entry toevoegen aan de games-lijst in `index.html`
   (`title`, `desc`, `icon`, `url`, `tag`, `glow`, optioneel `soon: true`).

## Deployen

Push naar `main`; GitHub Pages bouwt en publiceert automatisch vanaf de root.
Commit of push alleen wanneer de gebruiker daarom vraagt.

## Lokaal testen

```bash
python3 -m http.server 8000
```
