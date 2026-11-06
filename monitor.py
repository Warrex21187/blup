#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
📊 PHP2Shell Lab - Monitor en temps réel
Affiche les logs Apache et l'état des serveurs pendant les attaques
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
    """Efface l'écran du terminal."""
    if sys.platform == "win32":
        subprocess.run(["cls"], shell=True)
    else:
        subprocess.run(["clear"], shell=True)


def display_header():
    """Affiche l'en-tête du monitor."""
    clear_screen()
    print(f"""{Color.BLUE}
┌─────────────────────────────────────────────────────────────────────────────────────┐
│  {Color.BOLD}📊 PHP2Shell Lab - Monitor en temps réel{Color.RESET}{Color.BLUE}                                      │
│  CVE-2026-109618 (PHP2Shell) - Use-After-Free via OOM                              │
└─────────────────────────────────────────────────────────────────────────────────────┘{Color.RESET}
""")


def monitor_log_file(log_path, label, color):
    """Surveille un fichier de log et affiche les nouvelles lignes."""
    if not Path(log_path).exists():
        return
    
    # Lire les dernières lignes
    with open(log_path, 'r') as f:
        lines = f.readlines()
    
    if lines:
        print(f"\n{color}[{label}]{Color.RESET} Dernières entrées :")
        for line in lines[-10:]:  # Afficher les 10 dernières lignes
            line = line.strip()
            if line:
                # Coloriser les erreurs
                if "error" in line.lower() or "fatal" in line.lower():
                    print(f"  {Color.RED}{line}{Color.RESET}")
                elif "warning" in line.lower():
                    print(f"  {Color.YELLOW}{line}{Color.RESET}")
                else:
                    print(f"  {line}")


def monitor_logs():
    """Boucle principale de monitoring."""
    log_files = [
        ("vulnerable/logs/php2shell-error.log", "VULNÉRABLE (8888)", Color.RED),
        ("vulnerable/logs/php2shell-access.log", "VULNÉRABLE (8888)", Color.RED),
        ("patched/logs/php2shell-error.log", "PROTÉGÉ (8889)", Color.GREEN),
        ("patched/logs/php2shell-access.log", "PROTÉGÉ (8889)", Color.GREEN),
    ]
    
    last_sizes = {}
    
    while True:
        display_header()
        
        # Afficher l'état des serveurs
        print(f"\n{Color.BOLD}=== État des Serveurs ==={Color.RESET}")
        print(f"  {Color.RED}• Serveur vulnérable (8888) : PHP 8.4.26 - session.upload_progress.enabled = 1{Color.RESET}")
        print(f"  {Color.GREEN}• Serveur protégé (8889) : PHP 8.4.27 - session.upload_progress.enabled = 0{Color.RESET}")
        
        # Afficher les logs
        print(f"\n{Color.BOLD}=== Logs Apache (Dernières activités) ==={Color.RESET}")
        for log_path, label, color in log_files:
            monitor_log_file(log_path, label, color)
        
        # Conseils
        print(f"\n{Color.YELLOW}💡 Conseils :{Color.RESET}")
        print(f"  • Lancez une attaque avec : {Color.CYAN}python attack.py --oom{Color.RESET}")
        print(f"  • Comparez les logs entre les deux serveurs")
        print(f"  • Le serveur vulnérable affichera des erreurs OOM")
        print(f"  • Le serveur protégé bloquera les attaques")
        
        # Attendre avant de rafraîchir
        time.sleep(3)


def main():
    print(f"{Color.BOLD}\n🚀 Démarrage du monitor PHP2Shell Lab...{Color.RESET}")
    print(f"{Color.YELLOW}Appuyez sur Ctrl+C pour quitter{Color.RESET}\n")
    
    try:
        monitor_logs()
    except KeyboardInterrupt:
        print(f"\n{Color.RED}✗ Monitor arrêté{Color.RESET}")


if __name__ == "__main__":
    main()
