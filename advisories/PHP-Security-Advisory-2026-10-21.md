# PHP Security Advisory - October 21, 2026

## Critical Use-After-Free Vulnerabilities in PHP (CVE-2026-109618, CVE-2026-109619)

**Publication Date:** October 21, 2026  
**Last Updated:** November 6, 2026  
**Advisory ID:** PHP-SA-2026-10-21  
**CVE IDs:** CVE-2026-109618, CVE-2026-109619  
**Severity:** Critical (CVSS 9.2)

---

### Overview

The PHP development team has identified and fixed **critical Use-After-Free vulnerabilities** in the Zend Engine that affect PHP versions 8.4.x and 8.3.x. These vulnerabilities, collectively known as **PHP2Shell**, allow for **Remote Code Execution (RCE)** without authentication and are currently being **actively exploited in the wild**.

---

### Vulnerability Details

#### CVE-2026-109618: Use-After-Free via OOM in Zend Engine (session.upload_progress)

- **Type:** Use-After-Free (CWE-416)
- **Component:** Zend Engine - Session Upload Progress
- **CVSS Score:** 9.2 (Critical)
- **CVSS Vector:** CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
- **Status:** Fixed in PHP 8.4.27 and PHP 8.3.36

**Description:**

When `session.upload_progress.enabled` is set to `1` (the default in PHP 8.4.x), PHP tracks file upload progress using session variables. An attacker can send a massive multipart form data request that exceeds the PHP memory limit, causing an Out-of-Memory (OOM) condition. When the Zend Engine handles this error using `longjmp()`, it skips the cleanup step for `session.upload_progress` data, leaving stale pointers in memory. Subsequent requests can then trigger a Use-After-Free vulnerability, leading to Remote Code Execution.

#### CVE-2026-109619: Related Use-After-Free in PHP Session Handling

- **Type:** Use-After-Free (CWE-416)
- **Component:** Zend Engine - Session Management
- **CVSS Score:** 9.2 (Critical)
- **CVSS Vector:** CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H
- **Status:** Fixed in PHP 8.4.27 and PHP 8.3.36

**Description:**

This is a related vulnerability in PHP's session handling mechanism that can also be exploited through similar OOM trigger techniques. The fix for CVE-2026-109618 also addresses this vulnerability.

---

### Affected Versions

The following PHP versions are affected by these vulnerabilities:

| Version | Status |
|---------|--------|
| PHP 8.4.0 - PHP 8.4.26 | **VULNERABLE** |
| PHP 8.3.0 - PHP 8.3.35 | **VULNERABLE** (partial impact) |
| PHP 8.4.27 and later | **FIXED** |
| PHP 8.3.36 and later | **FIXED** (backported) |

---

### Fixed Versions

The vulnerabilities have been fixed in the following releases:

- **PHP 8.4.27** - Released October 22, 2026
- **PHP 8.3.36** - Released October 22, 2026 (backported fix)

---

### Impact

Successful exploitation of these vulnerabilities allows attackers to:

1. **Execute arbitrary code** on the server with the privileges of the web server process (typically `www-data`, `apache`, or `nobody`)
2. **Read, modify, or delete** files on the server
3. **Deploy malware** including ransomware
4. **Exfiltrate sensitive data** (databases, configuration files, etc.)
5. **Create backdoors** for persistent access
6. **Deface websites**
7. **Move laterally** within the network

---

### Exploitation

#### Exploitation Mechanism

1. Attacker identifies a vulnerable PHP server with `session.upload_progress.enabled = 1`
2. Attacker sends a POST request with multipart form data containing:
   - Content-Length > memory_limit (typically > 16MB)
   - `PHP_SESSION_UPLOAD_PROGRESS` parameter
   - Multiple form fields to exhaust memory
3. PHP attempts to parse the request and exceeds memory_limit
4. Zend Engine calls `longjmp()` to handle the error
5. `longjmp()` skips cleanup of `session.upload_progress` data
6. Stale pointers remain in memory
7. Attacker sends a second request to trigger Use-After-Free
8. Remote Code Execution is achieved

#### Exploitation in the Wild

CISA, CERT-EU, and independent security researchers have confirmed that these vulnerabilities are being **actively exploited in the wild** since at least October 17, 2026. Observed exploitation includes:

- **Ransomware attacks** targeting HR and finance departments
- **Data exfiltration** of HR databases and financial records
- **Website defacement** with hacker messages
- **Creation of backdoors** for persistent access

---

### Mitigation

#### Immediate Solution: Upgrade PHP

The **recommended and most effective** mitigation is to **upgrade to a fixed version of PHP** immediately:

**For PHP 8.4.x users:**
```bash
# Using Sury repository (Debian/Ubuntu)
apt-get update
apt-get install php8.4.27

# Manual compilation
wget https://www.php.net/distributions/php-8.4.27.tar.gz
tar -xzf php-8.4.27.tar.gz
cd php-8.4.27
./configure && make && make install
```

**For PHP 8.3.x users:**
```bash
# Using Sury repository (Debian/Ubuntu)
apt-get update
apt-get install php8.3.36

# Manual compilation
wget https://www.php.net/distributions/php-8.3.36.tar.gz
tar -xzf php-8.3.36.tar.gz
cd php-8.3.36
./configure && make && make install
```

After upgrading, restart your web server:
```bash
# Apache
systemctl restart apache2
# or
service apache2 restart

# Nginx with PHP-FPM
systemctl restart php8.4-fpm
# or
service php8.4-fpm restart
```

#### Temporary Mitigation: Disable session.upload_progress

If you cannot upgrade immediately, you can disable the vulnerable feature:

```ini
# In php.ini or a conf.d file (e.g., /etc/php/8.4/apache2/conf.d/99-disable-upload-progress.ini)
session.upload_progress.enabled = 0
```

Then restart your web server:
```bash
systemctl restart apache2
# or
service apache2 restart
```

**Note:** This is a temporary mitigation and does not fix the underlying vulnerability. You should still upgrade to a fixed version as soon as possible.

#### Partial Mitigation: Increase memory_limit

Increasing the `memory_limit` makes it harder for attackers to trigger the OOM condition, but it does not prevent exploitation completely:

```ini
# In php.ini
memory_limit = 128M
```

---

### Workarounds

#### Web Application Firewall (WAF)

Deploy a WAF with the following rules:

1. **Block large requests:**
   - Block requests with Content-Length > 10MB

2. **Block requests with many multipart parts:**
   - Block requests with more than 10 multipart parts

3. **Block specific parameters:**
   - Block requests containing `PHP_SESSION_UPLOAD_PROGRESS`

#### Apache Configuration

```apache
# Limit request body size
LimitRequestBody 10485760  # 10MB

# Disable multipart processing for large requests
LimitXMLRequestBody 10485760
```

#### Nginx Configuration

```nginx
# Limit client body size
client_max_body_size 10M;

# Limit multipart body
client_body_buffer_size 128k;
```

---

### Detection

#### Checking if Your Server is Vulnerable

1. **Check PHP version:**
   ```bash
   php -v
   ```

2. **Check session.upload_progress setting:**
   ```bash
   php -i | grep session.upload_progress.enabled
   # or
   php -r "echo ini_get('session.upload_progress.enabled');"
   ```

3. **Check for exploitation attempts:**
   ```bash
   # Apache access log - look for large POST requests
   grep "Content-Length.*[2-9][0-9][0-9][0-9][0-9][0-9]" /var/log/apache2/access.log
   
   # Apache error log - look for segmentation faults
   grep -i "segmentation fault" /var/log/apache2/error.log
   grep -i "Allowed memory size" /var/log/apache2/error.log
   
   # Check for proof files
   find /var/www -name "proof.*" -type f
   find /var/www -name ".h4ck3d" -type f
   ```

#### Indicators of Compromise (IOCs)

If your server has been compromised, you may find:

- **Network IOCs:**
  - HTTP POST requests with Content-Length > 16MB
  - Requests containing `PHP_SESSION_UPLOAD_PROGRESS`
  - Multiple multipart form data parts in a single request

- **Host IOCs:**
  - Apache error logs showing `segmentation fault`
  - PHP error logs showing `Allowed memory size exhausted`
  - Presence of files like:
    - `/var/www/html/proof.php`
    - `/var/www/html/.h4ck3d`
    - `/var/www/html/proof_ransomware.php`
    - `/var/www/html/DONNEES_RH_EXFILTREES.csv`
    - `/var/www/html/proof_deface.html`

---

### Response

If you believe your server has been compromised:

1. **Isolate the affected system** from the network
2. **Preserve logs and evidence** for forensic analysis
3. **Do not restart the system** as this may destroy evidence
4. **Contact your incident response team** or a cybersecurity professional
5. **Report the incident** to appropriate authorities:
   - CERT-EU: cert@cert.europa.eu
   - CISA: cisa@cisa.dhs.gov
   - Local CERT or CSIRT

---

### Credits

The PHP Security Team would like to thank the following individuals and organizations for their contributions to identifying and fixing these vulnerabilities:

- **Original Reporter:** Anonymous security researcher
- **PHP Security Team:** Sara Golemon, Nikita Popov, Joe Watkins
- **CERT-EU:** For coordinating disclosure and providing guidance
- **CISA:** For tracking exploitation in the wild
- **WatchTowerR:** For threat intelligence analysis
- **ANSSI:** For vulnerability analysis and coordination
- **Independent Security Researchers:** For additional testing and validation

---

### References

1. **CVE Details:**
   - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-109618
   - https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-109619

2. **CERT-EU Advisory:** https://cert.europa.eu/static/SecurityAdvisories/2026/CERT-EU-SA2026-018.txt

3. **CISA KEV Catalog:** https://www.cisa.gov/known-exploited-vulnerabilities-catalog

4. **WatchTowerR Analysis:** https://watchtowr.com/intelligence/php-cve-2026-109618-faq/

5. **ANSSI Alert:** https://cyberveille.esante.gouv.fr/alertes/php-cve-2026-109618-2026-10-21

6. **OpenCVE:**
   - https://app.opencve.io/cve/CVE-2026-109618
   - https://app.opencve.io/cve/CVE-2026-109619

---

### Timeline

| Date | Event |
|------|-------|
| October 17, 2026 | First reports of compromised PHP servers |
| October 17, 2026 | PHP Security Team receives initial report |
| October 18, 2026 | Security researchers confirm exploitation attempts |
| October 18-20, 2026 | PHP Security Team develops fix |
| October 21, 2026 | PHP Security Team publishes advisory |
| October 21, 2026 | CVE-2026-109618 and CVE-2026-109619 assigned |
| October 22, 2026 | PHP 8.4.27 and PHP 8.3.36 released with patches |
| October 22, 2026 | CERT-EU publishes alert |
| October 23, 2026 | CISA adds to Known Exploited Vulnerabilities catalog |
| November 6, 2026 | Mass exploitation observed |

---

### Contact

For questions or to report issues related to this advisory:

- **PHP Security Team:** security@php.net
- **PHP Bug Tracking System:** https://bugs.php.net/
- **PHP Mailing Lists:** https://www.php.net/mailing-lists.php

---

**Disclaimer:** The PHP Group is not responsible for the security of third-party applications or systems using PHP. Users and administrators are responsible for ensuring the security of their own systems and applications. This advisory is provided "as is" without warranty of any kind.
