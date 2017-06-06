class TemplateImport {
	constructor(loadEvent) {
		this.doc = loadEvent.target.import;
	}

	placeComponent(templateId, placeholderId) {
		var template = this.doc.getElementById(templateId);
		var placeholder = document.getElementById(placeholderId);
		var clone = document.importNode(template.content, true);
		placeholder.appendChild(clone);
		return clone;
	}
}
