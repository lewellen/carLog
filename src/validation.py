class KeyValidator:
	def __init__(self, dictValue, key):
		self.dictValue = dictValue
		self.key = key
		self.checks = []
		pass
	
	def exists(self):
		self.checks.append({
			"func": lambda : self.key in self.dictValue, 
			"msg" : "'%s' must be in dictionary." % self.key
		})
		return self

	def isNotNone(self):
		self.checks.append({
			"func" : lambda : self.dictValue[self.key] is not None,
			"msg" : "'%s' must not be None." % self.key
		})
		return self

	def isNotEmpty(self):
		self.checks.append({
			"func" : lambda : len(self.dictValue[self.key]) > 0,
			"msg" : "'%s' must not be empty string." % self.key
		})
		return self

	def isShorterThan(self, maxLen):
		self.checks.append({
			"func" : lambda : len(self.dictValue[self.key]) < maxLen,
			"msg" : "'%s' must be shorter than %d characters." % (self.key, maxLen)
		})
		return self

	def isPositiveInteger(self):
		self.checks.append({
			"func" : lambda : self.dictValue[self.key] > 0,
			"msg" : "'%s' must be a positive integer." % (self.key)
		})
		return self

	def isZeroOneBoolean(self):
		self.checks.append({
			"func" : lambda : self.dictValue[self.key] in ["0", "1"],
			"msg" : "'%s' must be a positive integer." % (self.key)
		})
		return self

	def existsNotNullShorterThan(self, maxLen):
		return self.exists().isNotNone().isNotEmpty().isShorterThan(maxLen)

	def existsNullableShorterThan(self, maxLen):
		if self.key in self.dictValue and self.dictValue[self.key] is not None and len(self.dictValue[self.key]) > 0:
			return self.existsNotNullShorterThan(maxLen)

		return self.exists()

	def existsPositiveInteger(self):
		return self.exists().isNotNone().isPositiveInteger()
		
	def existsZeroOneBoolean(self):
		return self.exists().isNotNone().isZeroOneBoolean()

	def validate(self):
		for check in self.checks:
			isValid = check["func"]()
			if not isValid:
				return False, check["msg"]

		return True, None

class DictValidator:
	def __init__(self, keyValidators):
		self.keyValidators = keyValidators
		pass

	def validate(self):
		for keyValidator in self.keyValidators:
			isValid, msg = keyValidator.validate()
			if not isValid:
				return isValid, msg

		return True, None
