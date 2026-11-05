#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔══════════════════════════════════════════════════════════════════════╗
║               CONSOLE D'ATTAQUE — DÉMONSTRATION SÉCURITÉ             ║
║               Simulation d'exploitation de la faille PHP             ║
║                    (CVE-2024-4577 / Sensibilisation)                 ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import sys
import time
import argparse
import csv

# Support UTF-8 sous Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import requests

# ─── Couleurs du Terminal ──────────────────────────────────────────
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
  ██████╗  ██████╗ ███████╗    ██╗  ██╗ █████╗  ██████╗██╗  ██╗
 ██╔════╝ ██╔════╝ ██╔════╝    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝
 ██║  ███╗██║  ███╗███████╗    ███████║███████║██║     █████╔╝ 
 ██║   ██║██║   ██║╚════██║    ██╔══██║██╔══██║██║     ██╔═██╗ 
 ╚██████╔╝╚██████╔╝███████║    ██║  ██║██║  ██║╚██████╗██║  ██╗
  ╚═════╝  ╚═════╝ ╚══════╝    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝
{Color.RESET}{Color.BOLD}   [+] CONSOLE D'EXPLOITATION — SIMULATION CYBERATTAQUE
   [+] Rôle : Attaquant externe (Sans identifiants / Sans accès préalable){Color.RESET}
""")


def simulate_exploit_steps(target_url):
    """Affiche les logs d'attaque réalistes avec un léger délai pour le suspense."""
    print(f"{Color.CYAN}[*] Cible verrouillée :{Color.RESET} {Color.WHITE}{target_url}{Color.RESET}")
    time.sleep(0.4)
    print(f"{Color.CYAN}[*] Reconnaissance :{Color.RESET} Analyse du serveur distant...")
    time.sleep(0.5)
    print(f"{Color.YELLOW}[!] Faille détectée :{Color.RESET} PHP-CGI vulnérable aux injections d'arguments (CVE-2024-4577)")
    time.sleep(0.4)
    print(f"{Color.CYAN}[*] Envoi du payload malveillant (Bypass Unicode %AD -> '-')...{Color.RESET}")
    time.sleep(0.6)


def attack_ransomware(target_url):
    """Déploie le rançongiciel."""
    print_banner()
    simulate_exploit_steps(target_url)

    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "ransomware"}, timeout=5)
        
        if r.status_code == 200:
            print(f"{Color.GREEN}[✓] Code malveillant injecté avec succès dans le serveur !{Color.RESET}")
            time.sleep(0.3)
            print(f"{Color.RED}{Color.BOLD}")
            print("  ╔══════════════════════════════════════════════════════════════════╗")
            print("  ║  🚨 ATTENTION : RANÇONGICIEL ACTIVÉ AVEC SUCCÈS !                ║")
            print("  ║                                                                  ║")
            print("  ║  • 842 fichiers d'entreprise chiffrés (Compta, RH, Contrats)     ║")
            print("  ║  • Le site officiel affiche la demande de rançon (50 000 €)      ║")
            print("  ║  • Compte à rebours de destruction des données enclenché         ║")
            print("  ╚══════════════════════════════════════════════════════════════════╝")
            print(f"{Color.RESET}")
            print(f"{Color.YELLOW}👉 Regardez l'écran du navigateur : le site est tombé instantanément !{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[✗] ÉCHEC DE L'ATTAQUE (HTTP 403) : Le serveur a rejeté la requête !{Color.RESET}")
            print(f"{Color.GREEN}[✓] Ce serveur possède le correctif de sécurité (PHP >= 8.3.8).{Color.RESET}\n")
        else:
            print(f"{Color.RED}[✗] Erreur de communication : HTTP {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[✗] Impossible de joindre la cible : {e}{Color.RESET}\n")


def attack_steal(target_url):
    """Exfiltre la base de données RH."""
    print_banner()
    simulate_exploit_steps(target_url)

    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "steal"}, timeout=5)
        
        if r.status_code == 200:
            data = r.json()
            stolen = data.get("stolen_data", [])
            print(f"{Color.GREEN}[✓] RCE confirmée ! Extraction directe de la base de données...{Color.RESET}\n")
            time.sleep(0.4)

            print(f"{Color.RED}{Color.BOLD}=== [DONNÉES CONFIDENTIELLES EXFILTRÉES EN CLAIR] ==={Color.RESET}")
            print(f"{Color.CYAN}{'─' * 80}{Color.RESET}")
            print(f"{Color.BOLD}{'NOM & PRÉNOM':<18} | {'POSTE':<20} | {'SALAIRE':<10} | {'MOT DE PASSE':<16} | {'N° SÉCU'}{Color.RESET}")
            print(f"{Color.CYAN}{'─' * 80}{Color.RESET}")

            csv_file = "DONNEES_RH_EXFILTREES.csv"
            with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f, delimiter=";")
                writer.writerow(["Nom", "Poste", "Salaire Net", "Mot de passe", "N° Securite Sociale", "IBAN"])
                for emp in stolen:
                    writer.writerow([emp['nom'], emp['poste'], emp['salaire'], emp['password'], emp['secu'], emp['iban']])
                    print(f"{Color.WHITE}{emp['nom']:<18}{Color.RESET} | {Color.YELLOW}{emp['poste']:<20}{Color.RESET} | {Color.GREEN}{emp['salaire']:<10}{Color.RESET} | {Color.RED}{emp['password']:<16}{Color.RESET} | {Color.WHITE}{emp['secu']}{Color.RESET}")

            print(f"{Color.CYAN}{'─' * 80}{Color.RESET}\n")
            print(f"{Color.GREEN}[✓] Fichier de fuite créé : {Color.BOLD}{csv_file}{Color.RESET}")
            print(f"{Color.YELLOW}👉 En 2 secondes, l'attaquant détient tous les salaires et mots de passe !{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[✗] ÉCHEC : Requête bloquée par le patch de sécurité !{Color.RESET}\n")
        else:
            print(f"{Color.RED}[✗] Erreur HTTP {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[✗] Erreur : {e}{Color.RESET}\n")


def attack_deface(target_url):
    """Défacement visuel du site web."""
    print_banner()
    simulate_exploit_steps(target_url)

    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "deface"}, timeout=5)
        if r.status_code == 200:
            print(f"{Color.GREEN}[✓] Contrôle complet du serveur obtenu !{Color.RESET}")
            print(f"{Color.RED}[!] Page d'accueil remplacée par la signature du pirate (Défacement).{Color.RESET}")
            print(f"{Color.YELLOW}👉 Regardez le site : le logo et tout le contenu ont été écrasés !{Color.RESET}\n")
        elif r.status_code == 403:
            print(f"{Color.RED}[✗] ÉCHEC : Le serveur est patché, le piratage est bloqué.{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[✗] Erreur : {e}{Color.RESET}\n")


def restore_system(target_url):
    """Restaure le portail dans son état initial."""
    print(f"\n{Color.CYAN}[*] Nettoyage et restauration du serveur...{Color.RESET}")
    try:
        r = requests.post(f"{target_url}/api.php", data={"action": "restore"}, timeout=5)
        if r.status_code == 200:
            print(f"{Color.GREEN}[✓] SUCCÈS : Le site Acme Corp est restauré dans son état normal.{Color.RESET}")
            print(f"{Color.YELLOW}👉 La page web redevient saine instantanément.{Color.RESET}\n")
        else:
            print(f"{Color.RED}[✗] Erreur HTTP {r.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"{Color.RED}[✗] Erreur : {e}{Color.RESET}\n")


def compare_both(vuln_url="http://localhost:8888", patched_url="http://localhost:8889"):
    """Démontre l'efficacité du correctif entre les deux serveurs."""
    print_banner()
    print(f"{Color.BOLD}=== DÉMONSTRATION COMPARATIVE : AVANT / APRÈS MISE À JOUR ==={Color.RESET}\n")

    print(f"{Color.YELLOW}1. Attaque sur le serveur NON MIS À JOUR ({vuln_url})...{Color.RESET}")
    try:
        r1 = requests.post(f"{vuln_url}/api.php", data={"action": "ransomware"}, timeout=3)
        if r1.status_code == 200:
            print(f"   {Color.RED}✗ RÉSULTAT : VULNÉRABLE — Le rançongiciel a pris le contrôle.{Color.RESET}\n")
        else:
            print(f"   {Color.YELLOW}? Code HTTP : {r1.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"   {Color.RED}Erreur : {e}{Color.RESET}\n")

    time.sleep(1)

    print(f"{Color.GREEN}2. Même attaque sur le serveur AVEC CORRECTIF ({patched_url})...{Color.RESET}")
    try:
        r2 = requests.post(f"{patched_url}/api.php", data={"action": "ransomware"}, timeout=3)
        if r2.status_code == 403:
            print(f"   {Color.GREEN}✓ RÉSULTAT : PROTÉGÉ — L'attaque est rejetée net par le patch (HTTP 403).{Color.RESET}\n")
        else:
            print(f"   {Color.YELLOW}? Code HTTP : {r2.status_code}{Color.RESET}\n")
    except Exception as e:
        print(f"   {Color.RED}Erreur : {e}{Color.RESET}\n")

    print(f"{Color.BOLD}Conclusion pour la direction & les équipes :{Color.RESET}")
    print(f"{Color.WHITE}Une simple mise à jour logicielle neutralise 100% de l'attaque sans impacter le service.{Color.RESET}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Console d'attaque pour démo de sensibilisation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
EXEMPLES POUR VOTRE PRÉSENTATION :
  python attack.py --ransomware              Déploie le rançongiciel (écran rouge + compte à rebours)
  python attack.py --steal                   Vole et affiche les fiches de paie / mots de passe
  python attack.py --deface                  Déface le site web (style hacker néon)
  python attack.py --restore                 Remet le site à neuf (état normal)
  python attack.py --compare                 Compare en direct le serveur vulnérable vs patché
  python attack.py --target http://localhost:8889 --ransomware   Teste l'attaque sur le serveur protégé
        """
    )

    parser.add_argument("--target", default="http://localhost:8888",
                        help="URL de la cible (défaut: http://localhost:8888)")
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--ransomware", action="store_true", help="Lancer l'attaque Rançongiciel")
    group.add_argument("--steal", action="store_true", help="Exfiltrer les données RH et salaires")
    group.add_argument("--deface", action="store_true", help="Défacer le site web")
    group.add_argument("--restore", action="store_true", help="Restaurer le site à la normale")
    group.add_argument("--compare", action="store_true", help="Comparer serveur vulnérable vs patché")

    args = parser.parse_args()

    if args.ransomware:
        attack_ransomware(args.target)
    elif args.steal:
        attack_steal(args.target)
    elif args.deface:
        attack_deface(args.target)
    elif args.restore:
        restore_system(args.target)
    elif args.compare:
        compare_both(args.target, "http://localhost:8889")


if __name__ == "__main__":
    main()

