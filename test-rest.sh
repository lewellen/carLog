#!/bin/bash

TEMPDBPATH=rest-tests.db
python src/rest.wsgi $TEMPDBPATH &
PID=$!

echo "DB_PATH: $TEMPDBPATH"
echo "Python WSGI PID $PID"

sleep 2 

curl -X POST "http://127.0.0.1:5000/users" -H "Content-Type:application/json" -d '{"name" : "John Smith"}'
curl -X POST "http://127.0.0.1:5000/vehicles" -H "Content-Type:application/json" -d '{"userId" : 1, "vin" : "TBD", "make" : "Make", "model" : "model", "year" : "2017", "stillOwn" : "1" }'
curl -X POST "http://127.0.0.1:5000/mileage" -H "Content-Type:application/json" -d '{ "vehicleId" : 1, "providerId" : 1, "destinationId" : 1, "fromDate" : "2017-05-01", "toDate" : "2017-05-19", "tripMileage" : 100.5, "totalMileage" : 80000, "gallons" : 10.5, "pricePerGallon" : 2.32 }'
curl -X POST "http://127.0.0.1:5000/maintenance" -H "Content-Type:application/json" -d '{"vehicleId" : 1, "providerId" : 1, "at" : "2017-05-19", "primaryContact" : "Jane Doe", "phoneNumber" : "555-123-4567", "description" : "Tire Rotation", "cost" : 5.99 }'

curl -X POST "http://127.0.0.1:5000/events" -H "Content-Type:application/json" -d '{"vehicleId" : 1, "at" : "2017-05-19", "totalMileage" : 80000, "description" : "80K" }'
curl -X POST "http://127.0.0.1:5000/providerTypes" -H "Content-Type:application/json" -d '{"name" : "ProviderTypeName"}'
curl -X POST "http://127.0.0.1:5000/providers" -H "Content-Type:application/json" -d '{"providerTypeId" : 1, "name" : "ProviderName", "address" : "1234 Street AnyTown, USA 12345"}'
curl -X POST "http://127.0.0.1:5000/destinations" -H "Content-Type:application/json" -d '{"name" : "DestinationName"}'

curl -X GET "http://127.0.0.1:5000/users"
curl -X GET "http://127.0.0.1:5000/users/1/vehicles"
curl -X GET "http://127.0.0.1:5000/vehicles/1/estimates"
curl -X GET "http://127.0.0.1:5000/vehicles/1/mileage"
curl -X GET "http://127.0.0.1:5000/vehicles/1/maintenance"
curl -X GET "http://127.0.0.1:5000/vehicles/1/events"
curl -X GET "http://127.0.0.1:5000/providerTypes"
curl -X GET "http://127.0.0.1:5000/providers"
curl -X GET "http://127.0.0.1:5000/destinations"

sleep 1

echo "Terminating PID $PID"
kill $PID

echo "Removing $TEMPDBPATH"
rm -rf $TEMPDBPATH
