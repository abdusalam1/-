import ply.lex as lex
#预处理


#lex
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
    'integer': 'INTEGER',
    'real': 'REAL',
    'boolean': 'BOOLEAN',
    'char': 'CHAR',
    'true': 'TRUE',
    'false': 'FALSE',
    'div': 'MULOP',
    'mod': 'MULOP',
    'and': 'MULOP',
    'or': 'ADDOP',
}

tokens = ['DIGITS','NUM','LETTERS','RELOP','ADDOP','MULOP','ID','ASSIGNOP','COMMENT','DOT'
          ] + list(reserved.values())

literals = [';', '.', '(', ')', ',', ':', '[', ']','=']

t_COLON = r':'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COM = r','
t_POINT = r'\.'
t_DOT=r'\.\.'
t_SEMICOLON = r';'
t_ASSIGNOP=r':='
t_LETTERS = r'\'[a-zA-Z]\''
t_RELOP = r'<=|>=|<>|<|>'
t_ADDOP = r'(?i)\+|-|OR'
t_MULOP = r'(?i)\*|\/|DIV|MOD|AND'
t_DIGITS=r'\d+'

def t_ID(t):
    r'[0-9a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    if t.value.isdigit():
             t.type='DIGITS'
    if(t.type=='ID'):
        if len(t.value)>=20:
             error.append({
                        "code": "A-03",
                        "info": {
                            "line": t.lineno,
                            "value": [t.value.split('\n')[0]],
                            "lexpos": t.lexpos
                        }
                    })
             t.value=t.value[:20]
        if t.value[0].isdigit() :  # 出现ID以数字开头的错误
                    error.append({
                        "code": "A-01",
                        "info": {
                            "line": t.lineno,
                            "value": [t.value.split('\n')[0]],
                            "lexpos": t.lexpos
                        }
                    })
                    while t.value[0].isdigit():
                        t.value = t.value[1:]  # 错误恢复：如果ID首元素是数字，则去掉该数字
    return t

def t_COMMENT(t):
    r'\{[^{}]*\}|//.*'
    t.lexer.lineno += t.value.count('\n')
    pass
    # No return value. Token discarded

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count('\n')

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
            error.append({  # 不在已有错误中，则为词法分析中的非法字符错误
                "code": "A-02",
                "info": {
                    "line": t.lineno,
                    "value": [t.value.split('\n')[0]],
                    "lexpos": t.lexpos
                }
            })
            t.lexer.skip(1)  # 错误处理：跳过该错误

t_ignore  = ' \t'

# Build the lexer
lexer = lex.lex()

def Lexical(filename):
    # Build the lexer
    lexer = lex.lex()
    filename = filename + ".pas"
    data = '''
     type 1aaaaaaaaaaaaaaaaaaaaa=1.2;
     a='ab'
'''
    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
                break      # No more input
        else:
            if find_column(data, tok)  < 1000:
                ans.append(tok)
            else:
                exit()

error=[]
ans = list()
Lexical("08_add2")
print(ans)
print(error)
