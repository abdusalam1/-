    def p_subprogram_declarations(p):
        'subprogram_declarations : subprogram_declarations subprogram SEMICOLON '
        # 标志不在子函数中
        self.inSubFun = False
        p[0] = {
            "length": len(p),
            "type": "subprogram_declarations",
            "subprograms": p[1]["subprograms"] + [p[2]]
        }
        # 符号表由产生式右侧生成
        p[0]["SymbolTable"] = p[1]["SymbolTable"] + [p[2]["SymbolTable"]]


    def p_subprogram_declarations_empty(p):
        'subprogram_declarations : empty '
        p[0] = {
                "length": len(p),
                "type": "subprogram_declarations",
                "subprograms": []
            }
        p[0]["SymbolTable"] = []


    def p_subprogram(p):
        'subprogram : subprogram_head SEMICOLON subprogram_body'
        p[0] = FucDefn(p[1]['name'],p[1]['lineno'],p[1]['formal'],p[1]['type'],
                       p[3]['con'],p[3]['var'],p[3]['block'])
        # 由产生式右侧构造符号表
        p[0]["SymbolTable"] = {
            "token": p[1]["SymbolTable"]["token"],
            "type": p[1]["SymbolTable"]["type"],
        }

    def p_subprogram_head_procedure(p):
        '''subprogram_head : PROCEDURE ID formal_parameter'''
        # 标识进入子过程
        self.inSubFun = True
        # 重置 subSymbol
        self.subSymbol = {}
        p[0] = {
            'name': p[2],
            'lineno': p.lineno(1),
            'formal': p[3],
            'type': ""
        }
        # 构造符号表
        p[0]["SymbolTable"] = {
            "token": p[2],
            "type": None,
            "references": p[3]["SymbolTable"]["references"] if p[3] is not None else None,
            "variables": p[3]["SymbolTable"]["variables"] if p[3] is not None else None,
        }

        # 讲子过程加入 subSymbol
        self.subSymbol = {p[2]: p[0]["SymbolTable"]}

        
    def p_subprogram_head_function(p):
        '''subprogram_head :  FUNCTION ID formal_parameter COLON basic_type'''
        # 标识进入子函数
        self.inSubFun = True
        # 重置 subSymbol
        self.subSymbol = {}
        p[0] = {
            'name': p[2],
            'lineno': p.lineno(1),
            'formal': p[3],
            'type': p[5]
        }
        p[0]["SymbolTable"] = {
            "token": p[2],
            "type": p[5]["SymbolTable"],
            "references": p[3]["SymbolTable"]["references"] if p[3] is not None else None,
            "variables": p[3]["SymbolTable"]["variables"] if p[3] is not None else None,
        }
        # 将子函数加入 subSymbol
        self.subSymbol = {p[2]: p[0]["SymbolTable"]}
        # 将各变量加入 subSymbol
        if p[0]["SymbolTable"]["variables"] is not None:
            self.subSymbol = p[0]["SymbolTable"]["variables"]

        # 参数列表
    def p_formal_parameter(p):
        'formal_parameter : LPAREN parameter_list RPAREN'
        p[0] = p[2]
        p[0]["SymbolTable"] = {
            "references": p[2]["SymbolTable"]["references"],
            "variables": p[2]["SymbolTable"]["variables"],
        }

    def p_formal_parameter_empty(p):
        'formal_parameter : empty'
        p[0] = {}

    # 参数总和
    def p_parameter_list(p):
        'parameter_list : parameter'
        p[0] = p[1]          # p[0]是一个dict
        p[0]["SymbolTable"] = {
            "references": p[1]["SymbolTable"]["references"],
            "variables": p[1]["SymbolTable"]["variables"],
        }

    def p_parameter_list_2(p):
        'parameter_list : parameter_list SEMICOLON parameter'
        p[0] = p[1].update(p[3])
        # 符号表从产生式右侧获取
        p[0]["SymbolTable"] = {
            "references": p[1]["SymbolTable"]["references"] + p[3]["SymbolTable"]["references"],
            "variables": p[1]["SymbolTable"]["variables"] + p[3]["SymbolTable"]["variables"],
        }

    # 各个参数，分为传参和传引用
    def p_parameter(p):
        'parameter : var_parameter'
        p[0] = FormalParameter(p[1] + True)
        p[0]["SymbolTable"] = p[1]["SymbolTable"]

    def p_parameter_value(p):
        'parameter : value_parameter'
        p[0] = FormalParameter(p[1] + False)
        # 符号表从产生式右侧获取
        p[0]["SymbolTable"] = p[1]["SymbolTable"]

    def p_var_parameter(p):
        'var_parameter : VAR value_parameter'
        p[0] = p[2]
        p[0]["SymbolTable"] = {
            # 函数定义变量是引用调用
            "references": True,
            "variables": p[2]["SymbolTable"]["variables"],
        }  # 规约value_parameter的符号表
    def p_value_parameter(p):
        'value_parameter : idlist COLON basic_type'
        p[0] = [p[1],p.lineno(1),p[3]]
        p[0]["SymbolTable"] = {
            # 函数定义变量不是引用调用
            "references": False,
            "variables": []
        }  # value_parameter的符号表
        for key,value in p[1].items():  # 遍历idlist中的每个id, 扩充符号表的变量列表
            p[0]["SymbolTable"]["variables"] = p[0]["SymbolTable"]["variables"] + [{
                "token": key,
                "type": p[3]["SymbolTable"],
            }]


        # 子程序体
    def p_subprogram_body(p):
        '''subprogram_body : const_declarations var_declarations  compound_statement'''
        p[0] = {
            'con': p[1],
            'var': p[2],
            'block':p[3]
        }
        p[0]["SymbolTable"] = {
            # 常量符号表
            "constants": p[1]["SymbolTable"] if p[1] else [],
            # 变量符号表
            "variables": p[2]["SymbolTable"] if p[2] else [],
        }
        # 将子函数加入 subSymbol
        self.subSymbol = p[0]["SymbolTable"]



    def p_compound_statement(p):
        'compound_statement : BEGIN statement_list END'
        p[0] = p[2]

    def p_statement_list(p):
        'statement_list : statement'
        p[0] = [p[1]]

    def p_statement_list_2(p):
        'statement_list :  statement_list SEMICOLON statement'
        p[0] = p[1] + [p[3]] if p[3] else p[1]

    def p_statement_empty(p):
        'statement : empty'
        # 在这里处理空语句的情况
        p[0] = None