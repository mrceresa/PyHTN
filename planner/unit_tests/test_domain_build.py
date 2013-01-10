import unittest
import s_expression
from domain_ast import domain
from domain_ast import node_type

class TestBuild(unittest.TestCase):

    def test_empty_domain(self):
        t = '''
            (:domain expected-name)
            '''
        actual = domain.build(s_expression.parse(t))
        self.assertEqual('expected_name', actual.name)

    def test_empty_methods(self):
        t = '''
            (:domain test_domain (:method (test_method ?v1 ?v2)))
            '''
        actual_domain = domain.build(s_expression.parse(t))
        actual_method = actual_domain.children[0]
        self.assertEqual('test_method', actual_method.name)
        self.assertEqual(['?v1', '?v2'], actual_method.variables)

    def test_modules(self):
        t = '''
            (:domain test_domain (:module mod_a) (:module mod_b *))
            '''
        actual_domain = domain.build(s_expression.parse(t))
        self.assertEqual(set([('mod_a', None), ('mod_b', '*')]), set(actual_domain.modules))

    def test_full_domain(self):
        t = '''
            (:domain test-domain
                (:method (test-method ?var_a ?var_b)
                    ((fact1 ?var_a str_const) (fact2 ?var_a 239.0) (fact3 ?var_b))
                    ((empty-method ?var_a ?var_b str_const 123.0))

                    branch_name
                    ((fact4))
                    ((empty-method2))
                )

                (:method (empty-method ?var_x ?var_y ?var_z ?var_w)
                    branch-default
                    ()
                    ()
                )
            )
            '''

        actual_domain = domain.build(s_expression.parse(t))

        self.assertEqual(2, len(actual_domain.children))

        test_method_node = actual_domain.children[0]
        empty_method_node = actual_domain.children[1]
        test_method_branch_node = test_method_node.children[0]
        test_method_tasklist = test_method_branch_node.tasklist

        self.assertEqual('test_method', test_method_node.name)
        self.assertEqual('empty_method', empty_method_node.name)

        self.assertEqual(['?var_x', '?var_y', '?var_z', '?var_w'], empty_method_node.variables)

        self.assertEqual('branch_0', test_method_branch_node.name)
        self.assertEqual(1, len(test_method_tasklist))
        self.assertEqual('empty_method', test_method_tasklist[0].name)
        self.assertEqual(['?var_a', '?var_b', 'str_const', 123.0], test_method_tasklist[0].child_names())

        self.assertEqual('branch_name', test_method_node.children[1].name)
