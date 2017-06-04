import datetime 
import operator
import sqlite3

import numpy
import scipy.stats
import scipy.stats.mstats

import matplotlib.cm as cm
import matplotlib.patches as mpatches
import matplotlib.pyplot as plot

#from sklearn.naive_bayes import GaussianNB
#from sklearn.model_selection import train_test_split
#from sklearn.metrics import confusion_matrix, accuracy_score

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

		self.ppd = map(lambda (x,y) : 0 if y == 0 else x / y, zip(self.extendedAmounts, self.daysBetween))

class Summarizer:
	def getSummary(self, dates, data):
		dateBins, dateTotals = self.groupByYear(dates, data)
		dateTotals = map(lambda x : dateTotals[x], dateBins)

		return {
			"total" : sum(dateTotals),
			"dateBins" : dateBins,
			"dateTotals" : dateTotals
		}

	def groupByYear(self, dates, data):
		print data
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
			id(self.data.daysBetween) : scipy.stats.gumbel_r,
			id(self.data.ppd) : scipy.stats.gumbel_r
		}

	def getBins(self, xs, numBins):
		assert numBins > 1

		if len(xs) == 0:
			return [], []

		xmin = min(xs)
		xmax = max(xs)
		xrng = xmax - xmin
		binSize = xrng / (numBins - 1)

		if binSize == 0:
			return [xmin], [ len(xs) ]

		binCenters = []
		for i in xrange(0, numBins):
			binCenters.append(xmin + binSize * i)

		binCounts = []
		for i in xrange(0, numBins):
			binCounts.append(0)

		for x in xs:
			xp = (x - xmin) / binSize
			binCounts[int(xp)] += 1

		return binCenters, binCounts

	def getParameters(self, xs):
		if id(xs) not in self.rvFromObj:
			return None

		alpha = 0.95
		length = len(xs)
		lb = int(round(0.5 * (1 - alpha) * length))
		ub = int(round(1 - 0.5 * (1 - alpha) * length))
		
		scipyRV = self.rvFromObj[id(xs)]
		loc, scale = scipyRV.fit(numpy.array(sorted(xs)[lb:ub]))
		interval = scipyRV.interval(alpha, loc, scale)
		#quantiles = scipy.stats.mstats.mquantiles(xs)
		#maximum = numpy.max(xs)

		return {
			"loc": loc,
			"scale": scale,
			"interval": interval,
		}

	def getPdf(self, xs, bins):
		if id(xs) not in self.rvFromObj:
			return None

		scipyRV = self.rvFromObj[id(xs)]
		loc, scale = scipyRV.fit(numpy.array(xs))
		return scipyRV.pdf(bins, loc, scale)

	def getSummary(self, xs, numBins):
		centers, counts = self.getBins(xs, numBins)
		params = self.getParameters(xs)
		ys = self.getPdf(xs, centers).tolist()

		return {
			"binCenters" : centers,
			"binCounts" : counts,
			"params" : params,
			"fit" : ys
		}

class Predictor:
	def __init__(self, mileageData):
		self.data = mileageData

	def guessDestination(self, newEntry):
		pass

#		minFromDate = min(self.data.fromDates)
#		dates = numpy.array(map(lambda x : (x - minFromDate).total_seconds() / 60 / 60 / 24, self.data.fromDates))

#		# time since prev event, time of event
#		features = numpy.column_stack((self.data.daysBetween, dates))

#		residuals = (newEntry["toDate"] - newEntry["fromDate"]).total_seconds() / 60 / 60 / 24
#		date = (newEntry["fromDate"] - minFromDate).total_seconds() / 60 / 60 / 24

#		model = GaussianNB()
#		model.fit(features, destinations)
#		predictY = model.predict(numpy.array([residual, date]))
#		return predictY[0]
