$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	$.ajax({
		url : "rest/drivers/1/vehicles",
		timeout: 3000,
		success : function(results) {
			new Vue({
				el: "#vehicles",
				data : { entries : results }
			});
		},
		fail : function(result) {
			pageNotifier.error("Failed to load vehicles");
		}
	});
});
