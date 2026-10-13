---
title: "Apache 2.4.49 path traversal (CVE-2021-41773)"
researcher: "Ash Daulton (HackerOne #1394916)"
year: 2021
url: "https://hackerone.com/reports/1394916"
topics: ["Path Traversal"]
techniques: ["Path Traversal"]
related: ["lab-23-gitlab-maven-traversal: same root-cause class — decode-ordering: lab 23 validated the pre-decoded URL, lab 24 checked for .. before decoding %2e to .; lab 23 writes files, lab 24 reads them", "lab-21-wp-file-inclusion: same attack family, different root cause — lab 21 is canonicalization without containment, lab 24 is check-then-decode ordering"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/24-apache-249-traversal"
summary: "Disclosed H1 report ($4,000 Internet Bug Bounty on the report page): 2.4.49 checked the path for ../ BEFORE decoding %2e to ., so /.%2e/ segments became live traversal after the check. With ScriptAlias /cgi-bin/ + mod_cgi, a GET reads files outside the web root (e.g. /etc/passwd). Fix is config hardening (Require all denied, per the official advisory); 2.4.50's fix was incomplete (CVE-2021-42013), so the upgrade note says >= 2.4.51."
---
