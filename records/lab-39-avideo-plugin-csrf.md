---
title: "CVE-2026-34394: AVideo — CSRF config plugin → takeover platform"
researcher: "aisafe.io (via WWBN/AVideo advisory)"
year: 2026
url: "https://github.com/WWBN/AVideo/security/advisories/GHSA-4wwr-7h7c-chqr"
topics: ["CSRF"]
techniques: ["CSRF", "missing token"]
related: []
type: "lab"
status: "shipped"
lab_url: "https://github.com/hengkerrusia/fixthecode/tree/main/labs/web/39-avideo-plugin-csrf"
summary: "POST /admin/save.json.php menulis field POST arbitrer ke konfigurasi plugin tanpa pernah memanggil isGlobalTokenValid()/verifyToken() (WWBN/AVideo <= 26.0, PHP; pelapor aisafe.io) — request tempaan bermodal cookie sesi admin mengubah paypalReceiverEmail plugin PayPerView; diperparah cookie SameSite=None yang eksplisit dan mass-assignment tanpa allowlist; CVSS 8.1. Fix anjuran advisory: isGlobalTokenValid() di save.json.php:10. Lab: mock stdlib panel admin (tanpa MySQL); exploit contract STATUS/PLUGIN/PAYPAL_EMAIL, bukti lewat GET /admin/plugins; fix = token CSRF divalidasi tepat setelah cek admin → 403 fail-closed."
---
