// VulnRadar investigation board — vanilla JS, no dependencies.
(function () {
  var svg = document.getElementById("board");
  var panel = document.getElementById("panel");
  if (!svg || !panel) return;
  var suppressClick = false; // set after a real pan so the release click doesn't fire

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
      "<h3>" + (d.badge === "lab" ? "Lab " + d.n : "Candidate") + badge + "</h3>" +
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
      var kind = d.badge === "lab" ? "Lab " + d.n : "Candidate";
      return '<li><a href="#" data-goto="' + slug + '">' + kind + " — " + esc(d.title) + "</a></li>";
    }).join("");
    panel.innerHTML =
      '<button class="x" aria-label="close">×</button>' +
      "<h3>📌 " + esc(name) + "</h3>" +
      "<p>" + labs.length + " record" + (labs.length === 1 ? "" : "s") + " use this technique:</p>" +
      "<ul>" + items + "</ul>";
    panel.hidden = false;
  }

  svg.addEventListener("click", function (ev) {
    if (suppressClick) return;
    openAt(ev.target);
  });

  function openAt(target) {
    var lab = target.closest(".labnode");
    var tech = target.closest(".technode");
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
  }

  // keyboard: Enter/Space on a focused node opens it, same as click
  svg.addEventListener("keydown", function (ev) {
    if (ev.key !== "Enter" && ev.key !== " ") return;
    var t = document.activeElement;
    if (!t || !svg.contains(t)) return;
    if (!t.closest(".labnode") && !t.closest(".technode")) return;
    ev.preventDefault();
    openAt(t);
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

  // ---- zoom & pan (vanilla JS, no dependencies) ----
  var viewport = document.getElementById("viewport");
  var zin = document.getElementById("zin");
  var zout = document.getElementById("zout");
  var zreset = document.getElementById("zreset");
  var view = { x: 0, y: 0, k: 1 };
  function vbH() { return svg.viewBox.baseVal.height; }
  function applyView() {
    viewport.setAttribute("transform",
      "translate(" + view.x + " " + view.y + ") scale(" + view.k + ")");
  }
  function zoomAt(px, py, factor) {
    var k2 = Math.min(5, Math.max(0.35, view.k * factor));
    var s = k2 / view.k;
    view.x = px - (px - view.x) * s;
    view.y = py - (py - view.y) * s;
    view.k = k2;
    applyView();
  }
  function clientToVB(ev) {
    var r = svg.getBoundingClientRect();
    return {
      x: (ev.clientX - r.left) / r.width * 1200,
      y: (ev.clientY - r.top) / r.height * vbH()
    };
  }
  function zoomCenter(f) { zoomAt(600, vbH() / 2, f); }
  if (zin) zin.addEventListener("click", function () { zoomCenter(1.25); });
  if (zout) zout.addEventListener("click", function () { zoomCenter(1 / 1.25); });
  if (zreset) zreset.addEventListener("click", function () {
    view = { x: 0, y: 0, k: 1 };
    applyView();
  });
  svg.addEventListener("wheel", function (ev) {
    if (!ev.ctrlKey) return;
    ev.preventDefault();
    var p = clientToVB(ev);
    zoomAt(p.x, p.y, ev.deltaY < 0 ? 1.15 : 1 / 1.15);
  }, { passive: false });

  var panning = false, downX = 0, downY = 0, lastX = 0, lastY = 0;
  svg.addEventListener("pointerdown", function (ev) {
    panning = true;
    downX = lastX = ev.clientX;
    downY = lastY = ev.clientY;
    svg.classList.add("grabbing");
    try { svg.setPointerCapture(ev.pointerId); } catch (e) {}
  });
  svg.addEventListener("pointermove", function (ev) {
    if (!panning) return;
    var dx = ev.clientX - lastX, dy = ev.clientY - lastY;
    lastX = ev.clientX;
    lastY = ev.clientY;
    var r = svg.getBoundingClientRect();
    view.x += dx / r.width * 1200;
    view.y += dy / r.height * vbH();
    applyView();
  });
  function endPan(ev) {
    if (panning) {
      // suppress the click only after a real drag (total distance from pointerdown)
      var dist = Math.abs(ev.clientX - downX) + Math.abs(ev.clientY - downY);
      if (dist > 5) {
        suppressClick = true;
        setTimeout(function () { suppressClick = false; }, 60);
      }
    }
    panning = false;
    svg.classList.remove("grabbing");
  }
  svg.addEventListener("pointerup", endPan);
  svg.addEventListener("pointercancel", endPan);
})();
