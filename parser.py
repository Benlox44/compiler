import ply.yacc as yacc
from lexer import tokens

# Tabla de variables en tiempo de ejecución
variables = {}

# Precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LESS', 'GREATER', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),  # Operador unario NOT
)

# ========================
# CLASES DEL AST (Árbol de Sintaxis Abstracta)
# ========================

class Number:
    """Representa un número en el AST."""
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class String:
    """Representa una cadena en el AST."""
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Char:
    """Representa un carácter en el AST."""
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Boolean:
    """Representa un valor booleano en el AST."""
    def __init__(self, value):
        self.value = value

    def evaluate(self):
        return self.value

class Variable:
    """Representa una variable almacenada en la tabla de símbolos."""
    def __init__(self, name):
        self.name = name

    def evaluate(self):
        if self.name not in variables:
            raise ValueError(f"Undefined variable '{self.name}'")
        return variables[self.name]

class BinOp:
    """Representa una operación binaria (+, -, *, etc.)."""
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
        if self.op == '%': return left_val % right_val
        if self.op == '<': return left_val < right_val
        if self.op == '>': return left_val > right_val
        if self.op == '<=': return left_val <= right_val
        if self.op == '>=': return left_val >= right_val
        if self.op == '==': return left_val == right_val
        if self.op == '!=': return left_val != right_val
        if self.op == '&&': return left_val and right_val
        if self.op == '||': return left_val or right_val

class NotOp:
    """Representa una operación unaria NOT."""
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        return not self.expression.evaluate()

class Assign:
    """Representa una asignación a una variable."""
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def execute(self):
        variables[self.name] = self.expression.evaluate()

class Print:
    """Representa una instrucción de impresión."""
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        print(self.expression.evaluate())

class IfElse:
    """Representa una instrucción condicional."""
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
    """Representa un bloque de declaraciones."""
    def __init__(self, statements):
        self.statements = statements

    def execute(self):
        for stmt in self.statements:
            stmt.execute()

class WhileLoop:
    """Representa un bucle while."""
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def execute(self):
        while self.condition.evaluate():
            self.block.execute()

class ForLoop:
    """Representa un bucle for."""
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

# ========================
# REGLAS DE LA GRAMÁTICA
# ========================

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

def p_assign_expression(p):
    'assign_expression : ID EQUALS expression'
    p[0] = Assign(p[1], p[3])

def p_assign_statement(p):
    'assign_statement : assign_expression SEMICOLON'
    p[0] = p[1]

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN block else_if_opt'''
    p[0] = IfElse(p[3], p[5], p[6])

def p_else_if_opt(p):
    '''else_if_opt : ELSE IF LPAREN expression RPAREN block else_if_opt
                   | ELSE block
                   | empty'''
    if len(p) == 8:
        p[0] = IfElse(p[4], p[6], p[7])
    elif len(p) == 3:
        p[0] = p[2]
    else:
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
                  | expression MODULO expression
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

# Construir el parser
parser = yacc.yacc(start='program')
