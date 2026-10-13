---
title: "MoPub login open redirect → XSS via javascript: URI (H1 #683298)"
researcher: "jackb898"
year: 2019
url: "https://hackerone.com/reports/683298"
topics: ["Open Redirect"]
techniques: ["Open Redirect", "XSS"]
related: ["finding-khan-academy-h1-3723458: both are open redirects with real impact; MoPub escalates to XSS via javascript: scheme, Khan steals an auth-transfer token"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/25-mopub-openredirect-xss"
summary: "app.mopub.com/login?next= accepted arbitrary destinations including the javascript: scheme; post-login navigation used window.location.href, so the javascript: URI executed as reflected XSS in the victim's session. Bounty paid (amount not shown on the report page). Lab is the first client-side build, verified with a headless-Chromium sidecar that proves JS execution. Fix: allowlist next to relative paths, reject schemes with 400."
---
