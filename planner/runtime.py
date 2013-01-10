import types
from domain_ast import lex_token

class MethodNode(object):

    def __init__(self, method_name):
        self.name = method_name
        self.children = []

    def to_string(self, indent_count=0, indent=' '):
        result = indent * indent_count + self.name + '\n'
        for child in self.children:
            result += child.to_string(indent_count+1, indent)

        return result

    def match(self, str_path):
        path = str_path.split('.')
        nodes = [self]
        for name in path:
            next_nodes = None
            for node in nodes:
                if name == node.name:
                    next_nodes = node.children
                    break
            if next_nodes == None:
                return False
            nodes = next_nodes
        return True

class Plan(object):

    def __init__(self):
        self.tasks = []
        self.tree = None

    def is_continue_task(self):
        return len(self.tasks) > 0 and self.tasks[0][0] == lex_token.CONTINUE

    def is_empty(self):
        return len(self.tasks) == 0

class Executor(object):

    def __init__(self, action_map, plan):
        self.action_map = action_map
        self.plan = plan
        self.step = 0
        self.action = None

    def finished(self):
        return self.step == len(self.plan.tasks)

    def begin(self):
        self.begin_next()

    def tick(self, timestamp):
        if self.action != None:
            if self.action.tick(timestamp):
                self.step += 1
                self.begin_next()

    def begin_next(self):
        while self.step < len(self.plan.tasks):
            task = self.plan.tasks[self.step]
            task_name = task[0]
            task_args = task[1:]
            self.action = self.action_map[task_name]

            if not self.action.begin(*task_args):
                break

            self.step += 1

        if self.finished():
            self.action = None

def find_plan(method, world_state={}, input_binding={}):
    result = Plan()
    task_stack = [method(world_state, input_binding)]
    node_queue = []

    while True:
        m = task_stack[-1]

        if isinstance(m, types.GeneratorType):
            res = m.next()

            if not isinstance(res, types.GeneratorType):
                if res != None:
                    node = MethodNode(m.__name__[len('method_'):])
                    node_queue.append(node)

                task_stack.pop()

            task_stack.append(res)
            continue

        m = task_stack.pop()

        if m != None:
            if (lex_token.CONTINUE,) in m:
                result.tasks = [(lex_token.CONTINUE,)]
                return result

        if len(task_stack) > 0:
            outer = task_stack[-1]
            res = outer.send(m)

            if not isinstance(res, types.GeneratorType):
                if res != None:
                    node = MethodNode(outer.__name__[len('method_'):])
                    node.children = node_queue
                    node_queue = [node]
                else:
                    node_queue = []

                task_stack.pop()

            task_stack.append(res)
            continue

        result.tasks = m
        result.tree = node_queue[0]
        return result

    return None
