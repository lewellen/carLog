import sys
import os.path
import datetime

import csv
import StringIO

from flask import Flask, request, jsonify, make_response
from flask.json import JSONEncoder

from dao import CarLogDB, UsersTable, VehiclesTable, MileageTable, MaintenanceTable, EventsTable, ProvidersTable, ProviderTypesTable, DestinationsTable
from exploratoryAnalysis import MileageData, Estimator, Summarizer

DB_PATH = "/var/www/carLog/db/carLog.db"

class CustomJSONEncoder(JSONEncoder):
	def default(self, obj):
		if isinstance(obj, datetime.datetime):
			try:
				return obj.strftime("%Y-%m-%d")
			except ValueError:
				return "%0.4d-%0.2d-%0.2d" % (obj.year, obj.month, obj.day)
	
		return JSONEncoder.default(obj)

application = Flask(__name__)
application.json_encoder = CustomJSONEncoder

def dictArrayToCSV(xs, fieldnames = None):
	content = None
	if len(xs) > 0:
		target = StringIO.StringIO()

		if fieldnames is None or len(fieldnames) == 0:
			fieldnames = xs[0].keys()

		writer = csv.DictWriter(target, fieldnames=fieldnames)
		writer.writeheader()
		for x in xs:
			writer.writerow(x)

		content = target.getvalue()

		target.close()

	return content

def csvResponse(xs, fieldnames = None, fileName = "export.csv"):
	content = dictArrayToCSV(xs, fieldnames)
	response = make_response(content)
	response.headers["Content-Disposition"] = "attachment; filename=%s" % fileName
	response.mimetype = "text/csv"
	return response

# Users -----------------------------------------------------------------------

@application.route("/users", methods=["POST"])
def addOrUpdateUser():
        with UsersTable(DB_PATH) as db:
                results = db.add(request.get_json())
        return jsonify(results)

@application.route("/users", methods=["GET"])
def findAllUsers():
        with UsersTable(DB_PATH) as db:
                results = db.findAll()
        return jsonify(results)

@application.route("/users/<userId>", methods=["GET"])
def findUser(userId):
        with UsersTable(DB_PATH) as db:
                results = db.find(userId)
        return jsonify(results)

@application.route("/users/<userId>", methods=["DELETE"])
def removeUser(userId):
        with UsersTable(DB_PATH) as db:
                results = db.remove(userId)
        return jsonify(results)

# Vehicles --------------------------------------------------------------------

@application.route("/vehicles", methods=["POST"])
def addOrUpdateVehicle():
	with VehiclesTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/vehicles", methods=["GET"])
def findAllVehicles():
	with VehiclesTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/users/<userId>/vehicles", methods=["GET"])
def findVehiclesByUserId(userId):
	with VehiclesTable(DB_PATH) as db:
		results = db.findByUserId(userId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>", methods=["GET"])
def findVehicle(vehicleId):
	with VehiclesTable(DB_PATH) as db:
		results = db.find(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>", methods=["DELETE"])
def removeVehicle(vehicleId):
	with VehiclesTable(DB_PATH) as db:
		results = db.remove(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/costSummary", methods=["GET"])
def getVehicleCostSummary(vehicleId):
	mileage = None
	with MileageTable(DB_PATH) as db:
		mileage = db.findByVehicleId(vehicleId)

	maintenance = None
	with MaintenanceTable(DB_PATH) as db:
		maintenance = db.findByVehicleId(vehicleId)

	s = Summarizer()
	return jsonify({
		"fuel" : s.getSummary(
			map(lambda x : x["toDate"], mileage),
			map(lambda x : x["pricePerGallon"] * x["gallons"], mileage)
		),
		"maintenance" : s.getSummary(
			map(lambda x : x["at"], maintenance),
			map(lambda x : x["cost"], maintenance)
		)
	});

@application.route("/vehicles/<vehicleId>/estimates", methods=["GET"])
def getVehicleEstimates(vehicleId):
	mileage = None
	with MileageTable(DB_PATH) as db:
		mileage = db.findByVehicleId(vehicleId)

	numBins = 10
	md = MileageData(mileage)
	est = Estimator(md)
	return jsonify({
		"tank" : est.getSummary(md.gallons, numBins),
		"mpg" : est.getSummary(md.mpg, numBins),
		"range" : est.getSummary(md.tripMileage, numBins),
		"ppm" : est.getSummary(md.ppm, numBins),
		"fuelCosts" : est.getSummary(md.extendedAmounts, numBins),
		"ppd" : est.getSummary(md.ppd, numBins)
	})

# Mileage ---------------------------------------------------------------------

@application.route("/mileage", methods=["POST"])
def addOrUpdateMileage():
	with MileageTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/mileage", methods=["GET"])
def findAllMileage():
	with MileageTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/mileage", methods=["GET"])
def findMileageByVehicleId(vehicleId):
	with MileageTable(DB_PATH) as db:
		results = db.findByVehicleId(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/mileage/csv", methods=["GET"])
def exportMileageByVehicleId(vehicleId):
	mileage = None
	with MileageTable(DB_PATH) as db:
		mileage = db.findByVehicleId(vehicleId)
	
	destinations = None
	with DestinationsTable(DB_PATH) as db:
		destinations = db.findAll()

	providers = None
	with ProvidersTable(DB_PATH) as db:
		providers = db.findAll()

	destNameFromId = { x["id"] : x["name"] for x in destinations }
	providerNameFromId = { x["id"] : x["name"] for x in providers }

	for x in mileage:
		del x["id"]
		del x["vehicleId"]

		x["provider"] = providerNameFromId[x["providerId"]]
		del x["providerId"]

		x["destination"] = destNameFromId[x["destinationId"]]
		del x["destinationId"]

	return csvResponse(mileage, ["fromDate", "toDate", "totalMileage", "tripMileage", "gallons", "pricePerGallon", "provider", "destination"], "mileageExport.csv")

@application.route("/mileage/<mileageId>", methods=["GET"])
def findMileage(mileageId):
	with MileageTable(DB_PATH) as db:
		results = db.find(mileageId)
	return jsonify(results)

@application.route("/mileage/<mileageId>", methods=["DELETE"])
def removeMileage(mileageId):
	with MileageTable(DB_PATH) as db:
		results = db.remove(mileageId)
	return jsonify(results)

# Maintenance -----------------------------------------------------------------

@application.route("/maintenance", methods=["POST"])
def addOrUpdateMaintenance():
	with MaintenanceTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/maintenance", methods=["GET"])
def findAllMaintenance():
	with MaintenanceTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/maintenance", methods=["GET"])
def findMaintenanceByVehicleId(vehicleId):
	with MaintenanceTable(DB_PATH) as db:
		results = db.findByVehicleId(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/maintenance/csv", methods=["GET"])
def exportMaintenanceByVehicleId(vehicleId):
	maintenance= None
	with MaintenanceTable(DB_PATH) as db:
		maintenance = db.findByVehicleId(vehicleId)
	
	providers = None
	with ProvidersTable(DB_PATH) as db:
		providers = db.findAll()

	providerNameFromId = { x["id"] : x["name"] for x in providers }

	for x in maintenance:
		del x["id"]
		del x["vehicleId"]

		x["provider"] = providerNameFromId[x["providerId"]]
		del x["providerId"]

	return csvResponse(maintenance, ["at", "provider", "primaryContact", "phoneNumber", "cost", "description"], "maintenanceExport.csv")

@application.route("/maintenance/<maintenanceId>", methods=["GET"])
def findMaintenance(maintenanceId):
	with MaintenanceTable(DB_PATH) as db:
		results = db.find(maintenanceId)
	return jsonify(results)

@application.route("/maintenance/<maintenanceId>", methods=["DELETE"])
def removeMaintenance(maintenanceId):
	with MaintenanceTable(DB_PATH) as db:
		results = db.remove(maintenanceId)
	return jsonify(results)

# Events ----------------------------------------------------------------------

@application.route("/events", methods=["POST"])
def addOrUpdateEvent():
	with EventsTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/events", methods=["GET"])
def getEvents():
	with EventsTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/events", methods=["GET"])
def getEventsByVehicleId(vehicleId):
	with EventsTable(DB_PATH) as db:
		results = db.findByVehicleId(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/events/csv", methods=["GET"])
def exportEventsByVehicleId(vehicleId):
	events = None
	with EventsTable(DB_PATH) as db:
		events = db.findByVehicleId(vehicleId)

	for x in events:
		del x["id"]
		del x["vehicleId"]

	return csvResponse(events, ["at", "totalMileage", "description"], "eventsExport.csv")

@application.route("/events/<eventId>", methods=["GET"])
def getEvent(eventId):
	with EventsTable(DB_PATH) as db:
		results = db.find(eventId)
	return jsonify(results)

@application.route("/events/<eventId>", methods=["DELETE"])
def removeEvent(eventId):
	with EventsTable(DB_PATH) as db:
		results = db.remove(eventId)
	return jsonify(results)

# ProviderTypes ---------------------------------------------------------------

@application.route("/providerTypes", methods=["POST"])
def addOrUpdateProviderType():
	with ProviderTypesTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/providerTypes", methods=["GET"])
def getProviderTypes():
	with ProviderTypesTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/providerTypes/<providerTypeId>", methods=["GET"])
def getProviderType(providerTypeId):
	with ProviderTypesTable(DB_PATH) as db:
		results = db.find(providerTypeId)
	return jsonify(results)

@application.route("/providerTypes/<providerTypeId>", methods=["DELETE"])
def removeProviderType(providerTypeId):
	with ProviderTypesTable(DB_PATH) as db:
		results = db.remove(providerTypeId)
	return jsonify(results)

# Providers -------------------------------------------------------------------

@application.route("/providers", methods=["POST"])
def addOrUpdateProvider():
	with ProvidersTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/providers", methods=["GET"])
def findAllProviders():
	with ProvidersTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/providers/<providerId>", methods=["GET"])
def findProvider(providerId):
	with ProvidersTable(DB_PATH) as db:
		results = db.find(providerId)
	return jsonify(results)

@application.route("/providers/<providerId>", methods=["DELETE"])
def removeProvider(providerId):
	with ProvidersTable(DB_PATH) as db:
		results = db.remove(providerId)
	return jsonify(results)

# Destinations ----------------------------------------------------------------

@application.route("/destinations", methods=["POST"])
def addOrUpdateDestination():
	with DestinationsTable(DB_PATH) as db:
		results = db.add(request.get_json())
	return jsonify(results)

@application.route("/destinations", methods=["GET"])
def getDestinations():
	with DestinationsTable(DB_PATH) as db:
		results = db.findAll()
	return jsonify(results)

@application.route("/destinations/<destinationId>", methods=["GET"])
def getDestination(destinationId):
	with DestinationsTable(DB_PATH) as db:
		results = db.find(destinationId)
	return jsonify(results)

@application.route("/destinations/<destinationId>", methods=["DELETE"])
def removeDestination(destinationId):
	with DestinationsTable(DB_PATH) as db:
		results = db.remove(destinationId)
	return jsonify(results)

if __name__ == "__main__":
	if len(sys.argv) == 2:
		DB_PATH = sys.argv[1]
		if not os.path.isfile(DB_PATH):	
			with CarLogDB(DB_PATH) as db:
				db.createFromSchema("db/createDb.sql")
	else:
		if not os.path.isfile(DB_PATH):
			DB_PATH = "www/carLog.db"

	application.run()
