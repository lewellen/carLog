import csv
import sys
import sqlite3
import datetime

def readFromCsv(csvPath):
	rows = []
	with open(csvPath, 'r') as csvFile:
		reader = csv.DictReader(csvFile)
		next(reader) # skip the header
		for row in reader:
			row["Start"] = datetime.datetime.strptime(row["Start"].strip(), "%m/%d/%Y")
			row["End"] = datetime.datetime.strptime(row["End"].strip(), "%m/%d/%Y")
			row["Distance"] = float(row["Distance"].strip().replace(",", ""))
			row["Total Dist"] = float(row["Total Dist"].strip().replace(",", ""))
			row["Fuel"] = float(row["Fuel"].strip().replace(",", ""))
			row["PPG"] = float(row["PPG"].strip().replace(",", "").replace("$", ""))
			row["Dest"] = row["Dest"].strip()
			rows.append(row)

	return rows

def uniqueDestinations(csvRows):
	return list(set(map(lambda x : x["Dest"], csvRows)))

def getAllDbDestinations(c):
	c.execute("select id, name from destinations")
	return { name : key for (key, name) in c.fetchall() }

def addMissingDestinations(c, csvDestinations):
	dbDestinations = getAllDbDestinations(c)
	csvDestinations = uniqueDestinations(csvRows)
	missingCsvDestinations = filter(lambda x : x not in dbDestinations, csvDestinations)
	c.executemany("insert into destinations (name) values (?)", 
		map(lambda x : (x,), missingCsvDestinations))

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("%s <sqlite3.db> <raw.csv>" % sys.argv[0])
		exit(1)

	sqlite3DbPath = sys.argv[1]
	conn = sqlite3.connect(sqlite3DbPath)
	c = conn.cursor()

	csvPath = sys.argv[2]
	csvRows = readFromCsv(csvPath)

	addMissingDestinations(c, uniqueDestinations(csvRows))
	dbDestinations = getAllDbDestinations(c)	

	entries = []
	for row in csvRows:
		entries.append(
			(1, 1, dbDestinations[row["Dest"]], row["Start"], row["End"], row["Distance"], row["Total Dist"], row["Fuel"], row["PPG"])
		)

	c.executemany('insert into mileageEntries (vehicleId, providerId, destinationId, fromDate, toDate, tripMileage, odometer, gallons, pricePerGallon) values (?, ?, ?, ?, ?, ?, ?, ?, ?)', entries)
	conn.commit()
	conn.close()
