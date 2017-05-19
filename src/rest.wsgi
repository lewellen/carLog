from flask import Flask, jsonify

from dao import CarLogDB

application = Flask(__name__)

@application.route("/users")
def getUsers():
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllUsers()
	return jsonify(results)

@application.route("/user/<userId>/vehicles")
def getUserVehicles(userId):
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllUserVehicles(userId)
	return jsonify(results)

@application.route("/vehicles/<vehicleId>")
def getVehicle(vehicleId):
	return "foo"

@application.route("/vehicle/<vehicleId>/estimates")
def getVehicleEstimates(vehicleId):
	return "foo"

@application.route("/vehicle/<vehicleId>/mileage")
def getVehicleMileage(vehicleId):
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllVehicleMileage(vehicleId)
	return jsonify(results)

@application.route("/vehicle/<vehicleId>/maintenance")
def getVehicleMaintenance(vehicleId):
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllVehicleMaintenance(vehicleId)
	return jsonify(results)

@application.route("/vehicle/<vehicleId>/events")
def getVehicleEvents(vehicleId):
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllVehicleEvents(vehicleId)
	return jsonify(results)

@application.route("/providerTypes")
def getProviderTypes():
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllProviderTypes()
	return jsonify(results)

@application.route("/providers")
def getProviders():
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllProviders()
	return jsonify(results)

@application.route("/destinations")
def getDestinations():
	with CarLogDB("www/carLog.db") as db:
		results = db.getAllDestinations()
	return jsonify(results)

if __name__ == "__main__":
	application.run()
