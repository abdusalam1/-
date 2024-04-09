import ply.yacc as yacc
import ply.lex as lex
import sys
from lex import Lexer
lexi=Lexer()
lexi.build()
tokens=lexi.tokens

from AST_structure import *



class parser():
    # pascal=Program()
    parse=None
    Symboltable=SymbolTable()
    error=[]
    def child(self):
        def p_programstruct(p):
            'programstruct : program_head SEMICOLON program_body POINT'
            # 语法树节点信息，记录上述产生式下非终结符的节点信息，下同
            p[0] = {
                        "length": len(p),
                        "type": "programstruct",
                        "program_head": p[1],
                        "program_body": p[3]
                    }
            # 符号表信息由 program_body 获取
        #    self.Symboltable =p[3]['symbolTable']
                    

        def p_program_head(p):
            'program_head : PROGRAM ID LPAREN idlist RPAREN '
           # p[0]=Program(p[2],p.lineno(1),p[4])

        # def p_program_head_error(p):
        #     'program_head : PROGRAM ID LPAREN error RPAREN '
        #     print("hfukaelfvgbkle")

        def p_program_head_jusi_id(p):
            'program_head :  PROGRAM ID'
           # p[0]=Program(p[2],p.lineno(1),'null')
        
        def p_program_body(p):
            '''program_body : const_declarations   var_declarations  subprogram_declarations compound_statement'''
           # p[0]=SubProgram(p[1],p[2],p[3],p[4])
            # 符号表信息
        #    p[0]['symbolTable']=SymbolTable('program_body',p[1]['constant'],p[2]['Variant'],p[3]['symbol Table'])
        def p_empty(p):
            'empty :'
            p[0]=None

        def p_idlist(p):
            '''idlist : ID 
                    | idlist COM ID'''
            if len(p)==2:
                p[0]={p[1]:p.lineno(1)}
            else:
                if p[1].get(p[3])== None : #判断重复
                    p[1][p[3]]=p.lineno(3)
                    p[0]=p[1]
                else:
                    self.error.append({
                        'type':'变量重复',
                        'line':p.lineno(3)
                    })

        def p_const_declerations_empty(p):
            'const_declarations : empty'
            p[0]=p[1]

        def p_const_declerations(p):
            'const_declarations :  CONST const_declaration SEMICOLON'
            #语法树
            p[0]=p[2]
            #符号表
            p[0]['constant']=p[2]['symbolTable']

        def p_const_decleration(p):
            'const_declaration : ID EQUAL const_value '
            p[0]={'constant':[Constant(p[1],p.lineno(1),p[3]['type'],p[3]['value'])]}
            #符号表
            p[0]['symbolTable']={p[1]:Constant(p[1],p.lineno(1),p[3]['type'],p[3]['value'])}
            
        def p_const_decleration_2(p):
            'const_declaration : const_declaration SEMICOLON ID EQUAL const_value'
            cur=[Constant(p[1],p.lineno(1),p[3]['type'],p[3]['value'])]
            p[0]=p[1]['constant']+cur
            #符号表
            cur={p[3]:Constant(p[1],p.lineno(1),p[3]['type'],p[3]['value'])}
            if p[1]['symbolTable'].get(p[3])==None:
                p[0]['symbolTable']=p[1]['symbolTable'].update(cur)
            else:
                [0]['symbolTable']=p[1]['symbolTable']
                self.error.append({
                        'type':'变量重复',
                        'line':p.lineno(3)
                    })
                
        def p_const_value_addop(p):
            '''const_value : ADDOP NUM
                        |    ADDOP DIGITS'''
            p[0]={
                'type':str(type(p[2]))[8:-2],
                'value':p[2] if p[1]=='+' else -p[2]
            }
        def p_const_value_num(p):
            '''const_value :  NUM 
                        |     DIGITS'''
            p[0]={
                'type':str(type(p[1]))[8:-2],
                'value':p[1] 
            }

        def p_const_value_letter(p):
            "const_value :  LETTERS "
            p[0]={
                'type':'str',
                'value':p[1]
            }

        def p_var_declarations(p):
            'var_declarations : VAR  var_declaration SEMICOLON'

        def p_var_declarations_empty(p):
            'var_declarations : empty '

        def p_var_declaration(p):
            'var_declaration : idlist COLON type'
            cursymbol={}

        def p_var_declaration_var(p):
            'var_declaration : var_declaration SEMICOLON idlist COLON type'

        def p_type(p):
            'type : basic_type '

        def p_type_array(p):
            'type :  ARRAY LBRACKET period RBRACKET OF basic_type'

        def p_basic_type_integer(p):
            'basic_type : INTEGER'

        def p_basic_type_real(p):
            'basic_type :  REAL '

        def p_basic_type_boolean(p):
            'basic_type : BOOLEAN '

        def p_basic_type_char(p):
            'basic_type : CHAR'

        def p_period(p):
            'period : DIGITS DOT DIGITS '

        def p_period_2(p):
            'period : period COM DIGITS DOT DIGITS'
            
        def p_subprogram_declarations(p):
            'subprogram_declarations : subprogram_declarations subprogram SEMICOLON '

        def p_subprogram_declarations_empty(p):
            'subprogram_declarations : empty '

        def p_subprogram(p):
            'subprogram : subprogram_head SEMICOLON subprogram_body'

        def p_subprogram_head_procedure(p):
            '''subprogram_head : PROCEDURE ID formal_parameter'''
            
        def p_subprogram_head_function(p):
            '''subprogram_head :  FUNCTION ID formal_parameter COLON basic_type'''
            
        def p_formal_parameter(p):
            'formal_parameter : LPAREN parameter_list RPAREN'
            p[0]=p[2]

        def p_formal_parameter_empty(p):
            'formal_parameter : empty'
            p[0]=p[1]


        def p_parameter_list(p):
            'parameter_list : parameter'
            para=FormalParameter()
            para.paraId=p[1]["paraId"]
            para.line=p[1]["linenum"]
            para.type=p[1]["type"]
            # 传值调用,引用调用的区分
            if p[1]["flag"]==True:
                para.flag=True
            p[0]=[para]

        def p_parameter_list_2(p):
            'parameter_list : parameter_list SEMICOLON parameter'
            para=FormalParameter()
            para.paraId=p[3]["paraId"]
            para.line=p[3]["linenum"]
            para.type=p[3]["type"]
            # 传值调用,引用调用的区分
            if p[1]["flag"]==True:
                para.flag=True
            p[0]=p[1].append(para)


        def p_parameter(p):
            'parameter : var_parameter'
            p[0]=p[1]

        def p_parameter_value(p):
            'parameter : value_parameter'
            p[1]["flag"]=False
            p[0]=p[1]

        def p_var_parameter(p):
            'var_parameter : VAR value_parameter'
            p[2]["flag"]=True
            p[0]=p[2]

        def p_value_parameter(p):
            'value_parameter : idlist COLON basic_type'
            p[0]={
                "type":p[3],
                "paraId":p[1].keys(),
                "linenum":p.lineno(2)
                }

        def p_subprogram_body(p):
            '''subprogram_body : const_declarations var_declarations  compound_statement'''

        def p_compound_statement(p):
            'compound_statement : BEGIN statement_list END'


        def p_statement_list(p):
            'statement_list : statement'

        def p_statement_list_2(p):
            'statement_list :  statement_list SEMICOLON statement'


        def p_statement_empty(p):
            'statement : empty'
            # 在这里处理空语句的情况

        def p_statement_variable_assign(p):
            'statement : variable ASSIGNOP expression'
            # 在这里处理变量赋值语句的情况

        def p_statement_func_assign(p):
            'statement : func_id ASSIGNOP expression'
            # 在这里处理函数赋值语句的情况

        def p_func_id(p):
            'func_id : ID'

        def p_statement_procedure_call(p):
            'statement : procedure_call'
            # 在这里处理过程调用语句的情况

        def p_statement_compound(p):
            'statement : compound_statement'
            # 在这里处理复合语句的情况

        def p_statement_if(p):
            'statement : IF expression THEN statement else_part'
            # 在这里处理条件语句的情况

        def p_statement_for(p):
            'statement : FOR ID ASSIGNOP expression TO expression DO statement'
            # 在这里处理for循环语句的情况

        def p_statement_read(p):
            'statement : READ LPAREN variable_list RPAREN'
            # 在这里处理读取语句的情况

        def p_statement_write(p):
            'statement : WRITE LPAREN expression_list RPAREN'
            # 在这里处理写入语句的情况
            
        def p_variable_list_single(p):
            'variable_list : variable'
            # 在这里处理只有一个变量的情况

        def p_variable_list_multiple(p):
            'variable_list : variable_list COM variable'
            # 在这里处理多个变量的情况


        def p_variable(p):
            'variable : ID id_varpart'

        def p_id_varpart_empty(p):
            'id_varpart : empty'
            # 在这里处理空的情况

        def p_id_varpart_with_indices(p):
            'id_varpart : LBRACKET expression_list RBRACKET'
            # 在这里处理带有索引的情况

        def p_procedure_call_no_args(p):
            'procedure_call : ID'
            # 在这里处理没有参数的过程调用情况

        def p_procedure_call_with_args(p):
            'procedure_call : ID LPAREN expression_list RPAREN'
            # 在这里处理带有参数的过程调用情况



        def p_else_part(p):
            'else_part : ELSE statement'

        def p_else_part_empty(p):
            'else_part : empty '

        def p_expression_list_single(p):
            'expression_list : expression'
            # 在这里处理只有一个表达式的情况

        def p_expression_list_multiple(p):
            'expression_list : expression_list COM expression'
            # 在这里处理多个表达式的情况


        def p_expression_simple(p):
            'expression : simple_expression'
            # 在这里处理单一简单表达式的情况

        def p_expression_with_relational_op(p):
            '''expression : simple_expression relop simple_expression
                            '''
            # 在这里处理带有关系运算符的表达式情况
        def p_relop(p):
            '''relop : RELOP 
                    | EQUAL'''

        def p_simple_expression_single_term(p):
            'simple_expression : term'
            # 在这里处理只有一个项的情况

        def p_simple_expression_with_addop(p):
            'simple_expression : simple_expression ADDOP term'
            # 在这里处理带有加法运算符的表达式情况


        def p_term_single_factor(p):
            'term : factor'
            # 处理只有一个因子的情况

        def p_term_with_mulop(p):
            'term : term MULOP factor'
            # 处理带有乘法运算符的表达式情况


        def p_factor_num(p):
            '''factor : NUM
                    | DIGITS'''
            # 处理数字的情况

        def p_factor_variable(p):
            'factor : variable'
            # 处理变量的情况

        def p_factor_expression(p):
            'factor : LPAREN expression RPAREN'
            # 处理表达式的情况

        def p_factor_function_call(p):
            'factor : ID LPAREN expression_list RPAREN'
            # 处理函数调用的情况

        def p_factor_not(p):
            'factor : NOT factor'
            # 处理NOT运算符的情况

        def p_factor_addop(p):
            'factor : ADDOP factor'
            # 处理一元运算符的情况

            
        # 错误处理
        # def p_error(p):
        #     print("语法错误")
        def p_error(p):
            raise yacc.YaccError("语法错误在第 %d 行，第 %d 列 %s" % (p.lineno, p.lexpos,p))

        self.parse=yacc.yacc()

# 建立语法分析器

pp=parser()
pp.child()
s=''' program example;
var x, y: integer;
function gcd(a, b: integer): integer;
begin 
if b=0 then gcd:=a
else gcd:=gcd(b, a mod b)
end;
begin
read(x, y);
write(gcd(x, y))
end. '''
result = pp.parse.parse(s)
print(result)

#parser = yacc.yacc()

