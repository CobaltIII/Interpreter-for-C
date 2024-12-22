import unittest
from tokens import * 
from parser import *
from evaluator import *
from obj_and_env import *
from parser import Boolean as BL

def testEval(input : str):
    l = Lexer(input)
    p = Parser(l)
    program = p.ParseProgram()
    env = NewEnvironment()
    return Eval(program , env)

def testIntegerObject(obj : Object , expected : int):
    if not (isinstance(obj , Integer)):
        return False
    if obj.value != expected:
        return False
    return True

def testBooleanObject(obj : Object , expected : bool):
    if not (isinstance(obj , Boolean)):
        return False
    if obj.value != expected:
        return False
    return True

def testNullObject(obj : Object):    
    if not (isinstance(obj , Null)):
        return False
    return True


class EvaluatorTest(unittest.TestCase):
    '''
    def testEvalIntegerExpression(self):
        tests = [
            {"input" : "5" , "expected" : 5} , 
            {"input" : "10" , "expected" : 10} , 
            {"input" : "-5" , "expected" : -5} , 
            {"input" : "-10" , "expected" : -10} , 
            {"input" : "5 + 5 + 5 + 5 - 10" , "expected" : 10} , 
            {"input" : "2 * 2 * 2 * 2 * 2" , "expected" : 32} , 
            {"input" : "-50 + 100 - 50" , "expected" : 0} ,
            {"input" : "5 * 2 + 10" , "expected" : 20} ,
            {"input" : "5 + 2 * 10" , "expected" : 25} ,
            {"input" : "20 + 2 * -10" , "expected" : 0} ,
            {"input" : "50 / 2 * 2 + 10" , "expected" : 60} ,
            {"input" : "2 * (5 + 10)" , "expected" : 30} ,
            {"input" : "3 * 3 * 3 + 10" , "expected" : 37} ,
            {"input" : "3 * (3 * 3) + 10" , "expected" : 37} ,
            {"input" : "(5 + 10 * 2 + 15 / 3) * 2 + -10" , "expected": 50} 
        ]
        for tt in tests:
            
            evaluated = testEval(tt["input"])
            self.assertTrue(testIntegerObject(evaluated, tt["expected"]))
    
    def testEvalBooleanExpression(self):
        tests = [
            {"input" : "true" , "expected" : True} , 
            {"input" : "false" , "expected" : False} , 
            {"input" : "1 < 2" , "expected" : True} , 
            {"input" : "1 > 2" , "expected" : False} , 
            {"input" : "1 < 1" , "expected" : False} , 
            {"input" : "1 > 1" , "expected" : False} , 
            {"input" : "1 == 1" , "expected" : True} , 
            {"input" : "1 != 1" , "expected" : False} , 
            {"input" : "1 == 2" , "expected" : False} , 
            {"input" : "1 != 2" , "expected" : True} , 
            {"input" : "true == true" , "expected" : True} , 
            {"input" : "false == false" , "expected" : True} , 
            {"input" : "true == false" , "expected" : False} , 
            {"input" : "true != false" , "expected" : True} , 
            {"input" : "false != true" , "expected" : True} , 
            {"input" : "(1 < 2) == true" , "expected" : True} , 
            {"input" : "(1 < 2) == false" , "expected" : False} , 
            {"input" : "(1 > 2) == true" , "expected" : False} , 
            {"input" : "(1 > 2) == false" , "expected" : True} 
        ]
        for tt in tests:
            evaluated = testEval(tt["input"])
            self.assertTrue(testBooleanObject(evaluated, tt["expected"]))

    def testBangOperator(self):
        tests = [
            {"input" : "!true" , "expected" : False} , 
            {"input" : "!false" , "expected" : True} , 
            {"input" : "!5" , "expected" : False} , 
            {"input" : "!!true" , "expected" : True} , 
            {"input" : "!!false" , "expected" : False} , 
            {"input" : "!!5" , "expected" : True} 
        ]
        for tt in tests:
            evaluated = testEval(tt["input"])
            self.assertTrue(testBooleanObject(evaluated, tt["expected"]))

    def testIfElseExpressions(self):
        tests = [
            {"input" : "if (true) { 10 }" , "expected" : 10} , 
            {"input" : "if (false) { 10 }" , "expected" : None} , 
            {"input" : "if (1) { 10 }" , "expected" : 10} , 
            {"input" : "if (1 < 2) { 10 }" , "expected" : 10} , 
            {"input" : "if (1 > 2) { 10 }" , "expected" : None} , 
            {"input" : "if (1 > 2) { 10 } else { 20 }" , "expected" : 20} , 
            {"input" : "if (1 < 2) { 10 } else { 20 }" , "expected" : 10} 
        ]
        for tt in tests:
            evaluated = testEval(tt["input"])
            if isinstance(tt["expected"] , int):
                self.assertTrue(testIntegerObject(evaluated , tt["expected"]))
            else:
                self.assertTrue(testNullObject(evaluated))
    '''
    def testReturnStatements(self):
        tests = [
            {"input" : "return 10;" , "expected" : 10} , 
            #{"input" : "return 10; 9;" , "expected" : 10} , 
            #{"input" : "return 2 * 5; 9;" , "expected" : 10} , 
            #{"input" : "9; return 2 * 5; 9;" , "expected" : 10} , 
            #{"input" : """
            #    if (10 > 1) {
            #        if (10 > 1) {
            #            return 10;
            #        }
            #    return 1; }""" , "expected" : 10},
            #{"input" : """
            #    let f = fn(x) {
            #        return x;
            #        x + 10;
            #    };
            #    f(10);""" , "expected" : 10},
            #{"input" : """
            #    let f = fn(x) {
            #        let result = x + 10;
            #        return result;
            #        return 10;
            #    };
            #    f(10);""" , "expected" : 20}       
        ]
        for tt in tests:
            evaluated = testEval(tt["input"])
            self.assertTrue(testIntegerObject(evaluated , tt["expected"]))

if __name__ == "__main__":
    unittest.main()