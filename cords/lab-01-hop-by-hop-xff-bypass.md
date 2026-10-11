---
title: "Abusing HTTP hop-by-hop request headers"
researcher: "Nathan Davison"
year: 2019
url: "https://nathandavison.com/blog/abusing-http-hop-by-hop-request-headers"
topics: ["Hop-by-Hop Abuse"]
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/01-hop-by-hop-xff-bypass"
summary: "Connection header tricks proxies into stripping security headers (X-Forwarded-For, Authorization) before the backend — enabling admin bypass and IP spoofing."
---
