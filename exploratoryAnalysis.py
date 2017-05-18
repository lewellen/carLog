import datetime 
import operator
import sqlite3

import numpy
import scipy.stats
import scipy.stats.mstats

import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plot

from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score

class CarLogDB:
	def __init__(self, sqlite3DbPath):
		self.conn = sqlite3.connect(sqlite3DbPath)

	def close(self):
		self.conn.close();

	def getAllMileageByVehicleId(self, vehicleId):
		c = self.conn.cursor()
		c.execute("select fromDate, toDate, tripMileage, totalMileage, gallons, pricePerGallon, destinationId from mileageEntries where vehicleId = 1");
		results = c.fetchall()

		data = []
		for result in results:
		    data.append({
			"fromDate": datetime.datetime.strptime(operator.itemgetter(0)(result), "%Y-%m-%d %H:%M:%S"),
			"toDate": datetime.datetime.strptime(operator.itemgetter(1)(result), "%Y-%m-%d %H:%M:%S"),
			"tripMileage": float(operator.itemgetter(2)(result)),
			"totalMileage" : float(operator.itemgetter(3)(result)),
			"gallons": float(operator.itemgetter(4)(result)),
			"pricePerGallon": float(operator.itemgetter(5)(result)),
			"destinationId" : operator.itemgetter(6)(result)
		    })

		return data

	def getAllDestinations(self):
		c = self.conn.cursor()		
		c.execute("select id, name from destinations")
		results = c.fetchall()
		nameFromDestId = { i : name for (i, name) in results }
		return nameFromDestId

class MileageData:
	def __init__(self, mileageEntries):
		data = mileageEntries

		# Base quantites
		self.fromDates = map(lambda x : x["fromDate"], data)
		self.toDates = map(lambda x : x["toDate"], data)
		self.tripMileage = map(lambda x : x["tripMileage"], data)
		self.gallons = map(lambda x : x["gallons"], data)
		self.pricePerGallon = map(lambda x : x["pricePerGallon"], data)
		self.destinationIds = map(lambda x : x["destinationId"], data)

		# Derived quantites
		self.extendedAmounts = map(lambda x : x["pricePerGallon"] * x["gallons"], data)
		self.mpg = map(lambda x : x["tripMileage"] / x["gallons"], data)

		nonZeroMileage = filter(lambda x : x["tripMileage"] > 0, data)
		costs = map(lambda (x, y) : x["pricePerGallon"] * y["gallons"], zip(nonZeroMileage, nonZeroMileage[1:]))
		self.ppm = map(lambda (x, y) : y / x["tripMileage"], zip(nonZeroMileage[1:], costs))

		self.daysBetween = map(lambda x : x.total_seconds() / 60 / 60 / 24, (numpy.array(self.toDates) - numpy.array(self.fromDates)))

class Summarizer:
	def __init__(self, mileageData):
		self.data = mileageData

	def groupByYear(self, dates, data):
		dateBins = range(min(dates).year, max(dates).year + 1)
		annualData = { dateBin : 0 for dateBin in dateBins }
		for (d, x) in zip(dates, data):
		    annualData[d.year] += x
		return dateBins, annualData

class Estimator:
	def __init__(self, mileageData):
		self.data = mileageData

		self.rvFromObj = {
			id(self.data.tripMileage) : scipy.stats.gumbel_l, 
			id(self.data.gallons) : scipy.stats.gumbel_l, 
			id(self.data.extendedAmounts) : scipy.stats.gumbel_l, 
			id(self.data.mpg) : scipy.stats.norm, 
			id(self.data.ppm) : scipy.stats.norm, 
			id(self.data.daysBetween) : scipy.stats.gumbel_r
		}
 
	def getParameters(self, xs):
		if id(xs) not in self.rvFromObj:
			return None

		scipyRV = self.rvFromObj[id(xs)]
		loc, scale = scipyRV.fit(numpy.array(xs))
		interval = scipyRV.interval(0.95, loc, scale)
		quantiles = scipy.stats.mstats.mquantiles(xs)
		maximum = numpy.max(xs)

		return {
			"loc": loc,
			"scale": scale,
			"interval": interval,
			"quantiles": quantiles,
			"maximum": maximum
		}

	def getPdf(self, xs, bins):
		if id(xs) not in self.rvFromObj:
			return None

		scipyRV = self.rvFromObj[id(xs)]
		loc, scale = scipyRV.fit(numpy.array(xs))
		return scipyRV.pdf(bins, loc, scale)

class Predictor:
	def __init__(self, mileageData):
		self.data = mileageData

	def guessDestination(self, newEntry):

		minFromDate = min(self.data.fromDates)
		dates = numpy.array(map(lambda x : (x - minFromDate).total_seconds() / 60 / 60 / 24, self.data.fromDates))

		# time since prev event, time of event
		features = numpy.column_stack((self.data.daysBetween, dates))

		residuals = (newEntry["toDate"] - newEntry["fromDate"]).total_seconds() / 60 / 60 / 24
		date = (newEntry["fromDate"] - minFromDate).total_seconds() / 60 / 60 / 24

		model = GaussianNB()
		model.fit(features, destinations)
		predictY = model.predict(numpy.array([residual, date]))
		return predictY[0]
