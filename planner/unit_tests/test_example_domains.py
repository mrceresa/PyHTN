import unittest
import world_state

from runtime import find_plan

import examples.breakfast
import examples.logic_ops
import examples.permute
import examples.empty_tasklist
import examples.domain_tree_test

class Test(unittest.TestCase):

    def test_breakfast_planning(self):
        ws = {}
        tea = object()
        world_state.add(ws, 'has-tea', (tea,))
        world_state.add(ws, 'has-eggs', ('eggs1',))
        actual = find_plan(examples.breakfast.create().method_have_breakfast, ws, {})
        expected = [('!make_drink', tea), ('!make_eggs', 'eggs1'), ('!eat',)]
        self.assertEqual(expected, actual.tasks)

    def test_logic_ops(self):
        ws = {'apple': [('a1',), ('a2',), ('a3',)], 'color': [('a1', 'red'), ('a2', 'green'), ('a3', 'yellow')]}

        actual = find_plan(examples.logic_ops.create().method_test, ws, {})
        self.assertEqual([('!result', 'a3')], actual.tasks)

        actual = find_plan(examples.logic_ops.create().method_test_call, ws, {})
        self.assertEqual([('!result', 'a2')], actual.tasks)

        actual = find_plan(examples.logic_ops.create().method_test_call_is_single_term, ws, {})
        self.assertEqual([('!OK', 'green')], actual.tasks)

        actual = find_plan(examples.logic_ops.create().method_test_std_pred, ws, {})
        self.assertEqual([('!OK',)], actual.tasks)

    def test_sort_by(self):
        ws = {'object' : [('o1',), ('o2',), ('o3',),], 'value' : [('o1', 10), ('o2', 5), ('o3', 15)]}
        actual = find_plan(examples.permute.create().method_test_sort, ws, {})
        self.assertEqual([('!result', 'o2')], actual.tasks)

    def test_epmpty_plan(self):
        actual = find_plan(examples.empty_tasklist.create().method_test, {}, {})
        self.assertEqual([], actual.tasks)

    def test_foreach(self):
        ws = {'apple': [('a1',), ('a2',), ('a3',)], 'color': [('a1', 'red'), ('a2', 'black'), ('a3', 'green')]}
        actual = find_plan(examples.logic_ops.create().method_test_foreach, ws, {})
        self.assertEqual([('!eat', 'a1'), ('!eat', 'a3')], actual.tasks)

    def test_plan_tree_1(self):
        plan = find_plan(examples.domain_tree_test.create().method_m1, {}, {})
        expected = \
'''
    m1
        m2
            m5
            m4
        m3
'''
        actual = plan.tree.to_string(indent=' '*4, indent_count=1)
        self.assertEqual(expected, '\n' + actual)

    def test_plan_tree_2(self):
        plan = find_plan(examples.domain_tree_test.create().method_k1, {}, {})
        expected = \
'''
    k1
        k3
'''
        actual = plan.tree.to_string(indent=' '*4, indent_count=1)
        self.assertEqual(expected, '\n' + actual)
