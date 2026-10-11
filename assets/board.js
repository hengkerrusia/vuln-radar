// VulnRadar investigation board — vanilla JS, no dependencies.
(function () {
  var svg = document.getElementById("board");
  var panel = document.getElementById("panel");
  if (!svg || !panel) return;

  function esc(s) {
    return String(s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function clearHl() {
    svg.querySelectorAll(".hl").forEach(function (el) { el.classList.remove("hl"); });
    svg.querySelectorAll(".dim").forEach(function (el) { el.classList.remove("dim"); });
  }

  function highlight(kind, id) {
    clearHl();
    var edges = [];
    svg.querySelectorAll("path.string, path.link").forEach(function (p) {
      var hit = kind === "lab"
        ? (p.getAttribute("data-lab") === id || p.getAttribute("data-a") === id || p.getAttribute("data-b") === id)
        : p.getAttribute("data-tech") === id;
      if (hit) { p.classList.add("hl"); edges.push(p); }
    });
    var keep = {};
    keep[kind + ":" + id] = true;
    edges.forEach(function (p) {
      ["data-lab", "data-tech", "data-a", "data-b"].forEach(function (a) {
        var v = p.getAttribute(a);
        if (v) keep[(a === "data-tech" ? "tech:" : "lab:") + v] = true;
      });
    });
    svg.querySelectorAll(".labnode, .technode").forEach(function (g) {
      var gid = g.classList.contains("labnode")
        ? "lab:" + g.getAttribute("data-lab")
        : "tech:" + g.getAttribute("data-tech");
      g.classList.add(keep[gid] ? "hl" : "dim");
    });
    svg.querySelectorAll("path.string, path.link").forEach(function (p) {
      if (!p.classList.contains("hl")) p.classList.add("dim");
    });
  }

  function labPanel(slug) {
    var d = BOARD_DATA[slug];
    if (!d) return;
    var badge = d.badge === "lab" ? ' <span class="badge lab">🧪 lab</span>' : "";
    var techs = d.techniques.map(function (t) {
      return '<span class="topic">' + esc(t) + "</span>";
    }).join("");
    var links = '<a href="' + esc(d.url) + '" target="_blank" rel="noopener">Read the original ↗</a>';
    if (d.lab_url) {
      links += ' · <a href="' + esc(d.lab_url) + '" target="_blank" rel="noopener">🧪 Try the lab ↗</a>';
    }
    panel.innerHTML =
      '<button class="x" aria-label="close">×</button>' +
      "<h3>Lab " + d.n + badge + "</h3>" +
      "<p><b>" + esc(d.title) + "</b></p>" +
      '<div class="meta">' + d.year + (d.researcher ? " — " + esc(d.researcher) : "") + "</div>" +
      '<div class="topics">' + techs + "</div>" +
      (d.summary ? "<p>" + esc(d.summary) + "</p>" : "") +
      '<div class="links">' + links + "</div>";
    panel.hidden = false;
  }

  function techPanel(name) {
    var labs = BOARD_TECH[name] || [];
    var items = labs.map(function (slug) {
      var d = BOARD_DATA[slug];
      return '<li><a href="#" data-goto="' + slug + '">Lab ' + d.n + " — " + esc(d.title) + "</a></li>";
    }).join("");
    panel.innerHTML =
      '<button class="x" aria-label="close">×</button>' +
      "<h3>📌 " + esc(name) + "</h3>" +
      "<p>" + labs.length + " lab" + (labs.length === 1 ? "" : "s") + " use this technique:</p>" +
      "<ul>" + items + "</ul>";
    panel.hidden = false;
  }

  svg.addEventListener("click", function (ev) {
    var lab = ev.target.closest(".labnode");
    var tech = ev.target.closest(".technode");
    if (lab) {
      var slug = lab.getAttribute("data-lab");
      highlight("lab", slug);
      labPanel(slug);
    } else if (tech) {
      var name = tech.getAttribute("data-tech");
      highlight("tech", name);
      techPanel(name);
    } else {
      clearHl();
      panel.hidden = true;
    }
  });

  svg.addEventListener("mouseover", function (ev) {
    var lab = ev.target.closest(".labnode");
    var tech = ev.target.closest(".technode");
    if (lab) highlight("lab", lab.getAttribute("data-lab"));
    else if (tech) highlight("tech", tech.getAttribute("data-tech"));
  });
  svg.addEventListener("mouseleave", clearHl);

  panel.addEventListener("click", function (ev) {
    if (ev.target.classList.contains("x")) {
      panel.hidden = true;
      clearHl();
      return;
    }
    var go = ev.target.closest("[data-goto]");
    if (go) {
      ev.preventDefault();
      var slug = go.getAttribute("data-goto");
      highlight("lab", slug);
      labPanel(slug);
    }
  });
})();
