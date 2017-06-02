class Notifier {
	constructor(divId) {
		this.element = document.getElementById(divId);
	}

	success(message) {
		this.__show("success", "img/fugue/tick-circle.png", message);
	}

	warn(message) {
		this.__show("notice", "img/fugue/exclamation-circle.png", message);
	}

	error(message) {
		this.__show("error", "img/fugue/cross-circle.png", message);
	}

	denied(message) {
		this.__show("error", "img/fugue/prohibition.png", message);
	}

	__show(className, imgPath, message) {
		this.element.className = className;
		this.element.innerHTML = '<img src="' + imgPath + '" class="icon" style="margin-right:1em;" />' + message;
	}
}
