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
        
    def method_m1(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            b0 = {}
            t0 = yield self.method_m2(world_state, b0)
            if t0 != None:
                b1 = {}
                t1 = yield self.method_m3(world_state, b1)
                if t1 != None:
                    t2 = [('!a1', )]
                    yield t0+t1+t2
        yield None
        
    def method_m2(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!a2', )]
            b1 = {}
            t1 = yield self.method_m5(world_state, b1)
            if t1 != None:
                b2 = {}
                t2 = yield self.method_m4(world_state, b2)
                if t2 != None:
                    t3 = [('!a4', )]
                    yield t0+t1+t2+t3
        yield None
        
    def method_m5(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!a3', )]
            yield t0
        yield None
        
    def method_m4(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!a5', )]
            t1 = [('!a6', )]
            yield t0+t1
        yield None
        
    def method_m3(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!a7', )]
            yield t0
        yield None
        
    def method_k1(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        def satisfy_branch_1(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            b0 = {}
            t0 = yield self.method_k2(world_state, b0)
            if t0 != None:
                yield t0
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_1(world_state, input_binding):
            precondition_satisfied = True
            b0 = {}
            t0 = yield self.method_k3(world_state, b0)
            if t0 != None:
                yield t0
        yield None
        
    def method_k2(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            b0 = {}
            t0 = yield self.method_k4(world_state, b0)
            if t0 != None:
                yield t0
        yield None
        
    def method_k4(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            output_binding = input_binding.copy()
            if eq(0,1):
                yield output_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!a1', )]
            yield t0
        yield None
        
    def method_k3(self, world_state, input_binding):
        def satisfy_branch_0(world_state, input_binding):
            yield input_binding
        precondition_satisfied = False
        for branch_satisfier in satisfy_branch_0(world_state, input_binding):
            precondition_satisfied = True
            t0 = [('!a2', )]
            yield t0
        yield None
        
