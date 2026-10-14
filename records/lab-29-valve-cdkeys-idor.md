---
title: "Valve partner CD keys IDOR (H1 #391217)"
researcher: "moskowsky"
year: 2018
url: "https://hackerone.com/reports/391217"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["finding-indico-cve-2025-53640: both are missing object authorization → mass exposure; Valve exposes game CD keys, Indico exposes user PII", "lab-28-paypal-idor-privesc: both are IDOR/BOLA in partner account flows; Valve leaks mass CD keys, PayPal escalates privilege across merchants"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/29-valve-cdkeys-idor"
summary: "GET /partnercdkeys/assignkeys on partner.steamgames.com performed no object-level authorization → any authenticated partner could download all CD keys of any game. Critical, $20,000 bounty ($15k + bonus). Lab: mock partner portal; exploit pulls 5 real keys of game_5002 as another partner (KEY1 validated against independent oracle); fix = is_owner(email, game_id) → 403."
---
