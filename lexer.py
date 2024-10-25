import ply.lex as lex

# Reserved words (sin 'true' y 'false')
reserved = {
    'print': 'PRINT',
    'if': 'IF',
    'else': 'ELSE'
}

# List of tokens
tokens = [
    'NUMBER', 'ID', 'EQUALS', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE',
    'LPAREN', 'RPAREN', 'STRING', 'CHAR', 'SEMICOLON', 'LESS', 'GREATER',
    'LEQ', 'GEQ', 'LBRACE', 'RBRACE', 'AND', 'OR', 'NOT', 'BOOLEAN',
    'EQ', 'NEQ'
] + list(reserved.values())

# Regular expression rules for tokens
t_EQ = r'=='
t_NEQ = r'!='
t_LEQ = r'<='
t_GEQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
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

# Ignore spaces and tabs
t_ignore = ' \t'

# Token for strings (double quotes)
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
    return t

# Token for character literals (single quotes)
def t_CHAR(t):
    r"\'([^\\\n]|(\\.))\'"
    t.value = t.value[1:-1]
    return t

# Token for booleans (true/false)
def t_BOOLEAN(t):
    r'true|false'
    t.value = True if t.value == 'true' else False
    return t

# Token for identifiers (variables)
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Token for numbers
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'//.*'
    pass  # Ignorar los comentarios

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
