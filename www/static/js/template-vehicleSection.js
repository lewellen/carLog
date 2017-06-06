class VehicleMenu {
	constructor(divId) {
		this.element = document.getElementById(divId);
		this.vehicleId = null;
	}

	set vehicleId(value) {
		var aEls = this.element.querySelectorAll("a");
		for(var aEl  of aEls) {
			var href = aEl.getAttribute("href");
			href = href.replace(/\?.*$/, "");
			href = href + "?id=" + value;
			aEl.setAttribute("href", href);
		}
	}
}

function loadVehicleSection(e) {
	var params = new URLSearchParams(document.location.search);
	var vehicleId = params.get("id");

	var templateImport = new TemplateImport(e);
	templateImport.placeComponent("vehicleMenu-template", "vehicleMenu");

	var vehicleMenu = new VehicleMenu("vehicleMenu");
	vehicleMenu.vehicleId = vehicleId;
}
