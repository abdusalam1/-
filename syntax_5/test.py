import ply.yacc as yacc
import ply.lex as lex
import sys
from lex import Lexer

from yaccnew import *


import os

name = list()
def traverse_folder(path):
    i=1
    for root, dirs, files in os.walk(path):
        for file in files:
            # 处理文件
            pp = parser()
            filename = sys.argv[1] if len(sys.argv) > 1 else os.path.join(root, file)
            try:
                [result,lex_error,comment] = pp.get_result(filename)
                Cfilename = filename.replace(".pas", ".c")
                #  print("代码生成：")
                codeg=CodeGenerator()
                codeg.ast=result["program"]
                codeg.anaAst()
                codeg.genHeadFile()
                codeg.output(Cfilename)
                codeg.AddComment(comment,Cfilename)
            except Exception as e:
                print(f'{filename}  {i}')
                i=i+1


traverse_folder('passcals\open_set')
