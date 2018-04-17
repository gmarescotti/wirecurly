from wirecurly.dialplan.applications import ApplicationBase

class Bridge(ApplicationBase):
	"""Bridge application"""
	def __init__(self, dialstring=None, delimiter=",", **variables):
		super(Bridge, self).__init__('bridge')
		
		var_dialstring = ','.join("{!s}={!s}".format(key,val) for (key,val) in variables.items())
		if var_dialstring:
			dialstring = "{%s}%s" % (var_dialstring, dialstring)

		if dialstring != None:
			self.endpoints_dialstrings = [dialstring]
		else:
			self.endpoints_dialstrings = []
		self.delimiter = delimiter

	def append_endpoint(self, ep_dialstring, **variables):
		var_dialstring = ','.join("{!s}={!s}".format(key,val) for (key,val) in variables.items())
		if var_dialstring:
			ep_dialstring = "[%s]%s" % (var_dialstring, ep_dialstring)
		if isinstance(ep_dialstring, ApplicationBase):
			self.endpoints_dialstrings.extend(ep_dialstring.endpoints_dialstrings)
		else:
			self.endpoints_dialstrings.append(ep_dialstring)

	@property
	def data(self):
		'''
			Data is the whole dialstring
		'''
		return self.delimiter.join(self.endpoints_dialstrings)
