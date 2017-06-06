function tileBarChart(canvasEl, def) {
	var ctx = canvasEl.getContext("2d")
	var chart = new Chart(ctx, {
		type: 'bar',
		data : {
			labels: def.binCenters.map(function(x) {
				return round(x, def.numDigits)
			}),
			datasets: [{
				data : def.binCounts,
				yAxisID : "freqYAxis",
				borderColor: "#333",
				backgroundColor: "#999"
			}, {
				type : 'line',
				data : def.fit,
				yAxisID : "fitYAxis",
				borderColor: "#f00",
				fill: false,
				pointRadius: 0
			}]
		},
		options : {
			legend: {
				display: false
			},
			scales: {
				xAxes: [{
					gridLines: {
						display: false
					},
					scaleLabel: {
						labelString: def.xLabel,
						display: true
					}
				}],
				yAxes: [{
					"id" : "freqYAxis",
					position: "left",
					scaleLabel: {
						labelString: def.yLabel,
						display: true
					}
				}, {
					"id" : "fitYAxis",
					position: "right",
					display: false
				}]
			}
		}
	});
}

function populateCostSummaryTile(clone, data, heading) {
	data.total = round(data.total, 2);

	for(var i = 0; i < data.dateTotals.length; ++i) {
		data.dateTotals[i] = round(data.dateTotals[i], 2)
	}

	clone.querySelector("#heading").innerHTML = heading;
	clone.querySelector("#total").innerHTML = "$" + data.total;

	tileBarChart(clone.querySelector("#chart"), {
		binCenters: data.dateBins,
		binCounts: data.dateTotals,
		numDigits: 0,
		xLabel: "Date",
		yLabel: "Total ($)"
	});
}

function populateEstimateTile(clone, data, heading, unit, numDigits) {
	data.params.loc = round(data.params.loc, numDigits);
	data.params.interval[0] = round(data.params.interval[0], numDigits);
	data.params.interval[1] = round(data.params.interval[1], numDigits);

	clone.querySelector("#heading").innerHTML = heading;
	clone.querySelector("#mean").innerHTML = data.params.loc;
	clone.querySelector("#confidenceInterval").innerHTML = "95% CI: " + data.params.interval[0] + " - " + data.params.interval[1];
	clone.querySelector("#unit").innerHTML = unit;

	tileBarChart(clone.querySelector("#chart"), {
		binCenters: data.binCenters,
		binCounts: data.binCounts,
		fit : data.fit,
		numDigits: numDigits,
		xLabel: heading + " " + unit,
		yLabel: "Frequency"
	});
}

$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");
	var params = new URLSearchParams(document.location.search);
	var vehicleId = params.get("id");

	$.ajax({
		method : "GET",
		url : "/rest/vehicles/" + vehicleId + "/costSummary",
		success : function(results) {
			tileIds = ["#fuelCostSummary", "#maintenanceCostSummary"];
			headings = ["Fuel", "Maintenance"]
			data = [results.fuel, results.maintenance];

			for(var i = 0; i < 2; ++i) {
				var template = document.querySelector("#summaryTile-template")
				var placeholder = document.querySelector(tileIds[i])
				var clone = document.importNode(template.content, true)
				populateCostSummaryTile(clone, data[i], headings[i]);
				placeholder.appendChild(clone)
			}
		},
		fail: function(results) {
			pageNotifier.error("Failed to load vehicle cost summaries.");
		}
	});

	$.ajax({
		method : "GET",
		url : "/rest/vehicles/" + vehicleId + "/estimates",
		success : function(results) {
			tileIds = ["#tankSize", "#mpg", "#range", "#ppm", "#fuelCosts", "#ppd"];
			data = [results.tank, results.mpg, results.range, results.ppm, results.fuelCosts, results.ppd];
			headings = ["Refill", "Fuel Economy", "Range", "Price Per Mile", "Refill Cost", "Price Per Day"]
			units = ["(gal)", "(mi/gal)", "(mi)", "($/mi)", "($)", "($/day)"]
			numDigits = [ 1, 1, 1, 3, 2, 2];

			for(var i = 0; i < 6; ++i) { 
				var template = document.querySelector("#estimateTile-template")
				var placeholder = document.querySelector(tileIds[i])
				var clone = document.importNode(template.content, true)
				populateEstimateTile(clone, data[i], headings[i], units[i], numDigits[i])
				placeholder.appendChild(clone)
			}
		},
		fail: function(results) {
			pageNotifier.error("Failed to lost vehicle estimates.");
		}
	});
});
