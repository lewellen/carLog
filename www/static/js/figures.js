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
				borderColor: "#f00",
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
				borderColor: "#00f",
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

	byDest = groupBy(pairs, function(x, i) { return mileage[i].destination });
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
