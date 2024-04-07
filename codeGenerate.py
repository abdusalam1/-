class CodeGenerator:
    """
    代码生成类
    """
    targetCode = ''#目标代码
    domain = []#作用域栈
    headFile = []#头文件
    f_stdio = False#头文件标志
    def __init__(self):
        self.targetCode = ''
        self.domain = []
        self.headFile = []
        self.f_stdio = False
        self.ast = None
        self.varT = None
        self.mainFucDef:str = 'main'#主函数接口声明 
        self.fucDefList:list[SubFucDef] = []#子函数接口列表
        self.fucList:list[SubFuc] = []#子函数定义列表
        
    
    def outputHeadFile(self):
        """
        输出头文件
        """
        pass

    def outputSubFucDef(self):
        """
        输出程序接口声明
        """
        pass


    

class SubFucDef:
    """
    子函数接口声明
    """
    def __init__(self):
        self.returnType:str = ''#"int","float","char","bool" void
        self.id:str = ''#名称
        self.paraList:list[str] =[]#参数
        self.paraIsRef:list[bool] =[]#参数是否引用
        self.paraType:list[str] = [] #参数类型
class SubFuc:
    """
    子函数定义
    """
    def __init__(self):
        self.constIdList:list[str] = []#常量标识符
        self.constTypeList:list[str] = []#常量类型
        self.constValList:list[str] = []#常量值
        self.varIdList:list[str] = []#变量标识符
        self.varTypeList:list[str] = []#变量类型
        self.varValList:list[str] = []#变量值
        self.statementDict = {}#语句：缩进值
    
    def outputConstList(self,retract):
        """
        输出常数列表
        """
        pass
    def outputVarList(self,retract):
        """
        输出变量列表
        """
        pass
    
    def outputStatement(self,retract):
        """
        输出语句
        """
        pass
    def outputSubFuc(self,retract):
        """
        输出函数的内容
        """
        pass



        