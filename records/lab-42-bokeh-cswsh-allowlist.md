---
title: "CVE-2026-21883: Bokeh CSWSH allowlist prefix-match → look-alike domain bypass"
researcher: "Bokeh"
year: 2026
url: "https://github.com/advisories/GHSA-793v-589g-574v"
topics: ["CSWSH"]
techniques: ["CSWSH"]
related: ["lab-41-mailpit-cswsh-bypass: trilogi CSWSH — pendahulu langsung; di sini validasi Origin ada dan aktif, tetapi logika matcher-nya cacat (prefix-match per label)"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/42-bokeh-cswsh-allowlist"
summary: "Bokeh < 3.8.2 validates WebSocket Origin against an allowlist, but match_host() compares host vs pattern per dot-label with zip(): zip stops at the shortest, and the code only rejects when the pattern is LONGER than the host — so the pattern matches as a PREFIX. Look-alike host portal.corp.evil.example passes for allowlist entry portal.corp → Cross-Site WebSocket Hijacking despite an active allowlist. Fixed in 3.8.2 (commit cedd113b0e271b439dce768671685cf5f861812e) by requiring equal label counts; CWE-1385, CVSS 3.1 5.4. Lab: stdlib-only mock of the vulnerable matcher; exploit contract = 101 handshake from look-alike Origin + event leak via independent oracle; fix = exact label-count match (fail-closed), mirroring upstream. Third in the CSWSH trilogy: (40) no validation at all → (41) validation defeated by normalization mismatch → (42) validation defeated by matcher logic flaw."
---
