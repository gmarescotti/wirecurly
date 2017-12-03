import logging

log = logging.getLogger(__name__)

__all__ = ['Node']

class Node(object):
	'''
		Node oject for acls
	'''

	def __init__(self, perm, cidr=None, domain=None):
		super(Node, self).__init__()
		if cidr:
			self.attrs = {'type' : perm , 'cidr' : cidr}
		else:
			self.attrs = {'type' : perm , 'domain' : domain}
		
	def todict(self):
		'''
			Create a dict so it can be converted/serialized
		'''
		return {'tag': 'node', 'attrs': self.attrs }
