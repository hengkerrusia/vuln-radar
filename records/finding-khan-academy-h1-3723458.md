---
title: "H1 #3723458: Khan Academy regex bypass → 1-click ATO"
researcher: ""
year: 2026
url: "https://hackerone.com/reports/3723458"
topics: ["Open Redirect"]
techniques: ["Open Redirect"]
related: ["lab-26-expo-oauth-openredirect: both are redirect-driven token theft → ATO; Khan bypasses an unescaped-dot regex, Expo bypasses a case-sensitive scheme check", "lab-25-mopub-openredirect-xss: both are open redirects with real impact; Khan steals an auth-transfer token, MoPub escalates to XSS via javascript: scheme"]
type: "finding"
status: "candidate"
lab_url: ""
summary: "KA_DOMAIN_REGEX left dots in uc.a.run.app unescaped, so attacker-registered xfarr-6fmjyrz2lq-uc-a-run.app passed validation; ?continue= login flow delivered a one-time transfer auth token to the attacker server → replay → full session cookies → 1-click ATO. Report frames it as a critical/P0 chain."
---
