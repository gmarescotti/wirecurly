class ApplicationBase(object):
	"""A base class for applications"""
	def __init__(self, app_name):
		super(ApplicationBase, self).__init__()
		self.app_name = app_name
		
	@property
	def data(self):
		'''
			Method that all must implement to provide data.
		'''
		raise NotImplementedError
	
	def __repr__(self):
		return "Application '%s': data=%s" % (self.app_name, self.data)