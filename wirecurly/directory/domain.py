import logging

log = logging.getLogger(__name__)

__all__ = ['Domain']
        
class Domain(object):
    """A domain object for the directory"""
    def __init__(self, name):
        super(Domain, self).__init__()
        self.domain = name
        self.group = None
        self.users = []
        self.elements = []
        self.parameters = None
        self.variables = None

    def addVariable(self, var, val):
        '''
            Set an extra variable for a domain
        '''
        if not self.variables:
            self.variables = []

        try:
            self.getVariable(var)
        except ValueError:
            self.variables.append({'name': var, 'value': val})
            return

        log.warning('Cannot replace existing variable.')
        raise ValueError

    def addUsersToGroup(self,group='default'):
        '''
            Add all users to group
        '''
        self.group = group

    def addUser(self, user):
        '''Add user to domain
        
        :param user: The user to add to the domain.
        :type user: object
        '''
        self.users.append(user)

    def addSection(self, element):
        '''
            Add a subelement to the domain.
        '''
        if not element.isEmpty():
            self.elements.append(element.todict())

    def addGateway(self, gateway):
        '''Add a gateway to domain
        
        :param gateway: The gateway to add to the domain.
        :type gateway: object
        '''
        self.users.append(gateway)

    def addParameter(self, param, val):
        '''
            Set an extra parameter for a domain
        '''
        if not self.parameters:
            self.parameters = []
        try:
            self.getParameter(param)
        except ValueError:
            self.parameters.append({'name': param, 'value': val})
            return
        
        log.warning('Cannot replace existing parameter.')
        raise ValueError

    def getParameter(self, param):
        '''
            Retrieve the value of a parameter by its name
        '''
        if self.parameters:
            for p in self.parameters:
                if p.get('name') == param:
                    return p.get('value')

        raise ValueError

    def getVariable(self, var):
        '''
            Retrieve the value of a variable by its name
        '''
        if self.variables:
            for v in self.variables:
                if v.get('name') == var:
                    return v.get('value')

        raise ValueError


    def todict(self):
        '''
            Create a dict so it can be converted/serialized
        '''
        children = []
        if self.parameters:
            children.append({'tag': 'params', 'children': [
                            {'tag': 'param', 'attrs': p} for p in self.parameters
                        ]})

        if self.variables:
            children.append({'tag': 'variables', 'children': [
                            {'tag': 'variable', 'attrs': v} for v in self.variables
                        ]})

        if self.elements:
            children.extend(self.elements)

        # if self.users:
        users_children = [u.todict() for u in self.users]
            
        # if self.group is None: children.extend(users_children)

        if self.group is not None:
            users = [{'tag': 'users', 'children': users_children}]
            group = [{'tag': 'group', 'children': users, 'attrs': {'name': self.group}}]
            groups = [{'tag': 'groups', 'children': group}]
            children.extend(groups)
            return {'tag': 'domain', 'children': children, 'attrs': {'name': self.domain}}
        else:
            users = [{'tag': 'users', 'children': users_children}]
            children.extend(users)
            return {'tag': 'domain', 'children': children, 'attrs': {'name': self.domain}}
