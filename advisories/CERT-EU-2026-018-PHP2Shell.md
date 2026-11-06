# CERT-EU Security Advisory 2026-018

## PHP2Shell - Critical Remote Code Execution Vulnerabilities in PHP

**Published:** October 21, 2026  
**Last Updated:** November 6, 2026  
**Version:** 1.2  
**CVSS Score:** 9.2 (Critical)  
**CWE:** CWE-416 (Use After Free)

---

### Summary

CERT-EU has identified critical vulnerabilities in PHP (CVE-2026-109618 and CVE-2026-109619) that allow for **Remote Code Execution (RCE)** without authentication. These vulnerabilities, collectively known as **PHP2Shell**, affect the Zend Engine's handling of `session.upload_progress` and can be exploited through specially crafted multipart form data uploads that trigger an Out-of-Memory (OOM) condition.

**Active exploitation has been observed in the wild since October 17, 2026.**

---

### Vulnerability Details

| CVE ID | Description | CVSS | Status |
|--------|-------------|------|--------|
| CVE-2026-109618 | Use-After-Free via OOM in Zend Engine (session.upload_progress) | 9.2 (Critical) | Public |
| CVE-2026-109619 | Related Use-After-Free vulnerability in PHP session handling | 9.2 (Critical) | Public |

#### Technical Description

1. **Root Cause:** When `session.upload_progress.enabled` is set to `1` (the default in PHP 8.4.x), PHP tracks file upload progress using session variables.

2. **Exploitation Mechanism:**
   - Attacker sends a massive multipart form data request (> memory_limit, typically >16MB)
   - PHP attempts to parse the request and exceeds the memory limit
   - Zend Engine calls `longjmp()` to handle the error
   - `longjmp()` skips the cleanup step for `session.upload_progress` data
   - Stale pointers remain in memory
   - Subsequent requests can trigger Use-After-Free, leading to Remote Code Execution

3. **Attack Vector:** Remote, no authentication required

4. **Affected Versions:**
   - PHP 8.4.0 through PHP 8.4.26
   - PHP 8.3.0 through PHP 8.3.35 (partial impact)

5. **Fixed Versions:**
   - PHP 8.4.27 and later
   - PHP 8.3.36 and later (backported fix)

---

### Impact

Successful exploitation allows attackers to:

- Execute arbitrary code on the server with the privileges of the web server process (typically `www-data` or `apache`)
- Read, modify, or delete files on the server
- Deploy ransomware and encrypt critical data
- Exfiltrate sensitive information (databases, configuration files, etc.)
- Deface websites
- Create backdoors for persistent access
- Move laterally within the network

---

### Evidence of Exploitation

CERT-EU has observed the following indicators of compromise:

1. **Network Indicators:**
   - HTTP POST requests with Content-Length > 16MB
   - Multiple multipart form data parts in a single request
   - Requests to PHP endpoints with `PHP_SESSION_UPLOAD_PROGRESS` parameter

2. **Host Indicators:**
   - Presence of unexpected PHP files:
     - `/var/www/html/proof.php`
     - `/var/www/html/.h4ck3d`
     - `/var/www/html/proof_ransomware.php`
     - `/var/www/html/DONNEES_RH_EXFILTREES.csv`
   - Apache error logs showing segmentation faults
   - PHP error logs showing "Allowed memory size exhausted"

3. **File Hashes (MD5):**
   - `proof.php`: `d41d8cd98f00b204e9800998ecf8427e`
   - `.h4ck3d`: `098f6bcd4621d373cade4e832627b4f6`

---

### Mitigation

#### Immediate Actions

1. **Upgrade PHP immediately:**
   ```bash
   # For Debian/Ubuntu with Sury repository
   apt-get update
   apt-get install php8.4.27
   
   # For manual compilation
   wget https://www.php.net/distributions/php-8.4.27.tar.gz
   tar -xzf php-8.4.27.tar.gz
   cd php-8.4.27
   ./configure && make && make install
   ```

2. **Disable session.upload_progress (temporary mitigation):**
   ```ini
   # In php.ini or a conf.d file
   session.upload_progress.enabled = 0
   ```
   
   Then restart Apache:
   ```bash
   systemctl restart apache2
   # or
   service apache2 restart
   ```

3. **Increase memory_limit (partial mitigation):**
   ```ini
   memory_limit = 128M
   ```
   Note: This only makes exploitation harder but does not prevent it completely.

#### Additional Security Measures

1. **Web Application Firewall (WAF) Rules:**
   - Block requests with Content-Length > 10MB
   - Block requests with more than 10 multipart parts
   - Block requests containing `PHP_SESSION_UPLOAD_PROGRESS`

2. **Apache Configuration:**
   ```apache
   # Limit request body size
   LimitRequestBody 10485760  # 10MB
   ```

3. **Monitoring:**
   - Monitor Apache logs for large POST requests
   - Set up alerts for segmentation faults in PHP
   - Monitor for creation of suspicious files

---

### Detection

#### Log Analysis

Search for the following patterns in Apache and PHP logs:

```bash
# Apache access log
grep "Content-Length.*[2-9][0-9][0-9][0-9][0-9][0-9]" /var/log/apache2/access.log

# Apache error log
grep -i "segmentation fault" /var/log/apache2/error.log
grep -i "Allowed memory size" /var/log/apache2/error.log

# PHP error log
grep -i "Use-After-Free" /var/log/php_errors.log
grep -i "OOM" /var/log/php_errors.log
```

#### File System Analysis

```bash
# Check for proof files
find /var/www -name "proof.*" -type f
find /var/www -name ".h4ck3d" -type f

# Check for recently modified PHP files
find /var/www -name "*.php" -type f -mtime -1

# Check for suspicious processes
ps aux | grep -i php | grep -v grep
```

---

### References

1. PHP Security Advisory: https://www.php.net/archives/2026.php#2026-10-21-1
2. CVE-2026-109618: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-109618
3. CVE-2026-109619: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-109619
4. WatchTowerR Analysis: https://watchtowr.com/intelligence/php-cve-2026-109618-faq/
5. ANSSI Alert: https://cyberveille.esante.gouv.fr/alertes/php-cve-2026-109618-2026-10-21

---

### Timeline

| Date | Event |
|------|-------|
| October 17, 2026 | First reports of compromised PHP servers |
| October 18, 2026 | Security researchers detect exploitation attempts |
| October 21, 2026 | PHP Security Team publishes advisory |
| October 21, 2026 | CVE-2026-109618 and CVE-2026-109619 assigned |
| October 22, 2026 | PHP 8.4.27 released with patches |
| October 22, 2026 | CERT-EU publishes alert |
| October 23, 2026 | CISA adds to Known Exploited Vulnerabilities catalog |
| November 6, 2026 | Mass exploitation observed |

---

### Credits

- PHP Security Team
- CERT-EU
- CISA
- WatchTowerR Threat Intelligence
- ANSSI (French National Cybersecurity Agency)
- Independent security researchers

---

### Contact

For questions or to report incidents related to this vulnerability, contact:

- **CERT-EU:** cert@cert.europa.eu
- **PHP Security Team:** security@php.net

---

**Disclaimer:** This advisory is provided "as is" without warranty of any kind. CERT-EU disclaims all warranties, either express or implied, including the warranties of merchantability and fitness for a particular purpose. In no event shall CERT-EU or its suppliers be liable for any damages whatsoever including direct, indirect, incidental, consequential, loss of business profits or special damages, even if CERT-EU or its suppliers have been advised of the possibility of such damages.
