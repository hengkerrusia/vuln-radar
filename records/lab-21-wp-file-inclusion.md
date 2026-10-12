---
title: "WordPress file inclusion (CVE-2026-87902)"
researcher: "Robert Ressl"
year: 2026
url: "https://ressl.ch/blog/cve-2026-87902-wordpress/"
topics: ["File Inclusion"]
techniques: ["File Inclusion", "Path Traversal"]
related: ["finding-wordpress-cve-2026-87902: research record for this CVE — this lab reproduces it hands-on", "lab-20-php-filter-chain: same family — file inclusion; lab 20 forges code via filter chains (RCE), lab 21 reads files via traversal (containment failure)"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/21-wp-file-inclusion"
summary: "Double-encoded pagename + numeric page_id make get_page_template() include a local PHP file outside the theme directory — realpath() canonicalizes but never proves containment. Conditional RCE via pearcmd.php."
---
