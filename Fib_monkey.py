from evaluator import *
from tokens import * 
from parser import *

code = """
let fibcalc = fn(x){
    if (x < 2) { 1 }
    else {fibcalc(x - 2) + fibcalc(x - 1)}
};
print(fibcalc(4));
print(fibcalc(5));
print(fibcalc(6));
print(fibcalc(7));
print(fibcalc(8));
"""
env = Environment()
lexer = Lexer(code)
parser = Parser(lexer)
program = parser.ParseProgram()

evaluated = Eval(program , env)
if evaluated != None:
    print("OUTPUT = " , end = "")
    print(evaluated.inspect())
