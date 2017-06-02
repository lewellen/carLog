function bindAdd(formUrl, postUrl, defaultData) {
	$("#addEntry").colorbox({
		href : formUrl,
		inline : true,
		onOpen: function() {
			new Vue({
				el: formUrl,
				data : defaultData
			});

			bindSubmit(postUrl);
		},
		onClosed : function() {
			location.reload();
		}
	});
}

function bindSubmit(postUrl) {
	$(".submit").click(function(e) {
		e.preventDefault();

		var formNotifier = new Notifier("formNotifier");

		formArray = $('form').serializeArray();
		var obj = { };
		for(var i = 0, len = formArray.length; i < len; ++i) {
			obj[formArray[i]["name"]] = formArray[i]["value"];
		}

		console.log(JSON.stringify(obj))

		$.ajax({
			type : "POST",
			url : postUrl,
			data : JSON.stringify(obj),
			contentType: "application/json",
			success : function(result) {
				console.log(result);
				if(result.success) {
					$.colorbox.close();
				} else {
					formNotifier.warn(result.msg);
				}
			},
			fail : function(result) {
				console.log(result);
				formNotifier.error("Failed to submit.");
			}
		});
	});
}

function bindEdit(formUrl, getUrl, selectDropDowns = null) {
	$(".edit").colorbox({
		inline: true,
		href: formUrl,
		onOpen: function() {
			$.ajax({
				method : "GET",
				url : getUrl + "/" + $(this).attr("rel"),
				success : function(result) {
					new Vue({
						el: formUrl,
						data : result
					});

					if(selectDropDowns != null)
						selectDropDowns(result)

					bindSubmit(getUrl);
				},
				fail : function(result) {
					console.log(result);
				}
			});
		},
		onClosed : function() {
			location.reload();
		}
	});
}

function bindRemove(deleteUrl) {
	$(".remove").click(function(e) {
		e.preventDefault();

		var confirmed = confirm("Are you sure you want to remove this record?");
		if(!confirmed) {
			return;
		}

		var pageNotifier = new Notifier("pageNotifier");

		$.ajax({
			method : "DELETE",
			url : deleteUrl + "/" + $(this).attr("rel"),
			success : function(result) {
				if(result.success == true) {
					location.reload();
				} else {
					pageNotifier.warn(result.msg);
				}
			},
			fail : function(result) {
				pageNotifier.warn("Failed to delete record.");
			}
		});
	});
}
