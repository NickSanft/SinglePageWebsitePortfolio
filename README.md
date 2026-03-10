# WebSitePorfolio

The source code behind [nick.sanft.com](https://nick.sanft.com/) — a single-page portfolio website generated from Python + Flask + Jinja2.

All content is driven by a single JSON file. Run the dev server or export a fully self-contained static site with one command.

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

Open [http://localhost:5000](http://localhost:5000). On first run, Font Awesome and Tailwind CSS are downloaded to `output/static/` automatically.

## Files

| File | Purpose |
|---|---|
| `main.py` | Flask app, data loading, static export logic |
| `music.py` | Separate page for the Divora musician subpage |
| `templates/index.html` | Jinja2 template (SPA) |
| `website_data.json` | All site content — auto-created from dummy data if missing |
| `output/` | Generated output (gitignored) — deploy this directory |
| `requirements.txt` | `flask` and `requests` |

## Customizing Content

Edit `website_data.json` to change:

- Bio, hero image, name, subtitle
- Work experience (grouped by company)
- Skills (with Font Awesome icons)
- Certifications (with credential links)
- Projects (one featured + grid of others)
- Contact/social links (GitHub, LinkedIn, Bandcamp, Ko-fi)
- Theme colors (light and dark mode separately)

The file is gitignored. If it's missing, running `main.py` creates it from embedded dummy data.

## Static Export

The Flask app auto-exports to `output/index.html` on startup. To deploy:

1. Run `python main.py` (or `python music.py` for the music subpage)
2. Copy the `output/` folder to any static host

Asset paths are rewritten to relative paths (`static/` instead of `/static/`) so the output is fully self-contained.

## Features

- **Dark/light mode** — toggleable, persisted in `localStorage`, respects `prefers-color-scheme`
- **Typewriter effect** on the hero subtitle
- **Scroll progress bar** and back-to-top button
- **Interactive card spotlight** — radial gradient follows your mouse on hover
- **Staggered fade-in animations** on scroll (via IntersectionObserver)
- **Active nav highlight** — current section highlighted as you scroll
- **Drag-to-reorder sections** via SortableJS (keyboard accessible, order saved in `localStorage`)
- **Live theme customizer** — pick your own accent/background/text colors, saved per light/dark mode
- **Mobile hamburger nav**
- **SEO meta tags** — `og:*`, `twitter:card`, description
- **Accessibility** — skip-to-content link, ARIA labels, focus-visible styles, `prefers-reduced-motion` support
- **Resume download** button linking to a configurable PDF URL
