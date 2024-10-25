import ply.yacc as yacc
from lexer import tokens

# Runtime symbol table for storing variables
variables = {}

# Arithmetic operation precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
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

class Variable:
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        return variables.get(self.name, f"Undefined variable '{self.name}'")

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
                 | assign_statement'''
    p[0] = p[1]

def p_print_statement(p):
    'print_statement : PRINT LPAREN expression RPAREN SEMICOLON'
    p[0] = Print(p[3])

def p_assign_statement(p):
    'assign_statement : ID EQUALS expression SEMICOLON'
    p[0] = Assign(p[1], p[3])

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = BinOp(p[1], p[2], p[3])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Number(p[1])

def p_expression_string(p):
    'expression : STRING'
    p[0] = String(p[1])

def p_expression_variable(p):
    'expression : ID'
    p[0] = Variable(p[1])

def p_error(p):
    if p:
        print(f"Syntax error at token '{p.value}' on line {p.lineno}")
    else:
        print("Syntax error: Unexpected end of input")

# Build the parser
parser = yacc.yacc(start='program')
