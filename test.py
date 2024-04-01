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

literals = [';', '.', '(', ')', ',', ':', '[', ']', '\'', '=']

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
    r'>=|<=|<>|<|>'
    return t

def t_ADDOP(t):
    r'\+|-'
    return t

def t_MULOP(t):
    r'\*|/'
    return t

def t_COMMENT(t):
    r'\{[^{}]*\}|//.*'
    pass
    # No return value. Token discarded

# Define a rule so we can track line numbers while finding the error 101
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Compute column.
# input is the input text string
# token is a token instance
def find_column(data,token):
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

def Lexical(filename):
    # Build the lexer
    lexer = lex.lex()
    filename = filename + ".pas"
    file = open(filename).readlines()
    for i in file:
        if len(i) > 1000:
            print(f"Line {file.index(i)} too long")
            exit()
        else:
            data = data + ''.join(i).lower()
    # Give the lexer some input
    lexer.input(data)


    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
                break      # No more input
        else:
            if find_column(data, tok) + len(tok.value) < 10000:
                ans.append(tok)
            else:
                exit()


ans = list()
Lexical("08_add2")
# print(ans)