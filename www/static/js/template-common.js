function loadCommon(e) {
	var template = new TemplateImport(e);
	template.placeComponent("#header-template", "#header");
	template.placeComponent("#footer-template", "#footer");
}
