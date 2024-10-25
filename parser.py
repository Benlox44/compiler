import ply.yacc as yacc
from lexer import tokens

# Runtime symbol table for variables
variables = {}

# Operator precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LESS', 'GREATER', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('right', 'NOT'),  # Unary NOT operator
)

# AST node classes
class Number:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class String:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Char:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Boolean:
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name not in variables:
            raise ValueError(f"Undefined variable '{self.name}'")
        return variables[self.name]
class WhileLoop:
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def execute(self):
        while self.condition.evaluate():
            self.block.execute()

class ForLoop:
    def __init__(self, init, condition, update, block):
        self.init = init
        self.condition = condition
        self.update = update
        self.block = block

    def execute(self):
        self.init.execute()
        while self.condition.evaluate():
            self.block.execute()
            self.update.execute()

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()

        if self.op == '+': return left_val + right_val
        if self.op == '-': return left_val - right_val
        if self.op == '*': return left_val * right_val
        if self.op == '/': return left_val / right_val
        if self.op == '<': return left_val < right_val
        if self.op == '>': return left_val > right_val
        if self.op == '<=': return left_val <= right_val
        if self.op == '>=': return left_val >= right_val
        if self.op == '==': return left_val == right_val
        if self.op == '!=': return left_val != right_val
        if self.op == '&&': return left_val and right_val
        if self.op == '||': return left_val or right_val

class NotOp:
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        return not self.expression.evaluate()

class Assign:
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def execute(self):
        variables[self.name] = self.expression.evaluate()

class Print:
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        print(self.expression.evaluate())

class IfElse:
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def execute(self):
        if self.condition.evaluate():
            self.if_block.execute()
        elif self.else_block:
            self.else_block.execute()

class Block:
    def __init__(self, statements):
        self.statements = statements

    def execute(self):
        for stmt in self.statements:
            stmt.execute()

# Grammar rules
def p_program(p):
    'program : statement_list'
    for statement in p[1]:
        statement.execute()

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : print_statement
                 | assign_statement
                 | if_statement
                 | for_statement
                 | while_statement'''
    p[0] = p[1]

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = Print(p[3])

def p_assign_statement(p):
    'assign_statement : ID EQUALS expression SEMICOLON'
    p[0] = Assign(p[1], p[3])

def p_assign_expression(p):
    'assign_expression : ID EQUALS expression'
    p[0] = Assign(p[1], p[3])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block else_if_opt'''
    p[0] = IfElse(p[3], p[5], p[6])

def p_else_if_opt(p):
    '''else_if_opt : ELSE IF LPAREN expression RPAREN block else_if_opt
                   | ELSE block
                   | empty'''
    if len(p) == 8:
        # Create an IfElse node for 'else if' chains
        p[0] = IfElse(p[4], p[6], p[7])
    elif len(p) == 3:
        # Handle final 'else' block
        p[0] = p[2]
    else:
        # No 'else if' or 'else' block
        p[0] = None

def p_while_statement(p):
    'while_statement : WHILE LPAREN expression RPAREN block'
    p[0] = WhileLoop(p[3], p[5])

def p_for_statement(p):
    '''for_statement : FOR LPAREN assign_expression SEMICOLON expression SEMICOLON assign_expression RPAREN block'''
    p[0] = ForLoop(p[3], p[5], p[7], p[9])

def p_block(p):
    'block : LBRACE statement_list RBRACE'
    p[0] = Block(p[2])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression LESS expression
                  | expression GREATER expression
                  | expression LEQ expression
                  | expression GEQ expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression AND expression
                  | expression OR expression'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_not(p):
    'expression : NOT expression'
    p[0] = NotOp(p[2])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = String(p[1])

def p_expression_char(p):
    'expression : CHAR'
    p[0] = Char(p[1])

def p_expression_boolean(p):
    'expression : BOOLEAN'
    p[0] = Boolean(p[1])

def p_expression_variable(p):
    'expression : ID'
    p[0] = Variable(p[1])

def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error: Unexpected end of input")

# Build the parser
parser = yacc.yacc(start='program')
