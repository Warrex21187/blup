# CERT-EU Security Advisory 2026-018
# Critical Vulnerabilities in PHP (PHP2Shell)

**Publication Date:** 21 October 2026  
**Last Updated:** 26 October 2026  
**Advisory ID:** CERT-EU-SA-2026-018  
**CVSS Scores:** CVE-2026-109618: 9.2 (Critical), CVE-2026-109619: 9.2 (Critical)  

---

## 🚨 Summary

The CERT-EU has identified **two critical vulnerabilities** in PHP, tracked as **CVE-2026-109618** and **CVE-2026-109619**, collectively referred to as **"PHP2Shell"**. These vulnerabilities allow **unauthenticated remote code execution (RCE)** on affected PHP installations.

**Active exploitation has been observed in the wild since 17 October 2026.**

---

## 📋 Vulnerability Details

### CVE-2026-109618: Use-After-Free via OOM Handling

- **CVSS Score:** 9.2 (Critical)
- **CWE:** CWE-416 (Use After Free)
- **Affected Components:** PHP Zend Engine memory management
- **Attack Vector:** Network
- **Attack Complexity:** Low
- **Privileges Required:** None
- **User Interaction:** None

#### Description

When PHP encounters an out-of-memory (OOM) condition during request setup, it uses `longjmp()` to abort the request. This abnormal control flow leaves **internal request data structures partially initialized**. The cleanup code then **trusts these invalid structures**, leading to memory corruption and potential code execution.

A specially crafted **multipart/form-data request** can trigger the OOM condition by exceeding `memory_limit`, even if `post_max_size` restrictions are in place.

**Exploitation occurs BEFORE any application code runs**, making this particularly dangerous for mod_php configurations.

#### Affected Versions

- PHP 8.5.x < 8.5.12
- PHP 8.4.x < 8.4.27
- PHP 8.3.x < 8.3.36
- PHP 8.2.x < 8.2.35
- PHP ≤ 8.1 (End of Life)

---

### CVE-2026-109619: Use-After-Free via Stale Global State

- **CVSS Score:** 9.2 (Critical)
- **CWE:** CWE-416 (Use After Free)
- **Affected Components:** PHP global state management
- **Attack Vector:** Network
- **Attack Complexity:** Low
- **Privileges Required:** None
- **User Interaction:** None

#### Description

Internal state owned by a request can **survive after its backing memory has been freed**, for example after a fatal error. A subsequent request processed by the **same worker** (in PHP-FPM, mod_php, etc.) may use this stale state before proper initialization, leading to **use-after-free conditions** and potential code execution.

This vulnerability is **exploitable via the session upload progress feature** (`session.upload_progress.enabled`), which is **enabled by default** in most configurations.

#### Affected Versions

Same as CVE-2026-109618 (see above).

---

## ⚡ Impact

Successful exploitation of either vulnerability allows an **unauthenticated, remote attacker** to:

- Execute **arbitrary code** with the privileges of the web server process
- **Read sensitive data** from server memory (CVE-2026-109619)
- **Bypass authentication** mechanisms
- **Take full control** of the affected server

**Note:** These vulnerabilities are being **actively exploited in the wild** against exposed PHP installations.

---

## 🔍 Evidence of Exploitation

- **First observed:** 17 October 2026
- **Peak activity:** After 21 October 2026 (following public disclosure)
- **CISA KEV Database:** Added 26 October 2026
- **Exposed instances:** Over 22.6 million (Palo Alto Networks telemetry)

---

## 🛡️ Mitigation & Remediation

### ✅ Immediate Actions (Before Patching)

#### For CVE-2026-109618:
```ini
# In php.ini or pool configuration (NOT modifiable via .htaccess or ini_set)
memory_limit = -1  # Disables memory limit (prevents OOM trigger)
post_max_size = 8M  # Limit POST data size
```

**Note:** `memory_limit = -1` is a **temporary mitigation only**. It prevents the OOM condition but may impact application behavior.

#### For CVE-2026-109619:
```ini
# In php.ini, pool configuration, or server config
session.upload_progress.enabled = 0
```

**CRITICAL:** After changing this setting, **ALL PHP workers must be restarted** for the change to take effect.

#### Additional Hardening:
- Limit the number of multipart parts, headers, and uploads
- Block multipart requests if your application doesn't use them
- **Do NOT use** `RLIMIT_AS` or `RLIMIT_DATA` as mitigations

⚠️ **WARNING:** These are **partial mitigations only**. The only complete solution is to **apply the security updates**.

---

### ✅ Permanent Solution: Apply Security Updates

Upgrade to the **fixed versions** as soon as possible:

| PHP Version | Fixed Version |
|-------------|---------------|
| PHP 8.5.x   | ≥ 8.5.12      |
| PHP 8.4.x   | ≥ 8.4.27      |
| PHP 8.3.x   | ≥ 8.3.36      |
| PHP 8.2.x   | ≥ 8.2.35      |
| PHP ≤ 8.1   | **No official fix** (EOL) |

**After upgrading, RESTART ALL PHP WORKERS.**

For PHP ≤ 8.1 (EOL):
- Use distribution/vendor backports
- Migrate to a supported PHP version
- Isolate PHP applications from the internet

---

## 📊 Technical Details

### Exploitation Mechanism (CVE-2026-109618)

1. Attacker sends a **multipart/form-data request** with carefully crafted data
2. Request triggers **memory_limit** exceedance
3. PHP calls `longjmp()` to abort request processing
4. **Internal structures remain partially initialized**
5. Cleanup code **trusts invalid data** → memory corruption
6. **Code execution** achieved on subsequent request

### Exploitation Mechanism (CVE-2026-109619)

1. Attacker sends a request that triggers a **fatal error**
2. Internal state is **not properly cleaned up**
3. Attacker sends a **second request** to the same worker
4. Worker **reuses stale state** before initialization
5. **Use-after-free** condition → code execution

---

## 🔗 References

- [PHP Official Security Advisory](https://www.php.net/archive/2026.php)
- [CISA KEV Entry](https://www.cisa.gov/news-events/alerts/2026/10/21/critical-vulnerabilities-php-require-immediate-patching)
- [GHSA-w8hw-w9fx-j79w (CVE-2026-109618)](https://github.com/advisories/GHSA-w8hw-w9fx-j79w)
- [GHSA-6wmf-4rv5-p3rp (CVE-2026-109619)](https://github.com/advisories/GHSA-6wmf-4rv5-p3rp)
- [Palo Alto Networks Advisory](https://security.paloaltonetworks.com/CVE-2026-109618)
- [Sophos Advisory](https://www.sophos.com/en-us/security-advisories/sophos-sa-20261021-php2shell)

---

## 📞 Contact

For questions or assistance, contact:
- CERT-EU: cert-eu@cert.europa.eu
- PHP Security Team: security@php.net

---

**© 2026 CERT-EU - European Computer Emergency Response Team**
