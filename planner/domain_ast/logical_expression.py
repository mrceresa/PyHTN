import s_expression
from s_expression import assert_node
from s_expression import assert_child
from domain_ast import node_type
from domain_ast import lex_token
from domain_ast import term

token_to_op = {
    lex_token.AND : node_type.OP_AND,
    lex_token.OR  : node_type.OP_OR,
    lex_token.NOT : node_type.OP_NOT,
    }

def build(s_expr):
    '''
    Build AST from the given S-expression
    '''
    root_node = node_type.LogicalOp()
    assert_node(s_expr, s_expression.List)

    if len(s_expr.children) == 0:
        root_node.op = node_type.OP_AND
        return root_node

    if len(s_expr.children) > 1:
        root_node.op = node_type.OP_AND

        for child_expr in s_expr.children:
            child_node = _build_recursive(child_expr)
            root_node.children.append(child_node)
    else:
        root_node = _build_recursive(s_expr.children[0])

    return root_node

def _build_recursive(s_expr):
    assert_node(s_expr, s_expression.List)
    symbol = assert_child(s_expr, 0, s_expression.Symbol)

    if token_to_op.has_key(symbol.text):
        return _build_logical_op(s_expr)

    if symbol.text == lex_token.CALL:
        return term.build(s_expr)

    return _build_atom(s_expr)

def _build_logical_op(s_expr):
    node = node_type.LogicalOp()
    symbol = assert_child(s_expr, 0, s_expression.Symbol)

    node.op = token_to_op[symbol.text]

    for child_expr in s_expr.children[1:]:
        child_node = _build_recursive(child_expr)
        node.children.append(child_node)

    return node

def _build_atom(s_expr):
    node = node_type.Atom()
    symbol = assert_child(s_expr, 0, s_expression.Symbol)

    node.name = symbol.text

    for arg_expr in s_expr.children[1:]:
        term_node = term.build(arg_expr)
        node.children.append(term_node)

    return node

def classify_variables(bound_variables, root_node):
    '''
    Classify logical expression variables into free, bound and constants sets.
    *bound_variables* contains parent method variables initially.
    *root_node* is a logical expression tree in DNF form.
    '''
    for child_node in root_node.children:
        _classify_variables_recursive(list(bound_variables), child_node)

def _classify_variables_recursive(bound_variables, root_node):
    if isinstance(root_node, node_type.Atom):
        for var_node in root_node.children:
            if var_node.is_variable():
                if var_node.name in bound_variables:
                    var_node.is_bound = True
                else:
                    bound_variables.append(var_node.name)

    if isinstance(root_node, node_type.LogicalOp):
        for child_node in root_node.children:
            _classify_variables_recursive(bound_variables, child_node)

def flatten(root_node):
    '''
    Replace chains of 'and' or 'or' ops with op with multiple children.
    Ex.: (and (a) (and (b) (and (c) ... -> (and (a) (b) (c) ...
    '''
    if isinstance(root_node, node_type.Atom):
        return root_node

    if isinstance(root_node, node_type.Term):
        return root_node

    if isinstance(root_node, node_type.LogicalOp):
        if root_node.op != node_type.OP_NOT:
            while True:
                new_children = []

                for child_node in root_node.children:
                    if isinstance(child_node, node_type.LogicalOp) and (child_node.op == root_node.op):
                        child_flattened_children = [flatten(c) for c in child_node.children]
                        new_children += child_flattened_children
                    else:
                        new_children += [child_node]

                if new_children == root_node.children:
                    break

                root_node.children = new_children
        else:
            root_node.children = [flatten(c) for c in root_node.children]

        return root_node

    # error
    return None

def convert_to_nnf(root_node):
    '''
    Convert AST to Negative Normal Form
    '''
    if isinstance(root_node, node_type.Atom):
        return root_node

    if isinstance(root_node, node_type.Term):
        return root_node

    if isinstance(root_node, node_type.LogicalOp):
        if root_node.op == node_type.OP_NOT:
            child_node = root_node.children[0]

            if isinstance(child_node, node_type.Atom):
                return root_node

            if isinstance(child_node, node_type.Term):
                return root_node

            if isinstance(child_node, node_type.LogicalOp):
                if child_node.op == node_type.OP_NOT:
                    return convert_to_nnf(child_node.children[0])

                new_op = {
                    node_type.OP_AND : node_type.OP_OR,
                    node_type.OP_OR  : node_type.OP_AND,
                    }[child_node.op]

                child_node.op = new_op
                converted_child_children = []

                for child_child_node in child_node.children:
                    new_child_child = node_type.LogicalOp()
                    new_child_child.op = node_type.OP_NOT
                    new_child_child.children = [child_child_node]

                    converted_child_children.append(convert_to_nnf(new_child_child))

                child_node.children = converted_child_children

                return child_node
        else:
            converted_children = []

            for child_node in root_node.children:
                converted_children.append(convert_to_nnf(child_node))

            root_node.children = converted_children

            return root_node

    # error
    return None

def convert_to_dnf(root_node):
    '''
    Convert AST to Disjunctive Normal Form
    '''
    # special case for empty preconditions
    if isinstance(root_node, node_type.LogicalOp) and len(root_node.children) == 0:
        return node_type.LogicalOp(op=node_type.OP_OR)

    nnf_root_node = flatten(convert_to_nnf(root_node))

    if isinstance(root_node, node_type.LogicalOp) and root_node.op == node_type.OP_OR:
        new_root_node = nnf_root_node
    else:
        new_root_node = node_type.LogicalOp(
            op=node_type.OP_OR,
            children=[nnf_root_node])

    return _convert_or_to_dnf(new_root_node)

def _is_literal(node):
    return \
        isinstance(node, node_type.Atom) or \
        (isinstance(node, node_type.LogicalOp) and node.op == node_type.OP_NOT) or \
        (isinstance(node, node_type.Term) and node.term_type == node_type.TERM_CALL)

def _is_conjunction_of_literals(node):
    if not isinstance(node, node_type.LogicalOp):
        return False

    if node.op != node_type.OP_AND:
        return False

    for child in node.children:
        if not _is_literal(child):
            return False

    return True

def _convert_and_to_dnf(and_node):
    or_node = None

    for child_node in and_node.children:
        if isinstance(child_node, node_type.LogicalOp) and child_node.op == node_type.OP_OR:
            or_node = child_node
            break

    new_children = []

    for or_node_child in or_node.children:
        new_child = node_type.LogicalOp(op=node_type.OP_AND)

        for child_node in and_node.children:
            if child_node != or_node:
                new_child.children.append(child_node)
            else:
                new_child.children.append(or_node_child)

        new_children.append(new_child)

    return [flatten(c) for c in new_children]

def _convert_or_to_dnf(or_node):
    while True:
        new_children = []

        all_children_converted = True

        for child_node in or_node.children:
            if _is_literal(child_node) or _is_conjunction_of_literals(child_node):
                new_children.append(child_node)
            else:
                new_children += _convert_and_to_dnf(child_node)
                all_children_converted = False

        or_node.children = new_children

        if all_children_converted:
            break

    return or_node
