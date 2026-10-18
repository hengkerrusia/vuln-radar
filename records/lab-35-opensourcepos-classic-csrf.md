---
title: "CVE-2025-68434: OpenSourcePOS — CSRF klasik tanpa token"
researcher: "Aditya Singh / Nixon-H"
year: 2025
url: "https://github.com/opensourcepos/opensourcepos/security/advisories/GHSA-wjm4-hfwg-5w5r"
topics: ["CSRF"]
techniques: ["CSRF", "missing token"]
related: []
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/35-opensourcepos-classic-csrf"
summary: "Global CSRF filter commented out with a TODO in app/Config/Filters.php (OpenSourcePOS 3.4.0/3.4.1, PHP/CodeIgniter) — every POST, including admin endpoints, rides the session cookie alone. Attacker's auto-submit form creates a rogue full-privilege Administrator when a logged-in admin visits it → complete POS system takeover, CVSS 8.8. Fixed in 3.4.2 (commit d575c8da). Lab: stdlib-only mock of the vulnerable POST /users; exploit contract STATUS/ADMIN_TOKEN, admin takeover proven via /me oracle (is_admin=true); fix = per-session CSRF token required on every POST → 403 without a valid token."
---
