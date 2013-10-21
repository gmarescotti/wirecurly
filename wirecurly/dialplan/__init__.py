import logging
import condition

log = logging.getLogger(__name__)

__all__ = ['Extension']

class Extension(object):
	""" An extension object for the dialplan """

	def __init__(self,extension):
		super(Extension, self).__init__()
		self.extension = extension
		self.conditions = [] 
	
	def addCondition(self,cond):
		'''
			Add a condition for this extension
		'''
		try:	
			self.getCondition(cond)
		except ValueError: #Condition doesnt exist
			self.conditions.append(cond)
			return
		log.warning('Cannot replace existing condition')
		raise ValueError

	def getCondition(self,cond):
		'''
			Returns a condition object based on its attributes
		'''
		for c in self.conditions:
			if type(c) == type(cond):
				if c.attrs == cond.attrs:
					return c
		raise ValueError

	def todict(self):
		'''
			Create a dict so it can be converted/serialized
		'''
		children = [] 

		if self.conditions:
			for c in self.conditions:
				children.append(c.todict())
	
		return {'tag': 'extension', 'children': children, 'attrs': {'name': self.extension}}
		