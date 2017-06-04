function mileageFigure(canvasId, mileage) {
	annualTotalsByGroupChart(
		canvasId, mileage, "Annual Mileage (mi)", "Total Mileage (mi)",
		function(x) { return new Date(x.fromDate).getFullYear(); },
		function(x) { return x.destination; },
		function(x) { return x.tripMileage; }
		);
}

function costFigure(canvasId, mileage) {
	annualTotalsByGroupChart(
		canvasId, mileage, "Annual Cost ($)", "Total Cost ($)",
		function(x) { return new Date(x.fromDate).getFullYear(); },
		function(x) { return x.provider; },
		function(x) { return x.gallons * x.pricePerGallon; }
		);
}

function daysBetweenRefillsByDestination(canvasId, mileage) {
	timeMapChart(canvasId, mileage, "Refill",
		function(x) { return new Date(x.toDate); },
		function(x) { return x.destination; }
		);
}

$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	$("#charts").slick({
		dots: true,
		infinite: true,
	});

	var params = new URLSearchParams(document.location.search)
	var vehicleId = params.get("id")
	$("#vehicleMenu").find("a").each(function(){
		$(this).attr("href", $(this).attr("href") + "?id=" + vehicleId)
	});

	bindAdd("#mileageForm", "/rest/mileage", {
		id : -1,
		toDate : toISO8601DateStr(new Date()),
		fromDate : toISO8601DateStr(new Date()),
		tripMileage : 0,
		odometer : 0,
		gallons : 0,
		pricePerGallon : 0,
		vehicleId : vehicleId 
	});

	$("#exportCSV").attr("href", "/rest/vehicles/" + vehicleId + "/mileage/csv")

	$.ajax({
		url : "rest/providers",
		timeout: 3000,
		success : function(providers) {
			new Vue({
				el: "#providerId",
				data : { entries : providers }
			});

			$.ajax({
				url : "rest/destinations",
				timeout: 3000,
				success : function(destinations) {
					new Vue({
						el: "#destinationId",
						data : { entries : destinations }
					});

					$.ajax({
						url: "/rest/vehicles/" + vehicleId + "/mileage",
						timeout: 3000,
						success : function(mileage) {
							substitute(mileage, "destination", (x) => x.destinationId, destinations, (x) => x.id, (x) => x.name);
							substitute(mileage, "provider", (x) => x.providerId, providers, (x) => x.id, (x) => x.name);

							mileageFigure("mileageChart", mileage);
							costFigure("costChart", mileage);
							mpgPpmFigure("mpgPpmChart", mileage);
							daysBetweenRefillsByDestination("daysBetweenChart", mileage);

							new Vue({
								el: "#mileageTable",
								data : { entries : order(mileage, function(x) { return x.toDate; }, descComparator) }
							});

							$(".editableRow")
								.mouseenter(function() {
									$(this).find(".edit").show();
									$(this).find(".remove").show();
								})
								.mouseleave(function() {
									$(this).find(".edit").hide();
									$(this).find(".remove").hide();
								});

							bindEdit("#mileageForm", "/rest/mileage", function(entry) {
								$("#providerId").val(entry.providerId);
								$("#destinationId").val(entry.destinationId);
							});

							bindRemove("/rest/mileage");
						},
						fail : function() {
							pageNotifier.error("Failed to load vehicle mileage.");
						}
					});
				},
				fail : function(results) {
					pageNotifier.error("Failed to load destinations.");
				}
			});
		},
		fail : function(results) {
			pageNotifier.error("Failed to load providers.");
		}
	});
});
