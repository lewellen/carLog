#!/bin/bash

TEMPDBPATH=rest-tests.db
python src/rest.wsgi $TEMPDBPATH &
PID=$!

echo "DB_PATH: $TEMPDBPATH"
echo "Python WSGI PID $PID"

sleep 5

curl -X POST "http://127.0.0.1:5000/users" -H "Content-Type:application/json" -d '{"name" : "foo"}'
curl -X GET "http://127.0.0.1:5000/users"
curl -X GET "http://127.0.0.1:5000/users/1/vehicles"

curl -X POST "http://127.0.0.1:5000/vehicles" -H "Content-Type:application/json" -d '{"name" : "foo"}'

curl -X GET "http://127.0.0.1:5000/vehicles/1/estimates"
curl -X GET "http://127.0.0.1:5000/vehicles/1/mileage"
curl -X GET "http://127.0.0.1:5000/vehicles/1/maintenance"
curl -X GET "http://127.0.0.1:5000/vehicles/1/events"

curl -X POST "http://127.0.0.1:5000/mileage" -H "Content-Type:application/json" -d '{"name" : "foo"}'

curl -X POST "http://127.0.0.1:5000/maintenance" -H "Content-Type:application/json" -d '{"name" : "foo"}'

curl -X POST "http://127.0.0.1:5000/events" -H "Content-Type:application/json" -d '{"name" : "foo"}'


curl -X POST "http://127.0.0.1:5000/providerTypes" -H "Content-Type:application/json" -d '{"name" : "foo"}'
curl -X GET "http://127.0.0.1:5000/providerTypes"

curl -X POST "http://127.0.0.1:5000/providers" -H "Content-Type:application/json" -d '{"name" : "foo"}'
curl -X GET "http://127.0.0.1:5000/providers"

curl -X POST "http://127.0.0.1:5000/destinations" -H "Content-Type:application/json" -d '{"name" : "foo"}'
curl -X GET "http://127.0.0.1:5000/destinations"

sleep 1

echo "Terminating PID $PID"
kill $PID

echo "Removing $TEMPDBPATH"
rm -rf $TEMPDBPATH
