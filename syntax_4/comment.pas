program example(aaa,bbb); 
const tt=1;pp=-2;
    ch='a';
var x, y: integer; ch1:char;
    r1,r2:real;

function gcd(a, b: integer): integer;
const k=1;
var  kk:real;
begin 
if b=0 then gcd:=a
else gcd:=gcd(b, a mod b)
end;

begin
read(x, y);
write(gcd(x, y))
end. 
