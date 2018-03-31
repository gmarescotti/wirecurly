from wirecurly.dialplan.applications import ApplicationBase

class Voicemail(ApplicationBase):
	"""Voicemail application"""
	def __init__(self, datastring):
		super(Voicemail, self).__init__('voicemail')
		self.datastring = datastring

	@property
	def data(self):
		'''
			Data is the whole datastring
		'''
		return self.datastring
	