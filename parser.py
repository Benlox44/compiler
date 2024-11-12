import ply.yacc as yacc
from lexer import tokens

# Tabla de variables en tiempo de ejecución
variables = {}
functions = {}

# Precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQ', 'NEQ'),
    ('left', 'LESS', 'GREATER', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MODULO'),
    ('right', 'NOT'),
    ('right', 'MINUS'),  # Es posible que aquí esté la duplicación
)

# ========================
# CLASES DEL AST (Árbol de Sintaxis Abstracta)
# ========================

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

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self):
        left_val = self.left.evaluate()
        right_val = self.right.evaluate()
        
        # Define las operaciones binarias
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
    def __init__(self, expressions):
        self.expressions = expressions

    def execute(self):
        values = [expr.evaluate() for expr in self.expressions]
        print(*values)

class IfElse:
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block

    def execute(self):
        if self.condition.evaluate():
            return self.if_block.execute()
        elif self.else_block:
            return self.else_block.execute()

class Block:
    def __init__(self, statements):
        self.statements = statements

    def execute(self):
        for stmt in self.statements:
            result = stmt.execute()
            if isinstance(result, Return):
                return result
        return None

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

# Clases para funciones
class Function:
    def __init__(self, name, parameters, block):
        self.name = name
        self.parameters = parameters
        self.block = block

    def execute(self, args):
        prev_variables = variables.copy()
        for param, arg in zip(self.parameters, args):
            variables[param] = arg.evaluate()

        result = self.block.execute()
        if isinstance(result, Return):
            result = result.evaluate()

        variables.update(prev_variables)
        return result

class FunctionCall:
    def __init__(self, name, arguments):
        self.name = name
        self.arguments = arguments

    def evaluate(self):
        if self.name == 'input':
            if len(self.arguments) == 0:
                return input()
            elif len(self.arguments) == 1:
                prompt = self.arguments[0].evaluate()
                return input(str(prompt))
            else:
                raise SyntaxError("La función 'input' acepta como máximo un argumento.")
        else:
            func = functions.get(self.name)
            if not func:
                raise ValueError(f"Undefined function '{self.name}'")
            return func.execute(self.arguments)

    def execute(self):
        return self.evaluate()

class List:
    def __init__(self, elements):
        self.elements = elements

    def evaluate(self):
        return [element.evaluate() for element in self.elements]

    def get_item(self, index):
        return self.elements[index].evaluate()

class ListAccess:
    def __init__(self, list_expr, index_expr):
        self.list_expr = list_expr
        self.index_expr = index_expr

    def evaluate(self):
        list_value = self.list_expr.evaluate()
        index_value = self.index_expr.evaluate()
        return list_value[index_value]

class Return:
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self):
        result = self.expression.evaluate()
        return result
    
    def execute(self):
        return self

# Nueva clase para declaraciones de expresiones
class ExpressionStatement:
    def __init__(self, expression):
        self.expression = expression

    def execute(self):
        self.expression.evaluate()

# Nueva clase Input para manejar la función input()
class Input:
    def __init__(self, prompt=None):
        self.prompt = prompt

    def evaluate(self):
        if self.prompt:
            prompt_value = self.prompt.evaluate()
            user_input = input(str(prompt_value))
        else:
            user_input = input()
        
        # Intentar convertir la entrada a entero
        try:
            return int(user_input)
        except ValueError:
            pass  # No es entero, intentar flotante
        
        # Intentar convertir la entrada a flotante
        try:
            return float(user_input)
        except ValueError:
            pass  # No es flotante, devolver cadena original
        
        # Devolver la cadena original si no es número
        return user_input

# ========================
# REGLAS DE LA GRAMÁTICA
# ========================

def p_program(p):
    'program : statement_list'
    statements = [stmt for stmt in p[1] if stmt is not None]
    for statement in statements:
        statement.execute()

def p_statement_list(p):
    '''statement_list : statement_list statement
                      | statement'''
    if len(p) == 3:
        if p[2] is not None:
            p[1].append(p[2])
        p[0] = p[1]
    else:
        p[0] = [p[1]]

def p_statement(p):
    '''statement : print_statement
                 | assign_statement
                 | if_statement
                 | for_statement
                 | while_statement
                 | function_definition
                 | return_statement
                 | expression SEMICOLON'''
    if len(p) == 3:
        p[0] = ExpressionStatement(p[1])
    else:
        p[0] = p[1]

def p_print_statement(p):
    'print_statement : PRINT LPAREN print_arguments RPAREN SEMICOLON'
    p[0] = Print(p[3])

def p_print_arguments_multiple(p):
    'print_arguments : print_arguments COMMA expression'
    p[0] = p[1] + [p[3]]

def p_print_arguments_single(p):
    'print_arguments : expression'
    p[0] = [p[1]]

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

def p_function_definition(p):
    'function_definition : FUNC ID LPAREN parameters RPAREN block'
    functions[p[2]] = Function(p[2], p[4], p[6])
    p[0] = None

def p_parameters(p):
    '''parameters : ID
                  | parameters COMMA ID
                  | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_function_call(p):
    '''expression : ID LPAREN arguments RPAREN
                  | INPUT LPAREN arguments RPAREN'''
    if p.slice[1].type == 'INPUT':
        if len(p[3]) == 0:
            p[0] = Input()
        elif len(p[3]) == 1:
            p[0] = Input(p[3][0])
        else:
            raise SyntaxError("La función 'input' acepta como máximo un argumento.")
    else:
        p[0] = FunctionCall(p[1], p[3])

def p_arguments(p):
    '''arguments : expression
                 | arguments COMMA expression
                 | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []

def p_return_statement(p):
    'return_statement : RETURN expression SEMICOLON'
    p[0] = Return(p[2])

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

def p_expression_negative(p):
    'expression : MINUS expression %prec MINUS'
    p[0] = BinOp(Number(0), '-', p[2])

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

def p_expression_list(p):
    'expression : LBRACKET elements RBRACKET'
    p[0] = List(p[2])

def p_expression_list_access(p):
    'expression : expression LBRACKET expression RBRACKET'
    p[0] = ListAccess(p[1], p[3])

def p_elements_multiple(p):
    'elements : elements COMMA expression'
    p[0] = p[1] + [p[3]]

def p_elements_single(p):
    'elements : expression'
    p[0] = [p[1]]

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
