---
title: "Zip Slip"
researcher: "Snyk Security Research Team"
year: 2018
url: "https://security.snyk.io/research/zip-slip-vulnerability"
topics: ["Path Traversal"]
techniques: ["Path Traversal", "Zip Slip"]
related: ["finding-wordpress-cve-2026-87902: same root-cause class — canonicalization without containment; read vs write primitive"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/19-zip-slip"
summary: "Archive entry names (e.g. ../../pwned.txt) written outside the extraction target — arbitrary file write via crafted archives. Concrete instance: CVE-2018-1002203 in unzipper <0.8.13."
---
