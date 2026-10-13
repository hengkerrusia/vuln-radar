---
title: "Khan Academy regex bypass → 1-click ATO (H1 #3723458)"
researcher: "HackerOne report #3723458"
year: 2026
url: "https://hackerone.com/reports/3723458"
topics: ["Open Redirect"]
techniques: ["Open Redirect"]
related: ["lab-25-mopub-openredirect-xss: both are open redirects with real impact; MoPub escalates to XSS via javascript: scheme, Khan steals an auth-transfer token", "lab-26-expo-oauth-openredirect: both are redirect-driven token theft → ATO; Khan bypasses an unescaped-dot regex, Expo bypasses a case-sensitive scheme check"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/27-khan-academy-regex-bypass"
summary: "Login continue validated by KA_DOMAIN_REGEX with unescaped dots in uc.a.run.app — attacker-registered xfarr-6fmjyrz2lq-uc-a-run.app passed, so post-login redirect carried a one-time transfer auth token (/transfer_auth?key=) to the attacker; replayed for full session cookies → 1-click ATO. Lab: mock login + transfer_auth; fix = escape the dots."
---
