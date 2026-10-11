---
title: "H1 #2293343: GitLab password reset array pollution → ATO"
researcher: "asterion04"
year: 2023
url: "https://hackerone.com/reports/2293343"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["finding-stripe-h1-1250037: both are IDOR → ATO via account identity flows; GitLab pollutes the reset recipient, Stripe changes the account email"]
type: "finding"
status: "candidate"
lab_url: ""
summary: "Array-polluting user[email] in the password-reset request redirected the reset link to the attacker's address → one-request ATO with no victim interaction. Critical 10.0, $35,000 bounty verified on the report page."
---
