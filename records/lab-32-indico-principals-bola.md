---
title: "CVE-2025-53640: Indico BOLA /api/principals → PII exposure"
researcher: "rafaelcorvino1"
year: 2025
url: "https://github.com/rafaelcorvino1/CVE-2025-53640"
topics: ["IDOR"]
techniques: ["IDOR", "BOLA"]
related: ["lab-29-valve-cdkeys-idor: both are missing object authorization → mass exposure; Indico exposes user PII, Valve exposes game CD keys", "lab-33-krayin-bola-password-reset: both are BOLA in real open-source software; Indico leaks PII, Krayin allows password reset → ATO"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/32-indico-principals-bola"
summary: "POST /api/principals with {\"values\":[\"User:<id>\"]} dumped name/email/affiliation for arbitrary user IDs — no authorization check on the object reference, CWE-639. Affects Indico 2.2–3.3.6, fixed in 3.3.7. Lab: mock principals API (stdlib-only); analyst User:100 enumerates User:1–5 and extracts EMAIL1 (amelia.hartono@lab.test) via POST {\"values\":[\"User:<id>\"]}; exploit contract STATUS/COUNT/EMAIL1, enumeration proven via independent server-side oracle; fix = resolve only self (if u and v == me) → foreign IDs return invalid, no PII leaks, self-resolution still works."
---
