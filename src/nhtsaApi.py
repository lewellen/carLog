import requests, json

class NHTSARestService:
	def __init__(self):
		self.baseURL = "https://vpic.nhtsa.dot.gov/api/"

	def decodeVin(self, vin, year):
		if vin is None or len(vin) <= 0:
			raise ValueError("vin must not be None or empty.")

		if int(year) < 0:
			raise ValueError("year must be positive integer.")

		queryString = "%s?format=%s&modelYear=%s" % (vin, "json", year)
		getURL = self.baseURL + "vehicles/DecodeVinValues/" + queryString

		response = requests.get(getURL)
		if response.status_code != requests.codes.ok:
			return False, None

		try:
			obj = response.json()
		except ValueError, e:
			print e
			print response.text
			return False, None

		if obj["Message"] != "Results returned successfully":
			return False, None

		pairs = obj["Results"][0]
		keys = pairs.keys()
		for key in keys:
			if pairs[key] is None or len(pairs[key]) <= 0:
				del pairs[key]

		return True, pairs
