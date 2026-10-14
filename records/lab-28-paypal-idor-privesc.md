---
title: "PayPal IDOR → cross-merchant privilege escalation (H1 #415081)"
researcher: "born2hack"
year: 2018
url: "https://hackerone.com/reports/415081"
topics: ["IDOR"]
techniques: ["IDOR"]
related: ["lab-30-stripe-email-idor-ato: both are IDOR in account management; PayPal escalates privilege across merchants, Stripe takes over accounts via email change"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/28-paypal-idor-privesc"
summary: "POST /businessmanage/users/api/v1/users accepted account_id from the request body without checking that the caller is a member of that account — attacker@evil.com added themselves as admin to victim merchant acct_1002, proven by the (properly authorized) read endpoint listing them. High 7.1, $10,500 bounty. Lab: mock merchant API; fix = is_member(email, account_id) before any mutation (cross-merchant → 403)."
---
