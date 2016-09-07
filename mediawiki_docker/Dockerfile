FROM synctree/mediawiki:1.23

ENV MEDIAWIKI_INSTALL_DIR /var/www/html

ADD LocalSettings.php ${MEDIAWIKI_INSTALL_DIR}/LocalSettings.php

RUN apt-get update  
RUN apt-get -y install php5-fpm php-apc php5-dev libpcre3-dev

RUN apt-get update && apt-get install -y libmemcached-dev \
    && pecl install memcached \
    && docker-php-ext-enable memcached

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]
