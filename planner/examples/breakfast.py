# Auto-generated with translate_domain.py


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
        
    def method_have_breakfast(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            b0 = {}
            t0 = yield self.method_choose_drink(world_state, b0)
            if t0 != None:
                b1 = {}
                t1 = yield self.method_make_meal(world_state, b1)
                if t1 != None:
                    t2 = [('!eat', )]
                    yield t0+t1+t2
        yield None
        
    def method_choose_drink(self, world_state, input_binding):
        def satisfy_branch_coffee(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('has-coffee', []):
                output_binding['?coffee'] = b[0]
                yield output_binding
        def satisfy_branch_tea(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('has-tea', []):
                output_binding['?tea'] = b[0]
                yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_coffee(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!make_drink', branch_satisfier['?coffee'])]
            yield t0
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_tea(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!make_drink', branch_satisfier['?tea'])]
            yield t0
        yield None
        
    def method_make_meal(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('has-bread', []):
                output_binding['?bread'] = b[0]
                for b in world_state.get('has-butter', []):
                    output_binding['?butter'] = b[0]
                    for b in world_state.get('has-ham', []):
                        output_binding['?ham'] = b[0]
                        yield output_binding
        def satisfy_branch_1(world_state, input_binding):
            output_binding = input_binding.copy()
            for b in world_state.get('has-eggs', []):
                output_binding['?eggs'] = b[0]
                yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!make_sandwich', branch_satisfier['?bread'],branch_satisfier['?butter'],branch_satisfier['?ham'])]
            yield t0
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_1(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!make_eggs', branch_satisfier['?eggs'])]
            yield t0
        yield None
        
