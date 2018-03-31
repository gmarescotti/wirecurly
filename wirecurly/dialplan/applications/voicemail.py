from wirecurly.dialplan.applications import ApplicationBase

class Voicemail(ApplicationBase):
	"""Voicemail application"""
	def __init__(self, datastring, use_bridge=False):
		self.use_bridge = use_bridge
		if use_bridge:
			super(Voicemail, self).__init__('bridge')
		else:
			super(Voicemail, self).__init__('voicemail')
		self.datastring = datastring

	@property
	def data(self):
		'''
			Data is the whole datastring
		'''
		if self.use_bridge:
			return "loopback/app=voicemail: %s" % self.datastring

		return self.datastring
	