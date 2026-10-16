---
title: "CVE-2023-22515: Confluence BFLA → rantai setup → admin takeover"
researcher: "Atlassian"
year: 2023
url: "https://confluence.atlassian.com/security/cve-2023-22515-privilege-escalation-vulnerability-in-confluence-data-center-and-server-1295682276.html"
topics: ["BFLA"]
techniques: ["BFLA"]
related: []
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/34-confluence-setup-bfla"
summary: "GET /server-info.action with XWork-style parameter binding bootstrapStatusProvider.applicationConfig.setupComplete=0 flips setup state on an already-configured instance — broken function-level authorization on /setup/*, CWE-285. Attacker chains setupadministrator-start → setupadministrator.action to create an administrator, then dologin → full ATO with zero authentication. Affects Confluence Data Center/Server 8.0.0–8.5.1 (fixed 8.3.3/8.4.3/8.5.2+), CVSS 10.0, CISA KEV, exploited by nation-state actors. Lab: lightweight stdlib-only mock; exploit contract STATUS/ADMIN_TOKEN, token proven via independent /me oracle (is_admin); fix = /server-info.action read-only + /setup/* → 403 after setup complete (fail-closed, mirrors Atlassian's interim mitigation)."
---
