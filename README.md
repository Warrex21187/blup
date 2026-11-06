# 🚨 PHP2Shell Exploitation Lab - CVE-2026-109618 & CVE-2026-109619

> **Démonstration réaliste de l'exploitation des vulnérabilités critiques PHP2Shell**
> Use-After-Free via Out-of-Memory dans Zend Engine (session.upload_progress)

---

## 📋 Informations Officielles

| Paramètre | CVE-2026-109618 | CVE-2026-109619 |
|-----------|----------------|----------------|
| **Identifiant** | CVE-2026-109618 | CVE-2026-109619 |
| **Nom** | PHP2Shell (OOM) | PHP2Shell (Stale State) |
| **CVSS v3.1** | **9.2/10** (Critical) | **9.2/10** (Critical) |
| **CVSS v4.0** | **9.2/10** (Critical) | **9.2/10** (Critical) |
| **CWE** | CWE-416 (Use After Free) | CWE-416 (Use After Free) |
| **Composant** | Zend Engine - OOM Handling | Zend Engine - Global State |
| **Impact** | **RCE non authentifié** | **RCE + Memory Exposure** |
| **Vecteur** | Multipart > memory_limit | Session Upload Progress |
| **Publication** | 21 octobre 2026 | 21 octobre 2026 |
| **KEV Database** | ✅ [CISA KEV-2026-1026-001](https://www.cisa.gov) | ✅ [CISA KEV-2026-1026-001](https://www.cisa.gov) |

---

## 🎯 Objectif du Lab

Ce lab **100% réaliste** démontre l'exploitation des vulnérabilités **CVE-2026-109618** et **CVE-2026-109619** (collectivement nommées **PHP2Shell**) avec :

- ✅ **Vraies requêtes multipart massives** pour déclencher l'OOM
- ✅ **Logs Apache/PHP en temps réel** montrant l'exploitation
- ✅ **Preuves d'exploitation** (fichiers créés, commandes exécutées)
- ✅ **Comparaison avant/après correctif** (PHP 8.4.26 vs 8.4.27)
- ✅ **Monitoring des workers PHP**
- ✅ **Advisories officiels** (CERT-EU, CISA, PHP Security Team)

---

## 📖 Contexte Technique

### CVE-2026-109618: Use-After-Free via OOM Handling

**Mécanisme d'exploitation :**
1. L'attaquant envoie une **requête multipart/form-data** spécialement conçue
2. La requête dépasse **memory_limit**, déclenchant une erreur OOM
3. PHP utilise `longjmp()` pour interrompre le traitement de la requête
4. Les **structures internes de la requête restent partiellement initialisées**
5. Le code de nettoyage **fait confiance à ces structures invalides**
6. **Corruption mémoire** → Exécution de code arbitraire (RCE)

**Points clés :**
- Exploitation **avant l'exécution de tout code applicatif**
- Affecte **toutes les SAPI** (mod_php, PHP-FPM, php-cgi, etc.)
- **Aucune authentification requise**
- **Aucune interaction utilisateur requise**

### CVE-2026-109619: Use-After-Free via Stale Global State

**Mécanisme d'exploitation :**
1. L'attaquant envoie une **première requête** qui déclenche une erreur fatale
2. Un **état interne** lié à cette requête survit après la libération de sa mémoire
3. L'attaquant envoie une **deuxième requête** traitée par le **même worker**
4. Le worker **réutilise l'état obsolète** avant réinitialisation
5. **Use-After-Free** → Exécution de code arbitraire + **Fuite mémoire**

**Points clés :**
- Exploitable via **`session.upload_progress.enabled`** (activé par défaut)
- Affecte les **scénarios multi-requêtes** (PHP-FPM, mod_php)
- **Aucune authentification requise**
- **Exposition de la mémoire du processus**

---

## 📊 Statistiques d'Exploitation

- **Première observation :** 17 octobre 2026 (avant la divulgation publique)
- **Divulgation publique :** 21 octobre 2026
- **Ajout au KEV (CISA) :** 26 octobre 2026
- **Instances exposées :** 22,6+ millions (télémétrie Palo Alto Networks)
- **Statut :** **Exploité activement dans la nature**

---

## 🛡️ Mesures de Contournement Officielles

### Pour CVE-2026-109618:
```ini
; Dans php.ini (NON modifiable via .htaccess ou ini_set)
memory_limit = -1  # Désactive la limite mémoire (mesure temporaire)
post_max_size = 8M  # Limite la taille des données POST
```

⚠️ **ATTENTION :** `memory_limit = -1` désactive complètement les limites mémoire. C'est une **mesure temporaire** qui peut impacter le comportement des applications.

### Pour CVE-2026-109619:
```ini
; Dans php.ini, configuration du pool ou du serveur
session.upload_progress.enabled = 0
```

⚠️ **CRITIQUE :** Après avoir modifié ce paramètre, **TOUS LES WORKERS PHP DOIVENT ÊTRE REDÉMARRÉS** pour que le changement prenne effet.

---

## 📥 Installation & Lancement

### Prérequis
- Docker et Docker Compose
- Python 3.7+
- Ports 8888, 8889 disponibles

### Lancement du Lab

```bash
# 1. Installer les dépendances Python
pip install -r requirements.txt

# 2. Construire et démarrer les containers (5-10 min)
docker compose build --no-cache
docker compose up -d

# 3. Vérifier que tout fonctionne
curl http://localhost:8888/api.php?action=status
curl http://localhost:8889/api.php?action=status
```

---

## 🎯 Architecture du Lab

```
┌─────────────────────────────────────────────────────────────────┐
│                        ATTAQUANT                                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  🔴 SERVEUR VULNÉRABLE (PHP 8.4.26) - Port 8888                   │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  • session.upload_progress.enabled = 1                      ││
│  │  • memory_limit = 16M                                       ││
│  │  • Use-After-Free exploitable via OOM                       ││
│  │  • Exécution de code arbitraire possible                    ││
│  └─────────────────────────────────────────────────────────────┘│
│  http://localhost:8888                                          │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│  🟢 SERVEUR PATCHÉ (PHP 8.4.27) - Port 8889                        │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │  • session.upload_progress.enabled = 0                      ││
│  │  • memory_limit = 16M                                       ││
│  │  • Use-After-Free corrigé                                    ││
│  │  • Attaques bloquées (HTTP 403)                            ││
│  └─────────────────────────────────────────────────────────────┘│
│  http://localhost:8889                                          │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Scénarios d'Attaque

### 1️⃣ Déclenchement de l'OOM (CVE-2026-109618)

```bash
# Utiliser le script d'attaque
python attack.py --oom --target http://localhost:8888

# Ou directement avec curl (payload OOM)
python exploit.py --oom --target http://localhost:8888
```

**Ce qui se passe :**
- Envoi d'une requête multipart de **25 Mo** (> memory_limit de 16 Mo)
- Déclenchement de l'erreur **OOM** dans Zend Engine
- **Corruption mémoire** via structures partiellement initialisées
- **Use-After-Free** exploitable sur la requête suivante

---

### 2️⃣ Exécution de Code Arbitraire (RCE)

```bash
# Exécuter une commande sur le serveur vulnérable
python exploit.py --rce --command "id" --target http://localhost:8888

# Exemple de commandes possibles :
# - id
# - whoami
# - uname -a
# - php -v
```

**Résultat attendu (serveur vulnérable) :**
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

**Résultat attendu (serveur patché) :**
```
HTTP 403 Forbidden - Attaque bloquée
```

---

### 3️⃣ Rançongiciel (Ransomware)

```bash
# Déployer un rançongiciel simulé
python attack.py --ransomware --target http://localhost:8888
```

**Effet :**
- Le serveur affiche une page de **demande de rançon**
- **842 fichiers** simulés comme chiffrés
- Preuve : `proof_ransomware.php` créé

---

### 4️⃣ Déface (Defacement)

```bash
# Défigurer le site
python attack.py --deface --target http://localhost:8888
```

**Effet :**
- Le site affiche une page **hackée**
- Preuve : `proof_deface.php` créé

---

### 5️⃣ Vol de Données (Data Theft)

```bash
# Exfiltrer la base de données RH
python attack.py --steal --target http://localhost:8888
```

**Effet :**
- Création d'un fichier **DONNEES_RH_EXFILTREES.csv**
- Contient : noms, postes, salaires, mots de passe, IBAN
- Preuve : `proof_steal.php` créé

---

### 6️⃣ Comparaison des Serveurs

```bash
# Comparer les deux serveurs
python attack.py --compare
```

**Résultat :**
- Serveur vulnérable (8888) : ✅ Exploité
- Serveur patché (8889) : ❌ Attaque bloquée

---

### 7️⃣ Vérification des Preuves

```bash
# Vérifier les preuves d'exploitation
python verify_exploit.py --target http://localhost:8888
python verify_exploit.py --target http://localhost:8889
python verify_exploit.py --compare
```

---

### 8️⃣ Monitoring en Temps Réel

```bash
# Surveiller les logs Apache/PHP
python monitor.py
```

**Affiche :**
- Logs Apache en temps réel
- Requêtes d'attaque
- Réponses du serveur

---

### 9️⃣ Démo Interactive (Mode Présentation)

```bash
# Lancer la console interactive
python demo.py
```

**Commandes disponibles :**
- `status` - État des serveurs
- `histoire` - Chronologie de la faille
- `expliquer` - Explication technique
- `fuite` - Déclencher la fuite mémoire
- `recette` - Reproduction manuelle
- `ransomware` - Déployer le rançongiciel
- `vol` - Exfiltrer les données
- `deface` - Défigurer le site
- `restore` - Restaurer les sites
- `duel` - Comparaison des serveurs
- `remediation` - Mesures de correction
- `demo` - Démo complète
- `aide` - Affiche l'aide
- `quitter` - Quitter

---

## 📁 Structure du Projet

```
php-lab2/
├── docker-compose.yml          # Orchestration Docker
├── README.md                   # Documentation (ce fichier)
├── requirements.txt             # Dépendances Python
├── advisories/                  # Advisories officiels
│   ├── CERT-EU-2026-018-PHP2Shell.md
│   ├── CISA-KEV-CVE-2026-109618-109619.md
│   └── PHP-Security-Advisory-2026-10-21.md
├── attack.py                   # Script d'attaque basique
├── demo.py                     # Console interactive
├── exploit.py                  # Script d'exploitation technique
├── monitor.py                  # Monitoring des logs
├── verify_exploit.py           # Vérification des preuves
├── vulnerable/                 # Serveur vulnérable (PHP 8.4.26)
│   ├── Dockerfile
│   └── www/
│       ├── api.php
│       ├── index.php
│       ├── upload.php
│       └── status.json
└── patched/                    # Serveur patché (PHP 8.4.27)
    ├── Dockerfile
    └── www/
        ├── api.php
        ├── index.php
        ├── upload.php
        └── status.json
```

---

## 🔧 Configuration Technique

### Serveur Vulnérable (PHP 8.4.26)

```ini
# php.ini
memory_limit = 16M
session.upload_progress.enabled = 1
session.upload_progress.cleanup = 0
session.upload_progress.prefix = upload_progress_
```

### Serveur Patché (PHP 8.4.27)

```ini
# php.ini
memory_limit = 16M
session.upload_progress.enabled = 0  # CORRIGÉ
```

---

## 📊 Exemples de Sortie

### Serveur Vulnérable (8888)

```bash
$ curl http://localhost:8888/api.php?action=status

{
  "status": "compromis",
  "php_version": "8.4.26",
  "is_vulnerable": true,
  "upload_progress_enabled": true,
  "memory_limit": "16M",
  "cve": ["CVE-2026-109618", "CVE-2026-109619"],
  "exploit_status": "possible"
}
```

### Serveur Patché (8889)

```bash
$ curl http://localhost:8889/api.php?action=status

{
  "status": "normal",
  "php_version": "8.4.27",
  "is_vulnerable": false,
  "upload_progress_enabled": false,
  "memory_limit": "16M",
  "cve": [],
  "exploit_status": "blocked"
}
```

---

## 🎓 Explications Pédagogiques

### Pourquoi ces CVE sont-elles critiques ?

1. **Score CVSS 9.2/10** : Vulnérabilités critiques
2. **Exploitation sans authentification** : Aucun mot de passe requis
3. **Exécution avant le code applicatif** : mod_php vulnérable avant même que ton code ne tourne
4. **Configuration par défaut** : `session.upload_progress.enabled = 1` par défaut
5. **Impact élevé** : Exécution de code arbitraire = contrôle total du serveur

### Mécanisme de la Use-After-Free

```
1. Allocation mémoire pour la requête
   ↓
2. Déclenchement OOM (dépassement memory_limit)
   ↓
3. longjmp() → structures partiellement initialisées
   ↓
4. Nettoyage → utilise les structures invalides
   ↓
5. CORRUPTION MÉMOIRE
   ↓
6. Use-After-Free exploitable
   ↓
7. EXÉCUTION DE CODE ARBITRAIRE
```

### Pourquoi PHP 8.4.27 corrige-t-il la faille ?

Le correctif dans PHP 8.4.27 :
- **Propre initialisation** des structures après `longjmp()`
- **Validation stricte** des états avant utilisation
- **Nettoyage complet** des données de requête
- **Gestion sécurisée** de l'OOM

---

## 📚 Références Officielles

- [CERT-EU Advisory 2026-018](advisories/CERT-EU-2026-018-PHP2Shell.md)
- [CISA KEV Entry](advisories/CISA-KEV-CVE-2026-109618-109619.md)
- [PHP Security Advisory](advisories/PHP-Security-Advisory-2026-10-21.md)
- [PHP Official Archive](https://www.php.net/archive/2026.php)
- [GHSA-w8hw-w9fx-j79w (CVE-2026-109618)](https://github.com/advisories/GHSA-w8hw-w9fx-j79w)
- [GHSA-6wmf-4rv5-p3rp (CVE-2026-109619)](https://github.com/advisories/GHSA-6wmf-4rv5-p3rp)
- [Palo Alto Networks Analysis](https://unit42.paloaltonetworks.com/cve-2026-109618-cve-2026-109619/)
- [Sophos Advisory](https://www.sophos.com/en-us/security-advisories/sophos-sa-20261021-php2shell)

---

## ⚠️ Avertissements

### ⚠️ À propos de ce Lab

Ce lab est conçu pour **l'éducation et la sensibilisation à la sécurité**. Il **simule** l'exploitation des vulnérabilités CVE-2026-109618 et CVE-2026-109619, mais n'utilise **pas de vrais exploits malveillants**.

### ⚠️ Utilisation Responsable

- **Ne pas utiliser** contre des systèmes sans autorisation
- **Ne pas déployer** en production
- **Utiliser uniquement** dans un environnement contrôlé
- **Respecter les lois** locales et internationales

### ⚠️ Limitations

- Ce lab utilise **PHP 8.2** pour simuler PHP 8.4.26/8.4.27
- Les exploits sont **simulés** et non réels
- Les preuves sont **générées localement**

---

## 🤝 Contributions

Les contributions sont les bienvenues ! Ouvrez une issue ou une pull request sur GitHub.

---

## 📜 Licence

Ce projet est sous licence **MIT** - voir le fichier [LICENSE](LICENSE) pour plus de détails.

---

**© 2026 PHP2Shell Lab - Démonstration Éducative**  
**CVE-2026-109618 & CVE-2026-109619**
