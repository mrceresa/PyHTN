import re

class MalformedExpressionError(Exception):

    def __init__(self, pos=(-1, -1)):
        self.pos = pos

class SyntaxException(MalformedExpressionError):

    def __init__(self, pos=(-1, -1), desc=''):
        super(SyntaxException, self).__init__(pos)
        self.desc = desc

class Node(object):

    def __init__(self, pos, text=''):
        self.pos = pos
        self.text = text
        self.children = []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        d = self.__dict__.copy()
        del d['children']
        return str(d)

class List(Node):

    def __init__(self, pos=(-1, -1), text=''):
        super(List, self).__init__(pos, text)

class Symbol(Node):

    def __init__(self, pos=(-1, -1), text=''):
        super(Symbol, self).__init__(pos, text)

class Number(Node):

    def __init__(self, pos=(-1, -1), text=''):
        super(Number, self).__init__(pos, text)

    @property
    def value(self):
        try:
            return int(self.text)
        except:
            try:
                return float(self.text)
            except:
                raise

def is_number(text):
    try:
        int(text)
        return True
    except:
        try:
            float(text)
            return True
        except:
            return False

def tokenize(text):
    newline = re.compile(r'\r\n?|\n')
    ws = re.compile(r'\s+')
    tok = re.compile(r'\(|\)|[^\(\)\s]+')
    ln_cmnt = re.compile(r';')

    begin = 0
    lineno = 1
    lineoffset = 0
    line_comment = False

    while begin < len(text):
        m = newline.match(text, begin)

        if m:
            lineno = lineno + 1
            begin = m.span()[1]
            lineoffset = begin
            line_comment = False
            continue

        m = ws.match(text, begin)

        if m:
            begin = m.span()[1]
            continue

        m = ln_cmnt.match(text, begin)

        if m:
            begin = m.span()[1]
            line_comment = True
            continue

        m = tok.match(text, begin)

        if m:
            begin = m.span()[1]
            if not line_comment:
                yield (m.group(), (lineno, m.span()[0] - lineoffset + 1))

def next_token(tokenizer):
    try:
        return tokenizer.next()
    except StopIteration:
        return None

def match_token(token, value):
    if token == None:
        raise MalformedExpressionError()
    if token[0] != value:
        raise MalformedExpressionError(token[1])
    return token

def parse(text):
    tokenizer = tokenize(text)
    token = match_token(next_token(tokenizer), '(')
    return parse_list(tokenizer, token[1])

def parse_list(tokenizer, start_pos):
    node = List(pos=start_pos)

    while True:
        token = next_token(tokenizer)

        if token == None:
            raise MalformedExpressionError()
            continue

        if token[0] == ')':
            break

        if token[0] == '(':
            child_node = parse_list(tokenizer, token[1])
            node.children.append(child_node)
            continue

        if is_number(token[0]):
            child_node = Number(pos=token[1], text=token[0])
            node.children.append(child_node)
            continue

        child_node = Symbol(pos=token[1], text=token[0])
        node.children.append(child_node)

    return node

def assert_node(node, node_type, text=None, error_description=''):
    result = match_node(node, node_type, text)

    if not result:
        raise SyntaxException(node.pos, error_description)

    return result

def assert_child(node, child_idx, child_type, text=None, error_description=''):
    result = match_child(node, child_idx, child_type, text)

    if not result:
        raise SyntaxException(node.pos, error_description)

    return result

def match_node(node, node_type, text=None):
    if not isinstance(node_type, list):
        node_type = [node_type]

    if text != None and not isinstance(text, list):
        text = [text]

    if any([isinstance(node, t) for t in node_type]):
        if text != None:
            if any([node.text == t for t in text]):
                return node

            return None

        return node

    return None

def match_child(node, child_idx, child_type, text=None):
    if child_idx < len(node.children):
        child_node = node.children[child_idx]
        return match_node(child_node, child_type, text)

    return None
