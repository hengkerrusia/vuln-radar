# VulnRadar

Web hacking research signals — what is getting louder.

A curated index of web security research (write-ups, advisories, CVEs) with a
signals dashboard, yearly archives, and — where a hands-on lab exists — a direct
link to try it in [fixthecode](https://github.com/hengkerrusia/fixthecode).

## Layout

- `records/` — one Markdown file per record, YAML frontmatter. This is the source of truth.
- `build.py` — stdlib-only static site generator. No dependencies, no build tools.
- `assets/` — `style.css`, `app.js` (vanilla JS, no frameworks).
- `docs/` — generated site. Served by GitHub Pages.

## Record format

```yaml
---
title: "HTTP/2: The Sequel is Always Worse"
researcher: "James Kettle"
year: 2021
url: "https://portswigger.net/research/http2"   # original publication — always link the original
topics: ["Request Smuggling"]                    # free-form, keep consistent
type: "finding"                                   # finding | lab
status: "candidate"                               # candidate | in-progress | shipped
lab_url: ""                                       # set when a lab ships
summary: "One or two lines on the technique."
---
```

Rules (stolen from webhacklist, adapted):

- `url` must be the **original publication** — never a rehash, never Medium.
- One record per research item, not per CVE instance, unless the instance adds a new sub-technique.
- `topics` reuse the fixthecode lab categories where possible.

## Build

```bash
python3 build.py
```

Output goes to `docs/`. Commit it; GitHub Pages serves `docs/` on `main`.

## Going live

1. Create repo `hengkerrusia/vuln-radar`, push this directory.
2. Settings → Pages → Deploy from branch → `main` → `/docs`.
3. Custom domain: add `vuln-radar.com` (+ `CNAME` file with the domain).
4. Optional: a "Submit research" button can point at a prefilled GitHub issue,
   webhacklist-style — no backend needed.

## Feeding it

- New vuln-watch findings: drop a `records/<slug>.md` with `type: finding`,
  `status: candidate`.
- When a lab ships: flip to `type: lab`, `status: shipped`, set `lab_url`.
