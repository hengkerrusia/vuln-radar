#!/usr/bin/env python3
"""VulnRadar static site generator — stdlib only.

Reads records/*.md (YAML frontmatter), generates:
  docs/index.json   — full dataset
  docs/index.html   — signals dashboard (loads app.js + index.json)
  docs/<year>.html  — yearly archive pages (plain HTML, no JS)
  docs/style.css, docs/app.js — copied from assets/

Usage: python3 build.py
"""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RECORDS_DIR = ROOT / "records"
ASSETS_DIR = ROOT / "assets"
OUT_DIR = ROOT / "docs"
SITE_NAME = "VulnRadar"
TAGLINE = "Web hacking research signals — what is getting louder."
LAB_REPO = "https://github.com/hengkerrusia/fixthecode"


def parse_frontmatter(text):
    """Parse a minimal YAML-subset frontmatter. Returns (dict, body)."""
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("missing frontmatter")
    data = {}
    for line in m.group(1).splitlines():
        line = line.strip()
        if not line or line.startswith("#") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            if not inner:
                data[key] = []
            else:
                data[key] = [
                    v.strip().strip('"').strip("'") for v in inner.split(",")
                ]
        elif val.startswith('"') and val.endswith('"'):
            data[key] = val[1:-1]
        elif val.startswith("'") and val.endswith("'"):
            data[key] = val[1:-1]
        elif re.fullmatch(r"-?\d+", val):
            data[key] = int(val)
        else:
            data[key] = val
    return data, m.group(2).strip()


def load_records():
    records = []
    for path in sorted(RECORDS_DIR.glob("*.md")):
        fm, _ = parse_frontmatter(path.read_text(encoding="utf-8"))
        for field in ("title", "year", "url", "topics", "type"):
            if field not in fm:
                raise ValueError(f"{path.name}: missing field '{field}'")
        fm["slug"] = path.stem
        fm.setdefault("status", "candidate" if fm["type"] == "finding" else "shipped")
        fm.setdefault("lab_url", "")
        fm.setdefault("researcher", "")
        fm.setdefault("summary", "")
        records.append(fm)
    records.sort(key=lambda r: (-r["year"], r["title"].lower()))
    return records


def esc(s):
    return html.escape(str(s), quote=True)


def topic_counts(records):
    counts = {}
    for r in records:
        for t in r["topics"]:
            counts[t] = counts.get(t, 0) + 1
    return dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))


def year_counts(records):
    counts = {}
    for r in records:
        counts[r["year"]] = counts.get(r["year"], 0) + 1
    return dict(sorted(counts.items()))


PAGE_HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} — {site}</title>
<link rel="stylesheet" href="{css_path}style.css">
</head>
<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{home}">{site}</a>
    <span class="tagline">{tagline}</span>
    <nav><a href="{home}">Signals</a><a href="{archive}">Archive</a></nav>
  </div>
</header>
<main class="wrap">
"""


def render_card(r):
    topics = " ".join(
        f'<span class="topic">{esc(t)}</span>' for t in r["topics"]
    )
    badge = ""
    if r["type"] == "lab":
        badge = '<span class="badge lab">🧪 lab</span>'
    elif r["status"] == "in-progress":
        badge = '<span class="badge wip">in progress</span>'
    elif r["status"] == "candidate":
        badge = '<span class="badge candidate">candidate</span>'
    links = [f'<a href="{esc(r["url"])}" target="_blank" rel="noopener">Read the original ↗</a>']
    if r.get("lab_url"):
        links.append(f'<a href="{esc(r["lab_url"])}" target="_blank" rel="noopener">🧪 Try the lab ↗</a>')
    researcher = f" — {esc(r['researcher'])}" if r["researcher"] else ""
    summary = f"<p>{esc(r['summary'])}</p>" if r["summary"] else ""
    return f"""<article class="card">
  <h3>{esc(r["title"])}{badge}</h3>
  <div class="meta">{r["year"]}{researcher}</div>
  <div class="topics">{topics}</div>
  {summary}
  <div class="links">{" · ".join(links)}</div>
</article>"""


def build_dashboard(records):
    tcounts = topic_counts(records)
    ycounts = year_counts(records)
    years = sorted(ycounts)
    labs = sum(1 for r in records if r["type"] == "lab")
    topics_json = json.dumps(sorted(tcounts))
    stats = (
        f'<div class="stats">'
        f'<div><b>{len(records)}</b><span>records</span></div>'
        f'<div><b>{labs}</b><span>labs</span></div>'
        f'<div><b>{len(tcounts)}</b><span>topics</span></div>'
        f'<div><b>{years[0]}–{years[-1]}</b><span>years</span></div>'
        f"</div>"
    )
    filters = ['<button class="filter active" data-topic="">All</button>'] + [
        f'<button class="filter" data-topic="{esc(t)}">{esc(t)} <i>{c}</i></button>'
        for t, c in tcounts.items()
    ]
    # SVG bar chart: records per year
    maxc = max(ycounts.values())
    bw, gap, hmax = 44, 10, 120
    bars = []
    x = 0
    for y, c in ycounts.items():
        h = max(4, round(c / maxc * hmax))
        ypos = hmax - h
        bars.append(
            f'<a href="{y}.html"><g class="bar" data-year="{y}">'
            f'<rect x="{x}" y="{ypos}" width="{bw}" height="{h}"/>'
            f'<text x="{x + bw/2}" y="{hmax + 16}" text-anchor="middle">{y}</text>'
            f'<text x="{x + bw/2}" y="{ypos - 6}" text-anchor="middle" class="count">{c}</text>'
            f"</g></a>"
        )
        x += bw + gap
    width = x
    chart = (
        f'<svg class="chart" viewBox="0 -24 {width} {hmax + 44}" '
        f'style="max-width:{width}px" role="img" aria-label="records per year">'
        + "".join(bars) + "</svg>"
    )
    return (
        PAGE_HEAD.format(title="Signals", site=SITE_NAME, tagline=TAGLINE,
                         css_path="", home="index.html", archive="archive.html")
        + f"<h1>Signals</h1><p class=\"lede\">What is getting louder in web hacking research — "
        + f"every record below links to the original publication, and records with a "
        + f"🧪 badge link to a hands-on <a href=\"{LAB_REPO}\">fixthecode</a> lab.</p>"
        + stats
        + "<h2>Records per year</h2>" + chart
        + "<h2>Topics</h2><div class=\"filters\">" + "".join(filters) + "</div>"
        + '<input id="q" type="search" placeholder="Filter: title, researcher, topic…  (try tag:smuggling)">'
        + '<div id="cards"></div>'
        + '<script>const TOPICS = ' + topics_json + ';</script>\n'
        + '<script src="app.js"></script>\n</main>\n'
        + '<footer class="wrap"><p>Curated research index. Every entry links to the original publication. '
        + 'Labs live at <a href="' + LAB_REPO + '">fixthecode</a>.</p></footer>\n</body>\n</html>\n'
    )


def build_archive_index(records):
    ycounts = year_counts(records)
    items = "".join(
        f'<li><a href="{y}.html">{y}</a> <span>{c} records</span></li>'
        for y, c in sorted(ycounts.items(), reverse=True)
    )
    return (
        PAGE_HEAD.format(title="Archive", site=SITE_NAME, tagline=TAGLINE,
                         css_path="", home="index.html", archive="archive.html")
        + "<h1>Archive</h1><p class=\"lede\">Yearly collections.</p>"
        + f"<ul class=\"years\">{items}</ul>\n</main>\n</body>\n</html>\n"
    )


def build_year_page(year, records):
    cards = "\n".join(render_card(r) for r in records)
    return (
        PAGE_HEAD.format(title=str(year), site=SITE_NAME, tagline=TAGLINE,
                         css_path="", home="index.html", archive="archive.html")
        + f"<h1>{year}</h1><p class=\"lede\">{len(records)} records.</p>"
        + cards + "\n</main>\n</body>\n</html>\n"
    )


def main():
    records = load_records()
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT_DIR / "index.html").write_text(build_dashboard(records), encoding="utf-8")
    (OUT_DIR / "archive.html").write_text(build_archive_index(records), encoding="utf-8")
    by_year = {}
    for r in records:
        by_year.setdefault(r["year"], []).append(r)
    for year, recs in by_year.items():
        (OUT_DIR / f"{year}.html").write_text(build_year_page(year, recs), encoding="utf-8")
    for name in ("style.css", "app.js"):
        shutil.copy(ASSETS_DIR / name, OUT_DIR / name)
    print(f"built {len(records)} records → {OUT_DIR}/ "
          f"({len(by_year)} yearly pages)")


if __name__ == "__main__":
    main()
