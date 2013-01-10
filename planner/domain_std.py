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
