---
title: "Stripe email change IDOR → ATO (H1 #1250037)"
researcher: "dk82hg"
year: 2021
url: "https://hackerone.com/reports/1250037"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["lab-28-paypal-idor-privesc: both are IDOR in account management; Stripe takes over accounts via email change, PayPal escalates privilege across merchants", "lab-29-valve-cdkeys-idor: both are missing object authorization; Stripe mutates account identity → ATO, Valve leaks mass CD keys", "finding-gitlab-h1-2293343: both are IDOR → ATO via account identity flows; Stripe changes the account email, GitLab pollutes the reset recipient"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/30-stripe-email-idor-ato"
summary: "Email-change flow on indiehackers.com (Stripe) took user_id from the request without binding it to the session → attacker changed a victim's account email to one they owned, then password-reset → ATO. Medium → critical. Lab: mock account API; exploit runs the full chain (change email → reset → login as victim, TOKEN validated via /me oracle + old credentials must fail); fix = user_id must equal session + password confirmation (403 fail-closed)."
---
