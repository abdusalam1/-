import ply.lex as lex

reserved = {
    'program': 'PROGRAM',
    'const': 'CONST',
    'type': 'TYPE',
    'record': 'RECORD',
    'array': 'ARRAY',
    'of': 'OF',
    'var': 'VAR',
    'function': 'FUNCTION',
    'procedure': 'PROCEDURE',
    'begin': 'BEGIN',
    'end': 'END',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'case': 'CASE',
    'while': 'WHILE',
    'repeat': 'REPEAT',
    'until': 'UNTIL',
    'for': 'FOR',
    'to': 'TO',
    'downto': 'DOWNTO',
    'do': 'DO',
    'read': 'READ',
    'write': 'WRITE',
    'readIn': 'READIN',
    'writeIn': 'WRITEIN',
    'not': 'NOT',
    'integer': 'INTERGER',
    'real': 'REAL',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE',
}

tokens = ['DIGITS','NUM','LETTERS','RELOP','ADDOP','MULOP','ID','ASSIGNOP','COMMENT','DOT'
          ] + list(reserved.values())

literals = [';', '.', '(', ')', ',', ':', '[', ']', '\'']

def t_DOT(t):
    r'\.\.'
    return t

def t_ASSIGNOP(t):
    r':='
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

def t_DIGITS(t):
    r'\d+'
    return t

def t_LETTERS(t):
    r"'[^'\n]'"
    return t

def t_RELOP(t):
    r'>=|<=|<>|<|>|='
    return t

def t_ADDOP(t):
    r'\+|-|or'
    return t

def t_MULOP(t):
    r'\*|/|and|div|mod'
    return t

def t_COMMENT(t):
    r'\{[^{}]*\}|//.*'
    pass
    # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
# input is the input text string
# token is a token instance
def find_column(input,token):
    last_cr = data.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = token.lexpos - last_cr
    return column

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

t_ignore  = ' \t'

# Build the lexer
lexer = lex.lex()

# Test it out
data = '''
3 + 4 * 10
    + -{548548}20 *2
    array[0..9,0..1]
    a=2.1
a= 0aq
'''

# Give the lexer some input
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: break      # No more input
    print (tok, tok.type, tok.value, tok.lineno, find_column(tok.value,tok))