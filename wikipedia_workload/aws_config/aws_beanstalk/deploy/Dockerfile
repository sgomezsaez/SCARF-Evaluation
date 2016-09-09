FROM sgomezsaez/mediawiki

ENV MEDIAWIKI_DB_HOST mediawiki-database.cqxl2sg3qwmu.eu-west-1.rds.amazonaws.com:3306
ENV MEDIAWIKI_DB_USER root 
ENV MEDIAWIKI_DB_PASSWORD wpFzCAqb 
ENV MEDIAWIKI_DB_NAME my_wiki
ENV MEDIAWIKI_INSTALL_DIR /var/www/html

ADD LocalSettings.php ${MEDIAWIKI_INSTALL_DIR}/LocalSettings.php

EXPOSE 80
EXPOSE 443

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]