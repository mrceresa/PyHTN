'''
Abstract Syntax Tree (AST) node types.
'''

OP_NONE     = 0
OP_OR       = 1
OP_NOT      = 2
OP_AND      = 3

TERM_NONE       = 0
TERM_VAR        = 1
TERM_SYMBOL     = 2
TERM_VAR_REF    = 3
TERM_NUMBER     = 4
TERM_CALL       = 5
TERM_CONST_REF  = 6

def print_tree(root_node, tab_count=0, tab=' '*4):
    if root_node != None:
        print tab * tab_count + root_node.__class__.__name__ + str(root_node)

        for child_node in root_node.children:
            print_tree(child_node, tab_count + 1)
    else:
        print tab * tab_count + 'None'

class Node(object):

    def __init__(self, name='', children=[]):
        self.name = name
        self.children = list(children)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        d = self.__dict__.copy()
        del d['children']
        return str(d)

    def child_names(self):
        result = []
        for child in self.children:
            result.append(child.name)
        return result

class Domain(Node):

    def __init__(self, name='', children=[], method_map={}, modules=[], constants={}):
        super(Domain, self).__init__(name, children)
        self.method_map = dict(method_map)
        self.modules = list(modules)
        self.constants = dict(constants)

class Method(Node):

    def __init__(self, name='', children=[], variables=[]):
        super(Method, self).__init__(name, children)
        self.variables = list(variables)

class Branch(Node):

    def __init__(self, name='', children=[], permute_atom=None, foreach=False):
        super(Branch, self).__init__(name, children)
        self.permute_atom = permute_atom
        self.foreach = foreach

    @property
    def precondition(self):
        return self.children[0]

    @property
    def tasklist(self):
        return self.children[1:]

class LogicalOp(Node):

    def __init__(self, op=OP_NONE, children=[]):
        super(LogicalOp, self).__init__('', children)
        self.op = op

class Atom(Node):

    def __init__(self, name='', children=[]):
        super(Atom, self).__init__(name, children)

    @property
    def bound_variables(self):
        result = []

        for child in self.children:
            if child.is_bound_variable():
                result.append(child.name)

        return result

    @property
    def unbound_variables(self):
        result = []

        for child in self.children:
            if child.is_variable() and not child.is_bound:
                result.append(child.name)

        return result

    @property
    def constants(self):
        result = []

        for child in self.children:
            if child.is_constant():
                result.append(child.name)

        return result

class Term(Node):

    def __init__(self, name='', term_type=TERM_NONE, children=[], is_bound=False):
        super(Term, self).__init__(name, children)
        self.term_type = term_type
        self.is_bound = is_bound

    def is_constant(self):
        return self.term_type == TERM_SYMBOL or self.term_type == TERM_NUMBER

    def is_constant_ref(self):
        return self.term_type == TERM_CONST_REF

    def is_variable(self):
        return self.term_type == TERM_VAR

    def is_variable_ref(self):
        return self.term_type == TERM_VAR_REF

    def is_bound_variable(self):
        return self.term_type == TERM_VAR and self.is_bound

    def is_call_term(self):
        return self.term_type == TERM_CALL
