import ply.yacc as yacc
from lexer import tokens

# Tabla de símbolos para almacenar variables
variables = {}

# Reglas gramaticales

# Asignación de variables
def p_assignment(p):
    'statement : ID EQUALS expression'
    variables[p[1]] = p[3]  # Guardar la variable en la tabla de símbolos

# Print de expresiones o variables
def p_print_statement(p):
    'statement : PRINT LPAREN expression RPAREN'
    print(p[3])

# Uso de variables en expresiones
def p_expression_variable(p):
    'expression : ID'
    p[0] = variables.get(p[1], f"Error: Variable '{p[1]}' no definida")

# Operaciones aritméticas
def p_expression_plus(p):
    'expression : expression PLUS term'
    p[0] = p[1] + p[3]

def p_expression_minus(p):
    'expression : expression MINUS term'
    p[0] = p[1] - p[3]

def p_term_multiply(p):
    'term : term MULTIPLY factor'
    p[0] = p[1] * p[3]

def p_term_divide(p):
    'term : term DIVIDE factor'
    p[0] = p[1] / p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = p[1]

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

# Manejo de errores sintácticos
def p_error(p):
    print("Error de sintaxis")

# Construir el analizador sintáctico
parser = yacc.yacc()
