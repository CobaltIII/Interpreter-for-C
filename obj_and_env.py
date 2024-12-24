from parser import *
from tokens import *
from abc import ABC, abstractmethod
import hashlib
from typing import Callable

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

class ObjectType:
    NULL_OBJ = "NULL"
    ERROR_OBJ = "ERROR"
    INTEGER_OBJ = "INTEGER"
    BOOLEAN_OBJ = "BOOLEAN"
    STRING_OBJ = "STRING"
    RETURN_VALUE_OBJ = "RETURN_VALUE"
    FUNCTION_OBJ = "FUNCTION"
    BUILTIN_OBJ = "BUILTIN"
    ARRAY_OBJ = "ARRAY"
    HASH_OBJ = "HASH"

class Object(ABC):
    @abstractmethod
    def type(self) -> ObjectType:
        pass
    
    @abstractmethod
    def inspect(self) -> str:
        pass

class HashKey():
    def __init__(self, type: ObjectType, value: int):
        self.Type_ = type
        self.Value = value    

class Hashable(ABC):
    @abstractmethod
    def hash_key(self) -> HashKey:
        pass

BuiltinFunction = Callable[[List[Object]], Object]

class Integer(Object , Hashable):
    def __init__(self, value: int):
        self.value = value
    
    def type(self) -> str:
        return ObjectType.INTEGER_OBJ
    
    def inspect(self) -> str:
        return str(self.value)
    
    def hash_key(self) -> HashKey:
        return HashKey(type = self.type(), value = int(self.value))
    
class Boolean(Object , Hashable):
    def __init__(self, value: bool):
        self.value = value
    
    def type(self) -> str:
        return ObjectType.BOOLEAN_OBJ
    
    def inspect(self) -> str:
        return str(self.value).lower()
    
    def hash_key(self) -> HashKey:
        valuee = 0
        if self.value:
            valuee = 1
        return HashKey(type = self.type(), value = valuee)

class Null(Object):
    def type(self) -> str:
        return ObjectType.NULL_OBJ
    
    def inspect(self) -> str:
        return None

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
    def __init__(self, parameters : list[Identifier], body : BlockStatement, env : Environment):
        self.parameters = parameters
        self.body = body
        self.env = env
    
    def type(self) -> str:
        return ObjectType.FUNCTION_OBJ
    
    def inspect(self) -> str:
        params = "[NO PARAMETERS]"
        if len(self.parameters) > 0:
            params = ""
            for i in self.parameters:
                params += i.String() + ", "
            params = params[:-2]
        return f"fn({params}) {{\n{self.body}\n}}"
    
class String(Object , Hashable):
    def __init__(self, value: str):
        self.value = value
    
    def type(self) -> str:
        return ObjectType.STRING_OBJ
    
    def inspect(self) -> str:
        return self.value
    
    def hash_key(self) -> HashKey:
        h = hashlib.blake2b(digest_size=8)  # 64 bits = 8 bytes.
        h.update(self.value.encode('utf-8'))
        x = HashKey(type=self.type(), value=int.from_bytes(h.digest(), byteorder='big'))
        return x

class Builtin(Object):
    def __init__(self, fn : BuiltinFunction):
        self.func = fn
    
    def type(self) -> str:
        return ObjectType.BUILTIN_OBJ
    
    def inspect(self) -> str:
        return "builtin function"

class Array(Object):
    def __init__(self, elements : list[Object]):
        self.elements = elements
    
    def type(self) -> str:
        return ObjectType.ARRAY_OBJ
    
    def inspect(self) -> str:
        elements = ""
        for i in self.elements:
            elements += i.inspect() + ", "
        elements = elements[:-2]
        return f"[{elements}]"

class HashPair:
    def __init__(self, key : Object, value : Object):
        self.key = key
        self.value = value

class Hash(Object):
    def __init__(self, pairs : dict[HashKey, HashPair] , godPairs : dict[HashKey, HashPair] = {}):
        self.pairs = pairs
        self.godPairs = godPairs
    
    def type(self) -> str:
        return ObjectType.HASH_OBJ
    
    def inspect(self) -> str:
        pairs = ""
        for key in self.pairs:
            pairs += f"{key.Value}: {self.pairs[key].value.inspect()}, "
        pairs = pairs[:-2]
        return f"{{{pairs}}}"

##############################################################
