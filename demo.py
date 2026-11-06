#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHP2Shell Interactive Demo Console - CVE-2026-109618 & CVE-2026-109619
Critical Remote Code Execution Vulnerabilities in PHP

CVSS: 9.2 (Critical)
CWE: CWE-416 (Use After Free)
Publication: October 21, 2026
Exploitation: Active in the wild since October 17, 2026
"""

import sys
import time
import requests
import subprocess

# Support UTF-8 on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


# Terminal Colors
class Color:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    PURPLE = "\033[95m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"


WIDTH = 80


def sep():
    return "-" * WIDTH


def print_header(title):
    print(f"\n{Color.BOLD}{sep()}")
    print(f"  {title}")
    print(f"{sep()}{Color.RESET}")


def print_step(num, title, description):
    print(f"\n{Color.CYAN}{sep()}")
    print(f"{Color.BOLD}[Step {num}]{Color.RESET} {Color.BLUE}{title}{Color.RESET}")
    print(f"{Color.YELLOW}-> {description}{Color.RESET}")
    print(f"{Color.CYAN}{sep()}{Color.RESET}")


def print_banner():
    print(f"""{Color.RED}
  +------------------------------------------------------------------+
  |  PHP2Shell Interactive Demo Console                              |
  |  CVE-2026-109618 & CVE-2026-109619 (Critical RCE)                 |
  |                                                                  |
  |  CVSS: 9.2 (Critical)  CWE: CWE-416 (Use After Free)              |
  |  Publication: October 21, 2026                                   |
  |  Status: ACTIVELY EXPLOITED IN THE WILD                          |
  +------------------------------------------------------------------+
{Color.RESET}
{Color.BOLD}  [+] Role: External attacker (No credentials required)             {Color.RESET}
{Color.BOLD}  [+] Target: PHP 8.4.26 (vulnerable) vs PHP 8.4.27 (patched)          {Color.RESET}
{Color.BOLD}  [+] Vector: session.upload_progress.enabled + OOM trigger           {Color.RESET}
""")


def check_servers():
    """Check if servers are running"""
    print_header("SERVER STATUS")
    
    servers = [
        ("localhost:8888", "VULNERABLE (PHP 8.4.26)"),
        ("localhost:8889", "PATCHED (PHP 8.4.27)")
    ]
    
    for host, label in servers:
        try:
            r = requests.get(f"http://{host}/api.php?action=status", timeout=3)
            if r.status_code == 200:
                data = r.json()
                php_version = data.get('php_version', '?')
                is_vuln = data.get('is_vulnerable', False)
                upload_progress = data.get('upload_progress_enabled', False)
                
                verdict = f"{Color.RED}VULNERABLE" if is_vuln else f"{Color.GREEN}PROTECTED"
                upload_status = f"{Color.RED}ON" if upload_progress else f"{Color.GREEN}OFF"
                
                print(f"  {label:<25} {Color.WHITE}PHP {php_version}{Color.RESET} | Status: {verdict}{Color.RESET} | upload_progress: {upload_status}{Color.RESET}")
            else:
                print(f"  {label:<25} {Color.RED}unreachable (HTTP {r.status_code}){Color.RESET}")
        except Exception as err:
            print(f"  {label:<25} {Color.RED}error: {err}{Color.RESET}")
    
    print()


def show_story():
    """Display the story behind the vulnerability"""
    print_header("THE STORY BEHIND CVE-2026-109618")
    
    print(f"""
{Color.WHITE}  On October 17, 2026, security researchers detected unusual{Color.RESET}
{Color.WHITE}  activity on PHP-based web servers. Multiple servers were{Color.RESET}
{Color.WHITE}  crashing with segmentation faults after processing large{Color.RESET}
{Color.WHITE}  multipart form uploads.{Color.RESET}

{Color.YELLOW}  October 18, 2026:{Color.RESET}
{Color.WHITE}  - First reports of compromised PHP servers{Color.RESET}
{Color.WHITE}  - Attackers exploiting unknown vulnerability{Color.RESET}
{Color.WHITE}  - Ransomware deployed on multiple targets{Color.RESET}

{Color.RED}  October 21, 2026:{Color.RESET}
{Color.WHITE}  - PHP Security Team publishes advisory{Color.RESET}
{Color.WHITE}  - CVE-2026-109618 assigned (CVSS: 9.2 Critical){Color.RESET}
{Color.WHITE}  - Use-After-Free in Zend Engine session.upload_progress{Color.RESET}
{Color.WHITE}  - CVE-2026-109619 assigned (related vulnerability){Color.RESET}

{Color.GREEN}  October 22, 2026:{Color.RESET}
{Color.WHITE}  - PHP 8.4.27 released with patches{Color.RESET}
{Color.WHITE}  - CERT-EU publishes alert{Color.RESET}
{Color.WHITE}  - CISA adds to Known Exploited Vulnerabilities catalog{Color.RESET}

{Color.PURPLE}  November 6, 2026 (TODAY):{Color.RESET}
{Color.WHITE}  - Mass exploitation in progress{Color.RESET}
{Color.WHITE}  - Organizations scrambling to patch{Color.RESET}
{Color.WHITE}  - This demo shows the vulnerability in action{Color.RESET}
""")


def explain_vulnerability():
    """Explain the technical details"""
    print_header("TECHNICAL EXPLANATION")
    
    print(f"""
{Color.BOLD}{Color.RED}CVE-2026-109618: Use-After-Free via OOM in Zend Engine{Color.RESET}

{Color.WHITE}  Technical Details:{Color.RESET}
{Color.YELLOW}  - Vulnerability Type: Use-After-Free (CWE-416){Color.RESET}
{Color.YELLOW}  - Component: Zend Engine session.upload_progress{Color.RESET}
{Color.YELLOW}  - Attack Vector: Remote, no authentication required{Color.RESET}
{Color.YELLOW}  - CVSS Score: 9.2 (Critical){Color.RESET}

{Color.WHITE}  How it works:{Color.RESET}

{Color.CYAN}  1. Attacker sends massive multipart form data (>16MB){Color.RESET}
{Color.CYAN}  2. PHP tries to parse the request{Color.RESET}
{Color.CYAN}  3. Memory limit (16M) is exceeded -> OOM condition{Color.RESET}
{Color.CYAN}  4. Zend Engine calls longjmp() to handle error{Color.RESET}
{Color.CYAN}  5. longjmp() skips cleanup of session.upload_progress data{Color.RESET}
{Color.CYAN}  6. Stale pointers remain in memory{Color.RESET}
{Color.CYAN}  7. Next request can trigger Use-After-Free{Color.RESET}
{Color.CYAN}  8. Remote Code Execution achieved{Color.RESET}

{Color.WHITE}  Configuration required for exploitation:{Color.RESET}
{Color.GREEN}  - session.upload_progress.enabled = 1 (DEFAULT in PHP 8.4.26){Color.RESET}
{Color.GREEN}  - memory_limit < size of upload (e.g., 16M){Color.RESET}

{Color.WHITE}  Mitigation:{Color.RESET}
{Color.GREEN}  - Upgrade to PHP 8.4.27 or later{Color.RESET}
{Color.GREEN}  - Set session.upload_progress.enabled = 0 in php.ini{Color.RESET}
""")


def trigger_data_leak():
    """Demonstrate data exfiltration"""
    print_header("DATA EXFILTRATION DEMO")
    
    print_step(1, "Reconnaissance", "Checking vulnerable server...")
    
    try:
        r = requests.post("http://localhost:8888/api.php", 
                         data={"action": "steal"}, 
                         timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Data exfiltration successful!{Color.RESET}")
            print(f"{Color.YELLOW}[*] File created: DONNEES_RH_EXFILTREES.csv{Color.RESET}")
            print(f"{Color.YELLOW}[*] Records exfiltrated: 12,482{Color.RESET}")
            print(f"{Color.YELLOW}[*] Data includes: SSN, Addresses, Salaries, Performance Reviews{Color.RESET}")
            
            # Try to verify the file exists
            try:
                r2 = requests.get("http://localhost:8888/DONNEES_RH_EXFILTREES.csv", timeout=3)
                if r2.status_code == 200:
                    print(f"{Color.GREEN}[+] File accessible at: http://localhost:8888/DONNEES_RH_EXFILTREES.csv{Color.RESET}")
            except:
                pass
        else:
            print(f"{Color.RED}[-] Attack failed (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}")
    
    print()


def trigger_ransomware():
    """Demonstrate ransomware deployment"""
    print_header("RANSOMWARE DEPLOYMENT DEMO")
    
    print_step(1, "Initial Access", "Exploiting CVE-2026-109618...")
    
    try:
        r = requests.post("http://localhost:8888/api.php", 
                         data={"action": "ransomware"}, 
                         timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Ransomware deployed!{Color.RESET}")
            print(f"{Color.RED}[!] WARNING: This is a simulation!{Color.RESET}")
            print(f"{Color.YELLOW}[*] Files encrypted: 842{Color.RESET}")
            print(f"{Color.YELLOW}[*] Ransom demanded: 50,000 EUR{Color.RESET}")
            print(f"{Color.YELLOW}[*] Website now shows ransom note{Color.RESET}")
            print(f"{Color.YELLOW}[*] Check: http://localhost:8888{Color.RESET}")
        else:
            print(f"{Color.RED}[-] Attack failed (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}")
    
    print()


def trigger_deface():
    """Demonstrate website defacement"""
    print_header("WEBSITE DEFACEMENT DEMO")
    
    print_step(1, "Initial Access", "Exploiting CVE-2026-109618...")
    
    try:
        r = requests.post("http://localhost:8888/api.php", 
                         data={"action": "deface"}, 
                         timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Website defaced!{Color.RESET}")
            print(f"{Color.YELLOW}[*] Homepage replaced with hacker message{Color.RESET}")
            print(f"{Color.YELLOW}[*] Message: HACKED BY PHP2Shell{Color.RESET}")
            print(f"{Color.YELLOW}[*] Check: http://localhost:8888{Color.RESET}")
        else:
            print(f"{Color.RED}[-] Attack failed (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}")
    
    print()


def trigger_restore():
    """Restore the vulnerable server"""
    print_header("RESTORING VULNERABLE SERVER")
    
    try:
        r = requests.post("http://localhost:8888/api.php", 
                         data={"action": "restore"}, 
                         timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Vulnerable server restored!{Color.RESET}")
            print(f"{Color.YELLOW}[*] Website is back to normal state{Color.RESET}")
        else:
            print(f"{Color.RED}[-] Restore failed (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}")
    
    print()


def trigger_duel():
    """Compare vulnerable vs patched"""
    print_header("VULNERABLE vs PATCHED: THE DUEL")
    
    print_step(1, "Attack on Vulnerable Server", "Testing PHP 8.4.26...")
    
    # Attack vulnerable server
    try:
        r = requests.post("http://localhost:8888/api.php", 
                         data={"action": "ransomware"}, 
                         timeout=5)
        if r.status_code == 200:
            print(f"{Color.RED}[+] VULNERABLE SERVER: COMPROMISED!{Color.RESET}")
        else:
            print(f"{Color.RED}[-] VULNERABLE SERVER: Attack failed{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] VULNERABLE SERVER: Error - {e}{Color.RESET}")
    
    print()
    print_step(2, "Attack on Patched Server", "Testing PHP 8.4.27...")
    
    # Attack patched server
    try:
        r = requests.post("http://localhost:8889/api.php", 
                         data={"action": "ransomware"}, 
                         timeout=5)
        if r.status_code == 403:
            print(f"{Color.GREEN}[+] PATCHED SERVER: ATTACK BLOCKED!{Color.RESET}")
            print(f"{Color.GREEN}[+] Security patch is working!{Color.RESET}")
        else:
            print(f"{Color.RED}[-] PATCHED SERVER: Unexpected response (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] PATCHED SERVER: Error - {e}{Color.RESET}")
    
    print()
    print(f"{Color.CYAN}{sep()}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  CONCLUSION:{Color.RESET}")
    print(f"{Color.CYAN}  - PHP 8.4.26 (vulnerable): Can be exploited{Color.RESET}")
    print(f"{Color.CYAN}  - PHP 8.4.27 (patched): Protected against attacks{Color.RESET}")
    print(f"{Color.CYAN}  - Always keep your PHP updated!{Color.RESET}")
    print(f"{Color.CYAN}{sep()}{Color.RESET}\n")


def show_remediation():
    """Show remediation steps"""
    print_header("REMEDIATION STEPS")
    
    print(f"""
{Color.GREEN}  IMMEDIATE ACTIONS:{Color.RESET}

{Color.WHITE}  1. UPGRADE PHP:{Color.RESET}
{Color.YELLOW}     - Upgrade to PHP 8.4.27 or later{Color.RESET}
{Color.YELLOW}     - apt-get update && apt-get install php8.4.27{Color.RESET}

{Color.WHITE}  2. DISABLE session.upload_progress:{Color.RESET}
{Color.YELLOW}     - Edit php.ini: session.upload_progress.enabled = 0{Color.RESET}
{Color.YELLOW}     - Or create conf.d file with same setting{Color.RESET}

{Color.WHITE}  3. INCREASE memory_limit (temporary mitigation):{Color.RESET}
{Color.YELLOW}     - Set memory_limit = 128M or higher{Color.RESET}
{Color.YELLOW}     - This makes OOM trigger harder but not impossible{Color.RESET}

{Color.WHITE}  4. MONITOR for exploitation attempts:{Color.RESET}
{Color.YELLOW}     - Check Apache logs for large multipart requests{Color.RESET}
{Color.YELLOW}     - Look for requests > 16MB in size{Color.RESET}
{Color.YELLOW}     - Monitor for files like proof.php, .h4ck3d, etc.{Color.RESET}

{Color.WHITE}  5. APPLY WAF RULES:{Color.RESET}
{Color.YELLOW}     - Block requests with Content-Length > 10MB{Color.RESET}
{Color.YELLOW}     - Block requests with many multipart parts{Color.RESET}

{Color.RED}  OFFICIAL ADVISORIES:{Color.RESET}
{Color.WHITE}  - PHP Security Advisory: https://www.php.net/archives/2026.php#2026-10-21-1{Color.RESET}
{Color.WHITE}  - CERT-EU: https://cert.europa.eu/static/SecurityAdvisories/2026/CERT-EU-SA2026-018.txt{Color.RESET}
{Color.WHITE}  - CISA KEV: https://www.cisa.gov/sites/default/files/known_exploited_vulnerabilities_catalog.csv{Color.RESET}
""")


def run_demo():
    """Run the complete demonstration"""
    print_banner()
    
    print(f"{Color.CYAN}{sep()}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  COMPLETE DEMONSTRATION OF CVE-2026-109618{Color.RESET}")
    print(f"{Color.CYAN}{sep()}{Color.RESET}\n")
    
    # Check servers
    check_servers()
    
    # Step 1: Data Leak
    print_step(1, "Data Exfiltration", "Stealing HR database...")
    trigger_data_leak()
    
    # Step 2: Ransomware
    print_step(2, "Ransomware Deployment", "Encrypting files...")
    trigger_ransomware()
    
    # Step 3: Restore
    print_step(3, "Restore", "Returning to normal state...")
    trigger_restore()
    
    # Step 4: Deface
    print_step(4, "Website Defacement", "Hacking the homepage...")
    trigger_deface()
    
    # Step 5: Duel
    print_step(5, "The Duel", "Vulnerable vs Patched...")
    trigger_duel()
    
    print(f"{Color.CYAN}{sep()}{Color.RESET}")
    print(f"{Color.BOLD}{Color.CYAN}  DEMONSTRATION COMPLETE{Color.RESET}")
    print(f"{Color.CYAN}{sep()}{Color.RESET}\n")


def show_help():
    """Show help menu"""
    print_banner()
    
    commands = {
        "status": "Check server status",
        "histoire": "Show the story behind the vulnerability",
        "expliquer": "Explain the technical details",
        "fuite": "Demonstrate data exfiltration",
        "recette": "Demonstrate ransomware deployment",
        "ransomware": "Demonstrate ransomware deployment",
        "vol": "Demonstrate data theft",
        "steal": "Demonstrate data theft",
        "deface": "Demonstrate website defacement",
        "restore": "Restore vulnerable server",
        "duel": "Compare vulnerable vs patched",
        "remediation": "Show remediation steps",
        "demo": "Run complete demonstration",
        "aide": "Show this help menu",
        "quitter": "Quit the console"
    }
    
    print(f"{Color.CYAN}Available commands:{Color.RESET}\n")
    for cmd, desc in commands.items():
        print(f"  {Color.GREEN}{cmd:<15}{Color.RESET} - {desc}")
    print()


def main():
    print_banner()
    
    commands = {
        "status": check_servers,
        "histoire": show_story,
        "story": show_story,
        "expliquer": explain_vulnerability,
        "explain": explain_vulnerability,
        "fuite": trigger_data_leak,
        "leak": trigger_data_leak,
        "steal": trigger_data_leak,
        "vol": trigger_data_leak,
        "recette": trigger_ransomware,
        "ransomware": trigger_ransomware,
        "deface": trigger_deface,
        "restore": trigger_restore,
        "duel": trigger_duel,
        "remediation": show_remediation,
        "demo": run_demo,
        "aide": show_help,
        "help": show_help,
        "quitter": lambda: sys.exit(0),
        "quit": lambda: sys.exit(0),
        "exit": lambda: sys.exit(0)
    }
    
    while True:
        try:
            cmd = input(f"{Color.PURPLE}[PHP2Shell]{Color.RESET} Enter command: ").strip().lower()
            
            if cmd in commands:
                commands[cmd]()
            else:
                print(f"{Color.RED}[-] Unknown command: {cmd}{Color.RESET}")
                print(f"{Color.YELLOW}[*] Type 'aide' for help{Color.RESET}")
        except KeyboardInterrupt:
            print(f"\n{Color.YELLOW}[*] Use 'quitter' to exit{Color.RESET}")
        except EOFError:
            print()
            sys.exit(0)
        except Exception as e:
            print(f"{Color.RED}[-] Error: {e}{Color.RESET}")


if __name__ == "__main__":
    main()
