---
title: "GitLab Maven registry traversal to authorized_keys write (HackerOne #733072)"
researcher: "saltyyolk (HackerOne)"
year: 2019
url: "https://hackerone.com/reports/733072"
topics: ["Path Traversal"]
techniques: ["Path Traversal", "Arbitrary File Write"]
related: ["lab-19-zip-slip: same primitive class — arbitrary file write via traversal; lab 19 via archive entry names, lab 23 via an API file_name segment", "lab-21-wp-file-inclusion: same root-cause class — canonicalization without containment; lab 21 reads files, lab 23 writes them"]
type: "lab"
status: "in-progress"
lab_url: ""
summary: "Disclosed H1 report ($1,000 bounty): the Grape router validated the pre-decoded URL, so %2e%2e%2f in the Maven file_name segment passed the no-slash regex — a PUT then wrote the attacker's SSH key over authorized_keys. Traversal on a write sink beats traversal on a read sink."
---
