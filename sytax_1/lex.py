import ply.lex as lex
import sys
#lex
class Lexer:
    error=[]#错误列表 
    data=None#输入数据
    COMMENT={}#注释集合字典 （行号，列号）："注释内容"
    lexer=None
    def build(self,filename,**kwargs):
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
        }
        reserved_2={
                'div': 'MULOP',
                'mod': 'MULOP',
                'and': 'MULOP',
                'or': 'ADDOP',
            }

        tokens = ['DIGITS','NUM','LETTERS','RELOP','ADDOP','MULOP','ID','ASSIGNOP','comment','DOT','COLON','LBRACKET','RBRACKET','LPAREN','RPAREN',
                    'COM','POINT','SEMICOLON','EQUAL'
                    ] + list(reserved.values())
        #状态转移元组
        states = (
                ('comment','exclusive'),
                )
        t_EQUAL=r'='
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
        t_RELOP = r'<=|>=|<>|<|>'
        t_ADDOP = r'(?i)\+|-'
        t_MULOP = r'(?i)\*|\/'

    # Match the first {. Enter comment state.
        def t_comment(t):
            r'\{'
            t.lexer.code_start = t.lexer.lexpos        # Record the starting position
            t.lexer.level = 1                          # Initial brace level
            t.lexer.begin('comment')                     # Enter 'ccode' state

    # Rules for the comment state
        def t_comment_lbrace(t):     
            r'\{'
            t.lexer.level +=1            

        def t_comment_rbrace(t):
            r'\}'
            t.lexer.level -=1

            # If closing brace, return the code fragment
            if t.lexer.level == 0:
                t.value=t.lexer.lexdata[t.lexer.code_start:t.lexer.lexpos+1]
                self.COMMENT[(t.lineno,self.find_column(self.data,t))] = t.value.split('{')[-1].split('}')[0] #去括号
                t.lexer.lineno += t.value.count('\n')
                t.lexer.begin('INITIAL')           #回归原状态
                pass

        def t_comment_LETTERS(t):
            r'[^{}]+'
            if t.value[-1] != self.data[-1] :
                pass
            else:#右花括号缺失
                self.error.append({
                            "code": "A-09",
                                "info": {
                                    "line": t.lineno,
                                    "value": ['Comment_Eof'],
                                    "column": self.find_column(self.data,t)
                        }})   
                # 恢复=》转成单行注释
                flag = t.lexer.lexpos+(t.value.find('\n')-len(t.value)) # 确认lex回移下标
                self.COMMENT[(t.lineno,self.find_column(self.data,t))]=t.lexer.lexdata[t.lexer.code_start:flag] #添加注释 
                t.lexer.lineno += t.lexer.lexdata[t.lexer.code_start:flag].count('\n') #增加行号
                t.lexer.lexpos = flag
                t.lexer.begin('INITIAL') #回归原状态

# Ignored characters 
        t_comment_ignore = " " 

# For bad characters, we just skip over it
        def t_comment_error(t):
            t.lexer.skip(1)
            
        def t_LETTERS(t):
                    r'\'[^\']*\'*'
                    t.value=t.value[1:] if len(t.value)!=1 else 'eof' #获取引号内内容
                    if t.value[-1]!='\'' or t.value=='eof': #引号未关闭
                        self.error.append({
                            "code": "A-05",
                                    "info": {
                                        "line": t.lineno,
                                        "value": ['Letter_Eof'],
                                        "column": self.find_column(self.data,t)
                        }})
                        index=t.value.find('\n')
                        t.lexer.skip(index-len(t.value)) #前进至换行符前
                        t.value=t.value[0] if t.value[0] else '\0' #取第一个字符为值
                    elif t.value=='\'': #字符常量为空
                        self.error.append({
                            "code": "A-06",
                                    "info": {
                                        "line": t.lineno,
                                        "value": ['Letter_Empty'],
                                        "column": self.find_column(self.data,t)
                        }})
                        t.value="\0" #取"\0"为值
                    elif '\n'in t.value:#字符常量先遇见换行符而非引号
                        self.error.append({
                            "code": "A-08",
                                    "info": {
                                        "line": t.lineno,
                                        "value": ['Letter_newline'],
                                        "column": self.find_column(self.data,t)
                        }})
                        index=t.value.find('\n')
                        t.lexer.skip(index-len(t.value)) #前进至换行符前
                        t.value=t.value[0] if t.value[0]!='\n' else "\0" #错误恢复,取第一个字符或"\0"为值
                    elif len(t.value[:-1])>1:
                        self.error.append({
                                "code": "A-07",
                                "info": {
                                    "line": t.lineno,
                                    "value": "字符过多:'"+t.value.split('\n')[0],
                                    "column": self.find_column(self.data,t)
                                }
                            })
                        t.value=t.value[0]
                    else:
                        t.value=t.value[:-1]
                    return t
        #浮点数
        def t_NUM(t):
            r'\d+\.\d+'
            t.value = float(t.value)
            return t
        def t_ID(t):
            r'[0-9a-zA-Z_][a-zA-Z_0-9]*'
            t.type = dict(reserved, **reserved_2).get(t.value,'ID')    # Check for reserved words
            if t.value.isdigit():
                    t.type='DIGITS'
                    t.value=int(t.value)
            if(t.type=='ID'):
                if len(t.value)>=20:
                    self.error.append({
                                "code": "A-02",
                                "info": {
                                    "line": t.lineno,
                                    "value": [t.value.split('\n')[0]],
                                "column": self.find_column(self.data,t)
                                }
                            })
                    t.value=t.value[:20]
                if t.value[0].isdigit() :  # 出现ID以数字开头的错误
                            self.error.append({
                                "code": "A-04",
                                "info": {
                                    "line": t.lineno,
                                    "value": [t.value.split('\n')[0]],
                                    "column": self.find_column(self.data,t)
                                }
                            })
                            while t.value[0].isdigit():
                                    t.value = t.value[1:]  # 错误恢复：如果ID首元素是数字，则去掉该数字
            return t
        #整数
        def t_DIGITS(t):
            r'\d+'
            t.value = int(t.value)
            return t
        
        # Define a rule so we can track line numbers
        def t_newline(t):
                r'\n+'
                t.lexer.lineno += t.value.count('\n')

        # 非法字符 handling rule
        def t_error(t):
                        self.error.append({  # 不在已有错误中，则为词法分析中的非法字符错误
                            "code": "A-03",
                            "info": {
                                "line": t.lineno,
                                "value": [t.value.split('\n')[0]],
                                "column": self.find_column(self.data,t)
                            }
                        })
                        t.lexer.skip(1)  # 错误处理：跳过该错误

        t_ignore  = ' \t'    
        self.lexer = lex.lex()
        with open(filename,'r',encoding='utf-8') as file: # input
            dataline=file.readlines()
            for i in range(0,len(dataline)):
                  if len(dataline[i])>100:
                        print(f"{'ERROR':^20}")
                        print(f"{'code:A-01'!s:<10}  {f'line:{str(i+1)}'!s:<3}   {'value:代码行长度过长'!s:<10}")
                        return 
            self.data=''.join(dataline).replace('\xa0',' ').lower()#转空格、小写  
            self.lexer.input(self.data) 
    def find_column(self,data,token,**kwargs):
            last_cr = data.rfind('\n',0,token.lexpos)
            if last_cr < 0:
                last_cr = 0
            column = token.lexpos - last_cr
            return column
    
    def debug(self,debug):
        if debug==1 :
            print(f"{'TOKEN':^20}\n{'type':<10} {'line':<5} {'column':<7} {'value':<8}")
            for tok in self.lexer:
                print(f'{tok.type:<10} {tok.lineno:<5} {self.find_column(self.data,tok):<7} {tok.value:<8}')
            if self.error != []:
                print(f"{'ERROR':^20}")
                print(f"{'code'!s:<5}  {'line'!s:<5} {'column'!s:<7} {'value'!s:<10}")
                for item in self.error:
                    print(f"{item['code']!s:<5}  {item['info']['line']!s:<5} {item['info']['column']!s:<7} {item['info']['value']!s:<10}")

if __name__ == '__main__':
     lexi=Lexer()
     lexi.build('lex_test\comment.pas')
     #lexi.debug('lex_test\id.pas',1)
     #lexi.debug(debug=int(sys.argv[2]))
     #输出注释，可通过成员变量COMMENT访问
     lexi.debug(1)
     print(f"{'COMMENT':^20}") if lexi.COMMENT!={} else print('无注释')
     for key,value in lexi.COMMENT.items():
           print(f'line:{key[0]!s:<5} column:{key[1]!s:<5} value:{value!s:<10}')
