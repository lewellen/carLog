$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	bindAdd("#destinationsForm", "/rest/destinations", {
		id : -1,
		name : ""
	});

	$.ajax({
		method : "GET",
		url : "/rest/destinations",
		success : function(results) {
			new Vue({
				el : "#destinationsTable",
				data : { entries : results }
			});
		},
		fail : function(result) {
			pageNotifier.error("Failed to load destinations.");
		}
	});
});
