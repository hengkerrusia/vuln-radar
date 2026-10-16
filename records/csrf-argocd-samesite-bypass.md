---
title: "CVE-2024-22424: Argo CD — CSRF via SameSite/cookie-scoping bypass"
researcher: "Upwind"
year: 2024
url: "https://www.upwind.io/feed/upwind-takes-over-argocd-and-an-eks-cluster-using-only-a-simple-csrf-vulnerability"
topics: ["CSRF"]
techniques: ["CSRF", "SameSite bypass"]
related: []
type: "finding"
status: "candidate"
summary: "Argo CD relied on SameSite=Lax as its CSRF defense — but SameSite is a site (eTLD+1) boundary, not an origin boundary, so an attacker on any sibling subdomain still gets the auth cookie; missing Content-Type validation let preflight-less requests reach state-changing API endpoints. Upwind demonstrated end-to-end: forged cross-site API calls deploy a malicious Application → privileged pods → full Kubernetes cluster takeover. Affects < 2.10-rc2 / 2.9.4 / 2.8.8 / 2.7.15. Fix: reject non-GET requests without application/json Content-Type. Lab candidacy: MODERATE — high impact and well-documented, but needs two same-parent-domain origins (hosts-file trick) plus a harness-simulated victim browser; fits an advanced tier."
---
