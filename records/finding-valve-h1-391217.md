---
title: "H1 #391217: Valve partner CD keys IDOR"
researcher: "moskowsky"
year: 2018
url: "https://hackerone.com/reports/391217"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["finding-indico-cve-2025-53640: both are missing object authorization → mass exposure; Valve exposes game CD keys, Indico exposes user PII"]
type: "finding"
status: "candidate"
lab_url: ""
summary: "/partnercdkeys/assignkeys/ performed no object-level authorization → any partner could pull all CD keys of any game. Critical, $20,000 bounty ($15k + bonus) verified on the report page."
---
