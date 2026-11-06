# 🚨 Lab Démo Realiste - CVE-2026-109618 (PHP2Shell)

> **Démonstration ultra-réaliste de l'exploitation de la faille CVE-2026-109618**
> Use-After-Free via Out-of-Memory dans Zend Engine (session.upload_progress)

---

## 🎯 Objectif

Ce lab **100% réaliste** démontre comment exploiter la faille **CVE-2026-109618** (PHP2Shell) avec :
- ✅ **Vraies requêtes multipart massives** pour déclencher l'OOM
- ✅ **Logs Apache/PHP en temps réel** montrant l'exploitation
- ✅ **Preuves d'exploitation** (fichiers créés, commandes exécutées)
- ✅ **Comparaison avant/après correctif**
- ✅ **Monitoring des workers PHP**

---

## 📊 Informations CVE-2026-109618

| Paramètre | Détail |
|---|---|
| **Identifiant** | CVE-2026-109618 (et CVE-2026-109619) |
| **Nom** | PHP2Shell |
| **CVSS v4.0** | **9.2/10** (Critique) |
| **Type** | Use-After-Free (CWE-416) |
| **Composant** | Zend Engine - Gestion mémoire OOM |
| **Impact** | **RCE non authentifié** |
| **Vecteur** | Requête multipart/form-data > memory_limit |
| **Versions vulnérables** | PHP 5.x-8.1 (EOL), 8.2 < 8.2.35, 8.3 < 8.3.36, **8.4 < 8.4.27** |
| **Correctif** | 21 octobre 2026 |

---

## 🚀 Installation & Lancement

### Prérequis
- Docker et Docker Compose
- Python 3.7+
- Ports 8888, 8889 disponibles

### Lancement du Lab

```bash
cd php-lab

# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Construire et démarrer les containers (5-10 min)
docker compose up -d --build

# 3. Vérifier que tout est prêt
docker compose ps
```

### Accès aux serveurs
- **🔴 Serveur vulnérable** : [http://localhost:8888](http://localhost:8888) (PHP 8.4.26)
- **🟢 Serveur protégé** : [http://localhost:8889](http://localhost:8889) (PHP 8.4.27)
- **📊 Logs Apache** : `vulnerable/logs/` et `patched/logs/`

---

## 🎬 Scénarios de Démo (Du plus simple au plus technique)

---

## 🎯 Niveau 1 : Démo Visuelle (Pour les non-techniques)

### 1️⃣ Déclencher un rançongiciel
```bash
python attack.py --ransomware
```
**Effet** : Le site vulnérable affiche une page de rançon avec compte à rebours

### 2️⃣ Voler les données RH
```bash
python attack.py --steal
```
**Effet** : Affiche les salaires, mots de passe, IBAN des employés + crée un CSV

### 3️⃣ Déface le site
```bash
python attack.py --deface
```
**Effet** : Le site affiche "HACKED BY PHP2Shell"

### 4️⃣ Restaurer
```bash
python attack.py --restore
```

---

## 🎯 Niveau 2 : Démo Technique (Pour les développeurs)

### 1️⃣ Déclencher la faille OOM (Mécanisme réel)
```bash
python attack.py --oom
```
**Ce que ça fait** :
- Envoie une requête multipart de **25 Mo** (> memory_limit = 16M)
- Déclenche l'Out-of-Memory dans Zend Engine
- Le `longjmp()` saute le nettoyage des structures
- Crée des **pointeurs orphelins** dans `session.upload_progress`

### 2️⃣ Exécuter une commande (Simulation RCE)
```bash
python exploit.py --rce --command "id"
```
**Effet** : Simule l'exécution de commande via l'exploitation

### 3️⃣ Créer une preuve d'exploitation
```bash
python exploit.py --proof
```
**Effet** : Crée un fichier `proof.php` sur le serveur

### 4️⃣ Vérifier les preuves
```bash
python verify_exploit.py --target http://localhost:8888
```
**Effet** : Liste tous les fichiers de preuve créés

---

## 🎯 Niveau 3 : Démo Expert (Pour les pentesters)

### 1️⃣ Exploitation complète avec logs
```bash
# Dans un terminal : Lancer le monitor
python monitor.py

# Dans un autre terminal : Lancer l'exploitation
python exploit.py --demo
```
**Ce que vous verrez** :
- Les logs Apache montrant les requêtes massives
- Les erreurs OOM dans les logs PHP
- La différence entre les deux serveurs

### 2️⃣ Analyser les logs
```bash
# Voir les logs du serveur vulnérable
tail -f vulnerable/logs/php2shell-error.log

# Voir les logs du serveur protégé
tail -f patched/logs/php2shell-error.log
```

### 3️⃣ Comparaison côté à côté
```bash
python verify_exploit.py --compare
```
**Effet** : Compare les preuves entre les deux serveurs

---

## 🎯 Niveau 4 : Console Interactive (Pour l'animation)

```bash
python demo.py
```

**Commandes disponibles** :
```
status          Affiche l'état des deux serveurs
histoire        Chronologie réelle de la faille
expliquer        Explication technique détaillée
fuite           Déclenche la faille OOM (25Mo de données)
recette         Commandes curl pour montrer que vous pilotez
ransomware      Déploie le rançongiciel
vol             Exfiltre les données RH
deface          Déface le site
restore         Restaure les sites
duel            Compare les deux serveurs face à une attaque
remediation     Affiche les mesures de correction
demo            Démo guidée complète
aide            Affiche l'aide
quitter         Quitte la console
```

**Exemple d'animation** :
```
php2shell ▶ status
php2shell ▶ histoire
php2shell ▶ expliquer
php2shell ▶ fuite vuln
php2shell ▶ ransomware
php2shell ▶ vol
php2shell ▶ duel
php2shell ▶ restore les-deux
```

---

## 🔍 Mécanisme Technique Expliqué

### L'arbre des causes (CVE-2026-109618)

```
[Requête Multipart > 16Mo]
       │
       ▼
[Allocation mémoire PHP]
       │
       ▼
[Dépassement memory_limit]
       │
       ▼
[Appel à longjmp()]
       │
       ├─✗ Nettoyage incomplet des structures
       │
       ▼
[Pointeurs orphelins dans session.upload_progress]
       │
       ▼
[Use-After-Free sur la requête suivante]
       │
       ▼
[Exécution de code arbitraire (RCE)]
```

### Le problème en 3 points

1. **`longjmp()` brutal** : Quand PHP rencontre une erreur OOM, il utilise `longjmp()` pour arrêter la requête. Ce saut **court-circuite** le nettoyage normal.

2. **Point aveugle** : Pendant le traitement de `session.upload_progress`, l'état est marqué comme actif **avant** que toutes les allocations soient garanties. En cas de `longjmp()`, l'état **n'est pas nettoyé**.

3. **Use-After-Free** : Le worker Apache/PHP-FPM traite plusieurs requêtes. Il conserve des **pointeurs vers une mémoire désynchronisée**, permettant une **corruption mémoire critique**.

---

## 🛡️ Mesures de Rémédiation

### 1️⃣ **Mise à jour immédiate** (Recommandé)
```bash
# Versions corrigées
PHP 8.2 → 8.2.35+
PHP 8.3 → 8.3.36+
PHP 8.4 → 8.4.27+
```

### 2️⃣ **Mitigation d'urgence** (Si mise à jour impossible)
```ini
# Dans php.ini
session.upload_progress.enabled = 0
```

**Vérification** :
```bash
php -i | grep session.upload_progress.enabled
# Résultat attendu : session.upload_progress.enabled => Off
```

### 3️⃣ **Redémarrage des workers**
```bash
# Apache
systemctl restart apache2

# PHP-FPM
systemctl restart php8.4-fpm
```

### 4️⃣ **Bloquer les requêtes multipart** (Mesure supplémentaire)
```apache
# Apache
RewriteCond %{HTTP:Content-Type} multipart/form-data [NC]
RewriteRule ^ - [F]
```

---

## 📁 Structure du Projet

```
php-lab/
├── docker-compose.yml          # Orchestration Docker
├── README.md                   # Ce fichier
├── requirements.txt            # Dépendances Python
├── attack.py                   # Script d'attaque (6 commandes)
├── exploit.py                  # Exploit technique (OOM, RCE, preuves)
├── verify_exploit.py           # Vérification des preuves
├── monitor.py                  # Monitor des logs en temps réel
├── demo.py                     # Console interactive
│
├── vulnerable/                 # Serveur VULNÉRABLE
│   ├── Dockerfile              # PHP 8.4.26 + session.upload_progress=1
│   ├── scripts/
│   │   └── start-apache.sh     # Script de démarrage avec logs
│   └── www/
│       ├── api.php             # API de contrôle
│       ├── index.php           # Portail web
│       ├── upload.php          # Déclencheur OOM
│       └── status.json         # État initial
│
└── patched/                    # Serveur PROTÉGÉ
    ├── Dockerfile              # PHP 8.4.27 + session.upload_progress=0
    ├── scripts/
    │   └── start-apache.sh     # Script de démarrage
    └── www/
        ├── api.php             # API avec blocage
        ├── index.php           # Portail protégé
        ├── upload.php          # Gestion sécurisée
        └── status.json         # État initial
```

---

## 🎯 Preuves d'Exploitation

Après une attaque réussie, vous pouvez vérifier les preuves :

### Sur le serveur vulnérable (8888)
- `proof.php` - Preuve générique
- `proof_ransomware.php` - Preuve de rançongiciel
- `proof_deface.php` - Preuve de défaçage
- `proof_steal.php` - Preuve de fuite de données
- `DONNEES_RH_EXFILTREES.csv` - Données exfiltrées

### Vérification
```bash
# Lister les preuves
python verify_exploit.py

# Accéder à une preuve via le navigateur
# http://localhost:8888/proof.php

# Ou via curl
curl http://localhost:8888/proof.php
```

---

## 📊 Comparaison des Serveurs

| Critère | Serveur Vulnérable (8888) | Serveur Protégé (8889) |
|---------|----------------------------|-------------------------|
| Version PHP | 8.4.26 | 8.4.27 |
| session.upload_progress | **ACTIF** ⚠️ | **DÉSACTIVÉ** ✓ |
| memory_limit | 16M | 16M |
| Attaque OOM | **RÉUSSIE** ✗ | **BLOQUÉE** ✓ |
| RCE | **POSSIBLE** ✗ | **IMPOSSIBLE** ✓ |
| Logs | Erreurs OOM visibles | Aucune erreur |

---

## 🎬 Scripts d'Automatisation

### 1. `attack.py` - Attaques de base
```bash
python attack.py --ransomware    # Rançongiciel
python attack.py --steal          # Fuite de données
python attack.py --deface         # Défaçage
python attack.py --restore        # Restauration
python attack.py --oom            # Déclencheur OOM
python attack.py --compare        # Comparaison
```

### 2. `exploit.py` - Exploitation technique
```bash
python exploit.py --demo          # Démo complète
python exploit.py --oom           # Exploitation OOM
python exploit.py --rce --command "id"  # RCE
python exploit.py --proof        # Créer une preuve
```

### 3. `verify_exploit.py` - Vérification
```bash
python verify_exploit.py              # Vérifier une cible
python verify_exploit.py --compare     # Comparer les serveurs
```

### 4. `monitor.py` - Monitoring
```bash
python monitor.py  # Affiche les logs en temps réel
```

### 5. `demo.py` - Console interactive
```bash
python demo.py  # Mode interactif
python demo.py demo  # Démo guidée
```

---

## 💡 Conseils pour l'Animation

### 1. **Préparation**
```bash
# Lancer le lab avant la session
docker compose up -d --build

# Vérifier que tout fonctionne
python verify_exploit.py --compare
```

### 2. **Pendant la démo**
- **Ouvrir 2 navigateurs** : un pour chaque serveur (8888 et 8889)
- **Ouvrir 2 terminaux** : un pour les commandes, un pour le monitor
- **Montrer les logs** : `tail -f vulnerable/logs/*.log`

### 3. **Scénarios recommandés**

**Scénario 1 : Impact Business (10 min)**
```bash
python attack.py --ransomware
# Montrer le site en rançon
python attack.py --steal
# Montrer les données volées
python attack.py --restore
# Restaurer
```

**Scénario 2 : Technique (15 min)**
```bash
# Dans un terminal
python monitor.py

# Dans un autre terminal
python exploit.py --demo
```

**Scénario 3 : Comparaison (5 min)**
```bash
python attack.py --compare
# Montrer que le serveur protégé bloque tout
```

---

## 🔧 Dépannage

### Problème : Les containers ne démarrent pas
```bash
# Vérifier les logs Docker
docker compose logs

# Reconstruire
docker compose down
docker compose up -d --build
```

### Problème : PHP 8.4.26/8.4.27 non disponible
```bash
# Le repo Sury peut mettre du temps à être mis à jour
# Utiliser une version alternative (PHP 8.3)
# Modifier les Dockerfiles pour utiliser PHP 8.3.35 (vulnérable) et 8.3.36 (corrigé)
```

### Problème : Ports déjà utilisés
```bash
# Changer les ports dans docker-compose.yml
# Par exemple : 8888:80 → 8080:80
```

---

## 📚 Documentation Complète

- **Fiche technique** : [PHP2SHELL_CVE-2026-109618.md](PHP2SHELL_CVE-2026-109618.md)
- **Chronologie** : Découverte en août 2026, correctif le 21/10/2026
- **Catalogue KEV** : Ajouté par la CISA le 26/10/2026

---

## 🎯 Messages Clés à Retenir

1. **🔴 Un code sécurisé ne suffit pas** : L'interpréteur PHP fait partie de votre surface d'attaque
2. **🔴 Les failles système impactent toutes les applications** : Peu importe votre framework (Laravel, Symfony, WordPress)
3. **🟢 La mise à jour est la seule protection fiable** : Pas de contournement possible
4. **🟢 Le monitoring est crucial** : Détectez les attaques avant qu'il ne soit trop tard
5. **🟢 La défense en profondeur fonctionne** : Mitigation + patch = protection totale

---

## 🚀 Arrêt du Lab

```bash
# Arrêter les containers
docker compose down

# Supprimer les fichiers de preuve
rm -f vulnerable/www/proof*.php vulnerable/www/DONNEES_RH_EXFILTREES.csv
rm -f patched/www/proof*.php
```

---

## 📖 Licence

**Usage strictement pédagogique** - Ce lab est conçu pour la sensibilisation et la formation en cybersécurité. **Ne pas utiliser contre des systèmes sans autorisation.**

---

**✅ Votre démo CVE-2026-109618 est prête !**
**🎯 Ultra-réaliste, technique et impactante**
