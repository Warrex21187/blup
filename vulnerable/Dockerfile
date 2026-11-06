# PHP 8.4.26 - VULNERABLE to CVE-2026-109618 & CVE-2026-109619 (PHP2Shell)
# Use-After-Free via OOM in Zend Engine (session.upload_progress)
# CVSS: 9.2 (Critical)
# Published: October 21, 2026
# Fixed in: PHP 8.4.27
#
# NOTE: PHP 8.4.26 doesn't exist yet in repos (Nov 2026)
# Using PHP 8.3.36 as base and simulating 8.4.26 for demo purposes

FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 \
        curl \
        gnupg2 \
        ca-certificates \
        lsb-release \
        net-tools && \
    rm -rf /var/lib/apt/lists/*

# Add Sury repository for PHP
RUN curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update

# Install PHP 8.3 (simulating 8.4.26 for demo)
RUN apt-get install -y --no-install-recommends \
        php8.3 \
        php8.3-cli \
        php8.3-apache2 \
        libapache2-mod-php8.3 && \
    rm -rf /var/lib/apt/lists/*

# Enable PHP 8.3 module for Apache
RUN a2enmod php8.3

# Configure Apache
RUN echo "ServerName localhost" > /etc/apache2/conf-available/servername.conf && \
    a2enconf servername

# Configure PHP - VULNERABLE (session.upload_progress.enabled = 1)
# This is the configuration that makes CVE-2026-109618 & CVE-2026-109619 exploitable
RUN echo "memory_limit = 16M" > /etc/php/8.3/apache2/conf.d/99-memory-limit.ini && \
    echo "session.upload_progress.enabled = 1" > /etc/php/8.3/apache2/conf.d/99-upload-progress.ini && \
    echo "session.upload_progress.cleanup = 0" >> /etc/php/8.3/apache2/conf.d/99-upload-progress.ini && \
    echo "session.upload_progress.prefix = upload_progress_" >> /etc/php/8.3/apache2/conf.d/99-upload-progress.ini

# Create version override to simulate PHP 8.4.26
RUN echo "<?php" > /usr/local/bin/php_version_override.php && \
    echo "if (isset(\$_SERVER['SCRIPT_FILENAME']) && strpos(\$_SERVER['SCRIPT_FILENAME'], 'api.php') !== false) {" >> /usr/local/bin/php_version_override.php && \
    echo "    header('X-PHP-Version: 8.4.26');" >> /usr/local/bin/php_version_override.php && \
    echo "}" >> /usr/local/bin/php_version_override.php && \
    echo "?>" >> /usr/local/bin/php_version_override.php

# Copy website files
COPY www/ /var/www/html/
RUN rm -f /var/www/html/index.html

# Set permissions
RUN mkdir -p /var/log/apache2 && \
    chown -R www-data:www-data /var/log/apache2 && \
    chown -R www-data:www-data /var/www/html && \
    chmod -R 755 /var/www/html

# Start Apache in foreground
EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
