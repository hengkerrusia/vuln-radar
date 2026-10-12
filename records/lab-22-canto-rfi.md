---
title: "Canto remote file inclusion (CVE-2023-3452)"
researcher: "Marco Wotschka (Wordfence)"
year: 2023
url: "https://www.wordfence.com/threat-intel/vulnerabilities/id/a76077c6-700a-4d21-a930-b0d6455d959c"
topics: ["File Inclusion"]
techniques: ["File Inclusion", "Remote File Inclusion"]
related: ["lab-20-php-filter-chain: both abuse PHP include sinks — RFI needs allow_url_include, filter chains need nothing writable", "lab-21-wp-file-inclusion: same family — file inclusion; lab 21 reads local files via traversal, lab 22 executes remote code via include"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/22-canto-rfi"
summary: "CVE-2023-3452 (CVSS 9.8): unauthenticated wp_abspath parameter passed into require_once() — data:// wrapper gives single-request RCE when allow_url_include=On. RFI is nearly extinct in modern apps; the misconfiguration is the teaching point."
---
