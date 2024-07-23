# 编译原理课程设计
◆ 题目：Pascal-S语言编译程序的设计与实现
◆ 目标：按照所给Pascal-S语言的语法，参考Pascal语言的语义，设计并实现Pascal-S语言的编译程序。
## pascal to c (Pascal-S 语言编译成对应的C语言）
**syntax_5 是最终版本，其中yacc.py是主程序**
**open_set包含pascal语言测试集和c语言转化结果**
***下面是一个例子：***
```pascal
program main;
var
  a: integer;
  b: integer;
  
function func(p: integer): integer;
begin
  p := p - 1;
  func := p;
end;

begin
  a := 10;
  b := func(a);

  write(b);
end.
```
转化结果：
```C
#include<stdio.h>
#include<stdbool.h>
int a;
void main1();
int defn();
int main(){
	main1();

}
void main1(){
	a=defn();
	printf("%d",a);

}
int defn(){
	int temp;
	temp=88;
	return 4;
}
```
