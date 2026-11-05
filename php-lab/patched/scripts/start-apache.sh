#!/bin/bash

# Script de démarrage pour Apache avec logs détaillés

echo "[PHP2Shell Lab] Démarrage du serveur protégé (PHP 8.4.27)..."
echo "[PHP2Shell Lab] Configuration : session.upload_progress.enabled = 0 (Mitigé)"
echo "[PHP2Shell Lab] Memory Limit : 16M"
echo "[PHP2Shell Lab] Correctif CVE-2026-109618 : ACTIF"
echo ""

# Démarrer Apache en arrière-plan
apachectl -D FOREGROUND &
APACHE_PID=$!

# Attendre que Apache soit prêt
sleep 2

echo "[PHP2Shell Lab] Serveur Apache démarré (PID: $APACHE_PID)"
echo "[PHP2Shell Lab] Logs disponibles dans : /var/log/apache2/"
echo "[PHP2Shell Lab] Toutes les attaques CVE-2026-109618 seront BLOQUÉES"
echo ""

# Afficher les logs en temps réel dans la console
tail -f /var/log/apache2/*.log &
TAIL_PID=$!

# Attendre la fin
wait $APACHE_PID

# Cleanup
kill $TAIL_PID 2>/dev/null
