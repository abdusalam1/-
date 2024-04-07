#符号表
class SymbolTable:
    def __init__(self):
        self.area='' 
        self.Constants={}#常量 常量名：{Constant}
        self.Variants={} #变量 变量名：{Type}
        self.subFuncs={} #函数 函数名：{SymbolTable}

#语法树 


class Program:
    """
    主程序类
    """
    def __init__(self,a,b,c):
        self.programId:str = a#程序标题声明名
        self.line:int = b      #程序标题行号
        self.paraDict:dict = c #参数标识符:行号
        self.subProgram:SubProgram = SubProgram()
class SubProgram:
    """
    子程序类
    """
    def __init__(self):
        self.constList:list[Constant] = [] #常量定义列表
        self.varList:list[Variant] = []    #变量定义列表
        self.subDefList:list[FucDefn]  = []#子程序和子函数
        self.block:Compound = Compound()#主程序体
class Constant:
    """
    常量定义类
    """
    def __init__(self):
        self.constId:str = ''   #标识符
        self.line:int = 0       #行号
        self.type:str = ''      #类型int,char,real,string（这个string指的是常量标识符的ID，因为可能由其他量赋值）
        self.charValue:str = '' #字符类型值
        self.intValue:int = 0   #整形
        self.realValue:float = 0#浮点


class Variant:
    """
    变量定义类
    """
    def __init__(self):
        self.varId:str = ''      #标识符名称
        self.type:Type = Type()  #变量类型

class Type:
    """
    变量类型类
    """
    def __init__(self):
        self.type:str = ''       #基本类型，int、char、real、boolean
        self.line:int = 0        #行号
        self.arrFlag:bool= 0     #0不是数组，1是数组
        self.lowerBound:int = 0  #数组下界
        self.upperBound:int = 0  #数组上界

class FucDefn:
    """
    过程与函数定义类
    """
    def __init__(self):
        self.fucId:str = ''      #名称
        self.line:int = 0        #行号
        self.formalParaList:list[FormalParameter] = FormalParameter() #形参列表
        self.type:str = ''       #如果type是空串，则为过程，否则为函数,取值为"integer","real","boolean","char"四种
        self.constList:list[Constant] = []#常数定义列表
        self.varList:list[Variant] = []#变量定义列表
        self.block:Compound = Compound()#程序体


class FormalParameter:
    """
    形参类
    """
    def __init__(self):
        self.paraId:str = '' #标识符
        self.line:int  = 0   #行号
        self.type:str = '' #基本类型，int、char、real、boolean
        self.flag:bool = False #false代表传值调用，true代表引用调用 


class Expression:
    """
    表达式类
    """
    def __init__(self):
        self.type:str = ''
        """
        表达式类型,"var"表示变量,"int"表示整数,"real"表示浮点数,"function"表示函数调用,
        "compound"表示复合表达式,compound有普通的二目运算符
        还有minus、not、bracket等单目运算符 
        """
        self.line:int = 0
        self.varRef:VarReference = VarReference()
        self.intNum:int = 0#整数
        self.realNum:float = 0#浮点
        self.strOfNum:str = ''#字符串的数
        self.charVal:str = ''#字符的值
        self.fucCall:FucCall = FucCall()
        self.operation:str = ''#复合表达式
        self.opType:str = ''#操作符类型
        self.subE1:Expression = Expression()#子式1
        self.subE2:Expression = Expression()#子式2

class FucCall:
    """
    函数调用
    """
    def __init__(self):
        self.fucId:str = ''#函数名称
        self.line:int = 0
        self.actParaList:list[Expression] = Expression()#参数列表

class VarReference:
    """
    变量引用
    """
    def __init__(self):
        self.varId:str = ''#变量名
        self.line:int = 0
        self.expList:list[Expression] = []#
        self.flag:bool = False #0表示非数组,1表示数组
class Statement:
    """
    语句类
    """
    def __init__(self):
        self.line:int = 0#行号
        self.type:str = ''#类型"compound","repeat","while","for","if","assign","procedure" 
        self.stateType:str = ''#区别于type，取值为"void"或"error"
class Assign(Statement):
    """
    赋值
    """
    def __init__(self):
        super().__init__()
        self.varRef:VarReference = VarReference()#左值变量
        self.exp:Expression = Expression()#右边表达式
class If(Statement):
    """
    条件语句
    """
    def __init__(self):
        self.condition:Expression =  Expression()#条件表达式
        self.then:Statement = Statement()#then语句
        self.els:Statement = Statement()#else语句
class While(Statement):
    """
    循环语句
    """
    def __init__(self):
        self.condition:Expression =  Expression()#条件表达式
        self.do:Statement = Statement()#循环体
class For(Statement):
    """
    for循环语句
    """
    def __init__(self):
        self.id:str = ''#循环变量
        self.state:Expression = Expression()#起始值
        self.end:Expression = Expression()#结束值
        self.do:Statement = Statement()#执行语句
class Repeat(Statement):
    """
    repeat语句
    """
    def __init__(self):
        self.condition:Expression = Expression()#条件
        self.do:Statement = Statement()

class Compound(Statement):
    """
    复合语句类
    """
    def __init__(self):
        self.statements:list[Statement] = []#语句列表

class ProcCall(Statement):
    """
    过程调用
    """
    def __init__(self):
        self.procId:str = ''#名称
        self.actParaList:list[Expression] = []#实参



if __name__ == '__main__':
    print('what can i say?')