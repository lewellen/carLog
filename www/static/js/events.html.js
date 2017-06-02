$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	var params = new URLSearchParams(document.location.search)
	var vehicleId = params.get("id")
	$("#vehicleMenu").find("a").each(function(){
		$(this).attr("href", $(this).attr("href") + "?id=" + vehicleId)
	});

	bindAdd("#eventsForm", "/rest/events", {
		id : -1,
		at : toISO8601DateStr(new Date()),
		odometer : 0,
		description : "",
		vehicleId : vehicleId
	});

	$("#exportCSV").attr("href", "/rest/vehicles/" + vehicleId + "/events/csv")

	$.ajax({
		url: "/rest/vehicles/" + vehicleId + "/events",
		timeout: 3000,
		success : function(events) {
			new Vue({
				el: "#eventsTable",
				data : {
					entries : order(events, function(x) { return x.at; }, descComparator)
				}
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

			bindEdit("#eventsForm", "/rest/events");

			bindRemove("/rest/events");
		},
		fail : function() {
			pageNotifier.error("Failed to load vehicle events.");
		}
	});
});
