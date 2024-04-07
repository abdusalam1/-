import ply.yacc as yacc
import ply.lex as lex
import sys
from lex import Lexer
lexi=Lexer()
lexi.build()
tokens=lexi.tokens

from AST_structure import *

pscal=Program()



def p_programstruct(p):
    'programstruct : program_head SEMICOLON program_body POINT'
    

def p_program_head(p):
    'program_head : PROGRAM ID LPAREN idlist RPAREN '


def p_program_head_jusi_id(p):
    'program_head :  PROGRAM ID'

def p_program_body(p):
    '''program_body : const_declarations   var_declarations  subprogram_declarations compound_statement'''
    
def p_empty(p):
    'empty :'


def p_idlist(p):
    'idlist : ID '
    
def p_idlist_2(p):
    'idlist : idlist COM ID'

def p_const_declerations_empty(p):
    'const_declarations : empty'
    p[0]={
        
    }

def p_const_declerations(p):
    'const_declarations :  CONST const_declaration SEMICOLON'


def p_const_decleration(p):
    'const_declaration : ID EQUAL const_value '

def p_const_decleration_2(p):
    'const_declaration : const_declaration SEMICOLON ID EQUAL const_value'

def p_const_value_addop(p):
    "const_value : ADDOP num "

def p_const_value_num(p):
    "const_value :  num "

def p_const_value_letter(p):
    "const_value :  LETTERS "

def p_num_fraction(p):
    'num : DIGITS fraction '

def p_num_digit(p):
    'num :  DIGITS'

def p_fraction(p):
    'fraction : POINT DIGITS'

def p_var_declarations(p):
    'var_declarations : VAR  var_declaration SEMICOLON'

def p_var_declarations_empty(p):
    'var_declarations : empty '

def p_var_declaration(p):
    'var_declaration : idlist COLON type'

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

def p_formal_parameter_empty(p):
    'formal_parameter : empty'


def p_parameter_list(p):
    'parameter_list : parameter'

def p_parameter_list_2(p):
    'parameter_list : parameter_list SEMICOLON parameter'

def p_parameter(p):
    'parameter : var_parameter'

def p_parameter_value(p):
    'parameter : value_parameter'

def p_var_parameter(p):
    'var_parameter : VAR value_parameter'

def p_value_parameter(p):
    'value_parameter : idlist COLON basic_type'

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
    'expression : simple_expression RELOP simple_expression'
    # 在这里处理带有关系运算符的表达式情况

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
    'factor : num'
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
def p_error(p):
    print("语法错误")

# 建立语法分析器

parser = yacc.yacc()

