import sys
import os.path

from flask import Flask, request, jsonify
from dao import CarLogDB

DB_PATH = "/var/www/carLog/carLog.db"

application = Flask(__name__)

# Users -----------------------------------------------------------------------

@application.route("/users", methods=["POST"])
def addUser():
	with CarLogDB(DB_PATH) as db:
		results = db.addUser(request.get_json())
	return jsonify(results)

@application.route("/users", methods=["GET"])
def getUsers():
	with CarLogDB(DB_PATH) as db:
		results = db.getAllUsers()
	return jsonify(results)

@application.route("/users/<userId>/vehicles", methods=["GET"])
def getUserVehicles(userId):
	with CarLogDB(DB_PATH) as db:
		results = db.getAllUserVehicles(userId)
	return jsonify(results)

# Vehicles --------------------------------------------------------------------

@application.route("/vehicles", methods=["POST"])
def addVehicle():
	with CarLogDB(DB_PATH) as db:
		results = db.addVehicle(request.get_json())
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/estimates", methods=["GET"])
def getVehicleEstimates(vehicleId):
	return "foo"

@application.route("/vehicles/<vehicleId>/mileage", methods=["GET"])
def getVehicleMileage(vehicleId):
	with CarLogDB(DB_PATH) as db:
		results = db.getAllVehicleMileage(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/maintenance", methods=["GET"])
def getVehicleMaintenance(vehicleId):
	with CarLogDB(DB_PATH) as db:
		results = db.getAllVehicleMaintenance(vehicleId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>/events", methods=["GET"])
def getVehicleEvents(vehicleId):
	with CarLogDB(DB_PATH) as db:
		results = db.getAllVehicleEvents(vehicleId)
	return jsonify(results)

# Mileage ---------------------------------------------------------------------

@application.route("/mileage", methods=["POST"])
def addMileage():
	with CarLogDB(DB_PATH) as db:
		results = db.addMileageEntry(request.get_json())
	return jsonify(results)

# Maintenance -----------------------------------------------------------------

@application.route("/maintenance", methods=["POST"])
def addMaintenance():
	with CarLogDB(DB_PATH) as db:
		results = db.addMaintenanceEntry(request.get_json())
	return jsonify(results)

# Events ----------------------------------------------------------------------

@application.route("/events", methods=["POST"])
def addEvent():
	with CarLogDB(DB_PATH) as db:
		results = db.addEventEntry(request.get_json())
	return jsonify(results)

# ProviderTypes ---------------------------------------------------------------

@application.route("/providerTypes", methods=["POST"])
def addProviderType():
	with CarLogDB(DB_PATH) as db:
		results = db.addProviderType(request.get_json())
	return jsonify(results)

@application.route("/providerTypes", methods=["GET"])
def getProviderTypes():
	with CarLogDB(DB_PATH) as db:
		results = db.getAllProviderTypes()
	return jsonify(results)

# Providers -------------------------------------------------------------------

@application.route("/providers", methods=["POST"])
def addProvider():
	with CarLogDB(DB_PATH) as db:
		results = db.addProvider(request.get_json())
	return jsonify(results)

@application.route("/providers", methods=["GET"])
def getProviders():
	with CarLogDB(DB_PATH) as db:
		results = db.getAllProviders()
	return jsonify(results)

# Destinations ----------------------------------------------------------------

@application.route("/destinations", methods=["POST"])
def addDestination():
	with CarLogDB(DB_PATH) as db:
		results = db.addDestination(request.get_json())
	return jsonify(results)

@application.route("/destinations", methods=["GET"])
def getDestinations():
	with CarLogDB(DB_PATH) as db:
		results = db.getAllDestinations()
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
