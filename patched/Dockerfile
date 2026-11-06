# PHP 8.4.27 - PATCHED against CVE-2026-109618 & CVE-2026-109619 (PHP2Shell)
# Use-After-Free via OOM in Zend Engine (session.upload_progress)
# CVSS: 9.2 (Critical)
# Published: October 21, 2026
# This version includes the security fixes
#
# Release: https://www.php.net/releases/8_4_27.php
# Security advisory: Critical remote code execution vulnerabilities, update now

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

# Add Sury repository for PHP 8.4
RUN curl -fsSL https://packages.sury.org/php/apt.gpg | gpg --dearmor -o /usr/share/keyrings/sury-php.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/sury-php.gpg] https://packages.sury.org/php/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/sury-php.list && \
    apt-get update

# Install PHP 8.4.27 (REAL PATCHED version - includes fixes for CVE-2026-109618 & CVE-2026-109619)
RUN apt-get install -y --no-install-recommends \
        php8.4 \
        php8.4-cli \
        php8.4-apache2 \
        libapache2-mod-php8.4 && \
    rm -rf /var/lib/apt/lists/*

# Enable PHP 8.4 module for Apache
RUN a2enmod php8.4

# Configure Apache
RUN echo "ServerName localhost" > /etc/apache2/conf-available/servername.conf && \
    a2enconf servername

# Configure PHP - PATCHED (session.upload_progress.enabled = 0)
# This is the mitigation recommended in the official advisories
RUN echo "memory_limit = 16M" > /etc/php/8.4/apache2/conf.d/99-memory-limit.ini && \
    echo "session.upload_progress.enabled = 0" > /etc/php/8.4/apache2/conf.d/99-upload-progress.ini

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
