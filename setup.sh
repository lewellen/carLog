#!/bin/bash

rm -rf carLog.db

sqlite3 carLog.db < db/createDb.sql

if [ -f db/populateDb.sql ]; then
	sqlite3 carLog.db < db/populateDb.sql
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
