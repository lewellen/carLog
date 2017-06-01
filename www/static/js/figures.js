function mpgPpmFigure(canvasId, mileage) { 
	return new Chart(document.getElementById(canvasId), {
		type: "scatter",
		data: {
			datasets: [{
				data: mileage.map(function(entry) {
					if(entry.gallons == 0 || entry.tripMileage == 0) {
						return null;
					}
					return {
						x: new Date(entry.toDate), 
						y: round(entry.tripMileage / entry.gallons, 1)
					};
				}),
				label: "MPG",
				yAxisID: "mpgAxis",
				fill: false,
				borderColor: "rgba(0, 0, 0, 0)",
				backgroundColor: "#d00"
			}, {
				data: mileage.map(function(entry) {
					if(entry.tripMileage == 0) {
						return null;
					}
					return { 
						x: new Date(entry.toDate), 
						y: round((entry.gallons * entry.pricePerGallon) / entry.tripMileage, 3)
					};
				}),
				label: "PPM",
				yAxisID: "ppmAxis",
				fill: false,
				borderColor: "rgba(0, 0, 0, 0)",
				backgroundColor: "#00d"
			}]
		},
		options: {
			legend: {
				position: "bottom"
			},
			scales: {
				xAxes: [{
					type: "time",
					time: {
						unit: "year"
					},
					position: "bottom",
					scaleLabel: {
						display: true,
						labelString: "Date"
					},
					display: true
				}],
				yAxes: [{
					"id": "mpgAxis",
					position: "left",
					scaleLabel: {
						display: true,
						labelString: "MPG (mi/gal)"
					}
				}, {
					"id": "ppmAxis",
					position: "right",
					scaleLabel: {
						display: true,
						labelString: "PPM ($/mi)"
					}
				}]
			}
		}
	});
}

function daysBetweenFigure(canvasId, mileage) {
	deltas = mileage.map(function(entry) {
		var daysBetween = (new Date(entry.toDate) - new Date(entry.fromDate)) / 1000 / 60 / 60 / 24;
		var logDaysBetween = Math.log(daysBetween + 1.0) / Math.log(10.0);
		var rounded = round(logDaysBetween, 2);
		return rounded;
	});

	pairs = deltas.slice(0, -1).map(function(entry, idx) {
		return { x: entry, y: deltas[idx + 1] }
	});

	byDest = groupBy(pairs, function(x, i) { return mileage[i].destination.substring(0,3) });
	colorsByDest = getColorFromIdMap(byDest);

	datasets = [];
	for(var [key, value] of byDest) {
		datasets.push({
			data: value,
			fill: false,
			label: key,
			borderColor: "rgba(0, 0, 0, 0)",
			backgroundColor: colorsByDest.get(key),
			showLine: false
		});
	}

	return new Chart(document.getElementById(canvasId), {
		type: 'scatter',
		data: {
			datasets: datasets
		},
		options: {
			legend: {
				position: "bottom"
			},
			scales: {
				xAxes: [{
					position: "bottom",
					scaleLabel: {
						display: true,
						labelString: "log(Time since last refill)"
					}
				}],
				yAxes: [{
					position: "left",
					scaleLabel: {
						display: true,
						labelString: "log(Time until next refill)"
					}
				}]
			}
		}
	});
}

function annualTotalsByGroupChart(canvasId, entries, annualLabel, totalLabel, dateSelector, groupSelector, valueSelector) {
	var years = entries.map(dateSelector)
	var minYear = years.reduce(function(acc, x) { return Math.min(acc, x); }, Infinity);
	var maxYear = years.reduce(function(acc, x) { return Math.max(acc, x); }, -Infinity);
	var yearRange = range(minYear, maxYear + 1)
	
	var byGroup = groupBy(entries, groupSelector);
	byGroup = orderMapKeys(byGroup, ascComparator);

	var colorsByProvider = getColorFromIdMap(byGroup); 
	var dataByProviderByYear = []

	for(var [key, value] of byGroup) {
		var byYear = groupBy(value, dateSelector);
		byYear = mapMapValues(byYear, function(xs) { return xs.reduce(function(acc, y) { return acc + valueSelector(y); }, 0.0); });
		byYear = addMissingMapKeys(byYear, yearRange, 0.0);
		byYear = orderMapKeys(byYear, ascComparator);
		byYear = mapMapValues(byYear, function(x) { return round(x, 2); });

		dataByProviderByYear.push({
			label: key,
			data: Array.from(byYear.values()),
			borderColor: "rgba(0, 0, 0, 0)",
			backgroundColor: colorsByProvider.get(key)
		});
	}

	var totalByYear = groupBy(entries, dateSelector);
	totalByYear = mapMapValues(totalByYear, function(xs) { return xs.reduce(function(acc, y) { return acc + valueSelector(y); }, 0.0); });
	totalByYear = addMissingMapKeys(totalByYear, yearRange, 0.0);
	totalByYear = orderMapKeys(totalByYear, ascComparator);
	totalByYear = scanMap(totalByYear, function(acc, x) { return acc + x; }, 0.0);
	totalByYear = mapMapValues(totalByYear, function(x) { return round(x, 2); });

	dataByProviderByYear.push({
		type: "line",
		yAxisID: "totalYAxis",
		label: "Total",
		data: Array.from(totalByYear.values()),
		borderColor: "#999",
		backgroundColor: "#333",
		fill: false
	});

	new Chart(document.getElementById(canvasId).getContext("2d"), {
		type: 'bar',
		data: {
			labels: yearRange,
			datasets: dataByProviderByYear,
		},
		options: {
			legend: {
				position: "bottom"
			},
			scales: {
				xAxes: [{
					stacked: true,
					scaleLabel: {
						display: true,
						labelString: "Year"
					}	
				}],
				yAxes: [{
					"id": "annualYAxis",
					position: "left",
					stacked: true,
					scaleLabel: {
						display: true,
						labelString: annualLabel
					}
				},{
					"id": "totalYAxis",
					position: "right",
					scaleLabel: {
						display: true,
						labelString: totalLabel
					}
				}]
			}
		}
	})

}
