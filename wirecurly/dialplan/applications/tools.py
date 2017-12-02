from wirecurly.dialplan.applications import ApplicationBase

class Answer(ApplicationBase):
	"""The answer application"""
	def __init__(self):
		super(Answer, self).__init__('answer')

	@property
	def data(self):
		'''
			Answer does not need data, so return None.
		'''
		return None

class Sleep(ApplicationBase):
	"""The sleep application"""
	def __init__(self, time_in_ms):
		super(Sleep, self).__init__('sleep')
		self.time_in_ms = time_in_ms
		
	@property
	def data(self):
		'''
			Sleep only needs to return the time to sleep in ms.
		'''
		return '%s' % self.time_in_ms

class BindMetaData(ApplicationBase):
	'''
		The bind_meta_data application: 
		https://wiki.freeswitch.org/wiki/Misc._Dialplan_Tools_bind_meta_app
	'''
	def __init__(self, key, listen_to="b", flags="s", app="execute_extension", params=None):
		super(BindMetaData, self).__init__('bind_meta_data')
		self.key = key
		self.listen_to = listen_to
		self.flags = flags
		self.app = app
		self.params = params
		
	@property
	def data(self):
		'''
			BindMetaData needs to return meta data in proper syntax.
		'''
		return '%(key)s %(listen_to)s %(flags)s %(app)s::%(params)s' % self.__dict__

class Set(ApplicationBase):
	"""Set a variable on the current executing channel"""
	def __init__(self, variable, value):
		super(Set, self).__init__('set')
		self.variable = variable
		self.value = value

	@property
	def data(self):
		'''
			Set needs return a string
		'''
		return '%s=%s' % (self.variable, self.value)

class Eval(ApplicationBase):
	"""The Eval application"""
	def __init__(self, text):
		super(Eval, self).__init__('eval')
		self.text = text

	@property
	def data(self):
		'''
			Eval needs return a string
		'''
		return '%s' % self.text
		
class Transfer(ApplicationBase):
	"""The Transfer application"""
	def __init__(self, text):
		super(Transfer, self).__init__('transfer')
		self.text = text

	@property
	def data(self):
		'''
			Eval needs return a string
		'''
		return '%s' % self.text
		
class Hash(ApplicationBase):
	"""Set a variable on the hash"""
	def __init__(self, op, realm, key, value):
		super(Hash, self).__init__('hash')
		self.op = op
		self.realm = realm
		self.key = key
		self.value = value

	@property
	def data(self):
		'''
			Set needs return a string
		'''
		return '%s/%s/%s/%s' % (self.op, self.realm, self.key, self.value)
		
class Export(ApplicationBase):
	"""Export a variable on the other b leg"""
	def __init__(self, variable, value, nolocal=False):
		super(Export, self).__init__('export')
		self.variable = variable
		self.value = value
		self.nolocal = nolocal

	@property
	def data(self):
		'''
			Set needs return a string
		'''
		if self.nolocal:
			return 'nolocal:%s=%s' % (self.variable, self.value)
		else:
			return '%s=%s' % (self.variable, self.value)

class ExecuteOnAnswer(ApplicationBase):
    """ExecuteOnAnswer a variable on the other b leg"""
    def __init__(self, cmd, nolocal=True):
        super(ExecuteOnAnswer, self).__init__('export')
        self.cmd = cmd
        self.nolocal = nolocal

    @property
    def data(self):
        '''
            Set needs return a string
        '''
        if self.nolocal:
            return 'nolocal:execute_on_answer=%s' % self.cmd
        else:
            return 'execute_on_answer=%s' % self.cmd