# PHP Security Advisory - October 21, 2026
# Critical: Use-After-Free Vulnerabilities in PHP (PHP2Shell)

**Publication Date:** October 21, 2026  
**Last Updated:** October 26, 2026  
**Advisory ID:** PHP-SA-2026-1021  
**Severity:** Critical (CVSS 9.2)

---

## 🚨 Executive Summary

The PHP Security Team has identified and patched **two critical Use-After-Free vulnerabilities** in the PHP interpreter, collectively known as **"PHP2Shell"**.

These vulnerabilities (**CVE-2026-109618** and **CVE-2026-109619**) allow **unauthenticated remote attackers** to execute arbitrary code on affected PHP installations. **Active exploitation has been observed in the wild since October 17, 2026.**

**All users are strongly advised to update immediately.**

---

## 📋 Vulnerability Details

### CVE-2026-109618: Use-After-Free in OOM Error Handling

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-109618 |
| **CVSS v3.1** | 9.2 (Critical) |
| **CVSS v4.0** | 9.2 (Critical) |
| **CWE** | CWE-416 (Use After Free) |
| **Affected** | All PHP versions before 8.5.12, 8.4.27, 8.3.36, 8.2.35 |

#### Technical Description

When PHP encounters an out-of-memory (OOM) condition during request initialization, it uses the `longjmp()` function to abort request processing. This abnormal control flow mechanism leaves **internal request data structures in a partially initialized state**.

The subsequent cleanup code **incorrectly trusts these invalid structures**, leading to memory corruption that can be exploited for **remote code execution (RCE)**.

**Key Technical Points:**
- Exploitation occurs **before any userland PHP code executes**
- Triggered by **multipart/form-data requests** exceeding `memory_limit`
- Affects **all SAPIs** (mod_php, PHP-FPM, php-cgi, etc.)
- **No authentication required**
- **No user interaction required**

#### Proof of Concept

A proof of concept exploit is available in open source repositories. The exploit involves:
1. Crafting a multipart request with specific characteristics
2. Triggering an OOM condition via memory exhaustion
3. Exploiting the resulting memory corruption

**Note:** The PHP Security Team does not distribute PoC code, but confirms that functional exploits exist in the wild.

---

### CVE-2026-109619: Use-After-Free in Global State Management

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-109619 |
| **CVSS v3.1** | 9.2 (Critical) |
| **CVSS v4.0** | 9.2 (Critical) |
| **CWE** | CWE-416 (Use After Free) |
| **Affected** | All PHP versions before 8.5.12, 8.4.27, 8.3.36, 8.2.35 |

#### Technical Description

Internal state owned by a PHP request can **persist after its backing memory has been freed**, typically following a fatal error or other exceptional condition. When a subsequent request is processed by the **same worker process** (in PHP-FPM, mod_php, etc.), this stale state may be **used before proper re-initialization**.

This leads to **use-after-free conditions** that can be exploited for **remote code execution** and **memory exposure**.

**Key Technical Points:**
- Exploitable via **session.upload_progress** feature (enabled by default)
- Affects **multi-request scenarios** (PHP-FPM, mod_php)
- **No authentication required**
- **No user interaction required**
- Can expose **sensitive memory contents**

---

### CVE-2026-115560: Additional Session Upload Progress Issue

| Field | Value |
|-------|-------|
| **CVE ID** | CVE-2026-115560 |
| **CVSS v3.1** | 7.5 (High) |
| **CWE** | CWE-416 (Use After Free) |
| **Affected** | Unusual configurations only |

#### Technical Description

A third vulnerability related to session upload progress was identified. This vulnerability affects **unusual configurations only** and no exploitation has been observed in the wild. A fix is planned for the next regular bugfix release.

**Mitigation:** Disabling `session.upload_progress.enabled` (as recommended for CVE-2026-109619) also mitigates this vulnerability.

---

## 🎯 Impact Assessment

### Affected Components

- ✅ **PHP Core** (Zend Engine)
- ✅ **All SAPIs**: mod_php, PHP-FPM, php-cgi, FrankenPHP, LiteSpeed
- ✅ **All platforms**: Linux, Windows, macOS, BSD

### Attack Surface

- **Network-based**: Remote attackers can exploit without authentication
- **Pre-authentication**: Exploitation occurs before any application code
- **High privilege**: Code executes with web server privileges
- **Widespread**: Affects default PHP configurations

### Business Impact

- **Full server compromise**
- **Data theft** (CVE-2026-109619 exposes memory)
- **Unauthorized access**
- **Service disruption**
- **Compliance violations**

---

## 🛡️ Mitigation & Remediation

### ✅ Immediate Mitigations (If Patching is Not Possible)

#### For CVE-2026-109618:
```ini
; In php.ini (NOT modifiable via .htaccess or ini_set)
memory_limit = -1

; Limit POST data size
post_max_size = 8M

; Additional hardening
max_file_uploads = 20
max_input_vars = 1000
```

**⚠️ WARNING:** `memory_limit = -1` disables memory limits entirely. This is a **temporary mitigation only** and may impact application behavior. Test thoroughly before deploying to production.

#### For CVE-2026-109619:
```ini
; In php.ini, pool configuration, or server configuration
session.upload_progress.enabled = 0
```

**⚠️ CRITICAL:** After changing this setting, **ALL PHP WORKERS MUST BE RESTARTED** for the change to take effect. Simply reloading PHP is not sufficient.

#### For CVE-2026-115560:
The mitigation for CVE-2026-109619 (disabling `session.upload_progress.enabled`) also mitigates this vulnerability.

#### Additional Hardening:
- Limit the number of multipart parts
- Limit the number of request headers
- Block multipart requests if your application doesn't use them
- **Do NOT use** `RLIMIT_AS` or `RLIMIT_DATA` as mitigations

---

### ✅ Permanent Solution: Apply Security Updates

**Fixed versions have been released for all supported PHP branches:**

| PHP Version | Vulnerable Versions | Fixed Version | Download |
|-------------|---------------------|---------------|----------|
| PHP 8.5 | < 8.5.12 | **8.5.12** | [Download](https://www.php.net/downloads.php#v8.5.12) |
| PHP 8.4 | < 8.4.27 | **8.4.27** | [Download](https://www.php.net/downloads.php#v8.4.27) |
| PHP 8.3 | < 8.3.36 | **8.3.36** | [Download](https://www.php.net/downloads.php#v8.3.36) |
| PHP 8.2 | < 8.2.35 | **8.2.35** | [Download](https://www.php.net/downloads.php#v8.2.35) |
| PHP ≤ 8.1 | All | **No Fix** | See below |

**For PHP ≤ 8.1 (End of Life):**
- Use distribution/vendor backports (if available)
- Migrate to a supported PHP version
- Isolate PHP applications from the internet

**⚠️ CRITICAL:** After updating PHP, **ALL WORKERS MUST BE RESTARTED**:
```bash
# Apache + mod_php
sudo apachectl restart

# PHP-FPM
sudo systemctl restart php-fpm

# Other SAPIs
sudo systemctl restart your-php-service
```

---

## 📊 Timeline

| Date | Event |
|------|-------|
| Oct 17, 2026 | First exploitation attempts observed in the wild |
| Oct 20, 2026 | PHP Security Team notified |
| Oct 21, 2026 | **Public disclosure + patches released** |
| Oct 21, 2026 | CERT-EU Advisory published |
| Oct 21, 2026 | Sophos Advisory published |
| Oct 22, 2026 | Palo Alto Networks Advisory published |
| Oct 26, 2026 | CISA KEV Database updated |
| Oct 26, 2026 | AWS Security Bulletin published |

---

## 🔍 Detection

### Indicators of Compromise (IoC)

**Network-based detection:**
- Multiple HTTP requests with unusually large `Content-Length` headers
- Rapid succession of multipart/form-data requests
- Requests with malformed multipart boundaries
- Requests to `/upload.php` or similar endpoints

**Host-based detection:**
- Unexpected PHP processes or worker crashes
- Unusual memory usage patterns
- Presence of suspicious PHP files (e.g., `proof.php`, `shell.php`)
- Unexpected outbound connections from PHP processes

### Log Analysis

**Apache access logs:**
```
192.168.1.100 - - [26/Oct/2026:14:30:22 +0000] "POST /upload.php HTTP/1.1" 200 5242 "-" "Mozilla/5.0"
192.168.1.100 - - [26/Oct/2026:14:30:23 +0000] "GET /proof.php HTTP/1.1" 200 1234 "-" "Mozilla/5.0"
```

**Apache error logs:**
```
[Fri Oct 26 14:30:22.123456 2026] [core:notice] [pid 1234] AH00163: Apache/2.4.68 configured -- resuming normal operations
[Fri Oct 26 14:30:22.123789 2026] [php:error] [pid 1234] PHP Fatal error:  Allowed memory size of 16777216 bytes exhausted
```

---

## 🔗 References

- [CERT-EU Advisory 2026-018](https://cert.europa.eu/publications/security-advisories/2026-018)
- [CISA KEV Entry](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching)
- [GHSA-w8hw-w9fx-j79w (CVE-2026-109618)](https://github.com/advisories/GHSA-w8hw-w9fx-j79w)
- [GHSA-6wmf-4rv5-p3rp (CVE-2026-109619)](https://github.com/advisories/GHSA-6wmf-4rv5-p3rp)
- [Palo Alto Networks Unit 42 Analysis](https://unit42.paloaltonetworks.com/cve-2026-109618-cve-2026-109619/)
- [Sophos Security Advisory](https://www.sophos.com/en-us/security-advisories/sophos-sa-20261021-php2shell)

---

## 📞 Contact

For questions regarding this advisory:
- **PHP Security Team:** security@php.net
- **Bug Bounty Program:** https://hackerone.com/php

**Do NOT disclose vulnerability details publicly until official disclosure.**

---

**© 2026 The PHP Group**  
**PHP Security Team**
