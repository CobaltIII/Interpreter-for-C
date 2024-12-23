from evaluator import *
from tokens import *
from obj_and_env import *
from parser import *

Prompter = " >> "

def Start():
    env = Environment()
    while True:
        print(Prompter, end="")
        line = input()
        lexer = Lexer(line)
        parser = Parser(lexer)
        program = parser.ParseProgram()
        if parser.errors:
            for error in parser.errors:
                print(error)
            continue

        evaluated = Eval(program, env)
        if evaluated:
            print(evaluated.inspect())

def Fib(x):
    env = Environment()
    input = """
    let fib = fn(n) { 
        if (n < 2) 
            { 1 } 
        else 
            { fib(n - 2) + fib(n - 1) } 
    };
    fib("""
    input += str(x) + ");"
    lexer = Lexer(input)
    parser = Parser(lexer)
    program = parser.ParseProgram()
    evaluated = Eval(program, env)
    if evaluated:
        print(evaluated.inspect())

if __name__ == "__main__":
    Fib(6)

