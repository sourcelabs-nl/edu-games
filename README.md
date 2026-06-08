# Edu Games

Een verzameling educatieve browsergames voor kinderen, gemaakt door Sourcelabs.

🎮 **Live:** https://sourcelabs-nl.github.io/edu-games/

## Games

| Game | Beschrijving | Map |
|------|--------------|-----|
| EU Topo Game | Leer de landen van Europa kennen op de kaart. | `topo/eu/` |

## Hoe het werkt

Het project is een statische site zonder build-stap. `index.html` in de root is de landingspagina met een overzicht van alle games. Elke game is een losse, op zichzelf staande HTML-pagina in een eigen submap.

De landingspagina genereert de game-tegels uit een lijst bovenin het `<script>`-blok van `index.html`. Een nieuwe game toevoegen doe je daar.

## Een nieuwe game toevoegen

1. Maak een nieuwe submap aan, bijvoorbeeld `rekenen/tafels/`, met daarin een `index.html`.
2. Voeg een entry toe aan de games-lijst in `index.html` met de velden: `title`, `desc`, `icon` (emoji), `url` (map), `tag`, `glow` (kleur) en optioneel `soon: true` voor "binnenkort".
3. Commit en push naar `main`; GitHub Pages publiceert automatisch.

## Lokaal draaien

Open `index.html` rechtstreeks in de browser, of serveer de map:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

## Hosting

De site wordt gehost via GitHub Pages vanaf de `main`-branch (root). Elke push naar `main` triggert een nieuwe build.
