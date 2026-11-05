# 🛡️ Lab Démo Awareness — Sécurité & Remédiation PHP

> [!TIP]
> **Fiche complète pour votre session technique :**  
> Retrouvez le guide complet d'analyse, l'explication du mécanisme d'ingénierie C et les étapes de démo dans [`PHP2SHELL_CVE-2026-109618.md`](file:///c:/Users/loris/Desktop/php-lab/PHP2SHELL_CVE-2026-109618.md).

> [!NOTE]
> Ce lab est configuré pour une **démonstration en direct** (sensibilisation des équipes et formation technique). 
> Il intègre la surveillance en direct du moteur PHP, la directive de mitigation `session.upload_progress.enabled = 0` et l'affichage des diagnostics d'infrastructure.

---

## 🚀 Lancement Rapide (Avant votre présentation)

Ouvrez un terminal dans le dossier `php-lab` :

```powershell
docker compose up -d
```

Ouvrez ensuite dans votre navigateur :
- 🌐 **Serveur d'entreprise cible :** [http://localhost:8888](http://localhost:8888)
- 🌐 **Serveur protégé (mise à jour) :** [http://localhost:8889](http://localhost:8889)

*(Placez le navigateur sur la moitié de votre écran et votre terminal d'attaquant sur l'autre moitié pour un effet saisissant !)*

---

## 🎯 Commandes de l'Attaquant (À taper pendant votre démo)

Vous n'avez pas de script rigide à suivre : vous tapez la commande voulue au moment où vous l'expliquez à l'audience. **Le site web réagit instantanément à l'écran sans même rafraîchir la page !**

### 1️⃣ Frapper avec un Rançongiciel (Le plus visuel !)
```powershell
python attack.py --ransomware
```
👉 **Effet en direct :** 
- Le terminal affiche le déploiement du crypto-locker.
- Le portail intranet vire **au rouge sang avec sirène clignotante**, alerte d'extorsion et **compte à rebours animé de 48 heures** pour payer 50 000 €.

---

### 2️⃣ Voler les données RH confidentielles
```powershell
python attack.py --steal
```
👉 **Effet en direct :**
- Le terminal affiche un tableau clair avec les **noms, salaires, IBAN et mots de passe** des directeurs et employés.
- Un fichier Excel/CSV `DONNEES_RH_EXFILTREES.csv` est créé immédiatement.
- Une bannière d'alerte jaune d'exfiltration apparaît sur le site.

---

### 3️⃣ Défaçage « Hacker » du site
```powershell
python attack.py --deface
```
👉 **Effet en direct :**
- Le site se transforme en page noire et verte fluo "HACKED BY ANONYMOUS".

---

### 4️⃣ Remettre le site à neuf (Nettoyage)
```powershell
python attack.py --restore
```
👉 **Effet en direct :**
- Le site redevient immédiatement normal et propre.

---

### 5️⃣ La Démonstration de la Solution (Serveur à jour)
```powershell
python attack.py --compare
```
*(Ou en ciblant le port 8889 : `python attack.py --target http://localhost:8889 --ransomware`)*

👉 **Le message clé :**
- L'attaque passe sur le serveur obsolète (Port 8888).
- L'attaque **est rejetée net (Code 403)** sur le serveur où la mise à jour PHP a été faite (Port 8889).
- **Morale :** Les mises à jour ne sont pas du confort technique, elles sauvent l'entreprise d'un arrêt complet.

---

## 🛑 Arrêt du Lab après la session

```powershell
docker compose down
```
