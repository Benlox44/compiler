import ply.lex as lex

# List of reserved words (currently only 'print')
reserved = {
    'print': 'PRINT'
}

# List of tokens
tokens = [
    'NUMBER', 'ID', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'STRING', 'SEMICOLON'
] + list(reserved.values())

# Regular expression rules for tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_SEMICOLON = r';'

# Ignore spaces and tabs
t_ignore = ' \t'

# Token for strings
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Remove quotes
    return t

# Token for identifiers (variables)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')  # Check if it's a reserved word
    return t

# Token for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert to integer
    return t

# Track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Handle errors
def t_error(t):
    print(f"Illegal character '{t.value[0]}' at line {t.lexer.lineno}")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
