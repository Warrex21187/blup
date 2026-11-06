FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install Apache + PHP 8.2 (default on Bookworm)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        apache2 \
        php \
        libapache2-mod-php8.2 \
        curl && \
    rm -rf /var/lib/apt/lists/*

# Config Apache
RUN a2enmod php8.2 rewrite && \
    echo "ServerName localhost" > /etc/apache2/conf-available/servername.conf && \
    a2enconf servername

# Config PHP - PATCHED (session.upload_progress.enabled = 0)
RUN echo "memory_limit = 16M" > /etc/php/*/apache2/conf.d/99-memory-limit.ini && \
    echo "session.upload_progress.enabled = 0" > /etc/php/*/apache2/conf.d/99-upload-progress.ini

# Copy website files
COPY www/ /var/www/html/
RUN chown -R www-data:www-data /var/www/html

EXPOSE 80
CMD ["apache2ctl", "-D", "FOREGROUND"]
