from AST_structure import *


class CodeGenerator:
    """
    代码生成类
    """
    targetCode = ''  # 目标代码
    domain = []  # 作用域栈
    headFile = []  # 头文件
    f_stdio = False  # 头文件标志

    def __init__(self):
        self.targetCode = ''
        # self.domain = []
        self.headFile = ''
        self.globalCode = ''
        self.f_stdio = False
        self.ast = None
        # self.varT = None
        # self.mainFucDef:str = 'main'#主函数接口声明
        self.fucDefList: list[SubFucDef] = []  # 子函数接口列表 void subFuc1();
        self.fucList: list[SubFuc] = []  # 子函数定义列表 void subFuc1() {};
        self.varList = []  # 全局变量列表
        self.varTypeList = []  # 全局变量对应类型
        self.arrId = []  # 数组
        self.arrl = []  # 数组下限
        self.arru = []  # 数组上限

    def varIsArr(self, var, fuc):
        fucname = fuc.id
        for i in range(len(self.fucDefList)):
            if fucname == self.fucDefList[i].id:
                fucdef = self.fucDefList[i]
                if var in fucdef.arr:
                    return 2  # 局部变量中
                else:
                    if var in self.arrId:
                        return 1  # 全局变量中
                    else:
                        return 0

    def genArr(self, var, expl, fuc):
        fucname = fuc.id
        arrs = var
        for i in range(len(self.fucDefList)):
            if fucname == self.fucDefList[i].id:
                fucdef = self.fucDefList[i]
                if var in fucdef.arr:  # 局部变量中
                    index1 = fucdef.arr.index(var)
                    bl = fucdef.arrl[index1]
                    for x in range(len(expl)):
                        bias = bl[x]
                        exp = expl[x]
                        para = exp.value
                        if self.varIsArr(para, fuc):  # 嵌套数组

                            expn = exp.varRef.expList
                            arrs += '[' + str(self.genArr(para, expn, fuc)) + '-' + str(bias) + ']'

                        else:

                            arrs += '[' + str(para) + '-' + str(bias) + ']'

                    return arrs
                else:
                    index2 = self.arrId.index(var)
                    bl = self.arrl[index2]
                    for x in range(len(expl)):
                        bias = bl[x]
                        exp = expl[x]
                        para = exp.value
                        if self.varIsArr(para, fuc):  # 嵌套数组

                            expn = exp.varRef.expList
                            arrs += '[' + str(self.genArr(para, expn, fuc)) + '-' + str(bias) + ']'

                        else:

                            arrs += '[' + str(para) + '-' + str(bias) + ']'

                    return arrs

    def genHeadFile(self):
        """
        输出头文件
        """
        if self.f_stdio == True:
            self.headFile += '#include<stdio.h>\n'
        self.headFile += '#include<stdbool.h>\n'
        self.targetCode += self.headFile

    def genSubFucDef(self):
        """
        输出程序接口声明
        """
        pass

    def varIsValid(self, var, fuc):
        fucname = fuc.id
        for i in range(len(self.fucList)):
            if fucname == self.fucList[i].id:
                if var in self.fucList[i].varList:
                    return True
                else:
                    if var in self.varList:
                        return True
                    else:
                        return False  # 报错处理

    def genGlobalDef(self, fuc):
        """
        输出全局变量定义
        """
        # fuc:SubFuc
        for i in range(len(fuc.constIdList)):
            id = fuc.constIdList[i]
            type = fuc.constTypeList[i]
            val = fuc.constValList[i]
            if type == 'int':
                self.globalCode += 'const ' + 'int ' + id + ' = ' + str(val) + ';\n'
            elif type == 'char':
                self.globalCode += 'const ' + 'char ' + id + ' = ' + str(val) + ';\n'
            elif type == 'boolen':
                self.globalCode += 'const ' + 'bool ' + id + ' = ' + str(val) + ';\n'
            else:
                self.globalCode += 'const ' + 'float ' + id + ' = ' + str(val) + ';\n'
        for i in range(len(fuc.varIdList)):
            id = fuc.varIdList[i]
            type = fuc.varTypeList[i]
            self.varList.append(id)
            self.varTypeList.append(type)
            if id in fuc.arr:  # 为数组
                j = fuc.arr.index(id)
                low = fuc.arrl[j]
                up = fuc.arru[j]
                self.arrId.append(id)
                self.arrl.append(low)
                self.arru.append(up)
                if type == 'int':
                    self.globalCode += 'int ' + id
                elif type == 'char':
                    self.globalCode += 'char ' + id
                elif type == 'boolen':
                    self.globalCode += 'bool ' + id
                else:
                    self.globalCode += 'float ' + id
                for k in range(len(low)):
                    len1 = up[k] - low[k] + 1
                    self.globalCode += '[' + str(len1) + ']'
                self.globalCode += ';\n'


            else:
                if type == 'int' or type == 'integer':
                    self.globalCode += 'int ' + str(id) + ';\n'
                elif type == 'char':
                    self.globalCode += 'char ' + str(id) + ';\n'
                elif type == 'boolen' or type == "bool":
                    self.globalCode += 'bool ' + str(id) + ';\n'
                else:
                    self.globalCode += 'float ' + str(id) + ';\n'

    def anaAst(self):
        """
        分析AST
        """
        ast1 = self.ast
        if ast1.programId == 'main':
            ast1.programId = 'main1'
        pMainDef = SubFucDef()  # void example();
        pMainDef.returnType = 'void'
        # pMainDef.id = ast1.programId  # 主程序名称
        pMainDef.id = 'main'  # 主程序名称
        self.fucDefList.append(pMainDef)
        pMain = SubFuc()  # main函数
        statement1 = ''
        statement1 += ast1.programId + '();\n'
        pMain.statements.append(statement1)  # 完成main函数
        pMain.back.append(1)
        pMain.id = 'main'
        pMainDef2 = SubFucDef()
        pMainDef2.returnType = 'void'
        pMainDef2.id = ast1.programId  # 主程序名称
        self.fucDefList.append(pMainDef2)  # 添加example定义
        self.fucList.append(pMain)  # 添加main
        pRealMain = SubFuc()  # example实现方法->mainBlock
        realMain = ast1.subProgram  # 真正的主程序 void example() {}
        # 进入主程序，定义的变量为全局变量
        self.genDef(realMain, pRealMain)  # 定义全局变量
        # for n in realMain.constList['constant'] :
        #     pRealMain.constIdList.append(n.constId)
        #     pRealMain.constTypeList.append(n.type)
        #     pRealMain.constValList.append(n.Value)
        # for d,i in realMain.varList:#程序定义加入常量和变量
        #     if d.type.arrFlag:
        #         pRealMain.arr.append(i)
        #         pRealMain.varTypeList.append(d.type.type)
        #         pRealMain.varIdList.append(i)
        #         pRealMain.arrl.append(d.type.lowerBound)
        #         pRealMain.arru.append(d.type.upperBound)
        #     else:
        #         pRealMain.varIdList.append(i)
        #         pRealMain.varTypeList.append(d.type.type)
        self.genGlobalDef(pRealMain)
        pRealMain.id = ast1.programId
        mainBlock = realMain.block  # 主程序代码块

        mainflag = 0
        if realMain.subDefList['type'] == 'subprogram_declarations':
            fList = realMain.subDefList['subprograms']  # 子函数定义列表
            if fList:
                for f in fList:
                    fuc1 = SubFucDef()  # 子函数接口声明
                    if f.type == '' or f.type == 'void':
                        fuc1.returnType = 'void'
                    else:
                        fuc1.returnType = f.type
                    fuc1.id = f.funcId
                    pl = f.formalParaList
                    # 未处理数组
                    for d, l in pl.items():
                        # print(type(d.paraId))
                        for k in d.paraId:
                            fuc1.paraList.append(k)
                            fuc1.paraType.append(d.type)
                            fuc1.paraIsRef.append(d.flag)
                    self.fucDefList.append(fuc1)  # 子函数接口声明完成
                for f in fList:
                    mainflag = mainflag + 1
                    fuc2 = SubFuc()  # 子函数定义
                    fuc2.id = f.funcId
                    if len(f.constList) and f.constList['constant'] is not None:
                        cl = f.constList['constant']
                        for c in cl:
                            fuc2.constIdList.append(c.constId)
                            fuc2.constTypeList.append(c.type)
                            fuc2.constValList.append(c.Value)
                    if len(f.varList):
                        vl = f.varList
                        for d, i in vl.items():
                            for id, val1 in d.idlist.items():
                                if d.type.arrFlag:
                                    fuc2.arr.append(id)
                                    fuc2.varTypeList.append(d.type.type)
                                    fuc2.varIdList.append(id)
                                    fuc2.arrl.append(d.type.lB)
                                    fuc2.arru.append(d.type.uB)
                                else:
                                    fuc2.varIdList.append(id)
                                    fuc2.varTypeList.append(d.type.type)
                    pblock = f.block
                    # 处理子程序代码块
                    # if pblock.type == "compound":
                    if isinstance(pblock, Compound):
                        self.genCompound(pblock, fuc2, 1)  # 程序代码块缩进为1
                    else:
                        self.genStatement(pblock, fuc2, 1)
                    self.fucList.append(fuc2)  # 子函数添加完成
                    if mainflag == 1:
                        # 处理主程序代码块
                        self.genCompound(mainBlock, pRealMain, 1)
                        self.fucList.append(pRealMain)
                        # 扔出错误
            else:
                # 处理主程序代码块
                self.genCompound(mainBlock, pRealMain, 1)
                self.fucList.append(pRealMain)

    def genExpr(self, expr: Expression, sin, fuc):  # 生成表达式的字符串
        s = ''
        if isinstance(expr, list):
            for item in expr:
                if item.type == 'var':
                    name = item.varRef.varId
                    fucname = fuc.id
                    for i in range(len(self.fucDefList)):
                        fucdef = self.fucDefList[i]
                        if fucdef.id == fucname:
                            index = fucdef.paraList.index(name)
                            if fucdef.paraIsRef[index]:
                                name = '*' + name
                    v = item.varRef
                    if sin.varRef:  # 如果是数组
                        # if sin.varRef.flag:
                        #     s +='['+sin.varRef.expList[0].value+']'
                        pass
                    else:
                        s += name
                    return s
                elif item.type == 'int':
                    # if sin.varRef:
                    #     if sin.varRef.flag:
                    #         s +='['+str(sin.varRef.expList[0].value)+']'
                    s += str(item.value)
                    return s
                elif item.type == 'float':
                    s += str(item.value)
                    return s
                elif item.type == 'function':
                    # 暂未考虑直接用函数名返回
                    f = item.fucCall
                    s += f.fucId + '('
                    for p in f.actParaList:
                        s += self.genExpr(p)
                        if p != f.actParaList[-1]:
                            s += ','
                    s += ')'
                    return s
                elif item.type == 'compound':
                    if item.opType == 'double':  # 双目运算符
                        s += '(' + self.genExpr(item.subE1, item, fuc) + item.operation + self.genExpr(item.subE2,
                                                                                                       item, fuc) + ')'
                    else:  # 单目运算符
                        s += '(' + item.operation + self.genExpr(item.subE1, item, fuc) + ')'
                    return s
        elif expr!=None :
            if expr.type == 'var':
                v = expr.varRef
                name = v.varId
                fucname = fuc.id
                for i in range(len(self.fucDefList)):
                    fucdef = self.fucDefList[i]
                    if fucdef.id == fucname:
                        if name in fucdef.paraList:
                            index = fucdef.paraList.index(name)
                            if fucdef.paraIsRef[index]:
                                name = '*' + name
                    else:
                        pass  # 扔出错误

                # if sin.varRef:  # 如果是数组 todo:sin可能没有varRef
                #     # if sin.varRef.flag:
                #     #     s +='['+sin.varRef.expList[0].value+']'
                #     pass
                # else:
                s += name
                return s
            elif expr.type == 'int':
                # if sin.varRef:
                #     if sin.varRef.flag:
                #         s +='['+str(sin.varRef.expList[0].value)+']'
                s += str(expr.value)
                return s
            elif expr.type == 'float':
                s += str(expr.value)
                return s
            elif expr.type == 'function':
                # 暂未考虑直接用函数名返回
                f = expr.fucCall
                s += f.fucId + '('
                for p in f.actParaList:
                    s += self.genExpr(p, sin, fuc)
                    if p != f.actParaList[-1]:
                        s += ','
                s += ')'
                return s
            elif expr.type == 'compound':
                if isinstance(expr, Expression):
                    if expr.operation == "=":
                        expr.operation = "=="
                    if expr.operation == "mod":
                        expr.operation = '%'
                    if expr.operation == "<>":
                        expr.operation = '!='
                    if expr.operation == "div":
                        expr.operation = "/"
                    if expr.operation == "and":
                        expr.operation = "&&"
                    if expr.operation == "not":
                        expr.operation = "!"
                    if expr.operation == "or":
                        expr.operation = "\\"
                if expr.opType == 'double':  # 双目运算符
                    s += '(' + self.genExpr(expr.subE1, expr, fuc) + expr.operation + self.genExpr(expr.subE2, expr,
                                                                                                   fuc) + ')'
                else:  # 单目运算符
                    s += '(' + expr.operation + self.genExpr(expr.subE1, expr, fuc) + ')'
                return s

    def genCompound(self, block: Compound, fuc, back):  # 生成函数的语句字典
        if isinstance(block, Compound):
            for sl in block.statements:
                s = sl
                if isinstance(s, list):
                    for item in s:
                        self.genStatement(item, fuc, back)
                else:
                    if s!=None and s.type == 'compound':
                        pass
                    else:
                        self.genStatement(s, fuc, back)
        elif isinstance(block, list):
            for item in block:
                self.genStatement(item, fuc, back)
        else:
            self.genStatement(block, fuc, back)

    def genStatement(self, statemnt: Statement, fuc, back):
        # fuc:SubFuc
        s: Statement = statemnt
        if s !=None:
            if s.type == 'compound':
                self.genCompound(s, fuc, back)  # todo:s没有block成员变量
            elif s.type == 'repeat':
                line = '' + 'while(!' + self.genExpr(s.condition) + '){'
                fuc.statements.append(line)
                fuc.back.append(back)
                self.genCompound(s.do, fuc, back + 1)
                fuc.statements.append('}')
                fuc.back.append(back)
                """
                while(!xxx == xxx){
                    do;
                }
                """
            elif s.type == 'while':
                line = '' + 'while(' + self.genExpr(s.condition) + '){'
                fuc.statements.append(line)
                fuc.back.append(back)
                self.genCompound(s.do, fuc, back + 1)
                fuc.statements.append('}')
                fuc.back.append(back)
                """
                while(xxx == xxx){
                    do;
                }
                """
            elif s.type == 'for':
                line = '' + 'for(' + s.id + "=" + self.genExpr(s.state, s, fuc) + ';' + s.id + "<=" + self.genExpr(s.end,
                                                                                                                s,
                                                                                                                fuc) + ';' + s.id + '++){'
                fuc.statements.append(line)
                fuc.back.append(back)
                self.genCompound(s.do, fuc, back + 1)
                fuc.statements.append('}')
                fuc.back.append(back)
                """
                for(xxx;xxx;xxx){
                    do;
                }
                """
            elif s.type == 'if':
                line = '' + 'if(' + self.genExpr(s.condition, s, fuc) + '){'
                fuc.statements.append(line)
                fuc.back.append(back)
                if isinstance(s.then, list):
                    for comd in s.then:
                        self.genStatement(comd, fuc, back + 1)

                else:
                    self.genStatement(s.then, fuc, back + 1)
                # self.genCompound(s.then, fuc, back + 1)
                fuc.statements.append('}')
                fuc.back.append(back)
                if s.els is not None:
                    fuc.statements.append('else{')
                    fuc.back.append(back)
                    if isinstance(s.els, list):
                        for comd in s.els:
                            self.genStatement(comd, fuc, back + 1)
                    else:
                        self.genStatement(s.els, fuc, back + 1)

                    fuc.statements.append('}')
                    fuc.back.append(back)
                """
                if(xxx == xxx){
                    do;
                }else{
                    do;
                }"""
            elif s.type == 'assign':
                v = s.varRef.varId
                if s.varRef:
                    bias = 0
                    if v in fuc.varIdList:  # 这块负责获数组的下标偏移值
                        index1 = fuc.varIdList.index(v)
                    else:
                        # 代表c是全局变量
                        pass
                    if s.varRef.flag:
                        if v in fuc.arr:  # 在局部变量中
                            index1 = fuc.arr.index(v)
                            bl = fuc.arrl[index1]

                            v = self.genArr(v, s.varRef.expList, fuc)
                        else:
                            if v in self.arrId:  # 在全局变量中
                                index1 = self.arrId.index(v)
                                bl = self.arrl[index1]
                                v = self.genArr(v, s.varRef.expList, fuc)
                            else:
                                pass  # 报错
                # 是否是传引用
                fucname = fuc.id
                for i in range(len(self.fucDefList)):
                    fucdef = self.fucDefList[i]
                    if fucdef.id == fucname:
                        if v in fucdef.paraList:
                            index = fucdef.paraList.index(v)
                            if fucdef.paraIsRef[index]:
                                v = '*' + v
                flag = 0
                for item in self.fucDefList:
                    if item.id == v:
                        flag = 1
                if flag:
                    line = "return " + self.genExpr(s.exp, s, fuc) + ';'
                else:
                    flag = 0
                    for item in self.fucDefList:  # 赋值表达式是否为函数赋值
                        if item.id == s.exp.value:
                            flag = 1
                    if flag:
                        line = '' + v + '=' + s.exp.value + '('  # ')'+ ';'
                        if s.exp.fucCall is not None:
                            for index, para in enumerate(s.exp.fucCall.actParaList):
                                flag = self.judgePara(s.exp, para.value, fuc, index)
                                if flag == 1:
                                    line += '*'
                                elif flag == 2:
                                    line += '&'
                                line += str(para.value)
                                if index != len(s.exp.fucCall.actParaList) - 1:
                                    line += ','
                        line += ')' + ';'
                    else:
                        line = '' + v + '=' + self.genExpr(s.exp, s, fuc) + ';'

                fuc.statements.append(line)
                fuc.back.append(back)
                """
                v = xxx;
                """
            elif s.type == 'procall':
                line = '' + s.procId + '('
                for p in s.actParaList:
                    line += self.genExpr(p, s, fuc)
                    if p != s.actParaList[-1]:
                        line += ','
                line += ');'
                fuc.statements.append(line)
                fuc.back.append(back)
                """
                procId(xxx,xxx,xxx);
                """
                pass
            elif s.type == 'print':
                flag = 0
                self.f_stdio = True
                line = 'printf("'
                for item in s.varlist:
                    # varId = item.value
                    if item.type == 'compound':
                        # line += self.genExpr(item.subE1, item, fuc) + item.operation + self.genExpr(item.subE2, item, fuc)
                        if item.value == "int":
                            line += '%d'
                    else:
                        if item.varRef is None:
                            line += str(item.value)
                            flag = 1
                        else:
                            varType = item.varRef.type
                            if varType == 'int':
                                line += '%d'
                            elif varType == 'float':
                                line += '%f'
                            else:  # todo:变量为其他的种类
                                pass
                if not flag:
                    line += '",'
                else:
                    line += '"'
                for index, item in enumerate(s.varlist):
                    if item.type == 'compound':
                        if item.operation == "div":
                            item.operation = "/"
                        if item.operation == "mod":
                            item.operation = "%"
                        line += self.genExpr(item.subE1, item, fuc) + item.operation + self.genExpr(item.subE2, item, fuc)
                    else:
                        if item.varRef is not None:
                            varId = item.value
                            line += str(varId)
                            if index != len(s.varlist) - 1:
                                line += ','
                line += ");\n"
                fuc.statements.append(line)
                fuc.back.append(back)
                """
                printf("%d",a);
                """
                pass
            elif s.type == 'scan':
                self.f_stdio = True
                line = 'scanf("'
                for item in s.varlist:
                    # varId = item.value
                    if item.type == 'compound':
                        # line += self.genExpr(item.subE1, item, fuc) + item.operation + self.genExpr(item.subE2, item, fuc)
                        if item.value == "int":
                            line += '%d'
                    else:
                        varType = item.type
                        if varType == 'int':
                            line += '%d'
                        elif varType == 'float':
                            line += '%f'
                        else:  # todo:变量为其他的种类
                            pass
                line += '",'
                for index, item in enumerate(s.varlist):
                    if item.type == 'compound':
                        line += self.genExpr(item.subE1, item, fuc) + item.operation + self.genExpr(item.subE2, item, fuc)
                    else:
                        varId = item.varId
                        line += '&' + varId
                        if index != len(s.varlist) - 1:
                            line += ','
                line += ");\n"
                fuc.statements.append(line)
                fuc.back.append(back)
                """
                printf("%d",a);
                """
                pass
            pass

    def judgePara(self, exp: Expression, var: str, fuc, index: int):
        """
        判断函数传入的参数是否需要加*或者&，0代表不加，1代表加*，2代表加&
        """
        fucid = exp.fucCall.fucId
        for item in self.fucDefList:
            if item.id == fucid:
                fucdef = item
        fucflag = fucdef.paraIsRef[index]
        varflag = self.varIsRef(var, fuc)  # 1表示当前这个参数是传引用
        if fucflag and varflag:
            return 0
        if not fucflag and not varflag:
            return 0
        if varflag and not fucflag:
            return 1
        if not varflag and fucflag:
            return 2

    def varIsRef(self, var, fuc):
        fucname = fuc.id
        for i in range(len(self.fucDefList)):
            fucdef = self.fucDefList[i]
            if fucdef.id == fucname:
                if var in fucdef.paraList:
                    index = fucdef.paraList.index(var)
                    return fucdef.paraIsRef[index]
                else:
                    return False

    def genDef(self, pfuc: SubProgram, cfuc):  # 生成函数定义的常量与变量定义
        if len(pfuc.constList) and pfuc.constList['constant'] is not None:
            for n in pfuc.constList['constant']:
                cfuc.constIdList.append(n.constId)
                if n.type == "char":
                    n.Value = "'"+n.Value +"'"
                cfuc.constTypeList.append(n.type)
                cfuc.constValList.append(n.Value)
        for d, i in pfuc.varList.items():  # 程序定义加入常量和变量
            if d.type.arrFlag:
                # cfuc.arr.append(i)
                # cfuc.varTypeList.append(d.type.type)
                # cfuc.varIdList.append(i)
                # cfuc.arrl.append(d.type.lowerBound)
                # cfuc.arru.append(d.type.upperBound)
                for d2, i2 in d.idlist.items():
                    cfuc.arr.append(d2)
                    cfuc.varTypeList.append(d.type.type)
                    cfuc.varIdList.append(d2)
                    cfuc.arrl.append(d.type.lB)
                    cfuc.arru.append(d.type.uB)
                    # self.varList.append({d2:d.type.lB})
                    # self.varTypeList.append(str(d.type.type))
            else:
                for idt, val2 in d.idlist.items():
                    cfuc.varIdList.append(idt)
                    if d.type.type:
                        cfuc.varTypeList.append(d.type.type)  # todo: 有时候报错有时候不报错
                    # self.varList.append(idt)
                    # self.varTypeList.append(d.type.type)

    def outputHeadFile(self,filename):
        # print(self.headFile)
        with open(filename, "w") as file:
            file.write(self.headFile)

    def outputGlobalCode(self,filename):
        # print(self.globalCode)
        with open(filename, "a") as file:
            file.write(self.globalCode)

    def output(self,filename):
        self.outputHeadFile(filename)
        self.outputGlobalCode(filename)
        self.creatFuc(filename)

    def creatFuc(self,filename):
        for i in range(len(self.fucDefList)):
            fucdef = self.fucDefList[i]
            # fuc = self.fucList[i]
            for item in self.fucList:
                if fucdef.id == item.id:
                    fuc = item
            if fucdef.id != 'main':
                statement = fucdef.returnType + " " + fucdef.id + "("
                if fucdef.paraList:
                    for index, item in enumerate(fucdef.paraList):
                        statement += fucdef.paraType[index] + " "
                        if self.varIsRef(item, fuc):
                            statement += '*'
                        statement += item
                        if index != len(fucdef.paraList) - 1:
                            statement += ','
                statement = statement + ");\n"
                with open(filename, "a") as file:
                    file.write(statement)
        for i in range(len(self.fucDefList)):
            with open(filename, "a") as file:
                fucdef = self.fucDefList[i]
                for item in self.fucList:
                    if fucdef.id == item.id:
                        fuc = item
                if fucdef.id == 'main':
                    fucdef.returnType = 'int'
                statement = fucdef.returnType + " " + fucdef.id + "("  # "){\n"
                for index, para in enumerate(fucdef.paraList):
                    statement += fucdef.paraType[index] + " "
                    if self.varIsRef(para, fuc):
                        statement += '*'
                    statement += para
                    if index != len(fucdef.paraList)-1:
                        statement += ','
                statement += "){\n"
                file.write(statement)
                fuc.FucCont(file)
                statement = "}\n"
                file.write(statement)


class SubFucDef:
    """
    子函数接口声明
    """

    def __init__(self):
        self.returnType: str = ''  # "int","float","char","bool" void
        self.id: str = ''  # 名称
        self.paraList: list[str] = []  # 参数
        self.paraIsRef: list[bool] = []  # 参数是否引用
        self.paraType: list[str] = []  # 参数类型
        self.arr: list = []  # 是否是数组
        self.arrl: list = []  # 数组下界[  [1,2] [2]         ]
        self.arru: list = []  # 数组上界[  [3,4] [7]         ]

    def __str__(self):
        s = ''
        s += self.returnType + '' + self.id + '('
        for i in range(len(self.paraList)):
            n = self.paraList[i]
            s += self.paraType[i] + ' '
            s += n
            if n in self.arr:
                c = self.arr.index(n)
                s += '[' + str(self.arru[c] - self.arrl[c] + 1) + ']'
            if i != len(self.paraList) - 1:
                s += ','
        s += ')'
        return s  # 不带封号


class SubFuc:
    """
    子函数定义
    """

    def __init__(self):
        self.id: str = ''  # 名称
        self.constIdList: list[str] = []  # 常量标识符
        self.constTypeList: list[str] = []  # 常量类型
        self.constValList: list[str] = []  # 常量值
        self.varIdList: list[str] = []  # 变量标识符
        self.varTypeList: list[str] = []  # 变量类型
        self.arr: list[str] = []  # 数组 应为变量名
        self.arrl: list = []  # 数组下界
        self.arru: list = []  # 数组上界
        self.statements = []  # 语句
        self.back: list = []  # 缩进

    def outputConstList(self, retract):
        """
        输出常数列表
        """
        pass

    def outputVarList(self, retract):
        """
        输出变量列表
        """
        pass

    def outputStatement(self, retract):
        """
        输出语句
        """
        pass

    def outputSubFuc(self, retract):
        """
        输出函数的内容
        """
        pass

    def FucCont(self, file):
        # for statement in self.statements:
        #     statement = statement+'\n'
        #     file.write(statement)
        if self.id !="main1":
            for i in range(len(self.varIdList)):
                var = self.varIdList[i]
                vartype = self.varTypeList[i]
                statement = ''
                statement = statement + "\t"
                statement += vartype +" "+var
                if var in self.arr:
                    index = self.arr.index(var)
                    lowlist = self.arrl[index]
                    uplist = self.arru[index]
                    for m in range(len(lowlist)):
                        x = uplist[m]-lowlist[m]+1
                        statement += "["+str(x)+"]"
                statement+=";\n"
                file.write(statement)
        for i in range(len(self.statements)):
            nback = self.back[i]
            statement = ''
            for j in range(int(nback)):
                statement = statement + "\t"
            statement = statement + self.statements[i] + '\n'
            file.write(statement)


if __name__ == '__main__':
    pass