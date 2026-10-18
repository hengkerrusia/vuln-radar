---
title: "CVE-2025-68481: fastapi-users — login CSRF via OAuth state"
researcher: "David (90-day coordinated disclosure)"
year: 2025
url: "https://github.com/fastapi-users/fastapi-users/security/advisories/GHSA-5j53-63w8-8625"
topics: ["CSRF"]
techniques: ["CSRF", "login CSRF"]
related: []
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/36-fastapiusers-login-csrf"
summary: "OAuth state parameter in fastapi-users < 15.0.2 was a stateless JWT (generate_state_token() always called with empty state_data) — valid ~1h for any client; the callback validated only signature and expiry, never binding state to the initiating session. Trick a logged-in victim into loading the attacker's callback URL (code + state) → attacker's upstream SSO identity permanently linked to the victim's account: '1-click Account Takeover' per the vendor advisory. Fixed in 15.0.2 (double-submit cookie, commit 7cf413cd). Lab: stdlib-only mock of the OAuth authorize/callback flow with a stub SSO provider; exploit contract STATUS/VICTIM/ATO_TOKEN, takeover proven via /me oracle plus an independent SSO-login replay; fix = double-submit cookie (oauth_csrf, HttpOnly + SameSite=Lax, compare_digest at callback → 400 fail-closed), mirroring the upstream patch."
---
