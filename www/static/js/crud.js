function bindAdd(formUrl, defaultData) {
	$("#addEntry").colorbox({
		href : formUrl,
		inline : true,
		onOpen: function() {
			new Vue({
				el: formUrl,
				data : defaultData
			});
		},
		onClosed : function() {
			location.reload();
		}
	});
}

function bindSubmit(postUrl) {
	$(".submit").click(function(e) {
		e.preventDefault();

		formArray = $('form').serializeArray();
		var obj = { };
		for(var i = 0, len = formArray.length; i < len; ++i) {
			obj[formArray[i]["name"]] = formArray[i]["value"];
		}

		$.ajax({
			type : "POST",
			url : postUrl,
			data : JSON.stringify(obj),
			contentType: "application/json",
			success : function(result) {
				if(result.id == null) {
					$("#formMessageBox").text(result.msg);
					$("#formMessageBox").addClass("notice");
				} else {
					$("#messageBox").text("Success!");
					$("#messageBox").addClass("success");
					$.colorbox.close();
				}
			},
			fail : function(result) {
				$("#formMessageBox").text(result.msg);
				$("#formMessageBox").addClass("error");
			}
		});
	});
}

function bindEdit(formUrl, getUrl) {
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

		$.ajax({
			method : "DELETE",
			url : deleteUrl + "/" + $(this).attr("rel"),
			success : function(result) {
				location.reload();
			},
			fail : function(result) {
				$("#messageBox").text("Failed to remove record.");
			}
		});
	});
}
