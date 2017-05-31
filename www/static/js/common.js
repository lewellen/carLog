function getColorFromIdMap(mapInstance) {
	indexFrom = new Map()
	var index = 0
	for(var key of mapInstance.keys()) {
		indexFrom.set(key, index)
		++index
	}

	colorFrom = new Map()
	for(var key of mapInstance.keys()) {
		var percent = 100.0 * indexFrom.get(key) / (1.0 * mapInstance.size)
		var color = tinycolor("hsl(" + percent + "%, 60%, 50%)").setAlpha(0.7)
		colorFrom.set(key, color.toRgbString())
	}

	return colorFrom
}

function groupBy(xs, selector) {
	grouped = new Map();
	index = 0
	for(var x of xs) {
		var k = selector(x, index);
		if(!grouped.has(k)) {
			grouped.set(k, []);
		}
		grouped.get(k).push(x);
		++index;
	}
	return grouped;
}

function round(x, numDigits) {
	c = Math.pow(10, numDigits);
	return Math.round(c * x) / c;
}
