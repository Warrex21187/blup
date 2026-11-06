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


BANNER = f"""{C.RED}
  ███████╗ ███████╗ ██████╗     ██╗  ██╗██████╗  ██████╗ ██████╗ ██╗     ███████╗███████╗
  ██╔════╝██╔════╝██╔═══██╗    ██║  ██║██╔══██╗██╔═══██╗██╔══██╗██║     ██╔════╝██╔════╝
  ███████╗█████╗  ██║   ██║    ███████║██████╔╝██║   ██║██████╔╝██║     █████╗  ███████╗
  ╚════██║██╔══╝  ██║   ██║    ██╔══██║██╔══██╗██║   ██║██╔══██╗██║     ██╔══╝  ╚════██║
  ███████║███████╗╚██████╔╝    ██║  ██║██║  ██║╚██████╔╝██║  ██║███████╗███████╗███████║
  ╚══════╝╚══════╝ ╚═════╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝╚══════╝
{C.RESET}{C.BOLD}   [+] CVE-2026-109618 & CVE-2026-109619 — RCE du moteur PHP (CVSS 9.2)
   [+] Deux serveurs : PHP 8.4.26 (:8888, vulnérable) vs 8.4.27 (:8889, corrigé)
   [+] Rôle : attaquant externe — sans compte, sans mot de passe{C.RESET}
"""

LARGEUR = 62


def sep(char="─"):
    print(f"{C.CYAN}{char * LARGEUR}{C.RESET}")


def etape(num, titre, description=""):
    print(f"\n{C.CYAN}{sep()}{C.RESET}")
    print(f"{C.BOLD}[Étape {num}]{C.RESET} {C.BLUE}{titre}{C.RESET}")
    if description:
        print(f"  {C.YELLOW}→ {description}{C.RESET}")
    print(f"{C.CYAN}{sep()}{C.RESET}")


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
    print(f"\n{C.BOLD}=== ÉTAT DES LIEUX ==={C.RESET}\n")
    for label, base in [("VULNÉRABLE (:8888)", cfg.vuln), ("CORRIGÉ (:8889)", cfg.patche)]:
        data, err = etat_serveur(base)
        if err:
            print(f"  {label:<22} {C.RED}✗ injoignable ({err}){C.RESET}")
            print(f"  {C.YELLOW}  → lance le lab : docker compose up -d --build{C.RESET}")
            continue
        verdict = (
            f"{C.RED}✗ MOTEUR NON CORRIGÉ{C.RESET}" if data.get("is_vulnerable")
            else f"{C.GREEN}✓ CORRECTIF ACTIF{C.RESET}"
        )
        print(f"  {label:<22} PHP {data.get('php_version','?'):<10} état: {data.get('state','?':<12} {verdict}")
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
    print(f"\n{C.BOLD}=== LA VRAIE HISTOIRE (tout est authentique) ==={C.RESET}\n")
    for date, txt in evenements:
        print(f"  {C.YELLOW}{date:<22}{C.RESET} {txt}")
        time.sleep(0.35)
    print(f"\n  {C.BOLD}Message clé :{C.RESET} entre la fuite et le correctif, il s'est passé {C.RED}moins de 24 h{C.RESET}.")
    print(f"  Une équipe qui met à jour « en fin de semaine » était déjà trop lente.\n")


# ──────────────── COMMANDE : expliquer ────────────────
def cmd_expliquer(cfg, _=None):
    print(f"""\n{C.BOLD}{'─' * LARGEUR}
  📖 EXPLICATION GRAND PUBLIC {C.RESET}
{'─' * LARGEUR}{C.RESET}

  Imaginez un chef de chantier avec un budget strict
  ({C.YELLOW}memory_limit{C.RESET} = plafond mémoire de PHP).

  Un client envoie un plan de maison GIGANTESQUE
  ({C.YELLOW}une requête multipart/form-data{C.RESET} — un gros formulaire).

  En plein montage, le budget explose : tout le monde doit sortir
  IMMÉDIATEMENT ({C.YELLOW}interruption brutale « bailout »{C.RESET}).

  Puis l'équipe de nettoyage range « comme d'habitude »...
  mais la maison était à moitié montée : elle jette des pièces
  encore utilisées et laisse des débris en place
  ({C.YELLOW}mémoire libérée mais données toujours « vivantes »{C.RESET}).

  Le client suivant hérite de la parcelle... et parfois, dans ses
  plans, on retrouve le carnet d'adresses du voisin :
  {C.RED}mots de passe, clés API, tokens{C.RESET} d'autres visiteurs.

{C.BOLD}{'─' * LARGEUR}
  🔧 VERSION TECHNIQUE {C.RESET}
{'─' * LARGEUR}{C.RESET}

  Deux use-after-free ({C.YELLOW}CWE-416{C.RESET}) dans le ZEND ENGINE — pas dans le code du site :

  {C.YELLOW}CVE-2026-109618{C.RESET} : pendant le setup de la requête (parsing multipart), si le plafond
    mémoire est dépassé, PHP saute au gestionnaire d'erreur via longjmp AVANT que
    les structures internes soient complètes. Le nettoyage traite des données à
    moitié construites comme valides → mémoire libérée puis réutilisée → RCE.
    Seul, ce bug fait aussi FUIR la mémoire du worker dans le cookie PHPSESSID
    (handler « session upload progress », actif par défaut, qui tourne AVANT
    session_start() et avant la première ligne du code applicatif).

  {C.YELLOW}CVE-2026-109619{C.RESET} : des états internes d'une requête survivent à la libération de
    la mémoire qui les porte. Le worker suivant réutilise l'état périmé
    avant que l'initialisation ne le réinitialise → use-after-free → RCE.

  Conditions d'attaque : une requête multipart (upload), {C.RED}aucune authentification{C.RESET},
  toutes les SAPI concernées (mod_php, FPM, php-cgi, FrankenPHP, LiteSpeed).
  {C.BOLD}mod_php est le plus exposé{C.RESET} : l'attaque réussit avant que le code applicatif tourne.

  Sévérité : CVSS v4.0 {C.RED}9.2 / 10{C.RESET} — exploité dans la nature depuis le 21/10/2026.
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
    print(f"\n{C.BOLD}=== DÉCLENCHEMENT RÉEL DE LA FUITE MÉMOIRE (CVE-2026-109618) ==={C.RESET}\n")
    
    for label, base in cible(cfg, arg or "vuln"):
        print(f"  {C.CYAN}→ Envoi d'une requête multipart massive ({cfg.parties} champs) vers {label}...{C.RESET}")
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
                print(f"  {C.GREEN}✓ Requête traitée en {elapsed:.2f}s{C.RESET}")
                print(f"  {C.YELLOW}  → Pic mémoire : {peak} octets{C.RESET}")
                if vuln:
                    print(f"  {C.RED}✗ SERVEUR VULNÉRABLE : Use-After-Free possible !{C.RESET}")
                else:
                    print(f"  {C.GREEN}✓ Serveur protégé : nettoyage mémoire correct{C.RESET}")
            else:
                print(f"  {C.YELLOW}? Réponse HTTP {r.status_code}{C.RESET}")
        except Exception as e:
            print(f"  {C.RED}✗ Erreur : {e}{C.RESET}")
    print()


# ──────────────── COMMANDE : recette ────────────────
def cmd_recette(cfg, _=None):
    print(f"""\n{C.BOLD}=== REPRODUCTION MANUELLE (pour montrer que TU pilotes) ==={C.RESET}

  1. Vérifier la version PHP du serveur vulnérable :
     {C.CYAN}curl -s http://localhost:8888/api.php?action=status | jq{C.RESET}

  2. Vérifier que session.upload_progress est ACTIF (vecteur de la faille) :
     {C.CYAN}curl -s http://localhost:8888/api.php?action=status | jq '.upload_progress_enabled'{C.RESET}

  3. Déclencher la faille OOM avec une requête multipart massive :
     {C.CYAN}curl -X POST http://localhost:8888/upload.php \\
       -H "Content-Type: multipart/form-data; boundary=----TEST" \\
       --data-binary @payload.txt{C.RESET}
     (où payload.txt est un fichier avec {cfg.parties} champs form-data)

  4. Vérifier que le serveur protégé bloque l'attaque :
     {C.CYAN}curl -X POST http://localhost:8889/api.php -d 'action=ransomware'{C.RESET}
     → Réponse : HTTP 403 (BLOCKED_BY_PATCH)

  5. Comparer les deux serveurs :
     {C.CYAN}python attack.py --compare{C.RESET}
""")


# ──────────────── COMMANDE : ransomware ────────────────
def cmd_ransomware(cfg, arg):
    for label, base in cible(cfg, arg or "vuln"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "ransomware"}, timeout=15)
            ok = r.status_code == 200
        except Exception:
            ok = False
        etat = f"{C.RED}compromis ✗{C.RESET}" if ok else f"{C.GREEN}protégé ✓{C.RESET}"
        print(f"  {label:<22} → {etat}")
    print(f"  {C.YELLOW}👉 Regarde le navigateur : le site vulnérable affiche la rançon !{C.RESET}\n")


# ──────────────── COMMANDE : vol ────────────────
def cmd_vol(cfg, arg):
    for label, base in cible(cfg, arg or "vuln"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "steal"}, timeout=15)
            if r.status_code == 200:
                data = r.json()
                vole = data.get("stolen_data", [])
                if vole:
                    print(f"\n  {C.RED}{C.BOLD}=== [DONNÉES CONFIDENTIELLES EXFILTRÉES] ==={C.RESET}")
                    print(f"  {C.CYAN}{'─' * 84}{C.RESET}")
                    print(f"  {C.BOLD}{'NOM & PRÉNOM':<18} | {'POSTE':<20} | {'SALAIRE':<9} | {'MOT DE PASSE':<16}{C.RESET}")
                    print(f"  {C.CYAN}{'─' * 84}{C.RESET}")
                    fichier_csv = "DONNEES_RH_EXFILTREES.csv"
                    with open(fichier_csv, mode="w", newline="", encoding="utf-8-sig") as f:
                        ecrivain = csv.writer(f, delimiter=";")
                        ecrivain.writerow(["Nom", "Poste", "Salaire Net", "Mot de passe", "N° Sécurité Sociale", "IBAN"])
                        for emp in vole:
                            ecrivain.writerow([emp["nom"], emp["poste"], emp["salaire"], emp["password"], emp["secu"], emp["iban"]])
                            print(f"  {C.WHITE}{emp['nom']:<18}{C.RESET} | {C.YELLOW}{emp['poste']:<20}{C.RESET} | {C.GREEN}{emp['salaire']:<9}{C.RESET} | {C.RED}{emp['password']:<16}{C.RESET}")
                    print(f"  {C.CYAN}{'─' * 84}{C.RESET}\n")
                    print(f"  {C.GREEN}[✓] Fichier créé : {C.BOLD}{fichier_csv}{C.RESET} (prêt pour la séance)")
                else:
                    print(f"  {C.GREEN}✓ Aucune donnée exfiltrée (serveur protégé){C.RESET}")
            elif r.status_code == 403:
                print(f"  {C.GREEN}✓ Attaque bloquée : {r.json().get('message', 'HTTP 403')}{C.RESET}")
            else:
                print(f"  {C.YELLOW}? Code HTTP : {r.status_code}{C.RESET}")
        except Exception as e:
            print(f"  {C.RED}✗ Erreur : {e}{C.RESET}")
    print(f"  {C.YELLOW}👉 Le portail affiche la bannière d'alerte « fuite de données en cours »{C.RESET}\n")


# ──────────────── COMMANDE : deface ────────────────
def cmd_deface(cfg, arg):
    for label, base in cible(cfg, arg or "vuln"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "deface"}, timeout=15)
            ok = r.status_code == 200
        except Exception:
            ok = False
        etat = f"{C.RED}défacé ✗{C.RESET}" if ok else f"{C.GREEN}protégé ✓{C.RESET}"
        print(f"  {label:<22} → {etat}")
    print(f"  {C.YELLOW}👉 Regarde le site : le logo et tout le contenu ont été écrasés !{C.RESET}\n")


# ──────────────── COMMANDE : restore ────────────────
def cmd_restore(cfg, arg):
    for label, base in cible(cfg, arg or "les-deux"):
        try:
            r = requests.post(f"{base}/api.php", data={"action": "restore"}, timeout=15)
            ok = r.status_code == 200
        except Exception:
            ok = False
        etat = f"{C.GREEN}restauré ✓{C.RESET}" if ok else f"{C.RED}échec{C.RESET}"
        print(f"  {label:<22} → {etat}")
    print(f"  {C.YELLOW}👉 Les portails redeviennent sains instantanément (recharge la page).{C.RESET}\n")


# ──────────────── COMMANDE : duel ────────────────
def cmd_duel(cfg):
    print(f"\n{C.BOLD}=== DUEL : UNE SEULE MISE À JOUR CHANGE TOUT ==={C.RESET}\n")
    cmd_status(cfg)
    time.sleep(1)

    print(f"\n{C.RED}1. Rançongiciel sur le serveur NON corrigé (PHP 8.4.26, :8888)…{C.RESET}")
    ok1 = envoyer_action(cfg, "ransomware", "vuln")
    if ok1:
        print(f"   {C.RED}✗ RÉSULTAT : VULNÉRABLE — Le portail affiche la rançon.{C.RESET}\n")
    time.sleep(1.5)

    print(f"\n{C.GREEN}2. La MÊME attaque sur le serveur corrigé (PHP 8.4.27, :8889)…{C.RESET}")
    ok2 = envoyer_action(cfg, "ransomware", "patche")

    print(f"\n{C.BOLD}{'─' * LARGEUR}")
    print(f"  RÉSUMÉ")
    print(f"{'─' * LARGEUR}{C.RESET}")
    print(f"  PHP 8.4.26 (:8888) : {C.RED}✗ compromis en une requête{C.RESET}")
    print(f"  PHP 8.4.27 (:8889) : {C.GREEN}✓ attaque rejetée net (HTTP 403){C.RESET}")
    print(f"\n{C.BOLD}Conclusion pour la direction et les équipes :{C.RESET}")
    print(f"{C.WHITE}Entre 8.4.26 et 8.4.27 il y a {C.BOLD}UN SEUL numéro de version{C.RESET} — celui du")
    print(f"correctif du 21/10/2026. La mise à jour neutralise 100 % de l'attaque,")
    print(f"sans changer une ligne du code applicatif, sans impact fonctionnel.\n")
    print(f"(Tape {C.CYAN}restore{C.RESET} pour remettre les portails à neuf.)\n")


# ──────────────── COMMANDE : remediation ────────────────
def cmd_remediation(cfg, _=None):
    print(f"""\n{C.BOLD}{'─' * LARGEUR}
  🚨 REMÉDIATION & BONNES PRATIQUES (issues des advisories réels)
{'─' * LARGEUR}{C.RESET}

  {C.GREEN}1. METTRE À JOUR PHP vers la branche corrigée{C.RESET}
     → 8.2.35 / 8.3.36 / 8.4.27 / 8.5.12 (selon la branche en place)
     → Toute installation qui sert du web est concernée, quelle que soit la SAPI
       (mod_php, PHP-FPM, php-cgi, FrankenPHP, LiteSpeed)

  {C.GREEN}2. REDÉMARRER LES WORKERS après la mise à jour{C.RESET}
     → {C.YELLOW}La mise à jour disque ne suffit PAS{C.RESET} : libphp.so / php-fpm restent résidents
     → systemctl restart apache2   |   systemctl restart php8.4-fpm
     → Vérifier le correctif : zgrep CVE-2026-109618 /usr/share/doc/php*-common/changelog*
       ou : rpm -q --changelog php-common | grep CVE-2026-109618

  {C.GREEN}3. GARDER « SESSION UPLOAD PROGRESS » DÉSACTIVÉ (même après le patch){C.RESET}
     → php.ini / pool FPM : {C.YELLOW}session.upload_progress.enabled = 0{C.RESET}
     → Recommandé par PHP le 23/10 (couvre aussi CVE-2026-115560)
     → Ne se règle PAS via ini_set() ni .user.ini : redémarrage requis

  {C.GREEN}4. BLOQUER MULTIPART/FORM-DATA INUTILE (mesure d'attente){C.RESET}
     → nginx :  if ($http_content_type ~* "multipart/form-data") {{ return 403; }}
     → Apache : RewriteCond %{HTTP:Content-Type} multipart/form-data [NC] → RewriteRule ^ - [F]
     → WAF : AWS « PHP2Shell_BODY », règle Azure bloquant le champ PHP_SESSION_UPLOAD_PROGRESS

  {C.GREEN}5. PHP 8.5 : fatal_error_backtraces = 0 + redémarrer les workers{C.RESET}

  {C.GREEN}6. CASSE-TÊTE PHP EOL (≤ 8.1) : aucun correctif officiel{C.RESET}
     → Paquets backportés : deb.sury.org / ppa:ondrej/php (5.6→8.1), Remi (RHEL),
       Ubuntu 22.04+ (8.1) — le numéro de version ne change pas, c'est le paquet qui est corrigé
     → Ou migrer vers une branche supportée (recommandé à terme)

  {C.GREEN}7. INVENTAIRE COMPLET{C.RESET}
     → ~22,6 M d'instances PHP exposées recensées : chercher PHP PARTOUT,
       y compris serveurs internes, outils oubliés, appliances

  {C.GREEN}8. TRACER LA MISE À JOUR (preuve datée){C.RESET}
     → apt : /var/log/apt/history.log   |   RHEL : dnf history
     → Les assureurs cyber (ex. Hiscox) demandent désormais des preuves datées

  {C.GREEN}9. Urgence objective{C.RESET}
     → Catalogue KEV de la CISA depuis le 26/10/2026 : délais de patch réglementaires
       pour les agences fédérales américaines — et référence pour vos audits
""")


# ──────────────── COMMANDE : demo ────────────────
def pause(txt=""):
    try:
        input(f"  {C.YELLOW}{txt}[Entrée pour continuer]{C.RESET}")
    except (KeyboardInterrupt, EOFError):
        raise SystemExit(0)


def cmd_demo(cfg):
    print(f"\n{C.BOLD}  DÉMO GUIDÉE — tu peux à tout moment taper tes propres commandes (Ctrl+C pour sortir).{C.RESET}\n")
    pause("Lance d'abord `status` toi-même si tu veux — ")

    etape(1, "État des lieux", "Deux serveurs identiques, un seul numéro de version les sépare.")
    print(f"  {C.BOLD}À dire :{C.RESET} « Voici deux serveurs jumeaux. Le premier exécute PHP 8.4.26, le second 8.4.27, publié le 21 octobre 2026 pour corriger CVE-2026-109618 et 109619. »")
    pause()
    cmd_status(cfg)

    etape(2, "L'histoire vraie", "Une fuite, 24 heures, des attaques avant même le correctif.")
    pause()
    cmd_histoire(cfg)

    etape(3, "Comprendre la faille", "Explication grand public, puis technique.")
    pause()
    cmd_expliquer(cfg)

    etape(4, "Déclencheur réel", "On envoie un formulaire piégé qui sature la mémoire du moteur.")
    print(f"  {C.BOLD}À dire :{C.RESET} « Aucun mot de passe, aucun compte. Juste un formulaire énorme. »")
    pause()
    cmd_fuite(cfg, "vuln")

    etape(5, "Comparaison avec le serveur corrigé", "La même requête piégée, côté patché.")
    pause()
    cmd_fuite(cfg, "patche")

    etape(6, "Impact 1 — Rançongiciel", "Le portail vulnérable tombe en direct.")
    print(f"  {C.BOLD}À dire :{C.RESET} « Ouvrez http://localhost:8888 dans le navigateur — regardez-le pendant l'attaque. »")
    pause()
    cmd_ransomware(cfg, None)

    etape(7, "Impact 2 — Fuite RH", "Salaires, mots de passe, IBAN en clair.")
    pause()
    cmd_vol(cfg, None)

    etape(8, "Le duel", "La même attaque, les deux serveurs, face caméra.")
    print(f"  {C.BOLD}À dire :{C.RESET} « Un seul numéro de version les sépare. Regardez. »")
    pause()
    cmd_duel(cfg)

    etape(9, "Nettoyage", "On rend le lab à son état initial.")
    pause()
    cmd_restore(cfg, "les-deux")

    etape(10, "Ce qu'il faut retenir", "La remédiation, avec les commandes réelles.")
    pause()
    cmd_remediation(cfg)

    print(f"\n{C.BOLD}{'─' * LARGEUR}")
    print(f"  ✅ FIN DE LA DÉMONSTRATION")
    print(f"{'─' * LARGEUR}{C.RESET}\n")


# ──────────────── Boucle interactive ────────────────
AIDE = f"""\n{C.BOLD}COMMANDES DISPONIBLES{C.RESET}
  {C.CYAN}status{C.RESET}                     état des deux serveurs (versions, verrou)
  {C.CYAN}histoire{C.RESET}                   la chronologie réelle de la faille (octobre 2026)
  {C.CYAN}expliquer{C.RESET}                   explication grand public + version technique
  {C.CYAN}fuite [cible]{C.RESET}               déclencheur RÉEL de la fuite mémoire (cible : vuln|patche|les-deux)
  {C.CYAN}recette{C.RESET}                    reproduction manuelle (curl) pour montrer que tu pilotes
  {C.CYAN}ransomware [cible]{C.RESET}          déploie le rançongiciel sur le portail
  {C.CYAN}vol [cible]{C.RESET}                exfiltre la base RH (salaires, mots de passe, IBAN)
  {C.CYAN}deface [cible]{C.RESET}             défacer le site web
  {C.CYAN}restore [cible]{C.RESET}            remet le(s) portail(s) à la normale
  {C.CYAN}duel{C.RESET}                       la même attaque sur vulnérable vs corrigé
  {C.CYAN}remediation{C.RESET}                le plan de correction réel (avec commandes)
  {C.CYAN}demo{C.RESET}                       déroulé guidé complet (parfait pour animer)
  {C.CYAN}aide{C.RESET}                       cette aide
  {C.CYAN}quitter{C.RESET}                    sortie
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
        print(f"{C.YELLOW}⚠ Serveur vulnérable injoignable : lance d'abord  docker compose up -d --build{C.RESET}\n")
    else:
        badge = "NON CORRIGÉ" if data.get("is_vulnerable") else "CORRIGÉ"
        print(f"{C.GREEN}✓ Serveur vulnérable (:8888) — PHP {data.get('php_version')} [{badge}]{C.RESET}")
    data, err = etat_serveur(cfg.patche)
    if err:
        print(f"{C.YELLOW}⚠ Serveur corrigé injoignable (:8889){C.RESET}\n")
    else:
        badge = "NON CORRIGÉ" if data.get("is_vulnerable") else "CORRIGÉ"
        print(f"{C.GREEN}✓ Serveur corrigé (:8889) — PHP {data.get('php_version')} [{badge}]{C.RESET}")
    print(AIDE)

    # Commande passée en argument (ex : python demo.py demo)
    if args.commande:
        nom = args.commande[0].lower()
        if nom in COMMANDES:
            COMMANDES[nom](cfg, " ".join(args.commande[1:]) or None)

    # Boucle interactive : c'est TOI qui pilotes
    while True:
        try:
            brut = input(f"  {C.RED}php2shell{C.RESET} ▶ ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {C.YELLOW}Fin de session — pense à `restore` puis `docker compose down`.{C.RESET}")
            break
        if not brut:
            continue
        if brut.lower() in ("quitter", "quit", "exit", "q"):
            print(f"  {C.YELLOW}Fin de session — pense à `restore` puis `docker compose down`.{C.RESET}")
            break
        morceaux = brut.split()
        nom = morceaux[0].lower()
        arg = " ".join(morceaux[1:]) or None
        fonction = COMMANDES.get(nom)
        if fonction is None:
            print(f"  {C.RED}Commande inconnue : {nom} — tape `aide`{C.RESET}")
            continue
        try:
            fonction(cfg, arg)
        except SystemExit:
            raise
        except Exception as e:
            print(f"  {C.RED}Erreur : {e}{C.RESET}")


if __name__ == "__main__":
    main()
