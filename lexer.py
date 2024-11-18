import ply.lex as lex

# Palabras reservadas (incluyendo 'input')
reserved = {
    'print': 'PRINT',
    'input': 'INPUT',  
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
    'func': 'FUNC',
    'return': 'RETURN'
}

# Lista de tokens
tokens = [
    'NUMBER', 'ID', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO',
    'LPAREN', 'RPAREN', 'STRING', 'CHAR', 'SEMICOLON', 'LESS', 'GREATER',
    'LEQ', 'GEQ', 'LBRACE', 'RBRACE', 'AND', 'OR', 'NOT', 'BOOLEAN',
    'EQ', 'NEQ', 'COMMA', 'LBRACKET', 'RBRACKET'
] + list(reserved.values())

# Reglas de expresiones regulares para tokens simples
t_EQ = r'=='
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'
t_LESS = r'<'
t_GREATER = r'>'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_AND = r'&&'
t_OR = r'\|\|'
t_NOT = r'!'
t_COMMA = r','
t_LBRACKET = r'\['
t_RBRACKET = r'\]'

# Ignorar espacios y tabs
t_ignore = ' \t'

# Token para cadenas de caracteres (comillas dobles)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remover las comillas
    return t

# Token para caracteres individuales (comillas simples)
def t_CHAR(t):
    r"\'([^\\\n]|(\\.))\'"
    t.value = t.value[1:-1]  # Remover las comillas
    return t

# Token para booleanos (true/false)
def t_BOOLEAN(t):
    r'\btrue\b|\bfalse\b'
    t.value = True if t.value == 'true' else False
    return t

# Token para identificadores (variables y palabras reservadas)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # Verificar si es una palabra reservada
    t.type = reserved.get(t.value, 'ID')
    return t

# Token para números (enteros y flotantes)
def t_NUMBER(t):
    r'\d+(\.\d+)?'
    if '.' in t.value:
        t.value = float(t.value)
    else:
        t.value = int(t.value)
    return t

# Token para comentarios (líneas que comienzan con //)
def t_COMMENT(t):
    r'//.*'
    pass  # Ignorar los comentarios

# Contador de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}' en la línea {t.lexer.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

if __name__ == "__main__":
    # Prueba de tokenización
    with open('input.txt', 'r', encoding='utf-8') as file:
        lexer.input(file.read())
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
