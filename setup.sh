#!/bin/bash

DBPATH=www/wsgi-scripts/carLog.db

rm -rf $DBPATH

sqlite3 $DBPATH < db/createDb.sql

if [ -f db/populateDb.sql ]; then
	sqlite3 $DBPATH < db/populateDb.sql
fi

if [ -f res/rawMileage.csv ]; then 
	python scripts/importRawMileage.py carLog.db res/rawMileage.csv
fi

if [ -f res/rawMaintenance.csv ]; then
	python scripts/importRawMaintenance.py carLog.db res/rawMaintenance.csv
fi

if [ -f res/rawEvents.csv ]; then
	python scripts/importRawEvents.py carLog.db res/rawEvents.csv
fi
