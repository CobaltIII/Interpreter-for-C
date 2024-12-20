from parser import *
from tokens import *

##############################################################

class Environment:
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    @staticmethod
    def NewEnclosedEnvironment(outer):
        env = Environment()
        env.outer = outer
        return env

    def Get(self, name):
        obj = self.store.get(name)
        if obj is None and self.outer is not None:
            return self.outer.get(name)
        return obj, obj is not None

    def Set(self, name, val):
        self.store[name] = val
        return val
    
class ObjectType:
    NULL_OBJ = "NULL"
    ERROR_OBJ = "ERROR"
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    FUNCTION_OBJ = "FUNCTION"

class Object:
    def type(self) -> str:
        raise NotImplementedError

    def inspect(self) -> str:
        raise NotImplementedError

class Integer(Object):
    def __init__(self, value: int):
        self.value = value

    def type(self) -> str:
        return ObjectType.INTEGER_OBJ

    def inspect(self) -> str:
        return str(self.value)

class Boolean(Object):
    def __init__(self, value: bool):
        self.value = value

    def type(self) -> str:
        return ObjectType.BOOLEAN_OBJ

    def inspect(self) -> str:
        return str(self.value).lower()

class Null(Object):
    def type(self) -> str:
        return ObjectType.NULL_OBJ

    def inspect(self) -> str:
        return "null"

class ReturnValue(Object):
    def __init__(self, value: Object):
        self.value = value

    def type(self) -> str:
        return ObjectType.RETURN_VALUE_OBJ

    def inspect(self) -> str:
        return self.value.inspect()

class Error(Object):
    def __init__(self, message: str):
        self.message = message

    def type(self) -> str:
        return ObjectType.ERROR_OBJ

    def inspect(self) -> str:
        return f"ERROR: {self.message}"

class Function(Object):
    def __init__(self, parameters: List[str], body: str, env: dict):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self) -> str:
        return ObjectType.FUNCTION_OBJ

    def inspect(self) -> str:
        params = ", ".join(self.parameters)
        return f"fn({params}) {{\n{self.body}\n}}"

##############################################################

NULL = None
TRUE = True
FALSE = False

def Eval (node, env):
    if isinstance(node, Program):
        return evalProgram(node, env)

    elif isinstance(node, BlockStatement):
        return evalBlockStatement(node, env)

    elif isinstance(node, ExpressionStatement):
        return Eval(node.Expression , env)

    elif isinstance(node, ReturnStatement):
        val = Eval(node.ReturnValue , env)
        if isError(val):
            return val
        else:
            return ReturnValue(val)

    elif isinstance(node, LetStatement):
        val = Eval(node.ReturnValue , env)
        if isError(val):
            return val
        else:
            env.Set(node.Name.Value , val)

    ################EXPRESSIONS################

    elif isinstance(node, IntegerLiteral):
        return Integer(node.Value)

    elif isinstance(node, Boolean):
        return nativeBoolToBooleanObject(node.Value)

    elif isinstance(node, PrefixExpression):
        right = Eval(node.Right , env)
        if isError(right):
            return right
        return evalPrefixExpression(node.Operator , right)

    elif isinstance(node, InfixExpression):
        left = Eval(node.Left , env)
        if isError(left):
            return left
        right = Eval(node.Right , env)
        if isError(right):
            return right
        return evalInfixExpression(node.Operator , left, right)

    elif isinstance(node, IfExpression):
        return evalIfExpression(node , env)

    elif isinstance(node, Identifier):
        return evalIdentifier(node, env)

    elif isinstance(node, FunctionLiteral):
        params = node.Parameters
        body = node.Body
        return Function(params , env , body)

    '''
    elif isinstance(node, CallExpression):
        function = Eval(node.Function , env)
        if isError(function):
            return function
        args = 
    '''
    return None

def evalProgram(program, env):
    result = None
    for statement in program.Statements:
        result = Eval(statement, env)

        if isinstance(result, ReturnValue):
            return result.value
        elif isinstance(result, Error):
            return result

    return result

def evalBlockStatement(block, env):
    result = Object()
    for statement in block.Statements:
        result = Eval(statement, env)
        if result != None:
            if isinstance(result , ObjectType.RETURN_VALUE_OBJ):
                return result
            if isinstance(result , ObjectType.ERROR_OBJ):
                return result

    return result

def nativeBoolToBooleanObject(input_bool):
    if input_bool:
        return True
    else:
        return False

def evalPrefixExpression(operator, right):
    if operator == "!":
        return evalBangOperatorExpression(right)
    elif operator == "-":
        return evalMinusPrefixOperatorExpression(right)
    else:
        return newError("unknown operator error : " , operator  , type(right))
    
def evalInfixExpression(operator, left, right):
    if isinstance(left, ObjectType.INTEGER_OBJ) and isinstance(right , ObjectType.INTEGER_OBJ):
        return evalIntegerInfixExpression(operator, left, right)
    elif operator == "==":
        return nativeBoolToBooleanObject(left == right)
    elif operator == "!=":
        return nativeBoolToBooleanObject(left != right)
    elif type(left) != type(right):
        return newError("Type mismatch : " , type(left) , operator , type(right))
    else:
        return newError("Unknown operator : " , type(left) , operator , type(right))
    
def evalBangOperatorExpression(right) : 
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE

def evalMinusPrefixOperatorExpression(right):
    if not isinstance(right, ObjectType.INTEGER_OBJ):
        return newError("unkown operator error : " , type(right))
    value = right.Value
    return Integer(-value)

def evalIntegerInfixExpression(operator , left, right):
    leftVal = left.Value
    rightVal = right.Value

    if operator == "+":
        return Integer(leftVal + rightVal)
    elif operator == "-":
        return Integer(leftVal - rightVal)
    elif operator == "*":
        return Integer(leftVal * rightVal)
    elif operator == "/":
        return Integer(leftVal / rightVal)
    elif operator == "<":
        return nativeBoolToBooleanObject(leftVal < rightVal)
    elif operator == ">":
        return nativeBoolToBooleanObject(leftVal > rightVal)
    elif operator == "==":
        return nativeBoolToBooleanObject(leftVal == rightVal)
    elif operator == "!=":
        return nativeBoolToBooleanObject(leftVal != rightVal)
    else:
        return newError("unkown operator error : " , type(right) , operator ,  type(left))
    
def evalIfExpression(ie , env):
    condition = Eval(ie.Condition, env)
    if isError(condition):
        return condition
    if isTruthy(condition):
        return Eval(ie.Consequence, env)
    elif ie.Alternative != None:
        return eval(ie.Alternative, env)
    else:
        return None
    
def evalIdentifier(node, env):
    val, found = env.get(node.value)
    if not found:
        return Error(f"identifier not found: {node.value}")

    return val

def isTruthy(obj):
    if obj == NULL:
        return False
    elif obj == TRUE:
        return True
    elif obj == FALSE :
        return False
    else:
        return True
    
def newError(format_string, *args):
    return Error(format_string.format(*args))

def isError(obj):
    if obj != None:
        return isinstance(obj, ObjectType.ERROR_OBJ)
    else:
        return False

def evalExpressions(exps, env):
    results = []
    for i in exps:
        evaluated = Eval(e, env)
        if isError(evaluated):
            return evaluated
        results.append(evaluated)
    return results

def applyFunction(fn, args):
    if not isinstance(fn, Function):
        return newError(f"not a function: {fn.type()}")

    extended_env = extendFunctionEnv(fn, args)
    evaluated = Eval(fn.body, extended_env)
    return unwrapReturnValue(evaluated)

def extendFunctionEnv(fn , args):
    env = Environment.NewEnclosedEnvironment(fn.env)
    for paramIdx in range (len(fn.Parameters)):
        param = fn.Parameters[paramIdx]
        env.Set(param.Value , args[paramIdx])

    return env

def unwrapReturnValue(obj):
    if isinstance(obj, ReturnValue):
        return obj.value

    return obj


