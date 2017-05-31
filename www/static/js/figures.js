function mpgPpmFigure(canvasId, mileage) {
	return new Chart(document.getElementById(canvasId), {
		type: 'line',
		data: {
			labels: mileage.map(function(entry) {
				return new Date(entry.toDate);
			}),
			datasets: [{
				data: mileage.map(function(entry) {
					if(entry.gallons == 0) {
						return null;
					}
					return Math.round(10.0 * entry.tripMileage / entry.gallons) / 10.0;
				}),
				label: "MPG",
				yAxisID: "mpgAxis",
				fill: false,
				borderColor: "#f00",
				backgroundColor: "#d00"
			}, {
				data: mileage.map(function(entry) {
					if(entry.tripMileage == 0) {
						return null;
					}
					return Math.round( 1000.0 * (entry.gallons * entry.pricePerGallon) / entry.tripMileage) / 1000.0;
				}),
				label: "PPM",
				yAxisID: "ppmAxis",
				fill: false,
				borderColor: "#00f",
				backgroundColor: "#00d"
			}]
		},
		options: {
			scales: {
				xAxes: [{
					time: [{
						unit: 'month'
					}],
					position: "bottom",
					scaleLabel: {
						display: true,
						labelString: "Date"
					},
					display: false
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
	// Calculate time between events
	deltas = mileage.map(function(entry) { 
		var daysBetween = (new Date(entry.toDate) - new Date(entry.fromDate)) / 1000 / 60 / 60 / 24;
		var logDaysBetween = Math.log(daysBetween)
		var rounded = Math.round(10 * logDaysBetween) / 10.0
		return rounded
	});

	// produce data set
	pairs = deltas.slice(0, -1).map(function(entry, idx) {
		return {
			x: entry,
			y: deltas[idx + 1]
		}
	});

	// Group by destination
	byDest = new Map()
	for(var i = 0, len = pairs.length; i < len; ++i) {
		destId = mileage[i].destinationId
		if(!byDest.has(destId)) {
			byDest.set(destId, [])
		}
		byDest.get(destId).push(pairs[i]);
	}

	indexFromDest = new Map()
	var index = 0
	for(var key of byDest.keys()) {
		indexFromDest.set(key, index)
		++index
	}

	// Generate colors for each destination
	colorsByDest = new Map()
	for(var key of byDest.keys()) {
		var percent = 100.0 * indexFromDest.get(key) / (1.0 * byDest.size)
		var color = tinycolor("hsl(" + percent + "%, 60%, 50%)")
		console.log(color.toHexString())
		colorsByDest.set(key, color.toHexString())
	}

	datasets = []
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
