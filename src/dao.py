import datetime
import operator
import sqlite3

class CarLogDB:
	def __init__(self, sqlite3DbPath):
		self.sqlite3DbPath = sqlite3DbPath
		self.conn = None

	def __enter__(self):
		self.open()
		return self

	def __exit__(self, exceptionType, exceptionValue, stackTrace):
		self.close()

	def open(self):
		if self.conn is None:
			self.conn = sqlite3.connect(self.sqlite3DbPath)

	def close(self):
		if self.conn is not None:
			self.conn.close();
			self.conn = None

	def getAllUsers(self):
		c = self.conn.cursor()
		c.execute("select id, name from users")
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"name" : operator.itemgetter(1)(result),
			})

		return data

	def getAllUserVehicles(self, userId):
		c = self.conn.cursor()
		c.execute("select id, userId, vin, make, model, year, stillOwn from vehicles where userId = ?", userId)
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"userId" : int(operator.itemgetter(1)(result)),
				"vin" : operator.itemgetter(2)(result),
				"make" : operator.itemgetter(3)(result),
				"model" : operator.itemgetter(4)(result),
				"year" : operator.itemgetter(5)(result),
				"stillOwn" : operator.itemgetter(6)(result)
			})

		return data

	def getAllProviderTypes(self):
		c = self.conn.cursor()
		c.execute("select id, name from providerTypes")
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"name" : operator.itemgetter(1)(result),
			})

		return data

	def getAllProviders(self):
		c = self.conn.cursor()
		c.execute("select id, providerTypeId, name, address from providers")
		results = c.fetchall()
		
		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"providerTypeId": int(operator.itemgetter(1)(result)),
				"name" : operator.itemgetter(2)(result),
				"address" : operator.itemgetter(3)(result)
			})

		return data

	def getAllDestinations(self):
		c = self.conn.cursor()
		c.execute("select id, name from destinations")
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"name" : operator.itemgetter(1)(result),
			})

		return data

	def getAllVehicleMaintenance(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, at, primaryContact, phoneNumber, description, cost from maintenanceEntries where vehicleId = ?", vehicleId);
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"vehicleId" : int(operator.itemgetter(1)(result)),
				"providerId" : int(operator.itemgetter(2)(result)),
				"at": datetime.datetime.strptime(operator.itemgetter(3)(result), "%Y-%m-%d %H:%M:%S"),
				"primaryContact" : operator.itemgetter(4)(result),
				"phoneNumber" : operator.itemgetter(5)(result),
				"description" : operator.itemgetter(6)(result),
				"cost" : operator.itemgetter(7)(result)
			})

		return data

	def getAllVehicleMileage(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, totalMileage, gallons, pricePerGallon from mileageEntries where vehicleId = ?", vehicleId)
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"vehicleId" : int(operator.itemgetter(1)(result)),
				"providerId" : int(operator.itemgetter(2)(result)),
				"destinationId" : int(operator.itemgetter(3)(result)),

				"fromDate": datetime.datetime.strptime(operator.itemgetter(4)(result), "%Y-%m-%d %H:%M:%S"),
				"toDate": datetime.datetime.strptime(operator.itemgetter(5)(result), "%Y-%m-%d %H:%M:%S"),
				"tripMileage": float(operator.itemgetter(6)(result)),
				"totalMileage" : float(operator.itemgetter(7)(result)),
				"gallons": float(operator.itemgetter(8)(result)),
				"pricePerGallon": float(operator.itemgetter(9)(result))
			})

		return data

	def getAllVehicleEvents(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, at, totalMileage, description from eventEntries where vehicleId = ?", vehicleId)
		results = c.fetchall()

		data = []
		for result in results:
			data.append({
				"id" : int(operator.itemgetter(0)(result)),
				"vehicleId" : int(operator.itemgetter(1)(result)),

				"at": datetime.datetime.strptime(operator.itemgetter(2)(result), "%Y-%m-%d %H:%M:%S"),
				"totalMileage" : operator.itemgetter(3)(result),
				"description": operator.itemgetter(4)(result),
			})

		return data
