# PHP 8.4.26 (Bookworm + Sury) - VULNERABLE à CVE-2026-109618
# Cette version contient la faille PHP2Shell (Use-After-Free dans Zend Engine)
FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Installer les dépendances
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 \
        curl \
        gnupg2 \
        ca-certificates \
        lsb-release \
        tail \
        net-tools && \
    # Ajouter le repo Sury pour PHP
    curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update && \
    # Installer PHP 8.4.26 (version VULNÉRABLE à CVE-2026-109618)
    apt-get install -y --no-install-recommends \
        php8.4 \
        php8.4-cli \
        php8.4-apache2 \
        libapache2-mod-php8.4 && \
    rm -rf /var/lib/apt/lists/*

# Activer mod_php (SAPI la plus exposée pour cette faille)
RUN a2enmod php8.4

# Configurer PHP avec memory_limit bas pour faciliter le déclenchement OOM
RUN echo "memory_limit = 16M" > /etc/php/8.4/apache2/conf.d/99-memory-limit.ini

# ACTIVER session.upload_progress (nécessaire pour la faille CVE-2026-109618)
RUN echo "session.upload_progress.enabled = 1" > /etc/php/8.4/apache2/conf.d/99-upload-progress.ini && \
    echo "session.upload_progress.cleanup = 0" >> /etc/php/8.4/apache2/conf.d/99-upload-progress.ini && \
    echo "session.upload_progress.prefix = upload_progress_" >> /etc/php/8.4/apache2/conf.d/99-upload-progress.ini

# Configurer Apache pour des logs détaillés
RUN echo "LogLevel alert" > /etc/apache2/conf-available/log-level.conf && \
    echo "ErrorLog /var/log/apache2/php2shell-error.log" >> /etc/apache2/conf-available/log-level.conf && \
    echo "CustomLog /var/log/apache2/php2shell-access.log combined" >> /etc/apache2/conf-available/log-level.conf && \
    a2enconf log-level

# Activer le module rewrite pour Apache
RUN a2enmod rewrite

# DirectoryIndex
RUN printf '<IfModule mod_dir.c>\n    DirectoryIndex index.php index.html\n</IfModule>\n' > /etc/apache2/mods-available/dir.conf

# Copier l'application web de démo
COPY www/ /var/www/html/
RUN rm -f /var/www/html/index.html

# Créer le répertoire des logs
RUN mkdir -p /var/log/apache2 && \
    chown -R www-data:www-data /var/log/apache2

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

# Script de démarrage personnalisé pour afficher les logs
COPY scripts/start-apache.sh /start-apache.sh
RUN chmod +x /start-apache.sh

EXPOSE 80
CMD ["/start-apache.sh"]
