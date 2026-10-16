---
title: "CVE-2026-38529: Krayin CRM BOLA → password reset → ATO"
researcher: "trexnegro"
year: 2026
url: "https://github.com/trexnegro/security-advisories/blob/HEAD/CVE-2026-38529/README.md"
topics: ["IDOR"]
techniques: ["IDOR", "BOLA"]
related: ["lab-32-indico-principals-bola: both are BOLA in real open-source software; Krayin allows password reset → ATO, Indico leaks PII"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/33-krayin-bola-password-reset"
summary: "PUT /admin/settings/users/edit/{id} with form-urlencoded password=... resets any non-admin user's password — gate checked roles ((caller non-admin) && (target non-admin)) but never ownership, CWE-269 + CWE-639. Affects Krayin CRM 2.2.x (tested commit ba25b7e7), CVSS 8.8. Lab: mock CRM (stdlib-only); attacker id 100 resets victim id 1's password then logs in as victim → ATO; exploit contract STATUS/VICTIM_TOKEN, token proven via independent /me oracle; fix = owner-or-admin → 403, self-edit and admin-edit still work."
---
