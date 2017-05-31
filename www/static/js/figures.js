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

function mileageFigure(canvasId, mileage) {
	pairs = mileage.map(function(entry, idx) {
		if(entry.odometer == 0) {
			return null;
		}
		return {
			x: new Date(entry.toDate),
			y: entry.odometer
		};
	});

	byDest = groupBy(pairs, function(x, i) { return mileage[i].destination.substring(0,3) });
	colorsByDest = getColorFromIdMap(byDest);

	byYear = groupBy(mileage, function(entry) { return new Date(entry.toDate).getFullYear() } )
	for(var [key, value] of byYear) {
		byYear.set(key, round(value.reduce(function(acc, x) { return acc + x.tripMileage}, 0), 1))
	}

	byYearScatter = []
	for(var [key, value] of byYear) {
		console.log(key)
		byYearScatter.push({ x: new Date(key, 11, 31), y: value})
	}

	console.log(byYearScatter)

	datasets = [];
	datasets.push({
		data: byYearScatter,
		yAxisID: "annualTripYAxis",
		label: "Annual",
		borderColor: "rgba(0, 0, 0, 0)",
		backgroundColor: "#333",
		fill: false
	});

	for(var [key, value] of byDest) {
		datasets.push({
			data: value.filter(function(x) { return x != null }),
			yAxisID: "odometerYAxis",
			label: key,
			borderColor: "rgba(0, 0, 0, 0)",
			backgroundColor: colorsByDest.get(key),
			fill: false,
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
					type: "time",
					time: {
						unit: "year"
					},
					position: "bottom",
					scaleLabel: {
						display: true,
						labelString: "Date"
					}
				}],
				yAxes: [{
					"id" : "odometerYAxis",		
					position: "left",
					scaleLabel: {
						display: true,
						labelString: "Odometer (mi)"
					}
				},{
					"id" : "annualTripYAxis",
					position: "right",
					scaleLabel: {
						display: true,
						labelString: "Annual Trip (mi)"
					}
				}]
			}
		}
	});
}
