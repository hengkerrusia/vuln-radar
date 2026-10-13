---
title: "CVE-2023-28131: Expo OAuth proxy open redirect → ATO"
researcher: "Salt Labs (Salt Security)"
year: 2023
url: "https://salt.security/blog/a-new-oauth-vulnerability-that-may-impact-hundreds-of-online-services"
topics: ["Open Redirect"]
techniques: ["Open Redirect"]
related: ["lab-27-khan-academy-regex-bypass: both are redirect-driven token theft → ATO; Khan bypasses an unescaped-dot regex, Expo bypasses a case-sensitive scheme check"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/26-expo-oauth-openredirect"
summary: "AuthSession proxy (auth.expo.io) stored attacker-influenced returnUrl in an ru cookie, then redirected the OAuth fragment (code+token) to it — the case-sensitive scheme check was bypassed with mixed-case hTTps://. Full ATO demonstrated on Codecademy. CVSS 9.6, hotfixed within hours. Lab: mock OAuth proxy + IdP, no browser needed; fix = case-insensitive scheme + host allowlist (400)."
---
