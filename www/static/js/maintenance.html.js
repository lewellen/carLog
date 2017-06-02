function costsByProvider(canvasId, maintenance) {
	annualTotalsByGroupChart(
		canvasId, maintenance, "Annual Expense ($)", "Total Expense ($)", 
		function(x) { return new Date(x.at).getFullYear(); }, 
		function(x) { return x.provider; }, 
		function(x) { return x.cost; }
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

	bindAdd("#maintenanceForm", "/rest/maintenance", {
		id : -1,
		vehicleId : vehicleId,
		providerId : 1,
		at : toISO8601DateStr(new Date()),
		primaryContact : "",
		phoneNumber : "",
		description : "",
		cost : 0
	});

	$("#exportCSV").attr("href", "/rest/vehicles/" + vehicleId + "/maintenance/csv")

	$.ajax({
		url : "rest/providers",
		timeout: 3000,
		success : function(providers) {
			new Vue({
				el: "#providerId",
				data : { entries : providers }
			});

			$.ajax({
				url: "/rest/vehicles/" + vehicleId + "/maintenance",
				timeout: 3000,
				success : function(maintenance) {
					maintenance = order(maintenance, function(x) { return x.at; }, descComparator);
					substitute(maintenance, "provider", (x) => x.providerId, providers, (x) => x.id, (x) => x.name);

					costsByProvider("costByProviderChart", maintenance);

					new Vue({
						el: "#maintenanceTable",
						data : { entries : maintenance }
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

					bindEdit("#maintenanceForm", "/rest/maintenance", function(entry) {
						$("#providerId").val(entry.providerId);
					});

					bindRemove("/rest/maintenance");
				},
				fail : function() {
					pageNotifier.error("Failed to load vehicle maintenance.");
				}
			});
		},
		fail: function() {
			pageNotifier.error("Failed to load providers.");
		}
	});
});
