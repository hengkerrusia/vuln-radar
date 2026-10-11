// VulnRadar dashboard — vanilla JS, no dependencies.
(function () {
  var state = { topic: "", q: "" };
  var records = [];
  var cardsEl = document.getElementById("cards");
  var qEl = document.getElementById("q");

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function badge(r) {
    if (r.type === "lab") return '<span class="badge lab">🧪 lab</span>';
    if (r.status === "in-progress") return '<span class="badge wip">in progress</span>';
    if (r.status === "candidate") return '<span class="badge candidate">candidate</span>';
    return "";
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
    return (
      '<article class="card"><h3>' + esc(r.title) + badge(r) + "</h3>" +
      '<div class="meta">' + r.year + esc(researcher) + "</div>" +
      '<div class="topics">' + topics + "</div>" +
      summary +
      '<div class="links">' + links.join(" · ") + "</div></article>"
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

  function render() {
    var list = records.filter(function (r) {
      var okTopic = !state.topic || r.topics.indexOf(state.topic) !== -1;
      return okTopic && matches(r, state.q);
    });
    cardsEl.innerHTML = list.length
      ? list.map(card).join("")
      : '<p class="empty">No records match. Try another topic or search.</p>';
  }

  document.querySelectorAll(".filter").forEach(function (btn) {
    btn.addEventListener("click", function () {
      document.querySelectorAll(".filter").forEach(function (b) { b.classList.remove("active"); });
      btn.classList.add("active");
      state.topic = btn.getAttribute("data-topic");
      render();
    });
  });

  var deb;
  qEl.addEventListener("input", function () {
    clearTimeout(deb);
    deb = setTimeout(function () { state.q = qEl.value; render(); }, 120);
  });

  fetch("index.json")
    .then(function (res) { return res.json(); })
    .then(function (data) { records = data; render(); })
    .catch(function () {
      cardsEl.innerHTML = '<p class="empty">Could not load index.json — serve over HTTP, not file://.</p>';
    });
})();
