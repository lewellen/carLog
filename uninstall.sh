apachectl stop

rm -rf /var/www/carLog
rm -rf /etc/apache2/sites-enabled/carLog.conf
rm -rf /etc/apache2/sites-available/carLog.conf

apachectl start
