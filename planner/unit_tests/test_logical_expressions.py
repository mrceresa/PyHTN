import unittest
import s_expression
from domain_ast import node_type
from domain_ast import logical_expression
from domain_ast import lex_token

class TestBuild(unittest.TestCase):

    def test_simple(self):
        t = '''
            ((or (a) (b) (c)))
            '''
        actual = logical_expression.build(s_expression.parse(t))

        expected = node_type.LogicalOp(
            op = node_type.OP_OR,
            children = [
                node_type.Atom(name='a'),
                node_type.Atom(name='b'),
                node_type.Atom(name='c'),
                ])

        self.assertEqual(expected, actual)

    def test_and_is_default_root(self):
        t = '''
            ((a) (b))
            '''
        actual = logical_expression.build(s_expression.parse(t))

        expected = node_type.LogicalOp(
            op = node_type.OP_AND,
            children = [
                node_type.Atom(name='a'),
                node_type.Atom(name='b'),
                ])

        self.assertEqual(expected, actual)

class TestConvertToNegativeNormalForm(unittest.TestCase):

    def test_neg_neg_is_pos(self):
        t = '''
            ((not (not (a))))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_nnf(actual)

        expected = node_type.Atom(name='a')

        self.assertEqual(expected, actual)

    def test_no_conversion_is_required(self):
        t = '''
            ((or (a) (b)))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_nnf(actual)

        expected = node_type.LogicalOp(
            op = node_type.OP_OR,
            children = [
                node_type.Atom(name='a'),
                node_type.Atom(name='b'),
                ])

        self.assertEqual(expected, actual)

    def test_de_morgans_law(self):
        t = '''
            ((not (and (a) (or (b) (not (c))))))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_nnf(actual)

        # !(a && (b || !c)) -> !a || !(b || c) -> !a || (!b && c)

        expected = node_type.LogicalOp(
            op = node_type.OP_OR,
            children = [
                node_type.LogicalOp(
                    op = node_type.OP_NOT,
                    children = [
                        node_type.Atom(name='a')
                        ]),

                node_type.LogicalOp(
                    op = node_type.OP_AND,
                    children = [
                            node_type.LogicalOp(
                                op = node_type.OP_NOT,
                                children = [node_type.Atom(name='b')]),

                            node_type.Atom(name='c'),
                        ])
                ])

        self.assertEqual(expected, actual)

class TestFlatten(unittest.TestCase):

    def test_and_chain_is_flattened(self):
        t = '''
            ((not (and (a) (and (b) (or (c) (d)) (and (e) (f))))))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.flatten(actual)

        # (a && (b && (c && d))) -> a && b && c && d

        expected = node_type.LogicalOp(
            op = node_type.OP_NOT,
            children = [
                node_type.LogicalOp(
                    op = node_type.OP_AND,
                    children = [
                        node_type.Atom(name='a'),
                        node_type.Atom(name='b'),
                        node_type.LogicalOp(
                            op = node_type.OP_OR,
                            children = [
                                node_type.Atom(name='c'),
                                node_type.Atom(name='d'),
                                ]),
                        node_type.Atom(name='e'),
                        node_type.Atom(name='f'),
                    ]),
                ])

        self.assertEqual(expected, actual)

class TestConversionToDisjunctiveNormalForm(unittest.TestCase):

    def test_empty_expression_is_dnf(self):
        actual = logical_expression.build(s_expression.parse('()'))
        actual = logical_expression.convert_to_dnf(actual)
        expected = node_type.LogicalOp(op=node_type.OP_OR)

        self.assertEqual(expected, actual)

    def test_literal_is_dnf(self):
        actual = logical_expression.build(s_expression.parse('((a))'))
        actual = logical_expression.convert_to_dnf(actual)
        expected = node_type.LogicalOp(
            op=node_type.OP_OR, 
            children=[node_type.Atom(name='a')])

        self.assertEqual(expected, actual)

        actual = logical_expression.build(s_expression.parse('((not (a)))'))
        actual = logical_expression.convert_to_dnf(actual)
        expected = node_type.LogicalOp(
                op=node_type.OP_OR,
                children=[node_type.LogicalOp(
                    op=node_type.OP_NOT, 
                    children=[node_type.Atom(name='a')])])

        self.assertEqual(expected, actual)

    def tree_to_sexp(self, root_node):
        op_to_token = {
            node_type.OP_AND : lex_token.AND,
            node_type.OP_OR  : lex_token.OR,
            node_type.OP_NOT : lex_token.NOT,
            }

        if isinstance(root_node, node_type.Atom):
            return '%s'%(root_node.name)

        if isinstance(root_node, node_type.Term) and root_node.term_type == node_type.TERM_CALL:
            return '%s'%(root_node.name)

        if isinstance(root_node, node_type.LogicalOp):
            result = '(' + op_to_token[root_node.op]

            for child_node in root_node.children:
                result += ' ' + self.tree_to_sexp(child_node)

            result += ')'

            return result

        return ''

    def test_conversion_1(self):
        t = '''
            ((and (q1) (or (r1) (r2)) (q2) (or (r3) (r4)) (q3)))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_dnf(actual)

        expected = '(or (and q1 r1 q2 r3 q3) (and q1 r1 q2 r4 q3) (and q1 r2 q2 r3 q3) (and q1 r2 q2 r4 q3))'

        self.assertEqual(expected, self.tree_to_sexp(actual))

    def test_conversion_2(self):
        t = '''
            ((a) (not (or (b) (c))))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_dnf(actual)

        expected = '(or (and a (not b) (not c)))'

        self.assertEqual(expected, self.tree_to_sexp(actual))

    def test_conversion_3(self):
        t = '''
            ((or (a) (b)))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_dnf(actual)

        expected = '(or a b)'

        self.assertEqual(expected, self.tree_to_sexp(actual))

    def test_conversion_4(self):
        t = '''
            ((or (not (call f1))))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_dnf(actual)

        expected = '(or (not f1))'

        self.assertEqual(expected, self.tree_to_sexp(actual))

    def test_conversion_5(self):
        t = '''
            ((t1) (or (not (t2)) (and (t2) (t3) (t4))))
            '''

        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_dnf(actual)

        expected = '(or (and t1 (not t2)) (and t1 t2 t3 t4))'

        self.assertEqual(expected, self.tree_to_sexp(actual))

    def test_conversion_with_call_term(self):
        t = '''
            ((or (a) (b)) (call func ?x ?y))
            '''
        actual = logical_expression.build(s_expression.parse(t))
        actual = logical_expression.convert_to_dnf(actual)
        expected = '(or (and a func) (and b func))'
        self.assertEqual(expected, self.tree_to_sexp(actual))

class TestVariables(unittest.TestCase):

    def world_state_facts(self, root_node, name):
        if isinstance(root_node, node_type.Atom):
            if root_node.name == name:
                yield root_node
        else:
            for child_node in root_node.children:
                for fact_node in self.world_state_facts(child_node, name):
                    yield fact_node

    def test_vars_are_bound_or_free_or_constants(self):
        t = '''
            ((or (a ?method_var str_const1) (b ?method_var str_const2)) (c ?method_var ?out_var) (d ?out_var 123.0))
            '''

        actual = logical_expression.build(s_expression.parse(t))

        bound_variables = ['?method_var']
        logical_expression.classify_variables(bound_variables=bound_variables, root_node=actual)
        
        # bound_variables argument isn't mutable
        self.assertEqual(['?method_var'], bound_variables)

        a_node = list(self.world_state_facts(actual, 'a'))[0]
        b_node = list(self.world_state_facts(actual, 'b'))[0]
        c_node = list(self.world_state_facts(actual, 'c'))[0]
        d_node = list(self.world_state_facts(actual, 'd'))[0]

        self.assertEqual(set(['?method_var']), set(a_node.bound_variables))
        self.assertEqual(set(['str_const1']),  set(a_node.constants))

        self.assertEqual(set(['?method_var']), set(b_node.bound_variables))
        self.assertEqual(set(['str_const2']),  set(b_node.constants))

        self.assertEqual(set(['?method_var']), set(c_node.bound_variables))
        self.assertEqual(set(),                set(c_node.constants))

        self.assertEqual(set(['?out_var']),    set(d_node.bound_variables))
        self.assertEqual(set([123.0]),         set(d_node.constants))
