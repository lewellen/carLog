apachectl stop

rm -rf /var/www/carLog
rm -rf /etc/apache2/sites-available/carLog.conf
rm -rf /etc/apache2/sites-enabled/carLog.conf

ln -s ~/Development/carLog/www /var/www/carLog
cp conf/apache-vh-carLog.conf /etc/apache2/sites-available/carLog.conf
cp conf/apache-vh-carLog.conf /etc/apache2/sites-enabled/carLog.conf

apachectl start
