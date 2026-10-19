---
title: "CVE-2026-34383: Admidio — penegakan CSRF kondisional pada input penyerang"
researcher: "Admidio"
year: 2026
url: "https://github.com/Admidio/admidio/security/advisories/GHSA-4rwm-c5mj-wh7x"
topics: ["CSRF"]
techniques: ["CSRF", "token validation flaw"]
related: []
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/38-admidio-imported-csrf"
summary: "Parameter POST 'imported' yang dikontrol penyerang memutuskan apakah validasi token CSRF dan validasi form dijalankan (admidio/admidio <= 5.0.7, PHP; pelapor @offset) — request tempaan tanpa token valid menyimpan item mentah ke inventory, termasuk quantity invalid yang pasti ditolak validasi normal; CVSS 4.3. Fixed 5.0.8 (commit 00494b95). Lab: mock stdlib modul inventory; exploit contract STATUS/ITEM_ID, bukti lewat GET /inventory (quantity negatif/non-integer); fix = token CSRF + validasi form selalu dijalankan — flag request tak boleh mengendalikan penegakan."
---
