FROM synctree/mediawiki:1.23

ENV MEDIAWIKI_INSTALL_DIR /var/www/html

ADD LocalSettings.php ${MEDIAWIKI_INSTALL_DIR}/LocalSettings.php

RUN apt-get update  

RUN apt-get install -y php5-apcu
RUN echo apc.enabled=1 >> /etc/php5/mods-available/apcu.ini 
RUN echo apc.enable_cli=1 >> /etc/php5/mods-available/apcu.ini 
RUN cp /etc/php5/mods-available/apcu.ini /usr/local/etc/php/conf.d/apcu.ini


RUN curl -fsSL 'https://xcache.lighttpd.net/pub/Releases/3.2.0/xcache-3.2.0.tar.gz' -o xcache.tar.gz \
    && mkdir -p xcache \
    && tar -xf xcache.tar.gz -C xcache --strip-components=1 \
    && rm xcache.tar.gz \
    && ( \
        cd xcache \
        && phpize \
        && ./configure --enable-xcache \
        && make -j$(nproc) \
        && make install \
    ) \
    && rm -r xcache \
    && docker-php-ext-enable xcache

RUN echo xcache.var_size=16M >> /usr/local/etc/php/conf.d/docker-php-ext-xcache.ini

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]
