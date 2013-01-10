import s_expression
from s_expression import assert_node
from s_expression import assert_child
from s_expression import match_node
from s_expression import match_child
from domain_ast import node_type
from domain_ast import lex_token
from domain_ast import logical_expression
from domain_ast import term

def build(s_exp):
    '''
    Build Domain AST from the given S-expression
    '''
    assert_node(s_exp, s_expression.List)
    assert_child(s_exp, 0, s_expression.Symbol, lex_token.DOMAIN)
    name_expr = assert_child(s_exp, 1, s_expression.Symbol)

    domain = node_type.Domain()
    domain.name = lex_token.fixup_name(name_expr.text)

    for child_expr in s_exp.children[2:]:
        assert_node(child_expr, s_expression.List)
        symbol = assert_child(child_expr, 0, s_expression.Symbol)

        if symbol.text == lex_token.METHOD:
            method = build_method(child_expr)
            domain.children.append(method)
            domain.method_map[method.name] = method

        if symbol.text == lex_token.MODULE:
            module_name = assert_child(child_expr, 1, s_expression.Symbol).text

            if len(child_expr.children) == 3:
                symbol_name = assert_child(child_expr, 2, s_expression.Symbol).text
            else:
                symbol_name = None

            domain.modules.append((module_name, symbol_name))

        if lex_token.is_constant(symbol.text):
            rhs_expr = assert_child(child_expr, 1, [s_expression.List, s_expression.Symbol, s_expression.Number])
            domain.constants[symbol.text] = term.build(rhs_expr)

    return domain

def build_method(s_exp):
    signature_expr = assert_child(s_exp, 1, s_expression.List)

    method = node_type.Method()
    method.name = lex_token.fixup_name(assert_child(signature_expr, 0, s_expression.Symbol).text)

    for child_expr in signature_expr.children[1:]:
        method.variables.append(assert_node(child_expr, s_expression.Symbol).text)

    build_branches(s_exp.children[2:], method)

    return method

def build_branches(s_exprs, method_node):
    index = 0
    branch_count = 0

    while index < len(s_exprs):
        s_expr = assert_node(s_exprs[index], [s_expression.List, s_expression.Symbol])

        branch_name = 'branch_' + str(branch_count)

        if match_node(s_expr, s_expression.Symbol):
            branch_name = s_expr.text
            
            if index + 1 < len(s_exprs):
                index = index + 1
                s_expr = s_exprs[index]
            else:
                raise s_expression.SyntaxException(s_expr.pos)

        precondition = None
        task_list = None

        if match_node(s_expr, s_expression.List):
            if match_child(s_expr, 0, s_expression.Symbol, lex_token.FOREACH):
                precondition = assert_child(s_expr, 1, s_expression.List)
                task_list = assert_child(s_expr, 2, s_expression.List)
                index = index + 1
            else:
                if index + 1 < len(s_exprs):
                    precondition = s_expr
                    task_list = assert_node(s_exprs[index + 1], s_expression.List)
                    index = index + 2
                else:
                    raise s_expression.SyntaxException(s_expr.pos)

        if precondition != None and task_list != None:
            branch = build_branch(branch_name, precondition, task_list, method_node)
            method_node.children.append(branch)
            branch_count = branch_count+1

            if match_child(s_expr, 0, s_expression.Symbol, lex_token.FOREACH):
                branch.foreach = True
        else:
            raise s_expression.SyntaxException(s_expr.pos)

def build_branch(name, precondition_expr, tasklist_expr, method_node):
    branch = node_type.Branch()
    branch.name = lex_token.fixup_name(name)

    if match_child(precondition_expr, 0, s_expression.Symbol, lex_token.PERMUTE):
        permute_atom_expr = assert_child(precondition_expr, 1, s_expression.List)
        branch.permute_atom = build_permute_atom(permute_atom_expr)
        precondition_expr.children = precondition_expr.children[2:]

    precondition_node = logical_expression.build(precondition_expr)
    logical_expression.classify_variables(method_node.variables, precondition_node)
    precondition_node = logical_expression.convert_to_dnf(precondition_node)

    task_list_nodes = build_task_list(tasklist_expr)

    branch.children = [precondition_node] + task_list_nodes

    return branch

def build_permute_atom(s_expr):
    node = node_type.Atom()
    node.name = assert_child(s_expr, 0, s_expression.Symbol).text

    for child_expr in s_expr.children[1:]:
        child_node = term.build(child_expr)
        node.children.append(child_node)

    return node

def build_task_list(s_expr):
    task_list = []

    for child_expr in s_expr.children:
        assert_node(child_expr, s_expression.List)
        task_node = node_type.Atom()
        symbol = assert_child(child_expr, 0, s_expression.Symbol)
        task_node.name = lex_token.fixup_name(symbol.text)

        for arg_expr in child_expr.children[1:]:
            term_node = term.build(arg_expr)
            task_node.children.append(term_node)

        task_list.append(task_node)

    return task_list
