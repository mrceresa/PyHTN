from contextlib import contextmanager
from domain_ast import node_type
from domain_ast import lex_token

class Writer(object):

    def __init__(self, tab=' '*4):
        self.code = []
        self.tab = tab
        self.level = 0

    def end(self):
        return ''.join(self.code)

    def ident(self):
        self.level = self.level + 1

    def dedent(self):
        if self.level == 0:
            raise SyntaxError, "Mismatching idents-dedents."
        self.level = self.level - 1

    def write(self, line):
        self.code.append(self.tab * self.level + line + '\n')

@contextmanager
def idented(writer):
    writer.ident()
    yield writer
    writer.dedent()

def generate(domain_node, inline_modules=[]):
    '''
    Generates python module code from the given domain AST
    '''
    w = Writer()

    for module_desc in domain_node.modules:
        if module_desc[1] != None:
            w.write('from %s import %s'%(module_desc[0], module_desc[1]))
        else:
            w.write('import '+module_desc[0])

    w.write('')

    for inline_module in inline_modules:
        text = inline_module.read()
        w.write(text)
        w.write('')

    w.write('def create():')
    with idented(w):
        w.write('return Domain()')
    w.write('')

    w.write('class Domain(object):')
    with idented(w):
        w.write('def __init__(self):')
        with idented(w):
            generate_consts_init(w, domain_node)

        for method_node in domain_node.children:
            generate_method(w, domain_node, method_node)

    return w.end()

def generate_consts_init(w, domain_node):
    w.write('self.constants = {}')
    for (const_name, const_node) in domain_node.constants.iteritems():
        w.write('self.constants[\'%s\'] = %s'%(const_name, constant_initializer_to_code(const_node)))
    w.write('')

def generate_method(w, domain_node, method_node):
    w.write('def method_%s(self, world_state, input_binding):'%(method_node.name))

    with idented(w):
        for branch_node in method_node.children:
            generate_branch_satisfier(w, domain_node, branch_node)

        for branch_node in method_node.children:
            generate_branch_tasklist(w, domain_node, branch_node)

        w.write('yield None')

        w.write('')

def generate_branch_satisfier(w, domain_node, branch_node):
    w.write('def satisfy_%s(world_state, input_binding):'%(branch_node.name))

    with idented(w):
        if len(branch_node.precondition.children) == 0:
            w.write('yield input_binding')
        else:
            w.write('output_binding = input_binding.copy()')

            for clause_node in branch_node.precondition.children:
                generate_clause(w, domain_node, clause_node)

def generate_clause(w, domain_node, clause_node):
    if isinstance(clause_node, node_type.LogicalOp) and clause_node.op == node_type.OP_AND:
        for literal_node in clause_node.children:
            generate_literal(w, domain_node, literal_node)
            w.ident()

        w.write('yield output_binding')

        for i in range(len(clause_node.children)):
            w.dedent()
    else:
        generate_literal(w, domain_node, clause_node)

        with idented(w):
            w.write('yield output_binding')

def generate_literal(w, domain_node, literal_node):
    fact_node = literal_node
    negative_literal = False

    if isinstance(literal_node, node_type.LogicalOp) and literal_node.op == node_type.OP_NOT:
        negative_literal = True
        fact_node = literal_node.children[0]

    if isinstance(fact_node, node_type.Atom):
        if negative_literal and len(fact_node.unbound_variables) == len(fact_node.children):
            w.write('if len(world_state.get(\'%s\', [])) == 0:'%(fact_node.name))
        else:
            w.write('for b in world_state.get(\'%s\', []):'%(fact_node.name))

            with idented(w):
                for (var_index, var_node) in enumerate(fact_node.children):
                    if var_node.is_constant() or var_node.is_constant_ref():
                        if negative_literal:
                            w.write('if b[%s] == %s:'%(var_index, constant_to_code(var_node)))
                        else:
                            w.write('if b[%s] != %s:'%(var_index, constant_to_code(var_node)))

                        with idented(w):
                            w.write('continue')

                    elif var_node.is_bound_variable():
                        w.write('if b[%s] != output_binding[\'%s\']:'%(var_index, var_node.name))

                        with idented(w):
                            w.write('continue')

                    elif var_node.is_call_term():
                        if negative_literal:
                            w.write('if b[%s] == %s:'%(var_index, call_term_to_code(var_node, 'output_binding')))
                        else:
                            w.write('if b[%s] != %s:'%(var_index, call_term_to_code(var_node, 'output_binding')))

                        with idented(w):
                            w.write('continue')

                for (var_index, var_node) in enumerate(fact_node.children):
                    if var_node.is_variable() and not var_node.is_bound_variable():
                        w.write('output_binding[\'%s\'] = b[%s]'%(var_node.name, var_index))

    if isinstance(fact_node, node_type.Term):
        if negative_literal:
            w.write('if not %s:'%(call_term_to_code(fact_node, 'output_binding')))
        else:
            w.write('if %s:'%(call_term_to_code(fact_node, 'output_binding')))

def generate_branch_tasklist(w, domain_node, branch_node):
    w.write('precondition_satisfied = False')

    if branch_node.foreach:
        w.write('%s_tasks = []'%(branch_node.name))

    if branch_node.permute_atom:
        permute_vars = '[' + ','.join(child_terms_to_code(branch_node.permute_atom, 'input_binding')) + ']'
        w.write('for branch_satisfier in %s(%s, satisfy_%s(world_state, input_binding)):'%(branch_node.permute_atom.name, permute_vars, branch_node.name))
    else:
        w.write('for branch_satisfier in satisfy_%s(world_state, input_binding):'%(branch_node.name))

    with idented(w):
        w.write('precondition_satisfied = True')

        saved_ident_level = w.level

        for (task_index, task_node) in enumerate(branch_node.tasklist):
            if lex_token.is_operator(task_node.name):
                generate_operator_task(w, task_index, domain_node, task_node)
            else:
                generate_method_task(w, task_index, domain_node, task_node)

        if branch_node.foreach:
            if len(branch_node.tasklist) > 0:
                w.write('%s_tasks += '%(branch_node.name) + '+'.join(['t%s'%index for index in range(len(branch_node.tasklist))]))
            else:
                w.write('pass')
        else:
            if len(branch_node.tasklist) > 0:
                w.write('yield ' + '+'.join(['t%s'%index for index in range(len(branch_node.tasklist))]))
            else:
                w.write('yield []')

        if branch_node.foreach:
            for task_node in reversed(branch_node.tasklist):
                if not lex_token.is_operator(task_node.name):
                    w.dedent()
                    w.write('else:')
                    with idented(w):
                        w.write('yield None')

        w.level = saved_ident_level

    if branch_node.foreach:
        w.write('if precondition_satisfied:')

        with idented(w):
            w.write('yield %s_tasks'%(branch_node.name))

def generate_operator_task(w, task_index, domain_node, task_node):
    if task_node.name == '!!print':
        w.write('t%s = []'%(task_index))
        w.write('print '+','.join([constant_to_code(arg_node) for arg_node in task_node.children]))
    else:
        args = []
        for arg_node in task_node.children:
            if arg_node.is_constant() or arg_node.is_constant_ref() or arg_node.is_variable_ref():
                args.append(constant_to_code(arg_node))
            elif arg_node.is_variable():
                args.append('branch_satisfier[\'%s\']'%(arg_node.name))
            elif arg_node.is_call_term():
                args.append(call_term_to_code(arg_node, 'branch_satisfier'))

        w.write('t%s = [(\'%s\', %s)]'%(task_index, task_node.name, ','.join(args)))

def generate_method_task(w, task_index, domain_node, task_node):
    w.write('b%s = {}'%(task_index))

    for (arg_index, arg_node) in enumerate(task_node.children):
        method_arg_name = domain_node.method_map[task_node.name].variables[arg_index]

        if arg_node.is_constant() or arg_node.is_constant_ref() or arg_node.is_variable_ref():
            w.write('b%s[\'%s\'] = %s'%(task_index, method_arg_name, constant_to_code(arg_node)))
        elif arg_node.is_variable():
            w.write('b%s[\'%s\'] = branch_satisfier[\'%s\']'%(task_index, method_arg_name, arg_node.name))
        elif arg_node.is_call_term():
            w.write('b%s[\'%s\'] = %s'%(task_index, method_arg_name, call_term_to_code(arg_node, 'branch_satisfier')))

    w.write('t%s = yield self.method_%s(world_state, b%s)'%(task_index, task_node.name, task_index))
    w.write('if t%s != None:'%(task_index))
    w.ident()

def constant_to_code(term_node):
    if term_node.term_type in [node_type.TERM_SYMBOL, node_type.TERM_VAR_REF]:
        return '\'' + term_node.name + '\''
    if term_node.term_type == node_type.TERM_NUMBER:
        return str(term_node.name)
    if term_node.term_type == node_type.TERM_CONST_REF:
        return 'self.constants[\'%s\']'%(term_node.name)

def call_term_to_code(term_node, binding_name):
    return term_node.name + '(' + ','.join(child_terms_to_code(term_node, binding_name)) + ')'

def child_terms_to_code(node, binding_name):
    result = []

    for child_node in node.children:
        if child_node.is_constant() or child_node.is_constant_ref():
            result.append(constant_to_code(child_node))
        elif child_node.is_variable():
            result.append('%s[\'%s\']'%(binding_name, child_node.name))
        elif child_node.is_variable_ref():
            result.append('\'%s\''%(child_node.name))
        elif child_node.is_call_term():
            result.append(call_term_to_code(child_node, binding_name))

    return result

def constant_initializer_to_code(term_node):
    if term_node.is_constant() or term_node.is_constant_ref():
        return constant_to_code(term_node)

    if term_node.is_call_term():
        return call_term_to_code(term_node, '#error_binding#')

    return 'None'
