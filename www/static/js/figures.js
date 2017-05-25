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
