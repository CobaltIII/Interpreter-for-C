from parser import *
from tokens import *
from abc import ABC, abstractmethod

##############################################################

class ObjectType:
    NULL_OBJ = "NULL"
    ERROR_OBJ = "ERROR"
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    FUNCTION_OBJ = "FUNCTION"

class Object(ABC):
    @abstractmethod
    def type(self) -> ObjectType:
        pass
    
    @abstractmethod
    def inspect(self) -> str:
        pass

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
        return "ERROR: " + self.message

class Function(Object):
    def __init__(self, parameters : list, body : str, env : dict):
        self.parameters = parameters
        self.body = body
        self.env = env
    
    def type(self) -> str:
        return ObjectType.FUNCTION_OBJ
    
    def inspect(self) -> str:
        params = ", ".join(self.parameters)
        return f"fn({params}) {{\n{self.body}\n}}"
    
##############################################################

class Environment:
    def __init__(self, outer=None):
        self.store = {}
        self.outer = outer

    def get(self, name):
        obj = self.store.get(name)
        if obj is None and self.outer is not None:
            obj = self.outer.get(name)
        return obj

    def set(self, name, val):
        self.store[name] = val
        return val

def NewEnclosedEnvironment(outer):
    env = Environment()
    env.outer = outer
    return env

def NewEnvironment():
    return Environment()

##############################################################