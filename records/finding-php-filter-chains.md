---
title: "PHP filter chain generator"
researcher: "Synacktiv"
year: 2022
url: "https://github.com/synacktiv/php_filter_chain_generator"
topics: ["File Inclusion"]
techniques: ["File Inclusion"]
related: ["finding-canto-rfi-cve-2023-3452: both abuse PHP include sinks — RFI needs allow_url_include, filter chains need nothing writable"]
type: "finding"
status: "candidate"
lab_url: ""
summary: "Chained php://filter iconv conversions forge executable PHP from a read-only include sink — LFI to RCE with no upload, no log, and no writable file."
---
