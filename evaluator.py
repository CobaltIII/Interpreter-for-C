from parser import *
from tokens import * 
from obj_and_env import *
from parser import Boolean as BL

##############################################################

NULL = Null()
TRUE = Boolean(True)
FALSE = Boolean(False)

builtins = {}
x = Builtin(fn=lambda args: (
    newError(f"wrong number of arguments. got={str(len(args))}, want=1") 
    if len(args) != 1 else (
        Integer(len(args[0].elements)) if isinstance(args[0], Array) else (
            Integer(len(args[0].value)) if isinstance(args[0], String) else
            newError("argument to `len` not supported, got ", args[0].type())
        )
    )
))
builtins["len"] = x

x = Builtin(fn=lambda args: (
    [print(arg.inspect()) for arg in args],
    NULL
)[1])
builtins["print"] = x

x = Builtin(
    fn=lambda args: (
        newError(f"wrong number of arguments. got={len(args)}, want=1")
        if len(args) != 1 else
        newError("argument to `first` must be ARRAY, got ", args[0].type())
        if args[0].type() != "ARRAY" else
        args[0].elements[0]
        if len(args[0].elements) > 0 else
        NULL
    )
)
builtins["first"] = x

x = Builtin(
    fn=lambda args: (
        newError(f"wrong number of arguments. got={len(args)}, want=1")
        if len(args) != 1 else
        newError("argument to `last` must be ARRAY, got ", args[0].type())
        if args[0].type() != "ARRAY" else
        args[0].elements[-1]
        if len(args[0].elements) > 0 else
        NULL
    )
)
builtins["last"] = x

x = Builtin(
    fn=lambda args: (
        newError(f"wrong number of arguments. got={len(args)}, want=1")
        if len(args) != 1 else
        newError("argument to `rest` must be ARRAY, got ", args[0].type())
        if not isinstance(args[0], Array) else
        Array(args[0].elements[1:])  
        if len(args[0].elements) > 0 else
        Array([])
    )
)
builtins["rest"] = x

x = Builtin(
    fn=lambda args: (
        newError(f"wrong number of arguments. got={len(args)}, want=2")
        if len(args) != 2 else
        newError("argument to `push` must be ARRAY, got ", args[0].type())
        if not isinstance(args[0], Array) else
        Array(args[0].elements + [args[1]])  # Create a new array by appending the second argument
    )
)
builtins["push"] = x


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
        x = ReturnValue(val)
        return ReturnValue(val)

    elif isinstance(node, LetStatement):
        val = Eval(node.Value , env)
        if isError(val):
            return val
        else:
            env.set(node.Name.Value , val)

    ################EXPRESSIONS################

    elif isinstance(node, IntegerLiteral):
        return Integer(node.Value)

    elif isinstance(node, StringLiteral):
        return String(value = node.Value)

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
        return Function(params , body , env)

    elif isinstance(node, CallExpression):
        function = Eval(node.Function , env)
        if isError(function):
            return function
        args = evalExpressions(node.Arguments , env)
        if len(args) == 1 and isError(args[0]):
            return args[0]
        return applyFunction(function, args)

    ################HIGHER OBJECTS################

    elif isinstance(node, ArrayLiteral):
        elementss = evalExpressions(node.Elements , env)
        if len(elementss) == 1 and isError(elementss[0]):
            return elementss[0]
        return Array(elements = elementss)

    elif isinstance(node, IndexExpression):
        left = Eval(node.Left , env)
        if isError(left):
            return left
        index = Eval(node.Index , env)
        if isError(index):
            return index
        return evalIndexExpression(left, index)
    
    elif isinstance(node, HashLiteral):
        return evalHashLiteral(node, env)

    return None

def evalProgram(program : Program, env : Environment):
    result = None
    for statement in program.Statements:
        result = Eval(statement, env)
        if isinstance(result, ReturnValue):
            return result.value
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
    elif left.type() == ObjectType.STRING_OBJ and right.type() == ObjectType.STRING_OBJ:
        return evalStringInfixExpression(operator, left, right)
    elif operator == "==":
        return nativeBoolToBooleanObject(left == right)
    elif operator == "!=":
        return nativeBoolToBooleanObject(left != right)
    elif left.type() != right.type():
        return newError("type mismatch: " , left.type() , operator , right.type())
    else:
        return newError("unknown operator: " , left.type() , operator , right.type())
    
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
        return newError("unknown operator: -" , right.type())
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

def evalStringInfixExpression(operator : str , left : Object, right : Object):
    if operator != "+":
        return newError("unknown operator: " , left.type() , operator , right.type())
    leftVal = left.value
    rightVal = right.value
    return String(leftVal + rightVal)

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
    val = env.get(node.Value)
    if val == None:
        return builtins.get(node.Value , newError(f"identifier not found: {node.Value}"))
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
    
def newError(format_string : str, *args):
    if len(args) == 0:
        return Error(format_string)
    elif len(args) == 1:
        return Error(format_string + args[0])        
    return Error(format_string + " ".join(args))

def isError(obj : Object):
    if obj != None:
        return (obj.type() == ObjectType.ERROR_OBJ)
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
        if isinstance(fn , Builtin):
            return fn.func(args)
        return newError(f"not a function: {fn.type()}")
    extended_env = extendFunctionEnv(fn, args)
    evaluated = Eval(fn.body, extended_env)
    return unwrapReturnValue(evaluated)

def extendFunctionEnv(fn : Function , args : list[Object]):
    env = NewEnclosedEnvironment(fn.env)
    for paramIdx in range (len(fn.parameters)):
        param = fn.parameters[paramIdx]
        env.set(param.Value , args[paramIdx])

    return env

def unwrapReturnValue(obj : Object):
    if isinstance(obj, ReturnValue):
        return obj.value

    return obj

def evalIndexExpression(left : Object, index : Object):
    if left.type() == ObjectType.ARRAY_OBJ and index.type() == ObjectType.INTEGER_OBJ:
        return evalArrayIndexExpression(left, index)
    elif left.type() == ObjectType.HASH_OBJ:
        return evalHashIndexExpression(left, index)
    else:
        return newError("index operator not supported: " , left.type())

def evalArrayIndexExpression(array : Object, index : Object):
    arrayObject = array
    idx = index.value
    max = len(arrayObject.elements) - 1
    if idx < 0 or idx > max:
        return NULL
    return arrayObject.elements[idx]

def evalHashLiteral(node : HashLiteral, env : Environment):
    pairs = {}
    godPairs = {}
    for keyNode, valueNode in node.Pairs.items():
        key = Eval(keyNode, env)
        if isError(key):
            return key
        value = Eval(valueNode, env)
        if isError(value):
            return value
        hashKey = key.hash_key()
        pairs[hashKey] = HashPair(key = key, value = value)
        godPairs[(key.type() , hashKey.Value)] = hashKey
    return Hash(pairs = pairs , godPairs = godPairs)

def evalHashIndexExpression(hash : Object, index : Object):
    hashObject = hash
    if not isinstance(index, Hashable):
        return newError(f"unusable as hash key: {index.type()}")
    key = hashObject.godPairs.get((index.type() , index.hash_key().Value))
    pair = hashObject.pairs.get(key)
    if pair == None:
        return NULL
    return pair.value
