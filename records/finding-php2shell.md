---
title: "php2shell — CVE-2026-109618 & CVE-2026-109619: unauthenticated RCE in PHP core"
researcher: "Calif (LCFR) et al."
year: 2026
url: "https://calif.io/php2shell/"
topics: ["RCE", "Memory Corruption"]
techniques: ["use-after-free", "OOM corruption", "stale global state", "interrupted cleanup"]
related: ["lab-20-php-filter-chain: sama-sama RCE yang berakar di runtime PHP, bukan logika aplikasi — filter chain butuh sink include di aplikasi, php2shell berjalan dari request mentah sebelum kode aplikasi dieksekusi"]
type: "finding"
status: "candidate"
added: "2026-10-22"
summary: "Dua kerentanan memory corruption di core PHP, bukan di aplikasi. CVE-2026-109618 (GHSA-w8hw-w9fx-j79w): fatal out-of-memory via longjmp di tengah inisialisasi request (parsing multipart/POST) meninggalkan bucket HashTable setengah terinisialisasi yang tetap dikonsumsi teardown saat request shutdown — RCE pre-auth, terkonfirmasi di mod_php sebelum kode aplikasi berjalan. CVE-2026-109619 (GHSA-6wmf-4rv5-p3rp): state global sisa satu request menunjuk memori request yang sudah dibebaskan (use-after-free) dan dikonsumsi request berikutnya pada worker yang sama; jalur terkonfirmasi termasuk session upload progress yang aktif secara default. Jalur kode rentan ada sejak PHP 5.4.0; semua SAPI web terdampak (mod_php, PHP-FPM, php-cgi, FrankenPHP, LiteSpeed), konfigurasi default, tanpa login; RCE terkonfirmasi terhadap WordPress, Drupal, Joomla, Magento dan lainnya. CVSS v4 9.2 (AC:H / AT:P). Fix resmi 8.5.12 / 8.4.27 / 8.3.36 / 8.2.35 plus backport source untuk 7.4–8.1; tidak ada mitigasi konfigurasi yang tuntas — update adalah satu-satunya perbaikan. Eksploitasi in-the-wild teramati sejak hari disclosure, 21 Oktober 2026. Soal PoC: exploit asli penemu (Calif) tidak dirilis ke publik; lab PoC dari dua peneliti independen (dinosn, xuehuolll) mengklaim RCE terhadap build yang belum dipatch lewat jendela pre-RINIT yang sama — callback session upload progress berjalan sebelum RINIT men-zero-kan global serializer — sementara mayoritas repo publik yang viral mengejar teori use-after-free pada pointer cache upload progress yang sudah dibantah oleh audit independen. Berstatus candidate dan bukan lab: bug berada di interpreter C dan eksploitasinya adalah eksploitasi biner spesifik-build (grooming heap, offset libphp, balapan antar-request), tidak cocok dengan format fixthecode yang menuntut exploit deterministik dan fix yang dapat ditulis learner."
---
