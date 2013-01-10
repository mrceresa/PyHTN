import s_expression
from s_expression import assert_node
from s_expression import assert_child
from s_expression import match_node
from s_expression import match_child
from domain_ast import node_type
from domain_ast import lex_token

def build(s_expr):
    node = node_type.Term()

    if match_node(s_expr, s_expression.List):
        assert_child(s_expr, 0, s_expression.Symbol, [lex_token.CALL, lex_token.VAR_REF])

        if match_child(s_expr, 0, s_expression.Symbol, lex_token.CALL):
            node.term_type = node_type.TERM_CALL
            node.name = assert_child(s_expr, 1, s_expression.Symbol).text

            for child_expr in s_expr.children[2:]:
                child_node = build(child_expr)
                node.children.append(child_node)

            return node

        if match_child(s_expr, 0, s_expression.Symbol, lex_token.VAR_REF):
            node.term_type = node_type.TERM_VAR_REF
            node.name = assert_child(s_expr, 1, s_expression.Symbol).text
            return node

    if match_node(s_expr, s_expression.Number):
        node.name = s_expr.value
        node.term_type = node_type.TERM_NUMBER
        return node

    if match_node(s_expr, s_expression.Symbol):
        node.name = s_expr.text

        if lex_token.is_variable(s_expr.text):
            node.term_type = node_type.TERM_VAR
            return node

        if lex_token.is_constant(s_expr.text):
            node.term_type = node_type.TERM_CONST_REF
            return node

        node.term_type = node_type.TERM_SYMBOL
        return node
