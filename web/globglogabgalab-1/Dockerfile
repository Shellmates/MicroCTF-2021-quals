FROM php:7.3-apache

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get -y --no-install-recommends install cowsay

COPY challenge /var/www/html

WORKDIR /var/www/html

RUN chmod 111 flag.runme

RUN chown root:root /var/www/html
