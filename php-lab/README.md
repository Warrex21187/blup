# 🚨 Lab Démo Awareness — Sécurité & Rémédiation PHP

> [!TIP]
> **Fiche complète pour votre session technique :** 
> Retrouvez le guide complet d'analyse, l'explication du mécanisme d'ingénierie C et les étapes de démo dans [`PHP2SHELL_CVE-2026-109618.md`](PHP2SHELL_CVE-2026-109618.md).

> [!NOTE]
> Ce lab est configuré pour une **démonstration en direct** (sensibilisation des équipes et formation technique). 
> Il intègre la surveillance en direct du moteur PHP, la directive de mitigation `session.upload_progress.enabled = 0` et l'affichage des diagnostics d'infrastructure.

---

## 🚀 Lancement Rapide (Avant votre présentation)

Ouvrez un terminal dans le dossier `php-lab` :

```bash
docker compose up -d --build
```

> **⚠️ Important :** Le build peut prendre 5-10 minutes car Docker télécharge et installe PHP 8.4.26 et 8.4.27.

Ouvrez ensuite dans votre navigateur :
- 🌐 **Serveur vulnérable (PHP 8.4.26) :** [http://localhost:8888](http://localhost:8888)
- 🔒 **Serveur protégé (PHP 8.4.27) :** [http://localhost:8889](http://localhost:8889)

*(Placez le navigateur sur la moitié de votre écran et votre terminal d'attaquant sur l'autre moitié pour un effet saisissant !)*

---

## 🎯 CVE-2026-109618 (PHP2Shell) - Informations Clés

| Paramètre | Détail |
|---|---|
| **Identifiant CVE** | **CVE-2026-109618** (et CVE-2026-109619) |
| **Nom public** | **PHP2Shell** |
| **Score CVSS v4.0** | **9.2 / 10** (Critique) |
| **Composant affecté** | Cœur du moteur PHP (Zend Engine — gestion mémoire OOM) |
| **Impact** | Exécution de code à distance (RCE) **non authentifiée** |
| **Versions vulnérables** | PHP 5.x à 8.1 (EOL), 8.2 < 8.2.35, 8.3 < 8.3.36, 8.4 < 8.4.27 |
| **Date de correctif** | 21 octobre 2026 (PHP Security Team) |

---

## 💻 Commandes de l'Attaquant (À taper pendant votre démo)

Vous n'avez pas de script rigide à suivre : vous tapez la commande voulue au moment où vous l'expliquez à l'audience. **Le site web réagit instantanément à l'écran sans même rafraîchir la page !**

### 1️⃣ Frapper avec un Rançongiciel (Le plus visuel !)
```bash
python attack.py --ransomware
```

👉 **Effet en direct :**
- Le terminal affiche le déploiement du crypto-locker.
- Le portail intranet vire **au rouge sang avec sirène clignotante**, alerte d'extorsion et **compte à rebours animé de 48 heures** pour payer 50 000 €.

---

### 2️⃣ Voler les données RH confidentielles
```bash
python attack.py --steal
```

👉 **Effet en direct :**
- Le terminal affiche un tableau clair avec les **noms, salaires, IBAN et mots de passe** des directeurs et employés.
- Un fichier CSV `DONNEES_RH_EXFILTREES.csv` est créé immédiatement.
- Une bannière d'alerte jaune d'exfiltration apparaît sur le site.

---

### 3️⃣ Défaçage « Hacker » du site
```bash
python attack.py --deface
```

👉 **Effet en direct :**
- Le site se transforme en page noire et verte fluo "HACKED BY PHP2SHELL".

---

### 4️⃣ Déclencher la faille OOM (Mécanisme technique)
```bash
python attack.py --oom
```

👉 **Effet en direct :**
- Envoie une requête multipart massive (>16Mo) pour déclencher l'Out-of-Memory
- Le terminal affiche les étapes du mécanisme d'exploitation (Use-After-Free)

---

### 5️⃣ Remettre le site à neuf (Nettoyage)
```bash
python attack.py --restore
```

👉 **Effet en direct :**
- Le site redevient immédiatement normal et propre.

---

### 6️⃣ La Démonstration de la Solution (Serveur à jour)
```bash
python attack.py --compare
```
*(Ou en ciblant le port 8889 : `python attack.py --target http://localhost:8889 --ransomware`)*

👉 **Le message clé :**
- L'attaque passe sur le serveur obsolète (Port 8888).
- L'attaque **est rejetée net (Code 403)** sur le serveur où la mise à jour PHP a été faite (Port 8889).
- **Morale :** Les mises à jour ne sont pas du confort technique, elles sauvent l'entreprise d'un arrêt complet.

---

## 🔍 Explications Techniques

### Mécanisme de la faille CVE-2026-109618 :

```
[Requête Multipart volumineuse > 16Mo]
               │
               ▼
[Allocation mémoire PHP] ━━━ (Épuisement / Out-of-Memory) ━━━━┐
                                                            ▼
                                                [Appel à longjmp()]
                                                            │
    ┌───────────────────────────────────────────────────────────────┐
    ▼
(Saut d'interruption brutal)
    │
    ├─✗ Le code saute l'étape de libération/nettoyage des structures en cours
    │
    ▼
[Pointeurs orphelins en mémoire globale / session.upload_progress]
    │
    ▼
[Use-After-Free (UAF) lors du recyclage du worker pour la requête suivante]
```

### Le problème en 3 points :
1. **Le mécanisme d'abandon (`longjmp`)** : Quand PHP rencontre une erreur d'allocation mémoire (`out-of-memory`), il utilise un saut direct (`longjmp`) pour stopper la requête en cours et libérer les ressources.
2. **Le point aveugle** : Pendant le traitement des fichiers avec suivi de progression (`session.upload_progress`), l'état interne est marqué comme actif *avant* que toutes les allocations ne soient garanties. En cas de saut `longjmp`, l'état n'est pas nettoyé correctement.
3. **La réutilisation de mémoire (Use-After-Free)** : Les processus serveurs (Apache workers) traitent plusieurs requêtes successives. Le worker conserve donc des pointeurs vers une mémoire désynchronisée ou réallouée, ouvrant la voie à une corruption mémoire critique.

---

## 🛡️ Mesures de Rémédiation

### 1. Mise à jour immédiate du runtime PHP
Appliquer la mise à jour officielle vers les versions supportées :
- **PHP 8.2** → version **8.2.35+**
- **PHP 8.3** → version **8.3.36+**
- **PHP 8.4** → version **8.4.27+**

### 2. Mitigation d'urgence (sans mise à jour)
Si la mise à niveau nécessite des tests préalables, appliquez immédiatement dans `php.ini` :

```ini
; Désactivation du suivi d'upload de session (aucun impact sur les uploads normaux)
session.upload_progress.enabled = 0
```

Vérifiez ensuite :
```bash
php -i | grep "session.upload_progress.enabled"
# Résultat attendu : session.upload_progress.enabled => Off
```

### 3. Redémarrage des workers
Après toute modification, redémarrez Apache ou PHP-FPM :
```bash
# Apache
systemctl restart apache2

# PHP-FPM
systemctl restart php8.4-fpm
```

---

## 📚 Messages Clés à Retenir

1. **Un code sans faille ne suffit pas** : L'interpréteur sous-jacent fait partie intégrante de votre surface d'attaque.
2. **Durcissement par défaut** : Désactiver systématiquement les fonctionnalités d'usine non indispensables (`session.upload_progress.enabled = 0`, `expose_php = Off`).
3. **Cycle de vie logiciel** : Surveiller les bulletins d'alerte officiels (CISA KEV, CERT-FR) et planifier les mises à jour régulières des runtimes.

---

## 🎬 Arrêt du Lab après la session

```bash
docker compose down
```

---

## 📖 Documentation Complète

- **Fiche technique détaillée** : [PHP2SHELL_CVE-2026-109618.md](PHP2SHELL_CVE-2026-109618.md)
- **Chronologie réelle** : La faille a été découverte en août 2026, des attaques ont été observées avant même la sortie du correctif le 21 octobre 2026.
- **Catalogue KEV** : CVE-2026-109618 a été ajouté au catalogue CISA KEV (Known Exploited Vulnerabilities) le 26 octobre 2026.

---

## 🔧 Configuration Technique

### Architecture du Lab :
- **Serveur vulnérable** (Port 8888) : PHP 8.4.26 + Apache mod_php + `session.upload_progress.enabled = 1`
- **Serveur protégé** (Port 8889) : PHP 8.4.27 + Apache mod_php + `session.upload_progress.enabled = 0`
- **Memory Limit** : 16Mo (pour faciliter le déclenchement de l'OOM en démo)

### Prérequis :
- Docker et Docker Compose installés
- Ports 8888 et 8889 disponibles
- Python 3.7+ pour les scripts d'attaque

### Installation des dépendances Python :
```bash
pip install -r requirements.txt
```
