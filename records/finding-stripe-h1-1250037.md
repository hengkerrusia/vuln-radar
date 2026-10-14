---
title: "H1 #1250037: Stripe IDOR email change → ATO"
researcher: "dk82hg"
year: 2021
url: "https://hackerone.com/reports/1250037"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["finding-gitlab-h1-2293343: both are IDOR → ATO via account identity flows; Stripe changes the account email, GitLab pollutes the reset recipient", "lab-28-paypal-idor-privesc: both are IDOR in account management; Stripe takes over accounts via email change, PayPal escalates privilege across merchants"]
type: "finding"
status: "candidate"
lab_url: ""
summary: "Account-update endpoint not bound to session identity → attacker changed another user's email, then reset the password → full ATO. Critical, $3,000 bounty verified on the report page."
---
