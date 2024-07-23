file = open('passcals\\open_set\\64_nested_loops.pas', "r", encoding='utf-8')
        # 读取文件内容
content = file.read().replace('][', ',')#.lower()
with open('passcals\\open_set\\64_nested_loops1.pas',"w") as F:
    F.write(content)