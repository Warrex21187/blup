#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PHP2Shell Lab - Monitor en temps reel
Affiche les logs Apache et l etat des serveurs pendant les attaques
"""

import sys
import time
import subprocess
import threading
from pathlib import Path

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


class Color:
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    PURPLE = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    BOLD = "\033[1m"
    RESET = "\033[0m"


def clear_screen():
    """Efface l ecran du terminal."""
    if sys.platform == "win32":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)


def display_header():
    """Affiche l en-tete du monitor."""
    clear_screen()
    header = f"""
+------------------------------------------------------------------------------------------------------+
|  {Color.BOLD}Monitor en temps reel - PHP2Shell Lab{Color.RESET}{Color.BLUE}                                              |
|  CVE-2026-109618 (PHP2Shell) - Use-After-Free via OOM                              {Color.RESET}|
+------------------------------------------------------------------------------------------------------+
"""
    print(header)


def monitor_logs():
    """Monitore les logs Apache en temps reel."""
    display_header()
    
    print(f"{Color.YELLOW}[*] Demarrage du monitoring...{Color.RESET}")
    print(f"{Color.YELLOW}[*] Appuyez sur Ctrl+C pour arreter{Color.RESET}\n")
    
    # Chemin des logs
    log_files = [
        './vulnerable/logs/php2shell-access.log',
        './vulnerable/logs/php2shell-error.log',
        './patched/logs/php2shell-access.log',
        './patched/logs/php2shell-error.log',
    ]
    
    # Verifier que les fichiers existent
    available_files = [f for f in log_files if Path(f).exists()]
    
    if not available_files:
        print(f"{Color.RED}[!] Aucun fichier de log trouve!{Color.RESET}")
        print(f"{Color.RED}[!] Assurez-vous que les conteneurs Docker sont en cours d execution{Color.RESET}")
        print(f"{Color.RED}[!] Les logs devraient etre dans : {', '.join(log_files)}{Color.RESET}")
        return
    
    print(f"{Color.GREEN}[+] Surveillance des fichiers:{Color.RESET}")
    for f in available_files:
        print(f"    - {f}")
    print()
    
    # Commande tail -f pour tous les fichiers
    if sys.platform == "win32":
        # Windows
        cmd = ['cmd', '/c', 'type'] + available_files
        print(f"{Color.YELLOW}[*] Executant : {' '.join(cmd)}{Color.RESET}")
        subprocess.run(cmd)
    else:
        # Linux/Mac
        cmd = ['tail', '-f'] + available_files
        print(f"{Color.YELLOW}[*] Executant : {' '.join(cmd)}{Color.RESET}")
        try:
            subprocess.run(cmd)
        except KeyboardInterrupt:
            print(f"\n{Color.YELLOW}[*] Monitoring arrete{Color.RESET}")


def display_server_status():
    """Affiche l etat des serveurs."""
    display_header()
    
    print(f"{Color.CYAN}[*] Etat des serveurs:{Color.RESET}\n")
    
    # Verifier les conteneurs Docker
    try:
        result = subprocess.run(
            ['docker', 'ps', '--filter', 'name=php2shell', '--format', 'table {{.Names}}\t{{.Status}}\t{{.Ports}}'],
            capture_output=True, text=True, timeout=5
        )
        print(f"{Color.GREEN}Conteneurs Docker:{Color.RESET}")
        print(result.stdout)
    except Exception as e:
        print(f"{Color.RED}[!] Erreur Docker : {e}{Color.RESET}")
    
    print()
    
    # Verifier les ports
    try:
        result = subprocess.run(
            ['netstat', '-tuln'] if sys.platform != "win32" else ['netstat', '-ano'],
            capture_output=True, text=True, timeout=5
        )
        lines = result.stdout.split('\n')
        for line in lines:
            if '8888' in line or '8889' in line:
                print(f"{Color.GREEN}Port : {line.strip()}{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED}[!] Erreur netstat : {e}{Color.RESET}")


def main():
    parser = import argparse
    parser = argparse.ArgumentParser(
        description='Monitor en temps reel pour PHP2Shell Lab',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f"""
Exemples:
  python monitor.py --logs
  python monitor.py --status
  python monitor.py
        """
    )
    
    parser.add_argument('--logs', '-l', action='store_true',
                        help='Monitore les logs Apache')
    parser.add_argument('--status', '-s', action='store_true',
                        help='Affiche l etat des serveurs')
    
    args = parser.parse_args()
    
    if args.status:
        display_server_status()
    elif args.logs:
        monitor_logs()
    else:
        # Mode par defaut : monitor les logs
        monitor_logs()


if __name__ == "__main__":
    main()
