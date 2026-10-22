---
title: "CVE-2026-67448: Mailpit — bypass cek Origin WebSocket via path percent-encoded"
researcher: "axllent/mailpit (vendor advisory)"
year: 2026
url: "https://github.com/axllent/mailpit/security/advisories/GHSA-8r62-w5wh-fc5m"
topics: ["CSWSH"]
techniques: ["CSWSH", "origin check bypass", "percent-encoding"]
related: ["lab-40-mailpit-cswsh: regresi dari fix Lab 40 — middleware Origin menguji URI mentah sedangkan router memakai path ter-decode", "lab-42-bokeh-cswsh-allowlist: lanjutan trilogi CSWSH — allowlist Origin yang aktif pun lolos via domain look-alike (prefix-match per label)"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/41-mailpit-cswsh-bypass"
summary: "Regresi CVE-2026-22689 di axllent/mailpit 1.29.0–1.30.5: perbaikan CSWSH diimplementasikan ulang sebagai middleware Origin di server.go yang gate-nya menguji URI mentah (strings.HasPrefix(r.RequestURI, \"/api/\")), sedangkan http.ServeMux me-route path yang sudah ter-decode dan upgrader WebSocket tetap CheckOrigin: return true. Request ke /%61pi/events melewatkan satu-satunya cek Origin lalu ter-route ke handler /api/events — halaman asing kembali menerima siaran event email (subjek, pengirim, cuplikan isi) secara real-time. Fix 1.30.6: gate pada r.URL.Path (ter-decode) dan upgrader memvalidasi Origin sendiri secara fail-closed. Lab: diferensial 403 (path polos) vs 101 (path ter-encode); fix dua lapis ala upstream."
---
