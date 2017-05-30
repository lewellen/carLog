class TemplateImport {
	constructor(loadEvent) {
		this.doc = loadEvent.target.import
	}

	placeComponent(templateId, placeholderId) {
		var template = this.doc.querySelector(templateId)
		var placeholder = document.querySelector(placeholderId)
		var clone = document.importNode(template.content, true)
		placeholder.appendChild(clone)
	}
}
