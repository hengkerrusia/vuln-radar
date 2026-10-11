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


def split_list(inner):
    """Split a [...] list on commas, ignoring commas inside quotes."""
    items, cur, quote = [], "", None
    for ch in inner:
        if quote:
            cur += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote, cur = ch, cur + ch
        elif ch == ",":
            items.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        items.append(cur.strip())
    return [v.strip().strip('"').strip("'") for v in items]


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
            data[key] = [] if not inner else split_list(inner)
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
        fm.setdefault("techniques", [])
        fm.setdefault("related", [])
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
    <nav><a href="{home}">Signals</a><a href="board.html">Board</a><a href="{archive}">Archive</a></nav>
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


def lab_number(slug):
    m = re.match(r"lab-(\d+)-", slug)
    return int(m.group(1)) if m else 0


def parse_related(records):
    """Parse 'slug: label' related strings into (from, to, label) edges, deduped."""
    by_slug = {r["slug"] for r in records}
    edges, seen = [], set()
    for r in records:
        for item in r.get("related", []):
            target, _, label = item.partition(": ")
            target = target.strip()
            if target not in by_slug:
                print(f"  warning: {r['slug']} -> unknown related '{target}'")
                continue
            key = tuple(sorted((r["slug"], target)))
            if key in seen:
                continue
            seen.add(key)
            edges.append((r["slug"], target, label.strip()))
    return edges


def build_board(records):
    tcounts = {}
    for r in records:
        for t in r.get("techniques", []):
            tcounts[t] = tcounts.get(t, 0) + 1
    techs = sorted(tcounts, key=lambda t: (-tcounts[t], t))

    W, PAD = 1200, 90
    tech_pos = {}
    for ri, row in enumerate([techs[:8], techs[8:]]):
        y = 66 + ri * 66
        n = len(row)
        for i, t in enumerate(row):
            x = PAD + i * ((W - 2 * PAD) / (n - 1)) if n > 1 else W / 2
            tech_pos[t] = (round(x, 1), y)

    series = [
        ("Labs 1\u20135 \u00b7 cache & hop-by-hop", [1, 2, 3, 4, 5]),
        ("Labs 6\u201310 \u00b7 request smuggling / desync", [6, 7, 8, 9, 10]),
        ("Labs 11\u201314 \u00b7 CSPT", [11, 12, 13, 14]),
        ("Labs 15\u201318 \u00b7 CRLF", [15, 16, 17, 18]),
        ("Lab 19 \u00b7 file inclusion / path traversal", [19]),
    ]
    node_pos, captions = {}, []
    y = 300
    for caption, nums in series:
        captions.append((caption, y - 52))
        n = len(nums)
        for i, num in enumerate(nums):
            x = PAD + 10 + i * ((W - 2 * PAD - 20) / (n - 1)) if n > 1 else W / 2
            slug = next(r["slug"] for r in records if lab_number(r["slug"]) == num)
            node_pos[slug] = (round(x, 1), y)
        y += 170
    findings = [r for r in records if r["type"] == "finding"]
    if findings:
        captions.append(("Candidates \u00b7 not yet labs", y - 52))
        n = len(findings)
        for i, r in enumerate(findings):
            x = PAD + 10 + i * ((W - 2 * PAD - 20) / (n - 1)) if n > 1 else W / 2
            node_pos[r["slug"]] = (round(x, 1), y)
        y += 170
    board_h = y - 170 + 110

    parts = []
    # record -> technique strings (under nodes)
    for r in records:
        lx, ly = node_pos[r["slug"]]
        for t in r.get("techniques", []):
            tx, ty = tech_pos[t]
            cx, cy = round((lx + tx) / 2, 1), min(ly, ty) - 34
            parts.append(
                f'<path class="string" data-lab="{r["slug"]}" data-tech="{esc(t)}" '
                f'd="M {lx} {ly - 30} Q {cx} {cy} {tx} {ty + 18}">'
                f'<title>{esc(r["title"])} \u2014 uses \u2014 {esc(t)}</title></path>'
            )
    # record -> record links
    for a, b, label in parse_related(records):
        x1, y1 = node_pos[a]
        x2, y2 = node_pos[b]
        if y1 == y2:
            cx, cy = (x1 + x2) / 2, y1 - 84
        else:
            cx, cy = (x1 + x2) / 2, (y1 + y2) / 2 - 90
        parts.append(
            f'<path class="link" data-a="{a}" data-b="{b}" '
            f'd="M {x1} {y1 - 30} Q {round(cx,1)} {round(cy,1)} {x2} {y2 - 30}">'
            f'<title>{esc(label)}</title></path>'
        )
    # technique pins
    for t, (x, y) in tech_pos.items():
        parts.append(
            f'<g class="technode" data-tech="{esc(t)}">'
            f'<circle class="pin" cx="{x}" cy="{y}" r="8"/>'
            f'<text class="techlabel" x="{x}" y="{y + 24}" text-anchor="middle">{esc(t)}</text>'
            f'<text class="techcount" x="{x}" y="{y + 38}" text-anchor="middle">{tcounts[t]} uses</text>'
            f'</g>'
        )
    # record nodes
    for r in records:
        x, y = node_pos[r["slug"]]
        num = lab_number(r["slug"])
        short = r["title"] if len(r["title"]) <= 26 else r["title"][:25] + "\u2026"
        if r["type"] == "lab":
            rect_class, node_label = "labrect", f"Lab {num} \U0001f9ea"
        else:
            rect_class, node_label = "labrect candidate", "\u25cb candidate"
        parts.append(
            f'<g class="labnode" data-lab="{r["slug"]}">'
            f'<rect class="{rect_class}" x="{x - 88}" y="{y - 30}" width="176" height="60" rx="10"/>'
            f'<text class="labnum" x="{x}" y="{y - 6}" text-anchor="middle">{esc(node_label)}</text>'
            f'<text class="labtitle" x="{x}" y="{y + 14}" text-anchor="middle">{esc(short)}</text>'
            f'</g>'
        )
    # series captions
    for caption, y in captions:
        parts.append(
            f'<text class="series" x="{W/2}" y="{y}" text-anchor="middle">{esc(caption)}</text>'
        )

    svg = (
        f'<svg id="board" viewBox="0 0 {W} {board_h}" role="img" '
        f'aria-label="technique relationship board">'
        + "".join(parts) + "</svg>"
    )
    data = {
        r["slug"]: {
            "n": lab_number(r["slug"]),
            "title": r["title"],
            "researcher": r["researcher"],
            "year": r["year"],
            "summary": r["summary"],
            "url": r["url"],
            "lab_url": r.get("lab_url", ""),
            "techniques": r.get("techniques", []),
            "badge": "lab" if r["type"] == "lab" else r.get("status", ""),
        }
        for r in records
    }
    tech_labs = {}
    for r in records:
        for t in r.get("techniques", []):
            tech_labs.setdefault(t, []).append(r["slug"])

    return (
        PAGE_HEAD.format(title="Board", site=SITE_NAME, tagline=TAGLINE,
                         css_path="", home="index.html", archive="archive.html")
        + "<h1>Investigation Board</h1>"
        + '<p class="lede">Every string is a claim: red strings tie a lab or candidate '
        + "to the techniques it uses, amber strings tie records that evolve or chain into each other "
        + "(hover for why). Click any node for details.</p>"
        + '<div class="legend"><span><i class="sw red"></i>uses technique</span>'
        + '<span><i class="sw amber"></i>related lab</span></div>'
        + '<div class="boardwrap">' + svg
        + '<aside id="panel" hidden></aside></div>'
        + "<script>const BOARD_DATA = " + json.dumps(data, ensure_ascii=False) + ";</script>\n"
        + "<script>const BOARD_TECH = " + json.dumps(tech_labs, ensure_ascii=False) + ";</script>\n"
        + '<script src="board.js"></script>\n</main>\n'
        + '<footer class="wrap"><p>Curated research index. Every entry links to the original publication. '
        + 'Labs live at <a href="' + LAB_REPO + '">fixthecode</a>.</p></footer>\n</body>\n</html>\n'
    )


def main():
    records = load_records()
    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "index.json").write_text(
        json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    (OUT_DIR / "index.html").write_text(build_dashboard(records), encoding="utf-8")
    (OUT_DIR / "board.html").write_text(build_board(records), encoding="utf-8")
    (OUT_DIR / "archive.html").write_text(build_archive_index(records), encoding="utf-8")
    by_year = {}
    for r in records:
        by_year.setdefault(r["year"], []).append(r)
    for year, recs in by_year.items():
        (OUT_DIR / f"{year}.html").write_text(build_year_page(year, recs), encoding="utf-8")
    for name in ("style.css", "app.js", "board.js"):
        shutil.copy(ASSETS_DIR / name, OUT_DIR / name)
    print(f"built {len(records)} records → {OUT_DIR}/ "
          f"({len(by_year)} yearly pages)")


if __name__ == "__main__":
    main()
