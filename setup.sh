#!/bin/bash

DBPATH=www/db/carLog.db

rm -rf $DBPATH

sqlite3 $DBPATH < db/createDb.sql
chown www-data:www-data $DBPATH
chmod g+w $DBPATH

chown www-data:www-data www/db
chmod g+w www/db

if [ -f db/populateDb.sql ]; then
	sqlite3 $DBPATH < db/populateDb.sql
fi

if [ -f res/rawMileage.csv ]; then 
	python scripts/importRawMileage.py $DBPATH res/rawMileage.csv
fi

if [ -f res/rawMaintenance.csv ]; then
	python scripts/importRawMaintenance.py $DBPATH res/rawMaintenance.csv
fi

if [ -f res/rawEvents.csv ]; then
	python scripts/importRawEvents.py $DBPATH res/rawEvents.csv
fi
