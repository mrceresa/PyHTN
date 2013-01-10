
'''Logical expression tokens'''
OR  = 'or'
AND = 'and'
NOT = 'not'

'''Terms'''
CALL = 'call'

'''Keywords'''
DOMAIN  = ':domain'
MODULE  = ':module'
METHOD  = ':method'
FOREACH = ':foreach'
PERMUTE = ':permute'
VAR_REF = ':var'

CONTINUE = '!continue'

def is_variable(token):
    return len(token) > 0 and token[0] == '?'

def is_operator(token):
    return len(token) > 0 and token[0] == '!'

def is_constant(token):
    return len(token) > 0 and token[0] == '#'

def fixup_name(name):
    return name.replace('-', '_')
