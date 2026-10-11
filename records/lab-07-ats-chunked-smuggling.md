---
title: "Apache Traffic Server chunked smuggling"
researcher: "CVE-2025-65114"
year: 2025
url: "https://nvd.nist.gov/vuln/detail/CVE-2025-65114"
topics: ["Request Smuggling"]
techniques: ["Request Smuggling", "HTTP Desync"]
related: ["lab-08-paypal-clte-cache-poison: smuggling as chain entry"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/07-ats-chunked-smuggling"
summary: "Stale CR flag in ATS chunked parser lets smuggled requests slip through to the origin — HTTP request smuggling via parser differentials."
---
