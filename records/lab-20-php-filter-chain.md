---
title: "PHP filter chains"
researcher: "Synacktiv"
year: 2022
url: "https://github.com/synacktiv/php_filter_chain_generator"
topics: ["File Inclusion"]
techniques: ["File Inclusion", "PHP Filter Chain"]
related: ["lab-19-zip-slip: same family — file inclusion / path traversal; lab 19 writes outside the target dir, lab 20 executes forged code via include", "finding-canto-rfi-cve-2023-3452: both abuse PHP include sinks — RFI needs allow_url_include, filter chains need nothing writable"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/20-php-filter-chain"
summary: "Chained php://filter iconv conversions forge executable PHP from a read-only include sink — LFI to RCE with no upload, no log poisoning, no writable file."
---
