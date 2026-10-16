---
title: "CVE-2026-34383: Admidio — CSRF validation skipped via parameter"
researcher: "Admidio"
year: 2026
url: "https://github.com/Admidio/admidio/security/advisories/GHSA-4rwmc5mjwh7x"
topics: ["CSRF"]
techniques: ["CSRF", "token validation flaw"]
related: []
type: "finding"
status: "candidate"
summary: "Inventory module's item_save endpoint reads a user-controllable POST parameter 'imported'; ItemService::save(true) completely skips CSRF token validation (and server-side form validation) when it is true — the app has CSRF tokens, but enforcement is conditional on attacker-controlled input. Affects admidio/admidio ≤ 5.0.7, fixed 5.0.8 (commit 00494b95). Impact is modest (arbitrary inventory writes, CVSS 4.3, privileges required). Sibling advisory CVE-2026-34384 (registration-approval actions via GET with no CSRF token → attacker merges own registration into an existing account, replacing credentials = ATO, CVSS 7.3) is the stronger pick if ATO is wanted in this slot. Advisory read via archive mirror — re-check the live GHSA page before committing to a lab. Lab candidacy: MODERATE (reserve)."
---
