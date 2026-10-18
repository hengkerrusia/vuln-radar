---
title: "CVE-2024-22424: Argo CD — CSRF via SameSite/cookie-scoping bypass"
researcher: "Upwind"
year: 2024
url: "https://www.upwind.io/feed/upwind-takes-over-argocd-and-an-eks-cluster-using-only-a-simple-csrf-vulnerability"
topics: ["CSRF"]
techniques: ["CSRF", "SameSite bypass"]
related: []
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/37-argocd-samesite-csrf"
summary: "Argo CD relied on SameSite=Lax as its CSRF defense — but SameSite is a site (eTLD+1) boundary, not an origin boundary, so an attacker on any sibling subdomain still gets the auth cookie; missing Content-Type validation let preflight-less requests reach state-changing API endpoints. Upwind demonstrated end-to-end: forged cross-site API calls deploy a malicious Application → privileged pods → full Kubernetes cluster takeover. Affects < 2.10-rc2 / 2.9.4 / 2.8.8 / 2.7.15. Fixed by rejecting non-GET requests without application/json Content-Type. Lab: stdlib-only mock of the Argo CD API; the exploit plays the victim browser (modeling SameSite-Lax + CORS preflight rules itself) and forges an Application from a sibling subdomain; contract STATUS/APP verified via the applications oracle; fix = require application/json on non-GET → 4xx fail-closed, mirroring the upstream breaking change."
---
