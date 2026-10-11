---
title: "Pi-hole response splitting to session fixation"
researcher: "GHSA-5v79-p56f-x7c4 (CVE-2025-59151)"
year: 2025
url: "https://github.com/advisories/GHSA-5v79-p56f-x7c4"
topics: ["CRLF Injection"]
techniques: ["CRLF Injection"]
related: ["lab-16-crlf-desync: CRLF-powered desync", "lab-17-formdata-crlf: CRLF family", "lab-18-morgan-log-forging: CRLF family"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/15-crlf-response-splitting"
summary: "CRLF injection in Pi-hole admin — response splitting injects Set-Cookie, leading to session fixation."
---
