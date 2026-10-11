---
title: "H1 #683298: MoPub login open redirect → XSS via javascript: URI"
researcher: "jackb898"
year: 2019
url: "https://hackerone.com/reports/683298"
topics: ["Open Redirect"]
techniques: ["Open Redirect"]
related: ["finding-khan-academy-h1-3723458: both are open redirects with real impact; MoPub escalates to XSS via javascript: scheme, Khan steals an auth-transfer token"]
type: "finding"
status: "candidate"
lab_url: ""
summary: "app.mopub.com/login?next= accepted arbitrary destinations including the javascript: scheme → post-login reflected XSS in the victim's session. Bounty paid (amount not shown on the report page)."
---
