$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	$.ajax({
		url : "rest/drivers",
		timeout: 3000,
		success : function(drivers) {
			new Vue({
				el: "#driverId",
				data : { entries : drivers }
			});

			bindAdd("#vehiclesForm", "/rest/vehicles", {
				id : -1,
				driverId : 1,
				vin : "",
				make : "",
				model : "",
				year : (new Date()).getFullYear(),
				stillOwn : true
			});		

			$.ajax({
				method : "GET",
				url : "/rest/drivers/1/vehicles",
				success : function(results) {
					substitute(results, "driver", (x) => x.driverId, drivers, (x) => x.id, (x) => x.name);

					new Vue({
						el : "#vehiclesTable",
						data : { entries : results }
					});

					$(".vin").colorbox({
						inline: true,
						href: "#vinDetail",
						onOpen: function() {
							nhtsa = JSON.parse($(this).attr("data"))
							console.log(nhtsa)
							new Vue({
								el: "#vinDetail",
								data : nhtsa
							});
						}
					});
				},
				fail : function(result) {
					pageNotifier.error("Failed to load vehicles.");
				}
			});
		},
		fail : function() {
			pageNotifier.error("Failed to load drivers.");
		}
	});
});
