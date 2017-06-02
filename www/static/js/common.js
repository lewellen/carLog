function getColorFromIdMap(mapInstance) {
	var indexFrom = new Map();
	var index = 0;
	for(var key of mapInstance.keys()) {
		indexFrom.set(key, index);
		++index;
	}

	var colorFrom = new Map();
	for(var key of mapInstance.keys()) {
		var percent = 100.0 * indexFrom.get(key) / (1.0 * mapInstance.size);
		var color = tinycolor("hsl(" + percent + "%, 60%, 50%)").setAlpha(0.7);
		colorFrom.set(key, color.toRgbString());
	}

	return colorFrom;
}

function groupBy(xs, selector) {
	var grouped = new Map();
	var index = 0;
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

function mapMapValues(mapInstance, f) {
	var result = new Map();
	for(var [key, value] of mapInstance) {
		result.set(key, f(value));
	}
	return result;
}

function range(xInc, xExc) {
	var result = [];
	for(var i = xInc; i < xExc; ++i) {
		result.push(i);
	}
	return result;
}

function round(x, numDigits) {
	var c = Math.pow(10, numDigits);
	return Math.round(c * x) / c;
}

function scanMap(mapInstance, f, init) {
	var result = new Map();
	var runningTotal = init;
	for(var [key, value] of mapInstance) {
		runningTotal = f(runningTotal, value);
		result.set(key, runningTotal);
	}
	return result;
}

function substitute(xs, xName, xIdSelector, ys, yIdSelector, yValueSelector) {
	var m = new Map(ys.map((y) => [yIdSelector(y), yValueSelector(y)]))
	for(var x of xs) {
		x[xName] = m.get(xIdSelector(x));
	}
}

function toISO8601DateStr(date) {
	var year = date.getFullYear();
	var month = date.getMonth() + 1;
	var day = date.getDate();

	var output = year.toString();
	output += "-";

	if(month < 10) {
		output += "0";
	}
	output += month.toString();
	output += "-";

	if(day < 10) {
		output += "0";
	}
	output += day.toString();

	return output;
}

function ascComparator(x, y) {
	if(x < y) {
		return -1;
	}

	if(x > y) {
		return +1;
	}

	return 0;
}

function descComparator(x, y) {
	if(x < y) {
		return +1;
	}

	if(x > y) {
		return -1;
	}

	return 1;
}

function order(xs, selector, comparator) {
	return xs.sort(function(a,b) {
		return comparator(selector(a), selector(b));
	});
}

function orderMapKeys(mapInstance, comparator) {
	var keys = Array.from(mapInstance.keys());
	keys = order(keys, function(x) { return x; }, comparator);

	var result = new Map();
	for(var key of keys) {
		result.set(key, mapInstance.get(key));
	}
	return result;
}

function addMissingMapKeys(mapInstance, keys, init) {
	var result = new Map(mapInstance);
	for(var key of keys) {
		if(!result.has(key)) {
			result.set(key, init);
		}
	}
	return result;
}
