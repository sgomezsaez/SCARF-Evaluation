FROM synctree/mediawiki:1.23

ENV MEDIAWIKI_INSTALL_DIR /var/www/html

#RUN sudo apt-get update
#RUN sudo apt-get -y install apache2 php5 libapache2-mod-php5 wget
#RUN sudo apt-get -y install php-apc php5-intl imagemagick vsftpd

#RUN sudo apt-get -y install wget
#RUN wget https://releases.wikimedia.org/mediawiki/1.23/mediawiki-1.23.2.tar.gz
#RUN tar -xzf mediawiki-1.23.2.tar.gz -C ${MEDIAWIKI_INSTALL_DIR} 

#RUN mv ${MEDIAWIKI_INSTALL_DIR}/mediawiki-1.23.2 ${MEDIAWIKI_INSTALL_DIR}/w

ADD LocalSettings.php ${MEDIAWIKI_INSTALL_DIR}/LocalSettings.php

RUN apt-get update  
RUN apt-get -y install php5-fpm php5-apcu php5-dev libpcre3-dev
RUN echo "; apc.ini, include the APC extension \n extension=apc.so" >> /etc/php5/cli/php.ini


EXPOSE 80
EXPOSE 443

#CMD ["/usr/sbin/apache2ctl", "-D", "FOREGROUND"]

ENTRYPOINT ["/entrypoint.sh"]
CMD ["apache2-foreground"]
