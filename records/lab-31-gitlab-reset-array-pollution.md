---
title: "GitLab password reset array pollution → ATO (H1 #2293343)"
researcher: "asterion04"
year: 2023
url: "https://hackerone.com/reports/2293343"
topics: ["Parameter Pollution"]
techniques: ["Parameter Pollution"]
related: ["lab-30-stripe-email-idor-ato: both are → ATO via account identity flows; GitLab pollutes the reset recipient, Stripe changes the account email"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/31-gitlab-reset-array-pollution"
summary: "user[email] sent as a JSON array where a string was expected → the mailer fanned the password-reset link out to every address in the array → one-request ATO with no victim interaction. Critical 10.0, $35,000. Lab: mock reset API + @attacker.lab-scoped mock inbox; exploit pollutes the array, takes the token from own inbox, resets and logs in as victim (TOKEN validated via /me oracle + old password must fail); fix = strict type check: email must be a string → 400 fail-closed."
---
