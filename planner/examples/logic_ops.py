# Auto-generated with translate_domain.py

import examples

'''
Inlined standard functions for call term.
'''

import itertools
import random

# predicates

def lt(a, b):
    return a < b

def le(a, b):
    return a <= b

def gt(a, b):
    return a > b

def ge(a, b):
    return a >= b

def eq(a, b):
    return a == b

def ne(a, b):
    return a != b

# arithmetics

def add(a, b):
    return a + b

def sub(a, b):
    return a - b

def mul(a, b):
    return a * b

def div(a, b):
    return a / b

# permutations

def randomize(args, satisfier):
    for s in random.shuffle([b.copy() for b in satisfier]):
        yield s

def sort_by(args, satisfier):
    for s in sorted([b.copy() for b in satisfier], key=lambda binding : binding[args[0]]):
        yield s

def first(args, satisfier):
    for s in take_n([1], satisfier):
        yield s

def first_n(args, satisfier):
    for s in itertools.islice(satisfier, args[0]):
        yield s

#

def match(plan, str_path):
    return plan != None and plan.tree.match(str_path)


def create():
    return Domain()

class Domain(object):
    def __init__(self):
        self.constants = {}
        self.constants['#zero'] = 0
        self.constants['#two'] = 2
        self.constants['#one'] = 1
        
    def method_test(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('apple', []):
                output_binding['?a'] = b[0]
                for b in world_state.get('color', []):
                    if b[0] != output_binding['?a']:
                        continue
                    if b[1] == 'red':
                        continue
                    for b in world_state.get('color', []):
                        if b[0] != output_binding['?a']:
                            continue
                        if b[1] == 'green':
                            continue
                        yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!result', branch_satisfier['?a'])]
            yield t0
        yield None
        
    def method_test_call(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('apple', []):
                output_binding['?a'] = b[0]
                for b in world_state.get('color', []):
                    if b[0] != output_binding['?a']:
                        continue
                    if b[1] != examples.get_green():
                        continue
                    yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!result', branch_satisfier['?a'])]
            yield t0
        yield None
        
    def method_test_call_is_single_term(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            if examples.get_true(examples.get_green()):
                yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!OK', examples.get_green())]
            yield t0
        yield None
        
    def method_test_std_pred(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            if lt(self.constants['#zero'],add(self.constants['#one'],self.constants['#two'])):
                yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!OK', )]
            yield t0
        yield None
        
    def method_test_foreach(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('apple', []):
                output_binding['?a'] = b[0]
                yield output_binding
        precondition_satisfied = False
        branch_0_tasks = []
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            b0 = {}
            b0['?a'] = branch_satisfier['?a']
            t0 = yield self.method_eat_apple_cond(world_state, b0)
            if t0 != None:
                branch_0_tasks += t0
            else:
                yield None
        if precondition_satisfied:
            yield branch_0_tasks
        yield None
        
    def method_eat_apple_cond(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('color', []):
                if b[0] != output_binding['?a']:
                    continue
                if b[1] != 'red':
                    continue
                yield output_binding
            for b in world_state.get('color', []):
                if b[0] != output_binding['?a']:
                    continue
                if b[1] != 'green':
                    continue
                yield output_binding
        def satisfy_branch_1(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!eat', branch_satisfier['?a'])]
            yield t0
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_1(world_state, input_binding):
            precondition_satisfied = True
            yield []
        yield None
        
    def method_test_negative_unbound(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            if len(world_state.get('has_object', [])) == 0:
                yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            yield []
        yield None
        
