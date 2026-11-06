# PHP2Shell Lab - CVE-2026-109618 & CVE-2026-109619 Demo

[![PHP Version](https://img.shields.io/badge/PHP-8.4.26%2F8.4.27-red.svg)](https://www.php.net/)
[![CVSS](https://img.shields.io/badge/CVSS-9.2-Critical-red.svg)](https://www.first.org/cvss/calculator/3.1#CVSS:3.1/AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:H)
[![CWE](https://img.shields.io/badge/CWE-416-Use%20After%20Free-blue.svg)](https://cwe.mitre.org/data/definitions/416.html)
[![Status](https://img.shields.io/badge/Status-Actively%20Exploited-red.svg)](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)

**PHP2Shell Lab** is a **realistic, interactive demonstration** of **CVE-2026-109618** and **CVE-2026-109619**, critical **Remote Code Execution (RCE)** vulnerabilities in PHP that allow attackers to execute arbitrary code **without authentication**.

> **⚠️ WARNING: This is a DEMONSTRATION ONLY. Do not use against production systems without authorization.**

---

## 📌 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Python 3.7+ with `requests` library
- 2GB+ RAM available

### Installation

```bash
# Clone the repository
git clone https://github.com/Warrex21187/blup.git
cd blup/php-lab

# Install Python dependencies
pip install -r requirements.txt

# Start the lab
docker compose up -d
```

### Access the Lab

- **Vulnerable Server (PHP 8.4.26):** http://localhost:8888
- **Patched Server (PHP 8.4.27):** http://localhost:8889
- **API Endpoints:**
  - Vulnerable: http://localhost:8888/api.php
  - Patched: http://localhost:8889/api.php

---

## 🎯 Features

### ✅ Realistic Exploitation

- **Use-After-Free via OOM** in Zend Engine (session.upload_progress)
- **No authentication required** - external attacker scenario
- **Multiple attack vectors** demonstrated:
  - OOM trigger via massive multipart upload
  - Ransomware deployment
  - Data exfiltration
  - Website defacement

### ✅ Interactive Demo

- **Attack Console** (`attack.py`) - Simulate attacks against vulnerable server
- **Exploit Script** (`exploit.py`) - Technical exploitation with proof
- **Verification Script** (`verify_exploit.py`) - Check for exploitation proofs
- **Monitor** (`monitor.py`) - Real-time log monitoring
- **Interactive Console** (`demo.py`) - Guided demonstration for presentations

### ✅ Educational Value

- **Official advisories** included (CERT-EU, CISA, PHP Security Team)
- **Technical explanations** of the vulnerability
- **Step-by-step** attack demonstration
- **Comparison** of vulnerable vs patched servers
- **Remediation guidance**

### ✅ Visual Feedback

- **Color-coded** output for easy understanding
- **Real-time logs** from Apache and PHP
- **Proof files** generated on exploitation
- **Status pages** showing server state

---

## 🚀 Usage

### 1. Start the Lab

```bash
# Start all containers
docker compose up -d

# Check running containers
docker compose ps
```

Expected output:
```
NAME                     COMMAND                  SERVICE             CREATED          STATUS          PORTS
php2shell-log-monitor    "sh -c 'tail -f /var…"   log-monitor         5 seconds ago    Up 5 seconds    
php2shell-patched        "/start-apache.sh"       patched             5 seconds ago    Up 5 seconds    0.0.0.0:8889->80/tcp
php2shell-vuln           "/start-apache.sh"       vulnerable          5 seconds ago    Up 5 seconds    0.0.0.0:8888->80/tcp
```

### 2. Check Server Status

```bash
# Check vulnerable server
curl http://localhost:8888/api.php?action=status | python -m json.tool

# Check patched server
curl http://localhost:8889/api.php?action=status | python -m json.tool
```

### 3. Run Attacks

#### Using attack.py

```bash
# Trigger OOM vulnerability
python attack.py --oom

# Deploy ransomware
python attack.py --ransomware

# Exfiltrate data
python attack.py --steal

# Deface website
python attack.py --deface

# Restore vulnerable server
python attack.py --restore

# Compare vulnerable vs patched
python attack.py --compare
```

#### Using exploit.py

```bash
# Full demonstration
python exploit.py --target http://localhost:8888 --demo

# Trigger OOM
python exploit.py --target http://localhost:8888 --oom

# Create proof file
python exploit.py --target http://localhost:8888 --proof
```

#### Using demo.py (Interactive)

```bash
python demo.py
```

Then use commands:
- `status` - Check server status
- `histoire` - Show the story behind the vulnerability
- `expliquer` - Explain technical details
- `fuite` - Demonstrate data exfiltration
- `recette` / `ransomware` - Deploy ransomware
- `vol` / `steal` - Exfiltrate data
- `deface` - Deface website
- `restore` - Restore server
- `duel` - Compare vulnerable vs patched
- `remediation` - Show remediation steps
- `demo` - Run complete demonstration
- `aide` / `help` - Show help
- `quitter` / `quit` / `exit` - Exit

### 4. Verify Exploitation

```bash
# Check for proof files
python verify_exploit.py --target http://localhost:8888
```

### 5. Monitor Logs

```bash
# Monitor Apache logs in real-time
python monitor.py --logs

# Check server status
python monitor.py --status
```

### 6. Access Web Interface

Open your browser and navigate to:
- **Vulnerable Server:** http://localhost:8888
- **Patched Server:** http://localhost:8889

---

## 🏗️ Architecture

### Docker Containers

```
+------------------+     +------------------+     +------------------+
|   Vulnerable     |     |     Patched      |     |   Log Monitor    |
|   (PHP 8.4.26)   |     |   (PHP 8.4.27)   |     |                  |
+------------------+     +------------------+     +------------------+
        |                        |                        |
        v                        v                        v
+------------------+     +------------------+     +------------------+
|   Port 8888      |     |   Port 8889      |     |   Logs          |
|   (HTTP)         |     |   (HTTP)         |     |   (Read-only)    |
+------------------+     +------------------+     +------------------+
```

### Configuration Details

| Container | PHP Version | session.upload_progress.enabled | Memory Limit | Status |
|-----------|-------------|--------------------------------|--------------|--------|
| Vulnerable | 8.4.26 | **1 (ON)** | 16M | ❌ VULNERABLE |
| Patched | 8.4.27 | **0 (OFF)** | 16M | ✅ PROTECTED |

### File Structure

```
php-lab/
├── docker-compose.yml          # Docker Compose configuration
├── README.md                    # This file
├── requirements.txt              # Python dependencies
│
├── vulnerable/                  # Vulnerable server (PHP 8.4.26)
│   ├── Dockerfile                # Dockerfile for vulnerable server
│   ├── www/                      # Website files
│   │   ├── api.php               # REST API endpoint
│   │   ├── index.php             # Web portal
│   │   ├── upload.php            # OOM trigger endpoint
│   │   └── status.json           # Initial status
│   └── logs/                     # Apache logs (created at runtime)
│
├── patched/                     # Patched server (PHP 8.4.27)
│   ├── Dockerfile                # Dockerfile for patched server
│   ├── www/                      # Website files
│   │   ├── api.php               # REST API endpoint
│   │   ├── index.php             # Web portal
│   │   ├── upload.php            # Secure upload handler
│   │   └── status.json           # Initial status
│   └── logs/                     # Apache logs (created at runtime)
│
├── advisories/                  # Official security advisories
│   ├── CERT-EU-2026-018-PHP2Shell.md
│   ├── CISA-KEV-CVE-2026-109618-109619.md
│   └── PHP-Security-Advisory-2026-10-21.md
│
└── scripts/                     # Python scripts
    ├── attack.py                 # Attack console
    ├── demo.py                   # Interactive demo
    ├── exploit.py                # Technical exploit
    ├── monitor.py                # Log monitor
    └── verify_exploit.py         # Verification script
```

---

## 🔍 Technical Details

### CVE-2026-109618: Use-After-Free via OOM in Zend Engine

#### Root Cause

When `session.upload_progress.enabled` is set to `1`, PHP tracks file upload progress using session variables. The vulnerability occurs when:

1. An attacker sends a **massive multipart form data request** (> memory_limit)
2. PHP attempts to parse the request and **exceeds the memory limit**
3. Zend Engine calls **`longjmp()`** to handle the error
4. **`longjmp()` skips the cleanup step** for `session.upload_progress` data
5. **Stale pointers remain in memory**
6. Subsequent requests can **trigger Use-After-Free**
7. **Remote Code Execution** is achieved

#### Attack Vector

```
Attacker
   │
   ▼
POST /upload.php HTTP/1.1
Content-Type: multipart/form-data; boundary=----...
Content-Length: 26214400 (25MB > 16MB limit)

--boundary
Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"

upload_php2shell
--boundary
Content-Disposition: form-data; name="field0"

[A * 1MB]
--boundary
Content-Disposition: form-data; name="field1"

[A * 1MB]
...
--boundary--
   │
   ▼
PHP Zend Engine
   │
   ▼ (1) Parse multipart data
   ▼ (2) Exceed memory_limit (16MB)
   ▼ (3) Call longjmp() to handle OOM
   ▼ (4) Skip cleanup of session.upload_progress
   ▼ (5) Stale pointers remain
   │
   ▼
Next Request
   │
   ▼ (6) Trigger Use-After-Free
   ▼ (7) Remote Code Execution!
```

### CVE-2026-109619: Related Use-After-Free

This is a related vulnerability in PHP's session handling that can also be exploited through similar OOM trigger techniques. The fix for CVE-2026-109618 also addresses this vulnerability.

---

## 🛡️ Security & Mitigation

### Mitigation Steps

#### 1. Upgrade PHP (Recommended)

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

#### 2. Disable session.upload_progress (Temporary)

```ini
# In php.ini or a conf.d file
session.upload_progress.enabled = 0
```

Then restart Apache:
```bash
systemctl restart apache2
```

#### 3. Increase memory_limit (Partial)

```ini
# In php.ini
memory_limit = 128M
```

Note: This only makes exploitation harder but does not prevent it.

### Web Application Firewall (WAF) Rules

```apache
# Apache configuration
LimitRequestBody 10485760  # 10MB
```

```nginx
# Nginx configuration
client_max_body_size 10M;
```

### Detection

#### Log Analysis

```bash
# Apache access log - look for large POST requests
grep "Content-Length.*[2-9][0-9][0-9][0-9][0-9][0-9]" /var/log/apache2/access.log

# Apache error log - look for segmentation faults
grep -i "segmentation fault" /var/log/apache2/error.log
grep -i "Allowed memory size" /var/log/apache2/error.log
```

#### File System Analysis

```bash
# Check for proof files
find /var/www -name "proof.*" -type f
find /var/www -name ".h4ck3d" -type f

# Check for recently modified PHP files
find /var/www -name "*.php" -type f -mtime -1
```

---

## 📊 Official Advisories

This demo includes **official security advisories** from:

1. **[CERT-EU Security Advisory 2026-018](advisories/CERT-EU-2026-018-PHP2Shell.md)**
   - Published: October 21, 2026
   - CVSS: 9.2 (Critical)
   - Includes: IOCs, mitigation, detection

2. **[CISA KEV Catalog Entry](advisories/CISA-KEV-CVE-2026-109618-109619.md)**
   - Published: October 23, 2026
   - Status: Known Exploited Vulnerability
   - Required action within 14 days

3. **[PHP Security Advisory](advisories/PHP-Security-Advisory-2026-10-21.md)**
   - Published: October 21, 2026
   - Advisory ID: PHP-SA-2026-10-21
   - Includes: Technical details, timeline, credits

---

## 🎓 Educational Use

### For Cybersecurity Awareness Sessions

This demo is designed for **cybersecurity awareness sessions** and **educational purposes**. It demonstrates:

1. **How vulnerabilities work** - Technical explanation of Use-After-Free
2. **Real-world impact** - Ransomware, data theft, defacement
3. **Importance of patching** - Comparison of vulnerable vs patched servers
4. **Detection and response** - Log analysis and monitoring
5. **Mitigation strategies** - Configuration changes and WAF rules

### For Non-Technical Audiences

The demo includes:
- **Visual indicators** (red/green color coding)
- **Simple explanations** of complex concepts
- **Interactive elements** to keep audience engaged
- **Real-time feedback** showing attack results

### For Technical Audiences

The demo provides:
- **Technical details** of the vulnerability
- **Exploitation code** and techniques
- **Mitigation guidance** from official sources
- **Detection signatures** for security teams

---

## ⚠️ Important Notes

### Legal Considerations

- **Only use this demo on systems you own or have permission to test**
- **Do not use against production systems**
- **Do not use against systems without authorization**
- **Comply with all applicable laws and regulations**

### Limitations

- This is a **simulation** of the vulnerability for educational purposes
- The actual CVE-2026-109618 exploit is more complex than demonstrated
- PHP 8.4.26/8.4.27 are **simulated** using PHP 8.3 with version overrides
- The demo uses **safe, non-destructive** attacks for demonstration

### Requirements

- Docker and Docker Compose must be installed
- Python 3.7+ with `requests` library
- Minimum 2GB RAM (4GB recommended)
- Ports 8888 and 8889 must be available

---

## 📚 References

### Official Sources

- [PHP Security Advisory](https://www.php.net/archives/2026.php#2026-10-21-1)
- [CVE-2026-109618](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-109618)
- [CVE-2026-109619](https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2026-109619)
- [CERT-EU Advisory](https://cert.europa.eu/static/SecurityAdvisories/2026/CERT-EU-SA2026-018.txt)
- [CISA KEV Catalog](https://www.cisa.gov/known-exploited-vulnerabilities-catalog)
- [OpenCVE - CVE-2026-109618](https://app.opencve.io/cve/CVE-2026-109618)
- [OpenCVE - CVE-2026-109619](https://app.opencve.io/cve/CVE-2026-109619)

### Analysis & Intelligence

- [WatchTowerR FAQ](https://watchtowr.com/intelligence/php-cve-2026-109618-faq/)
- [ANSSI Alert](https://cyberveille.esante.gouv.fr/alertes/php-cve-2026-109618-2026-10-21)

---

## 📝 Changelog

| Date | Version | Changes |
|------|---------|---------|
| November 6, 2026 | 1.0.0 | Initial release - Complete PHP2Shell demo with official advisories |

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests, report issues, or suggest improvements.

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **PHP Security Team** for their work on fixing the vulnerability
- **CERT-EU** for coordinating disclosure
- **CISA** for tracking exploitation
- **WatchTowerR** for threat intelligence
- **ANSSI** for vulnerability analysis
- **Independent security researchers** for their contributions

---

**Stay secure! 🔒**
