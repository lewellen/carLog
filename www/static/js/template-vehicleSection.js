class VehicleMenu {
	constructor(element) {
		this.element = element;
		this.vehicleId = null;
	}

	set vehicleId(value) {
		var aEls = this.element.querySelectorAll("a");
		for(var aEl  of aEls) {
			var href = aEl.getAttribute("href");
			href = href.replace(/\?.*$/, "");
			href = href + "?id=" + this.vehicleId;
			aEl.setAttribute("href", href);
		}
	}
}

function loadVehicleSection(e) {
	var params = new URLSearchParams(document.location.search);
	var vehicleId = params.get("id");

	var templateImport = new TemplateImport(e);
	var vehicleMenu = new VehicleMenu(templateImport.placeComponent(
		"vehicleMenu-template", "vehicleMenu"
		));

	vehicleMenu.vehicleId = vehicleId;
}
