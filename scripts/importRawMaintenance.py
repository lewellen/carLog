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
			if row["Date"] == "???":
				row["Date"] = datetime.datetime(1, 1, 1)
			else:
				row["Date"] = datetime.datetime.strptime(row["Date"].strip(), "%m/%d/%y")

			row["Event"] = row["Event"].strip()
			rows.append(row)

	return rows

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("%s <sqlite3.db> <raw.csv>" % sys.argv[0])
		exit(1)

	sqlite3DbPath = sys.argv[1]
	conn = sqlite3.connect(sqlite3DbPath)
	c = conn.cursor()

	csvPath = sys.argv[2]
	csvRows = readFromCsv(csvPath)

	entries = []
	for row in csvRows:
		entries.append(
			(1, 1, row["Date"], row["Event"])
		)

	c.executemany('insert into maintenanceEntries (vehicleId, providerId, at, description) values (?, ?, ?, ?)', entries)
	conn.commit()
	conn.close()
