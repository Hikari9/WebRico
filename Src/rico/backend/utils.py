def isstring(variable):
	return isinstance(variable, (str, unicode))

def uni(variable):
	return unicode(variable, 'ascii', 'ignore')