from parser import *
from tokens import * 
from obj_and_env import *
from parser import Boolean as BL

##############################################################

NULL = Null()
TRUE = Boolean(True)
FALSE = Boolean(False)

def Eval (node : Node, env : Environment) -> Object:

    #print(node.String() , type(node) , node)

    ################STATEMENTS################

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
        return ReturnValue(val)

    elif isinstance(node, LetStatement):
        val = Eval(node.Value , env)
        if isError(val):
            return val
        else:
            env.Set(node.Name , val)

    ################EXPRESSIONS################

    elif isinstance(node, IntegerLiteral):
        return Integer(node.Value)

    elif isinstance(node, Boolean) or isinstance(node, BL):
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

    elif isinstance(node, CallExpression):
        function = Eval(node.Function , env)
        if isError(function):
            return function
        args = evalExpressions(node.Arguments , env)
        if len(args) == 1 and isError(args[0]):
            return args[0]
        return applyFunction(function, args)

    return None

def evalProgram(program : Program, env : Environment):
    result = None
    for statement in program.Statements:
        result = Eval(statement, env)
        if isinstance(result, ReturnValue):
            return result.value()
        elif isinstance(result, Error):
            return result
    return result

def evalBlockStatement(block : BlockStatement, env : Environment):
    result = None
    for statement in block.Statements:
        result = Eval(statement, env)
        if result != None:
            x = result.type()
            if x == ObjectType.RETURN_VALUE_OBJ or x == ObjectType.ERROR_OBJ:
                return result
    return result

def nativeBoolToBooleanObject(input_bool : bool):
    if input_bool:
        return TRUE
    else:
        return FALSE

def evalPrefixExpression(operator : str, right : Object):
    if operator.strip() == "!":
        return evalBangOperatorExpression(right)
    elif operator.strip() == "-":
        return evalMinusPrefixOperatorExpression(right)
    else:
        return newError("unknown operator error : " , operator  , right.type())
    
def evalInfixExpression(operator : str, left : Object, right : Object):
    if left.type() == ObjectType.INTEGER_OBJ and right.type() == ObjectType.INTEGER_OBJ:
        return evalIntegerInfixExpression(operator, left, right)
    elif operator == "==":
        return nativeBoolToBooleanObject(left == right)
    elif operator == "!=":
        return nativeBoolToBooleanObject(left != right)
    elif left.type() != right.type():
        return newError("Type mismatch : " , left.type() , operator , right.type())
    else:
        return newError("Unknown operator : " , left.type() , operator , right.type())
    
def evalBangOperatorExpression(right : Object) : 
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE

def evalMinusPrefixOperatorExpression(right : Object):
    if right.type() != ObjectType.INTEGER_OBJ.strip():
        return newError("unkown operator error : " , type(right))
    value = right.value
    return Integer(-value)

def evalIntegerInfixExpression(operator : str , left : Object, right : Object):
    leftVal = left.value
    rightVal = right.value

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
    
def evalIfExpression(ie : IfExpression, env : Environment):
    condition = Eval(ie.Condition, env)
    if isError(condition):
        return condition
    if isTruthy(condition):
        return Eval(ie.Consequence, env)
    elif ie.Alternative != None:
        return Eval(ie.Alternative, env)
    else:
        return NULL
    
def evalIdentifier(node : Identifier, env : Environment):
    val, found = env.get(node.value)
    if not found:
        return Error(f"identifier not found: {node.value}")

    return val

def isTruthy(obj : Object):
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

def isError(obj : Object):
    if obj != None:
        return (obj.type == ObjectType.ERROR_OBJ)
    else:
        return False

def evalExpressions(exps : list[Expression], env : Environment):
    results = []
    for i in exps:
        evaluated = Eval(i, env)
        if isError(evaluated):
            return evaluated
        results.append(evaluated)
    return results

def applyFunction(fn : Object, args : list[Object]):
    if not isinstance(fn, Function):
        return newError(f"not a function: {fn.type()}")

    extended_env = extendFunctionEnv(fn, args)
    evaluated = Eval(fn.body, extended_env)
    return unwrapReturnValue(evaluated)

def extendFunctionEnv(fn : Function , args : list[Object]):
    env = Environment.NewEnclosedEnvironment(fn.env)
    for paramIdx in range (len(fn.Parameters)):
        param = fn.Parameters[paramIdx]
        env.Set(param.Value , args[paramIdx])

    return env

def unwrapReturnValue(obj : Object):
    if isinstance(obj, ReturnValue):
        return obj.value

    return obj

