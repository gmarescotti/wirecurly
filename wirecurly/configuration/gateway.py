import logging
from wirecurly.configuration import Section


log = logging.getLogger(__name__)

__all__ = ['Gateway']
        
class Gateway(object):
    """A gateway object"""
    def __init__(self, name):
        super(Gateway, self).__init__()
        self.name = name
        self.parameters = []
        self.variables = []

    def addParameter(self, param, val):
        '''Set an extra parameter for a gateway

        :param param: The paramenter to add
        :type param: str
        :param val: The value of the paramenter
        :type val: str
        :raises: ValueError -- in case the param already exists
        '''
        try:
            self.getParameter(param)
        except ValueError:
            self.parameters.append({'name': param, 'value': val})
            return

        log.warning('Cannot replace existing parameter.')
        raise ValueError

    def getParameter(self, param):
        '''Retrieve the value of a parameter by its name

        :rtype: str

        :raises: ValueError -- in case the param does not exist
        '''
        for p in self.parameters:
            if p.get('name') == param:
                return p.get('value')

        raise ValueError

    def addVariable(self, var, val, direction=None):
        '''Set an extra parameter for a gateway

        :param var: The variable to add
        :type var: str
        :param val: The value of the variable
        :type val: str
        :raises: ValueError -- in case the variable already exists
        '''
        try:
            self.getVariable(var)
        except ValueError:
            if direction:
                self.variables.append({'name': var, 'value': val, 'direction': direction})
            else:
                self.variables.append({'name': var, 'value': val})
            return

        log.warning('Cannot replace existing variable.')
        raise ValueError

    def getVariable(self, var):
        '''Retrieve the value of a variable by its name

        :rtype: str

        :raises: ValueError -- in case the variable does not exist
        '''
        for p in self.variables:
            if p.get('name') == var:
                return p.get('value')

        raise ValueError


    def todict(self):
        '''Create a dict so it can be converted/serialized

        :rtype: dict -- a dict ready to be serialized
        '''
        if self.parameters:
            children =[{'tag': 'param', 'attrs': p} for p in self.parameters]
        
        if self.variables:
            children =[{'tag': 'params', 'children': children}]
            children.append({'tag': 'variables', 'children': [{'tag': 'variable', 'attrs': p} for p in self.variables]})
    
        return {'tag': 'gateway', 'children': children, 'attrs': {'name': self.name}}
