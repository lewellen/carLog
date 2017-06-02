$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	bindAdd("#driversForm", "/rest/drivers", {
		id : -1,
		name : ""
	});

	$.ajax({
		method : "GET",
		url : "/rest/drivers",
		success : function(results) {
			new Vue({
				el : "#driversTable",
				data : { entries : results }
			});
		},
		fail : function(result) {
			pageNotifier.error("Failed to get drivers.");
		}
	});
});
