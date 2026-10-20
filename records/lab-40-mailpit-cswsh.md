---
title: "CVE-2026-22689: Mailpit — CSWSH tanpa validasi Origin"
researcher: "axllent/mailpit (vendor advisory)"
year: 2026
url: "https://github.com/axllent/mailpit/security/advisories/GHSA-524m-q5m7-79mm"
topics: ["CSWSH"]
techniques: ["CSWSH", "missing origin validation"]
related: ["lab-41-mailpit-cswsh-bypass: regresi fix ini — bypass cek Origin via path percent-encoded (CVE-2026-67448)"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/40-mailpit-cswsh"
summary: "WebSocket upgrader Mailpit disetel CheckOrigin: return true (axllent/mailpit < 1.28.2, Go/gorilla; CVE-2026-22689, CVSS 6.5) — halaman asing bisa membuka socket ke ws://localhost:8025/api/events dan menerima siaran event email (subjek, pengirim, cuplikan isi) secara real-time. Fix 1.28.2: hapus CheckOrigin (default gorilla: Origin harus cocok Host). Lab: server WebSocket asli stdlib (handshake 101 + text frame); exploit contract STATUS/EVENT_ID/EVENT_SUBJECT, bukti lewat GET /api/events; fix = tolak Origin yang host-nya != Host → 403."
---
