class SubProgram:
    """
    子程序类
    """
    def __init__(self,a,b,c,d):
        self.constList: dict = a if a else {}  # 常量定义列表
        self.varList: dict = b if b else {}    # 变量定义列表
        self.subDefList: dict = c if c else {}  # 子程序和子函数
        self.block: Compound = Compound(d)  # 主程序体

class FucDefn:
    """
    过程与函数定义类
    """
    def __init__(self,name,lineno,formal,types,con,var,block):
        self.fucId:str = name      #名称
        self.line:int = lineno        #行号
        self.formalParaList:dict = formal if formal else {}#形参列表
        self.type:str = types       #如果type是空串，则为过程，否则为函数,取值为"integer","real","boolean","char"四种
        self.constList:dict = con if con else {} #常数定义列表
        self.varList:dict = var if var else {} #变量定义列表
        self.block:Compound = Compound(block) #程序体


class FormalParameter:
    """
    形参类
    """
    def __init__(self,formal):
        self.paraId:str = formal[0] #标识符
        self.line:int  = formal[1]   #行号
        self.type:str = formal[2] #基本类型，int、char、real、boolean
        self.flag:bool = formal[3] #false代表传值调用，true代表引用调用


