---
title: "HTTP/2: The Sequel is Always Worse"
researcher: "James Kettle"
year: 2021
url: "https://portswigger.net/research/http2"
topics: ["Request Smuggling"]
techniques: ["Request Smuggling", "HTTP Desync"]
related: ["lab-10-0cl-expect-desync: desync family"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/09-h2-downgrade-desync"
summary: "H2.CL downgrade desync — HTTP/2 frontend and HTTP/1 backend disagree on where a request ends, enabling request smuggling."
---
