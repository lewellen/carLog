import datetime
import operator
import sqlite3

from validation import KeyValidator, DictValidator

class CarLogDB(object):
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

	def getResult(self, idValue = None, success = True, msg = None):
		return { "id" : idValue, "success" : success, "msg" : None if msg is None else repr(msg) }

	def strToDate(self, value):
		if value is None:
			return None
		try:
			return datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
		except ValueError:
			return datetime.datetime.strptime(value, "%Y-%m-%d")


class DriversTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(DriversTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"name" : operator.itemgetter(1)(result)
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, "Driver cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into drivers (name) values (?)", (entry["name"],))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, destinationId):
		c = self.conn.cursor()
		c.execute("select id, name from drivers where id = ?", (destinationId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, name from drivers")
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, entryId):
		try:
			c = self.conn.cursor()
			c.execute("delete from drivers where id = ?", (entryId,))
			self.conn.commit()
			return self.getResult(entryId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(entryId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, "Driver cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.add(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("update drivers set name = ? where id = ?", (entry["name"], entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

class VehiclesTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(VehiclesTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"driverId" : int(operator.itemgetter(1)(result)),
			"vin" : operator.itemgetter(2)(result),
			"make" : operator.itemgetter(3)(result),
			"model" : operator.itemgetter(4)(result),
			"year" : operator.itemgetter(5)(result),
			"stillOwn" : operator.itemgetter(6)(result)
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, False, "Vehicle cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		if "stillOwn" not in entry:
			entry["stillOwn"] = False 

		validator = DictValidator([
			KeyValidator(entry, "driverId").existsPositiveInteger(),
			KeyValidator(entry, "vin").existsNotNullShorterThan(256),
			KeyValidator(entry, "make").existsNotNullShorterThan(256),
			KeyValidator(entry, "model").existsNotNullShorterThan(256),
			KeyValidator(entry, "year").existsPositiveInteger(),
			KeyValidator(entry, "stillOwn").existsZeroOneBoolean()
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into vehicles (driverId, vin, make, model, year, stillOwn) values (?, ?, ?, ?, ?, ?)", (entry["driverId"], entry["vin"], entry["make"], entry["model"], entry["year"], entry["stillOwn"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, driverId, vin, make, model, year, stillOwn from vehicles where id = ?", (vehicleId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, driverId, vin, make, model, year, stillOwn from vehicles")
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def findByDriverId(self, driverId):
		c = self.conn.cursor()
		c.execute("select id, driverId, vin, make, model, year, stillOwn from vehicles where driverId = ?", driverId)
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, entryId):
		try:
			c = self.conn.cursor()
			c.execute("delete from vehicles where id = ?", (entryId,))
			self.conn.commit()
			return self.getResult(entryId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(entryId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, False, "Vehicle cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.update(entry)

		if "stillOwn" not in entry:
			entry["stillOwn"] = False 

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "driverId").existsPositiveInteger(),
			KeyValidator(entry, "vin").existsNotNullShorterThan(256),
			KeyValidator(entry, "make").existsNotNullShorterThan(256),
			KeyValidator(entry, "model").existsNotNullShorterThan(256),
			KeyValidator(entry, "year").existsPositiveInteger(),
			KeyValidator(entry, "stillOwn").existsZeroOneBoolean()
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("update vehicles set driverId = ?, vin = ?, make = ?, model = ?, year = ?, stillOwn = ? where id = ?", (entry["driverId"], entry["vin"], entry["make"], entry["model"], entry["year"], entry["stillOwn"], entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)


class MileageTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(MileageTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"vehicleId" : int(operator.itemgetter(1)(result)),
			"providerId" : int(operator.itemgetter(2)(result)),
			"destinationId" : int(operator.itemgetter(3)(result)),
			"fromDate": self.strToDate(operator.itemgetter(4)(result)),
			"toDate": self.strToDate(operator.itemgetter(5)(result)),
			"tripMileage": float(operator.itemgetter(6)(result)),
			"odometer" : float(operator.itemgetter(7)(result)),
			"gallons": float(operator.itemgetter(8)(result)),
			"pricePerGallon": float(operator.itemgetter(9)(result))
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, None, "Entry cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "providerId").existsPositiveInteger(),
			KeyValidator(entry, "destinationId").existsPositiveInteger(),
			KeyValidator(entry, "fromDate").exists().isNotNone(),
			KeyValidator(entry, "toDate").exists().isNotNone(),
			KeyValidator(entry, "tripMileage").existsPositiveInteger(),
			KeyValidator(entry, "odometer").existsPositiveInteger(),
			KeyValidator(entry, "gallons").existsPositiveInteger(),
			KeyValidator(entry, "pricePerGallon").existsPositiveInteger()
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, None, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into mileageEntries (vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, odometer, gallons, pricePerGallon) values (?, ?, ?, ?, ?, ?, ?, ?, ?)", (entry["vehicleId"], entry["providerId"], entry["destinationId"], entry["fromDate"], entry["toDate"], entry["tripMileage"], entry["odometer"], entry["gallons"], entry["pricePerGallon"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, None, e)

	def find(self, mileageId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, odometer, gallons, pricePerGallon from mileageEntries where id = ?", (mileageId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, odometer, gallons, pricePerGallon from mileageEntries")
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def findByVehicleId(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, odometer, gallons, pricePerGallon from mileageEntries where vehicleId = ?", (vehicleId,))
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, entryId):
		try:
			c = self.conn.cursor()
			c.execute("delete from mileageEntries where id = ?", (entryId,))
			self.conn.commit()
			return self.getResult(entryId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(entryId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, None, "Entry cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.add(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "providerId").existsPositiveInteger(),
			KeyValidator(entry, "destinationId").existsPositiveInteger(),
			KeyValidator(entry, "fromDate").exists().isNotNone(),
			KeyValidator(entry, "toDate").exists().isNotNone(),
			KeyValidator(entry, "tripMileage").existsPositiveInteger(),
			KeyValidator(entry, "odometer").existsPositiveInteger(),
			KeyValidator(entry, "gallons").existsPositiveInteger(),
			KeyValidator(entry, "pricePerGallon").existsPositiveInteger()
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, None, msg)

		try:
			c = self.conn.cursor()
			c.execute("update mileageEntries set vehicleId = ?, providerId = ?, destinationId = ?, fromDate = ?, toDate = ?, tripMileage = ?, odometer = ?, gallons = ?, pricePerGallon = ? where id = ?", (entry["vehicleId"], entry["providerId"], entry["destinationId"], entry["fromDate"], entry["toDate"], entry["tripMileage"], entry["odometer"], entry["gallons"], entry["pricePerGallon"], entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, None, e)

class MaintenanceTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(MaintenanceTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"vehicleId" : int(operator.itemgetter(1)(result)),
			"providerId" : int(operator.itemgetter(2)(result)),
			"at": self.strToDate(operator.itemgetter(3)(result)),
			"primaryContact" : operator.itemgetter(4)(result),
			"phoneNumber" : operator.itemgetter(5)(result),
			"description" : operator.itemgetter(6)(result),
			"cost" : operator.itemgetter(7)(result)
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, False, "Entry cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

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
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into maintenanceEntries (vehicleId, providerId, at, primaryContact, phoneNumber, description, cost) values (?, ?, ?, ?, ?, ?, ?)", (entry["vehicleId"], entry["providerId"], entry["at"], entry["primaryContact"], entry["phoneNumber"], entry["description"], entry["cost"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, maintenanceId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, at, primaryContact, phoneNumber, description, cost from maintenanceEntries where id = ?", (maintenanceId,) );
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, at, primaryContact, phoneNumber, description, cost from maintenanceEntries");
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def findByVehicleId(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, providerId, at, primaryContact, phoneNumber, description, cost from maintenanceEntries where vehicleId = ?", vehicleId);
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, maintenanceId):
		try:
			c = self.conn.cursor()
			c.execute("delete from maintenanceEntries where id = ?", (maintenanceId,))
			self.conn.commit()
			return self.getResult(maintenanceId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(maintenanceId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, "Entry cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.add(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
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
			return self.getResult(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("update maintenanceEntries set vehicleId = ?, providerId = ?, at = ?, primaryContact = ?, phoneNumber = ?, description = ?, cost = ? where id = ?", (entry["vehicleId"], entry["providerId"], entry["at"], entry["primaryContact"], entry["phoneNumber"], entry["description"], entry["cost"], entry["id"] ))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)


class EventsTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(EventsTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"vehicleId" : int(operator.itemgetter(1)(result)),
			"at": self.strToDate(operator.itemgetter(2)(result)),
			"odometer" : operator.itemgetter(3)(result),
			"description": operator.itemgetter(4)(result),
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, False, "Event cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "at").exists().isNotNone(),
			KeyValidator(entry, "odometer").exists(),
			KeyValidator(entry, "description").existsNullableShorterThan(256)
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into eventEntries (vehicleId, at, odometer, description) values (?, ?, ?, ?)", (entry["vehicleId"], entry["at"], entry["odometer"], entry["description"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, entryId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, at, odometer, description from eventEntries where id = ?", (entryId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, at, odometer, description from eventEntries")
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def findByVehicleId(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select id, vehicleId, at, odometer, description from eventEntries where vehicleId = ?", (vehicleId,))
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, entryId):
		try:
			c = self.conn.cursor()
			c.execute("delete from eventEntries where id = ?", (entryId,))
			rowsAffected = c.rowcount
			self.conn.commit()
			return self.getResult(entryId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(entryId, False, e)
		
	def update(self, entry):
		if entry is None:
			return self.getResult(None, False, "Event cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.add(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "vehicleId").existsPositiveInteger(),
			KeyValidator(entry, "at").exists().isNotNone(),
			KeyValidator(entry, "odometer").exists(),
			KeyValidator(entry, "description").existsNullableShorterThan(256)
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("update eventEntries set vehicleId = ?, at = ?, odometer = ?, description = ? where id = ?", (entry["vehicleId"], entry["at"], entry["odometer"], entry["description"], entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1,  None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

class ProviderTypesTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(ProviderTypesTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"name" : operator.itemgetter(1)(result)
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, "ProviderType cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into providerTypes (name) values (?)", (entry["name"],))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, destinationId):
		c = self.conn.cursor()
		c.execute("select id, name from providerTypes where id = ?", (destinationId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, name from providerTypes")
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, entryId):
		try:
			c = self.conn.cursor()
			c.execute("delete from providerTypes where id = ?", (entryId,))
			self.conn.commit()
			return self.getResult(entryId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(entryId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, "ProviderTypes cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.add(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("update providerTypes set name = ? where id = ?", (entry["name"],entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

class ProvidersTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(ProvidersTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"providerTypeId": int(operator.itemgetter(1)(result)),
			"name" : operator.itemgetter(2)(result),
			"address" : operator.itemgetter(3)(result)
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, False, "Provider cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "providerTypeId").existsPositiveInteger(),
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
			KeyValidator(entry, "address").existsNullableShorterThan(256)
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into providers (providerTypeId, name, address) values (?, ?, ?)", (entry["providerTypeId"], entry["name"], entry["address"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, providerId):
		c = self.conn.cursor()
		c.execute("select id, providerTypeId, name, address from providers where id = ?", (providerId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, providerTypeId, name, address from providers")
		results = c.fetchall()	
		return map(lambda x : self.__tupleToDict(x), results)

	def findByProviderTypeId(self, providerTypeId):
		c = self.conn.cursor()
		c.execute("select id, providerTypeId, name, address from providers where providerTypeId = ?", (providerTypeId,))
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, providerId):
		try:
			c = self.conn.cursor()
			c.execute("delete from providers where id = ?", (providerId,))
			self.conn.commit()
			return self.getResult(providerId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(providerId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, False, "Provider cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "providerTypeId").existsPositiveInteger(),
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
			KeyValidator(entry, "address").existsNullableShorterThan(256)
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, msg)

		try:
			c = self.conn.cursor()
			c.execute("update providers set providerTypeId = ?, name = ?, address = ? where id = ?", (entry["providerTypeId"], entry["name"], entry["address"], entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(entry["id"], False, e)

class DestinationsTable(CarLogDB):
	def __init__(self, sqlite3DbPath):
		super(DestinationsTable, self).__init__(sqlite3DbPath)

	def __tupleToDict(self, result):
		return {
			"id" : int(operator.itemgetter(0)(result)),
			"name" : operator.itemgetter(1)(result)
		}

	def add(self, entry):
		if entry is None:
			return self.getResult(None, "Destination cannot be empty.")

		if "id" in entry and int(entry["id"]) > 0:
			return self.update(entry)

		validator = DictValidator([
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("insert into destinations (name) values (?)", (entry["name"],))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)

	def find(self, destinationId):
		c = self.conn.cursor()
		c.execute("select id, name from destinations where id = ?", (destinationId,))
		result = c.fetchone()
		return self.__tupleToDict(result)

	def findAll(self):
		c = self.conn.cursor()
		c.execute("select id, name from destinations")
		results = c.fetchall()
		return map(lambda x : self.__tupleToDict(x), results)

	def remove(self, destinationId):
		try:
			c = self.conn.cursor()
			c.execute("delete from destinations where id = ?", (destinationId,))
			self.conn.commit()
			return self.getResult(destinationId, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(destinationId, False, e)

	def update(self, entry):
		if entry is None:
			return self.getResult(None, "Destination cannot be empty.")

		if "id" in entry and int(entry["id"]) < 0:
			return self.add(entry)

		validator = DictValidator([
			KeyValidator(entry, "id").existsPositiveInteger(),
			KeyValidator(entry, "name").existsNotNullShorterThan(256),
		])

		isValid, msg = validator.validate()
		if not isValid:
			return self.getResult(None, False, msg)

		try:
			c = self.conn.cursor()
			c.execute("update destinations set name = ? where id = ?", (entry["name"],entry["id"]))
			self.conn.commit()
			return self.getResult(c.lastrowid, c.rowcount == 1, None)
		except sqlite3.Error, e:
			return self.getResult(None, False, e)
