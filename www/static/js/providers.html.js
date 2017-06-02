$(document).ready(function() {
	var pageNotifier = new Notifier("pageNotifier");

	$.ajax({
		url : "rest/providerTypes",
		timeout: 3000,
		success : function(providerTypes) {
			new Vue({
				el: "#providerTypeId",
				data : { entries : providerTypes }
			});

			bindAdd("#providersForm", "/rest/providers", {
				id : -1,
				providerTypeId : 1,
				name : "",
				address : ""
			});

			$.ajax({
				method : "GET",
				url : "/rest/providers",
				success : function(results) {
					substitute(results, "providerType", (x) => x.providerTypeId, providerTypes, (x) => x.id, (x) => x.name);

					new Vue({
						el : "#providersTable",
						data : { entries : results }
					});
				},
				fail : function(result) {
					pageNotifier.error("Failed to load providers.");
				}
			});
		},
		fail : function(result) {
			pageNotifier.error("Failed to load providers types.");
		}
	});
});
