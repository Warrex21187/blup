# PHP 8.4.27 (Bookworm + Sury) - CORRIGÉ contre CVE-2026-109618
# Cette version contient le correctif pour la faille PHP2Shell
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 \
        curl \
        gnupg2 \
        ca-certificates \
        lsb-release && \
    # Ajouter le repo Sury pour PHP
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && \
    # Installer PHP 8.4.27 (version CORRIGÉE avec patch CVE-2026-109618)
    apt-get install -y --no-install-recommends \
        php8.4 \
        php8.4-cli \
        php8.4-apache2 \
        libapache2-mod-php8.4 && \
    rm -rf /var/lib/apt/lists/*

# Activer mod_php
RUN a2enmod php8.4

# Configurer PHP avec memory_limit bas pour la démo
RUN echo "memory_limit = 16M" > /etc/php/8.4/apache2/conf.d/99-memory-limit.ini

# DÉSACTIVER session.upload_progress (mitigation recommandée)
# Même avec le patch, c'est une bonne pratique de désactiver cette fonctionnalité inutilisée
RUN echo "session.upload_progress.enabled = 0" > /etc/php/8.4/apache2/conf.d/99-upload-progress.ini

# DirectoryIndex
RUN printf '<IfModule mod_dir.c>\n    DirectoryIndex index.php index.html\n</IfModule>\n' > /etc/apache2/mods-available/dir.conf

# Copier l'application web de démo
COPY www/ /var/www/html/
RUN rm -f /var/www/html/index.html

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

# Activer le module rewrite pour Apache
RUN a2enmod rewrite

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
