---
title: "CVE-2026-34394: AVideo — CSRF chained to platform takeover"
researcher: "aisafe.io (via WWBN/AVideo advisory)"
year: 2026
url: "https://github.com/WWBN/AVideo/security/advisories/GHSA-4wwr-7h7c-chqr"
topics: ["CSRF"]
techniques: ["CSRF", "chained"]
related: []
type: "finding"
status: "candidate"
summary: "Chain of three flaws in AVideo ≤ 26.0: (a) admin/save.json.php writes arbitrary plugin settings with no CSRF token check; (b) the app explicitly weakens browser defaults with session.cookie_samesite=None, so cross-origin form POSTs carry the session; (c) the plugins table sits in ignoreTableSecurityCheck(), bypassing ORM-level access controls. One forged form POST rewrites PayPal/Stripe/S3/LDAP plugin config → full platform and payment takeover, CVSS 8.1; the advisory ships the full auto-submit PoC. Documented fix: isGlobalTokenValid() at admin/save.json.php:10. Advisory read via archive mirror — re-check the live GHSA page before committing to a lab. Lab candidacy: deferred — see the CSRF curation notes; kept as a genuine finding record."
---
