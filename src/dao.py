import datetime
import operator
import sqlite3

from validation import KeyValidator, DictValidator

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

	def createFromSchema(self, path):
		with open(path) as f:
			self.conn.cursor().executescript(f.read())
		self.conn.commit() 

	def __addReturn(self, idValue, msg):
		return { "id" : idValue, "msg" : repr(msg) }

	def strToDate(self, value):
		if value is None:
			return None

		try:
			return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
		except ValueError:
			return datetime.datetime.strptime(value, "%Y-%m-%d")

	def addUser(self, user):
		if user is None:
			return self.__addReturn(None, "User cannot be empty.")

		validator = DictValidator([
			KeyValidator(user, "name").existsNotNullShorterThan(256) 
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into users (name) values (?)", (user["name"],) )
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	def addVehicle(self, vehicle):
		if vehicle is None:
			return self.__addReturn(None, "Vehicle cannot be empty.")

		validator = DictValidator([
			KeyValidator(vehicle, "userId").existsPositiveInteger(),
			KeyValidator(vehicle, "vin").existsNotNullShorterThan(256),
			KeyValidator(vehicle, "make").existsNotNullShorterThan(256),
			KeyValidator(vehicle, "model").existsNotNullShorterThan(256),
			KeyValidator(vehicle, "year").existsPositiveInteger(),
			KeyValidator(vehicle, "stillOwn").existsZeroOneBoolean()
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into vehicles (userId, vin, make, model, year, stillOwn) values (?, ?, ?, ?, ?, ?)", (vehicle["userId"], vehicle["vin"], vehicle["make"], vehicle["model"], vehicle["year"], vehicle["stillOwn"]))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	def addProviderType(self, providerType):
		if providerType is None:
			return self.__addReturn(None, "ProviderType cannot be empty.")

		validator = DictValidator([
			KeyValidator(providerType, "name").existsNotNullShorterThan(256),
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into providerTypes (name) values (?)", (providerType["name"],))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	
	def addProvider(self, provider):
		if provider is None:
			return self.__addReturn(None, "Provider cannot be empty.")

		validator = DictValidator([
			KeyValidator(provider, "providerTypeId").existsPositiveInteger(),
			KeyValidator(provider, "name").existsNotNullShorterThan(256),
			KeyValidator(provider, "address").existsNullableShorterThan(256),
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into providers (providerTypeId, name, address) values (?, ?, ?)", (provider["providerTypeId"], provider["name"], provider["address"]))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	def addDestination(self, destination):
		if destination is None:
			return self.__addReturn(None, "Destination cannot be empty.")

		validator = DictValidator([
			KeyValidator(destination, "name").existsNotNullShorterThan(256),
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into destinations (name) values (?)", (destination["name"],))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	def addMileageEntry(self, entry):
		if entry is None:
			return self.__addReturn(None, "Entry cannot be empty.")

		validator = DictValidator([
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "providerId").existsPositiveInteger(),
			KeyValidator(entry, "destinationId").existsPositiveInteger(),
			KeyValidator(entry, "fromDate").exists().isNotNone(),
			KeyValidator(entry, "toDate").exists().isNotNone(),
			KeyValidator(entry, "tripMileage").existsPositiveInteger(),
			KeyValidator(entry, "totalMileage").existsPositiveInteger(),
			KeyValidator(entry, "gallons").existsPositiveInteger(),
			KeyValidator(entry, "pricePerGallon").existsPositiveInteger()
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into mileageEntries (vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, totalMileage, gallons, pricePerGallon) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (entry["vehicleId"], entry["providerId"], entry["destinationId"], entry["fromDate"], entry["toDate"], entry["tripMileage"], entry["totalMileage"], entry["gallons"], entry["pricePerGallon"]))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	def addMaintenanceEntry(self, entry):
		if entry is None:
			return self.__addReturn(None, "Entry cannot be empty.")

		validator = DictValidator([
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "providerId").existsPositiveInteger(),
			KeyValidator(entry, "at").exists().isNotNone(),
			KeyValidator(entry, "primaryContact").existsNullableShorterThan(256),
			KeyValidator(entry, "phoneNumber").existsNullableShorterThan(256),
			KeyValidator(entry, "description").existsNotNullShorterThan(256),
			KeyValidator(entry, "cost").existsPositiveInteger()
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into maintenanceEntries (vehicleId, providerId, at, primaryContact, phoneNumber, description, cost) values (?, ?, ?, ?, ?, ?, ?)", (entry["vehicleId"], entry["providerId"], entry["at"], entry["primaryContact"], entry["phoneNumber"], entry["description"], entry["cost"]))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

	def addEventEntry(self, entry):
		if entry is None:
			return self.__addReturn(None, "Entry cannot be empty.")

		validator = DictValidator([
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "at").exists().isNotNone(),
			KeyValidator(entry, "totalMileage").exists(),
			KeyValidator(entry, "description").existsNullableShorterThan(256)
		])
		isValid, msg = validator.validate()
		if not isValid:
			return self.__addReturn(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into eventEntries (vehicleId, at, totalMileage, description) values (?, ?, ?, ?)", (entry["vehicleId"], entry["at"], entry["totalMileage"], entry["description"]))
			self.conn.commit()
			return self.__addReturn(c.lastrowid, None)
		except sqlite3.Error, e:
			return self.__addReturn(None, e)

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
				"at": self.strToDate(operator.itemgetter(3)(result)),
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
				"fromDate": self.strToDate(operator.itemgetter(4)(result)),
				"toDate": self.strToDate(operator.itemgetter(5)(result)),
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
				"at": self.strToDate(operator.itemgetter(2)(result)),
				"totalMileage" : operator.itemgetter(3)(result),
				"description": operator.itemgetter(4)(result),
			})

		return data
