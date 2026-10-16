// VulnRadar dashboard — vanilla JS, no dependencies.
(function () {
  var state = { topic: "", q: "", sort: "newest", year: null };
  var records = [];
  var cardsEl = document.getElementById("cards");
  var qEl = document.getElementById("q");
  var countEl = document.getElementById("count");
  var sortEl = document.getElementById("sort");
  var activeEl = document.getElementById("activefilters");

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  // "new" = added to the index within the last 30 days.
  function isNew(r) {
    if (!r.added) return false;
    var t = Date.parse(r.added + "T00:00:00");
    if (isNaN(t)) return false;
    var now = Date.now();
    return t <= now + 864e5 && now - t < 30 * 864e5;
  }

  function statusClass(r) {
    if (r.type === "lab") return "lab";
    if (r.status === "candidate") return "candidate";
    if (r.status === "in-progress") return "wip";
    return "";
  }

  function badge(r) {
    var b = "";
    if (r.type === "lab") b = '<span class="badge lab">🧪 lab</span>';
    else if (r.status === "in-progress") b = '<span class="badge wip">in progress</span>';
    else if (r.status === "candidate") b = '<span class="badge candidate">candidate</span>';
    if (isNew(r)) b += '<span class="badge new">new</span>';
    return b;
  }

  function citeText(r) {
    var who = r.researcher ? " — " + r.researcher : "";
    return "[" + r.title + who + " (" + r.year + ")](" + r.url + ")";
  }

  function card(r) {
    var topics = r.topics.map(function (t) {
      return '<span class="topic">' + esc(t) + "</span>";
    }).join("");
    var links = [
      '<a href="' + esc(r.url) + '" target="_blank" rel="noopener">Read the original ↗</a>'
    ];
    if (r.lab_url) {
      links.push('<a href="' + esc(r.lab_url) + '" target="_blank" rel="noopener">🧪 Try the lab ↗</a>');
    }
    var researcher = r.researcher ? " — " + esc(r.researcher) : "";
    var summary = r.summary ? "<p>" + esc(r.summary) + "</p>" : "";
    var cite = '<button class="citebtn" data-slug="' + esc(r.slug) +
      '" title="Copy citation as Markdown">⧉ cite</button>';
    return (
      '<article class="card ' + statusClass(r) + '"><h3>' + esc(r.title) + badge(r) + "</h3>" +
      '<div class="meta">' + r.year + esc(researcher) + "</div>" +
      '<div class="topics">' + topics + "</div>" +
      summary +
      '<div class="links">' + links.join(" · ") + " · " + cite + "</div></article>"
    );
  }

  // Supports "tag:smuggling" syntax like webhacklist's global search.
  function matches(r, q) {
    q = q.trim().toLowerCase();
    if (!q) return true;
    var m = q.match(/^tag:(.+)$/);
    if (m) {
      var t = m[1];
      return r.topics.some(function (x) { return x.toLowerCase().indexOf(t) !== -1; });
    }
    var hay = (r.title + " " + r.researcher + " " + r.topics.join(" ") + " " + (r.summary || "")).toLowerCase();
    return q.split(/\s+/).every(function (w) { return hay.indexOf(w) !== -1; });
  }

  function filtered() {
    return records.filter(function (r) {
      var okTopic = !state.topic || r.topics.indexOf(state.topic) !== -1;
      var okYear = !state.year || r.year === state.year;
      return okTopic && okYear && matches(r, state.q);
    });
  }

  function titleCmp(a, b) {
    return a.title.toLowerCase().localeCompare(b.title.toLowerCase());
  }

  function sortList(list) {
    var l = list.slice();
    if (state.sort === "az") l.sort(titleCmp);
    else if (state.sort === "oldest") l.sort(function (a, b) { return a.year - b.year || titleCmp(a, b); });
    else l.sort(function (a, b) { return b.year - a.year || titleCmp(a, b); });
    return l;
  }

  function syncHash() {
    var p = [];
    if (state.topic) p.push("topic=" + encodeURIComponent(state.topic));
    if (state.q) p.push("q=" + encodeURIComponent(state.q));
    if (state.sort !== "newest") p.push("sort=" + state.sort);
    if (state.year) p.push("year=" + state.year);
    history.replaceState(null, "", p.length ? "#" + p.join("&") : location.pathname + location.search);
  }

  function readHash() {
    var h = location.hash.replace(/^#/, "");
    if (!h) return;
    h.split("&").forEach(function (kv) {
      var i = kv.indexOf("=");
      if (i < 0) return;
      var k = kv.slice(0, i), v = decodeURIComponent(kv.slice(i + 1));
      if (k === "topic") state.topic = v;
      else if (k === "q") state.q = v;
      else if (k === "sort" && ["newest", "oldest", "az"].indexOf(v) >= 0) state.sort = v;
      else if (k === "year" && /^\d{4}$/.test(v)) state.year = parseInt(v, 10);
    });
  }

  function setYear(y) {
    state.year = y;
    document.querySelectorAll(".chart .bar").forEach(function (g) {
      var on = state.year && parseInt(g.getAttribute("data-year"), 10) === state.year;
      g.classList.toggle("active", !!on);
      g.setAttribute("aria-pressed", on ? "true" : "false");
    });
    render();
  }

  function render() {
    var list = sortList(filtered());
    countEl.textContent = "showing " + list.length + " of " + records.length + " records";
    activeEl.innerHTML = state.year
      ? '<button class="yearchip" id="clearyear" title="clear year filter">' + state.year + " ×</button>"
      : "";
    var cy = document.getElementById("clearyear");
    if (cy) cy.addEventListener("click", function () { setYear(null); });
    cardsEl.innerHTML = list.length
      ? list.map(card).join("")
      : '<p class="empty">No records match. Try another topic or search.</p>';
    syncHash();
  }

  // topic pill filters
  document.querySelectorAll(".filter").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".filter").forEach(function (b) {
        b.classList.remove("active");
        b.setAttribute("aria-pressed", "false");
      });
      btn.classList.add("active");
      btn.setAttribute("aria-pressed", "true");
      state.topic = btn.getAttribute("data-topic");
      render();
    });
  });

  // year bars = in-place filter
  document.querySelectorAll(".chart .bar").forEach(function (g) {
    function toggle() {
      var y = parseInt(g.getAttribute("data-year"), 10);
      setYear(state.year === y ? null : y);
    }
    g.addEventListener("click", toggle);
    g.addEventListener("keydown", function (ev) {
      if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); toggle(); }
    });
  });

  sortEl.addEventListener("change", function () {
    state.sort = sortEl.value;
    render();
  });

  var deb;
  qEl.addEventListener("input", function () {
    clearTimeout(deb);
    deb = setTimeout(function () { state.q = qEl.value; render(); }, 120);
  });

  // "/" focuses search, GitHub-style
  document.addEventListener("keydown", function (ev) {
    if (ev.key !== "/") return;
    var tag = document.activeElement ? document.activeElement.tagName : "";
    if (/^(INPUT|TEXTAREA|SELECT)$/i.test(tag)) return;
    ev.preventDefault();
    qEl.focus();
  });

  // copy citation (event delegation — cards re-render on filter)
  cardsEl.addEventListener("click", function (ev) {
    var b = ev.target.closest(".citebtn");
    if (!b) return;
    var r = null;
    for (var i = 0; i < records.length; i++) {
      if (records[i].slug === b.getAttribute("data-slug")) { r = records[i]; break; }
    }
    if (!r) return;
    var txt = citeText(r);
    function done() {
      b.textContent = "✓ copied";
      setTimeout(function () { b.textContent = "⧉ cite"; }, 1500);
    }
    function fallback() {
      var ta = document.createElement("textarea");
      ta.value = txt;
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand("copy"); } catch (e) {}
      document.body.removeChild(ta);
      done();
    }
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(txt).then(done, fallback);
    } else {
      fallback();
    }
  });

  function download(name, mime, text) {
    var a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([text], { type: mime }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    setTimeout(function () { URL.revokeObjectURL(a.href); a.remove(); }, 500);
  }

  function csvEsc(v) {
    v = String(v == null ? "" : v);
    return /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
  }

  document.getElementById("exp-json").addEventListener("click", function () {
    download("vulnradar.json", "application/json", JSON.stringify(sortList(filtered()), null, 2));
  });

  document.getElementById("exp-csv").addEventListener("click", function () {
    var rows = [["title", "year", "researcher", "type", "status", "topics", "url", "lab_url", "summary"]];
    sortList(filtered()).forEach(function (r) {
      rows.push([
        r.title, r.year, r.researcher, r.type, r.status,
        r.topics.join("; "), r.url, r.lab_url || "", r.summary || ""
      ].map(csvEsc));
    });
    download("vulnradar.csv", "text/csv", rows.map(function (x) { return x.join(","); }).join("\n"));
  });

  // restore shared state from URL hash
  readHash();
  qEl.value = state.q;
  sortEl.value = state.sort;
  if (state.topic) {
    document.querySelectorAll(".filter").forEach(function (b) {
      var on = b.getAttribute("data-topic") === state.topic;
      b.classList.toggle("active", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
  } else {
    document.querySelectorAll(".filter").forEach(function (b, i) {
      b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
    });
  }

  fetch("index.json")
    .then(function (res) { return res.json(); })
    .then(function (data) {
      records = data;
      setYear(state.year); // applies bar highlight, then renders
    })
    .catch(function () {
      cardsEl.innerHTML = '<p class="empty">Could not load index.json — serve over HTTP, not file://.</p>';
    });
})();
