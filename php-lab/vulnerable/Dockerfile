# PHP 8.1 (Bookworm + Sury) — version vulnérable à CVE-2024-4577
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
    # Installer PHP 8.1 CGI (version vulnérable)
    apt-get install -y --no-install-recommends \
        php8.1-cgi \
        php8.1-cli && \
    rm -rf /var/lib/apt/lists/*

# Activer les modules Apache nécessaires
RUN a2enmod cgid actions

# Configurer Apache pour utiliser php-cgi
RUN printf '<IfModule mod_actions.c>\n\
    ScriptAlias /php-cgi/ "/usr/lib/cgi-bin/"\n\
    <Directory "/usr/lib/cgi-bin">\n\
        AllowOverride None\n\
        Options +ExecCGI\n\
        Require all granted\n\
    </Directory>\n\
    Action php-cgi /php-cgi/php8.1\n\
    AddHandler php-cgi .php\n\
</IfModule>\n' > /etc/apache2/conf-available/php-cgi.conf && \
    a2enconf php-cgi

# Désactiver mod_php s'il existe
RUN a2dismod php8.1 2>/dev/null || true

# DirectoryIndex
RUN printf '<IfModule mod_dir.c>\n    DirectoryIndex index.php index.html\n</IfModule>\n' > /etc/apache2/mods-available/dir.conf

# Copier la configuration de mitigation temporaire
COPY conf/security-mitigation.ini /etc/php/8.1/mods-available/mitigation.ini
RUN phpenmod -v 8.1 mitigation

# Copier l'application web de démo
COPY www/ /var/www/html/
RUN rm -f /var/www/html/index.html

RUN chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

EXPOSE 80
CMD ["apachectl", "-D", "FOREGROUND"]
