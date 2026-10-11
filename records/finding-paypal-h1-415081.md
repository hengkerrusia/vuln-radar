---
title: "H1 #415081: PayPal IDOR → cross-merchant privilege escalation"
researcher: "born2hack"
year: 2018
url: "https://hackerone.com/reports/415081"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["finding-stripe-h1-1250037: both are IDOR in account management; PayPal escalates privilege across merchants, Stripe takes over accounts via email change"]
type: "finding"
status: "candidate"
lab_url: ""
summary: ".../businessmanage/users/api/v1/users let the caller add secondary users to other merchants' business accounts — no ownership check on the target account ID. High 7.1, $10,500 bounty verified on the report page."
---
