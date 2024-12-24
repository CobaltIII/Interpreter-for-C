from typing import List, Optional
from tokens import Token
import unittest

class Node:
    def TokenLiteral(self) -> str:
        pass

    def String(self) -> str:
        pass
class Statement(Node):
    def statementNode(self):
        pass
class Expression(Node):
    def expressionNode(self):
        pass
class Program(Node):
    def __init__(self):
        self.Statements: List[Statement] = []

    def TokenLiteral(self) -> str:
        if len(self.Statements) > 0:
            return self.Statements[0].TokenLiteral()
        else:
            return ""

    def String(self) -> str:
        out = []
        for s in self.Statements:
            out.append(s.String())
        return "".join(out)

# Statements
class LetStatement(Statement):
    def __init__(self, token: Token, name=None, value=None):
        self.Token = token
        self.Name = name
        self.Value = value

    def statementNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        out = []
        out.append(f"{self.TokenLiteral()} {self.Name.String()} = ")
        if self.Value:
            out.append(self.Value.String())
        out.append(";")
        return "".join(out)
class ReturnStatement(Statement):
    def __init__(self, token: Token, return_value=None):
        self.Token = token
        self.ReturnValue = return_value

    def statementNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        out = [f"{self.TokenLiteral()} "]
        if self.ReturnValue:
            out.append(self.ReturnValue.String())
        out.append(";")
        return "".join(out)
class ExpressionStatement(Statement):
    def __init__(self, token: Token, expression=None):
        self.Token = token
        self.Expression = expression

    def statementNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        if self.Expression:
            return self.Expression.String()
        return ""
class BlockStatement(Statement):
    def __init__(self, token: Token):
        self.Token = token
        self.Statements: List[Statement] = []

    def statementNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        out = []
        for s in self.Statements:
            out.append(s.String())
        return "".join(out)
# Expressions
class Identifier(Expression):
    def __init__(self, token: Token, value: str):
        self.Token = token
        self.Value = value

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return self.Value
class Boolean(Expression):
    def __init__(self, token: Token, value: bool):
        self.Token = token
        self.Value = value

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return self.Token.literal
class IntegerLiteral(Expression):
    def __init__(self, token: Token, value: int):
        self.Token = token
        self.Value = value

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return self.Token.literal
class PrefixExpression(Expression):
    def __init__(self, token: Token, operator: str, right: Expression):
        self.Token = token
        self.Operator = operator
        self.Right = right

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return f"({self.Operator}{self.Right.String()})"
class InfixExpression(Expression):
    def __init__(self, token: Token, left: Expression, operator: str, right: Expression):
        self.Token = token
        self.Left = left
        self.Operator = operator
        self.Right = right

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return f"({self.Left.String()} {self.Operator} {self.Right.String()})"
class IfExpression(Expression):
    def __init__(self, token: Token, condition: Expression, consequence: BlockStatement, alternative: Optional[BlockStatement]):
        self.Token = token
        self.Condition = condition
        self.Consequence = consequence
        self.Alternative = alternative

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        out = [f"if{self.Condition.String()} {self.Consequence.String()}"]
        if self.Alternative:
            out.append(f"else {self.Alternative.String()}")
        return "".join(out)
class FunctionLiteral(Expression):

    def __init__(self):
        self.Token = None
        self.Parameters = None
        self.Body = None

    def __init__(self, token: Token, parameters: List[Identifier], body: BlockStatement):
        self.Token = token
        self.Parameters = parameters
        self.Body = body

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        params = [p.String() for p in self.Parameters]
        return f"{self.TokenLiteral()}({', '.join(params)}) {self.Body.String()}"
class CallExpression(Expression):
    def __init__(self, token: Token, function: Expression, arguments: List[Expression]):
        self.Token = token
        self.Function = function
        self.Arguments = arguments

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        args = [arg.String() for arg in self.Arguments]
        return f"{self.Function.String()}({', '.join(args)})"
class StringLiteral(Expression):
    def __init__(self, token: Token, value: str):
        self.Token = token
        self.Value = value

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return self.Token.literal
class ArrayLiteral(Expression):
    def __init__(self, token: Token, elements: List[Expression]):
        self.Token = token
        self.Elements = elements

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        if len(self.Elements) == 0:
            return "[]"
        if len(self.Elements) == 1:
            return f"[{self.Elements[0].String()}]"
        elements = [e.String() for e in self.Elements]
        return f"[{', '.join(elements)}]"
class IndexExpression(Expression):
    def __init__(self, token: Token, left: Expression, index: Expression):
        self.Token = token
        self.Left = left
        self.Index = index

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        return f"({self.Left.String()}[{self.Index.String()}])"
class HashLiteral(Expression):
    def __init__(self, token: Token, pairs: dict[Expression : Expression]):
        self.Token = token
        self.Pairs = pairs

    def expressionNode(self):
        pass

    def TokenLiteral(self) -> str:
        return self.Token.literal

    def String(self) -> str:
        if len(self.Pairs) == 0:
            return "{}"
        pairs = [f"{k.String()}: {v.String()}" for k, v in self.Pairs.items()]
        return f"{{{', '.join(pairs)}}}"

'''
class TestStringMethod(unittest.TestCase):
    def test_string(self):
        program = Program()
        program.Statements = [
            LetStatement(
                token = Token("LET", "let"),
                name=Identifier(
                    token=Token("IDENT", "five"),
                    value="five",
                ),
                value=Identifier(
                    token=Token("IDENT", "5"),
                    value="5",
                ),
            )
        ]

        expected = "let five = 5;"
        self.assertEqual(program.String(), expected, f"program.String() wrong. got={program.String()}")

'''

########################################################################################################################################################

from tokens import TokenType

LOWEST = 1
EQUALS = 2        # ==
LESSGREATER = 3   # > or <
SUM = 4           # +
PRODUCT = 5       # *
PREFIX = 6        # -X or !X
CALL = 7          # myFunction(X)
INDEX = 8

# Token precedences
precedences = {
    TokenType.EQ: EQUALS,
    TokenType.NOT_EQ: EQUALS,
    TokenType.LT: LESSGREATER,
    TokenType.GT: LESSGREATER,
    TokenType.PLUS: SUM,
    TokenType.MINUS: SUM,
    TokenType.SLASH: PRODUCT,
    TokenType.ASTERISK: PRODUCT,
    TokenType.LPAREN: CALL,
    TokenType.LBRACKET : INDEX
}

class Parser : 
    def registerPrefix(self, tokenType, fn):
        self.prefixParseFns[tokenType] = fn

    def registerInfix(self, tokenType, fn):
        self.infixParseFns[tokenType] = fn

    def __init__(self , lexer_instance):
        self.l = lexer_instance
        self.errors = []

        self.curToken = None
        self.peekToken = None

        self.prefixParseFns = {}
        self.infixParseFns = {}

        self.registerPrefix(TokenType.IDENT, self.parseIdentifier)
        self.registerPrefix(TokenType.INT, self.parseIntegerLiteral)
        self.registerPrefix(TokenType.STRING, self.parseStringLiteral)
        self.registerPrefix(TokenType.BANG, self.parsePrefixExpression)
        self.registerPrefix(TokenType.MINUS, self.parsePrefixExpression)
        self.registerPrefix(TokenType.TRUE, self.parseBoolean)
        self.registerPrefix(TokenType.FALSE, self.parseBoolean)
        self.registerPrefix(TokenType.LPAREN, self.parseGroupedExpression)
        self.registerPrefix(TokenType.IF, self.parseIfExpression)
        self.registerPrefix(TokenType.FUNCTION, self.parseFunctionLiteral)
        self.registerPrefix(TokenType.LBRACKET, self.parseArrayLiteral)
        self.registerPrefix(TokenType.LBRACE, self.parseHashLiteral)

        self.registerInfix(TokenType.PLUS, self.parseInfixExpression)
        self.registerInfix(TokenType.MINUS, self.parseInfixExpression)
        self.registerInfix(TokenType.SLASH, self.parseInfixExpression)
        self.registerInfix(TokenType.ASTERISK, self.parseInfixExpression)
        self.registerInfix(TokenType.EQ, self.parseInfixExpression)
        self.registerInfix(TokenType.NOT_EQ, self.parseInfixExpression)
        self.registerInfix(TokenType.LT, self.parseInfixExpression)
        self.registerInfix(TokenType.GT, self.parseInfixExpression)
        self.registerInfix(TokenType.LPAREN, self.parseCallExpression)
        self.registerInfix(TokenType.LBRACKET, self.parseIndexExpression)

        self.nextToken()
        self.nextToken()

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.l.next_token()
    
    def curTokenIs(self , t):
        return self.curToken.type == t
    
    def peekTokenIs(self, t):
        return self.peekToken.type == t
    
    def expectPeek(self, t):
        if self.peekTokenIs(t):
            self.nextToken()
            return True
        else:
            self.peekError(t)
            return False
    
    def Errors(self):
        return self.errors
    
    def peekError(self, t):
        msg = f"expected next token to be {t}, got {self.peekToken.type} instead"
        self.errors.append(msg)

    def noPrefixParseFnError(self, t):
        msg = f"no prefix parse function for {t} found"
        self.errors.append(msg)
    
    def ParseProgram(self):
        program = Program()
        program.Statements = []

        while not self.curTokenIs(TokenType.EOF):
            stmt = self.parseStatement()
            if stmt is not None:
                program.Statements.append(stmt)
            self.nextToken()

        return program
    
    def parseStatement(self):
        if self.curToken.type == TokenType.LET:
            return self.parseLetStatement()
        elif self.curToken.type == TokenType.RETURN:
            return self.parseReturnStatement()
        else:
            return self.parseExpressionStatement()
    
    def parseLetStatement(self):
        stmt =  LetStatement(token=self.curToken)

        if not self.expectPeek(TokenType.IDENT):
            return None

        stmt.Name =  Identifier(token=self.curToken, value=self.curToken.literal)

        if not self.expectPeek(TokenType.ASSIGN):
            return None

        self.nextToken()

        stmt.Value = self.parseExpression(LOWEST)

        if self.peekTokenIs(TokenType.SEMICOLON):
            self.nextToken()

        return stmt
    
    def parseReturnStatement(self):
        stmt = ReturnStatement(token=self.curToken)

        self.nextToken()

        stmt.ReturnValue = self.parseExpression(LOWEST)

        if self.peekTokenIs(TokenType.SEMICOLON):
            self.nextToken()

        return stmt
    
    def parseExpressionStatement(self):
        stmt =  ExpressionStatement(token=self.curToken , expression=self.parseExpression(LOWEST))

        #stmt.Expression = self.parseExpression(LOWEST)

        if self.peekTokenIs(TokenType.SEMICOLON):
            self.nextToken()
        return stmt
    
    def parseExpression(self, precedence):
        prefix = self.prefixParseFns.get(self.curToken.type)
        if prefix is None:
            self.noPrefixParseFnError(self.curToken.type)
            return None
        leftExp = prefix()
        

        while not self.peekTokenIs(TokenType.SEMICOLON) and precedence < self.peekPrecedence():
            infix = self.infixParseFns.get(self.peekToken.type)
            if infix is None:
                return leftExp

            self.nextToken()
            leftExp = infix(leftExp)
        
        return leftExp

    def peekPrecedence(self):
        return precedences.get(self.peekToken.type, LOWEST)

    def curPrecedence(self):
        return precedences.get(self.curToken.type, LOWEST)

    def parseIdentifier(self):
        return  Identifier(token=self.curToken, value=self.curToken.literal)

    def parseIntegerLiteral(self):
        try : 
            lit =  IntegerLiteral(token=self.curToken , value = int(self.curToken.literal))
        except ValueError:
            msg = f"could not parse {self.curToken.literal} as integer"
            self.errors.append(msg)
            return None
        return lit

    def parseStringLiteral(self):
        return StringLiteral(token= self.curToken, value = self.curToken.literal)

    def parsePrefixExpression(self):
        x = self.curToken
        self.nextToken()
        expression =  PrefixExpression(
            token =x,
            operator=x.literal,
            right=self.parseExpression(PREFIX)
        )

        return expression

    def parseInfixExpression(self, left):
        x = self.curToken
        precedence = self.curPrecedence()
        self.nextToken()
        expression =  InfixExpression(
            token =x,
            operator=x.literal,
            left=left,
            right=self.parseExpression(precedence)
        )

        return expression

    def parseBoolean(self):
        return  Boolean(
            token=self.curToken,
            value=self.curTokenIs(TokenType.TRUE)
        )
    
    def parseGroupedExpression(self):
        self.nextToken()
        exp = self.parseExpression(LOWEST)

        if not self.expectPeek(TokenType.RPAREN):
            return None

        return exp

    def parseIfExpression(self):
        para_token = self.curToken
        if not self.expectPeek(TokenType.LPAREN):
            return None
        self.nextToken()
        para_condition = self.parseExpression(LOWEST)
        if not self.expectPeek(TokenType.RPAREN):
            return None

        if not self.expectPeek(TokenType.LBRACE):
            return None
        
        para_consequence = self.parseBlockStatement()
        para_alternative = None
        if self.peekTokenIs(TokenType.ELSE):
            self.nextToken()

            if not self.expectPeek(TokenType.LBRACE):
                return None

            para_alternative = self.parseBlockStatement()
        
        expression = IfExpression(token=para_token , condition=para_condition , consequence=para_consequence , alternative=para_alternative)
        return expression

    def parseBlockStatement(self):
        block =  BlockStatement(token=self.curToken)
        block.Statements = []

        self.nextToken()

        while not self.curTokenIs(TokenType.RBRACE) and not self.curTokenIs(TokenType.EOF):
            stmt = self.parseStatement()
            if stmt is not None:
                block.Statements.append(stmt)
            self.nextToken()

        return block

    def parseFunctionLiteral(self):
        para_token = self.curToken
        if not self.expectPeek(TokenType.LPAREN):
            return None

        para_Parameters = self.parseFunctionParameters()

        if not self.expectPeek(TokenType.LBRACE):
            return None

        para_Body = self.parseBlockStatement()

        lit =  FunctionLiteral(token=para_token , parameters=para_Parameters , body=para_Body)
        return lit

    def parseFunctionParameters(self):
        identifiers = []

        if self.peekTokenIs(TokenType.RPAREN):
            self.nextToken()
            return identifiers

        self.nextToken()
        ident =  Identifier(token=self.curToken, value=self.curToken.literal)
        identifiers.append(ident)

        while self.peekTokenIs(TokenType.COMMA):
            self.nextToken()
            self.nextToken()
            ident =  Identifier(token=self.curToken, value=self.curToken.literal)
            identifiers.append(ident)

        if not self.expectPeek(TokenType.RPAREN):
            return None

        return identifiers
    
    def parseCallExpression(self, function):
        exp =  CallExpression(token=self.curToken, function=function, arguments=self.parseExpressionList(TokenType.RPAREN))
        return exp
    
    def parseExpressionList(self, end : Token):
        listt = []
        if self.peekTokenIs(end):
            self.nextToken()
            return listt
        self.nextToken()
        listt.append(self.parseExpression(LOWEST))
        while self.peekTokenIs(TokenType.COMMA):
            self.nextToken()
            self.nextToken()
            listt.append(self.parseExpression(LOWEST))
        if not self.expectPeek(end):
            return None
        return listt

    def parseArrayLiteral(self):
        array =  ArrayLiteral(token=self.curToken, elements=self.parseExpressionList(TokenType.RBRACKET))
        return array
    
    def parseIndexExpression(self, left: Expression):
        x = self.curToken
        self.nextToken()
        indexx = self.parseExpression(LOWEST)
        if not self.expectPeek(TokenType.RBRACKET):
            return None
        return IndexExpression(token=x, left=left, index=indexx)

    def parseHashLiteral(self):
        hash =  HashLiteral(token=self.curToken, pairs={})
        while not self.peekTokenIs(TokenType.RBRACE):
            self.nextToken()
            key = self.parseExpression(LOWEST)
            if not self.expectPeek(TokenType.COLON):
                return None
            self.nextToken()
            value = self.parseExpression(LOWEST)
            hash.Pairs[key] = value
            if not self.peekTokenIs(TokenType.RBRACE) and not self.expectPeek(TokenType.COMMA):
                return None
            
        if not self.expectPeek(TokenType.RBRACE):
            return None
        
        return hash
    
    '''
    def parseCallArguments(self):
        args = []

        if self.peekTokenIs(TokenType.RPAREN):
            self.nextToken()
            return args

        self.nextToken()
        args.append(self.parseExpression(LOWEST))

        while self.peekTokenIs(TokenType.COMMA):
            self.nextToken()
            self.nextToken()
            args.append(self.parseExpression(LOWEST))

        if not self.expectPeek(TokenType.RPAREN):
            return None

        return args'''

###########################################################################################################################################################################

import unittest
from tokens import Lexer

def check_parser_errors(parser):
    errors = parser.errors
    if len(errors) > 0:
        raise AssertionError(f"Parser had {len(errors)} errors: {errors}")

def test_let_statement(stmt, name):
    assert stmt.TokenLiteral() == "let", f"s.TokenLiteral not 'let'. got={stmt.TokenLiteral()}"
    assert isinstance(stmt, LetStatement), f"s not LetStatement. got={type(stmt)}"
    assert stmt.Name.Value == name, f"letStmt.Name.Value not '{name}'. got={stmt.Name.Value}"
    assert stmt.Name.TokenLiteral() == name, f"s.Name not '{name}'. got={stmt.Name.TokenLiteral()}"
    return True

def test_literal_expression(exp, expected):
    if isinstance(expected, bool):
        return test_boolean_literal(exp, expected)
    elif isinstance(expected, str):
        return test_identifier(exp, expected)
    elif isinstance(expected, int):
        return test_integer_literal(exp, expected)
    else:
        #fail(f"Type of exp not handled. got={type(exp)}")
        return False

def test_integer_literal(exp, value):
    assert isinstance(exp, IntegerLiteral), f"exp is not IntegerLiteral. got={type(exp)}"
    assert exp.Value == value, f"exp.Value not {value}. got={exp.Value}"
    assert exp.TokenLiteral() == str(value), f"exp.TokenLiteral() not {value}. got={exp.TokenLiteral()}"
    return True

def test_identifier(exp, value):
    assert isinstance(exp, Identifier), f"exp is not Identifier. got={type(exp)}"
    assert exp.Value == value, f"ident.Value not {value}. got={exp.Value}"
    assert exp.TokenLiteral() == value, f"ident.TokenLiteral not {value}. got={exp.TokenLiteral()}"
    return True

def test_boolean_literal(exp, value):
    assert isinstance(exp, Boolean) , f"exp not Boolean. got={type(exp)}"
    assert exp.Value == value, f"bo.Value not {value}. got={exp.Value}"
    assert exp.TokenLiteral() == str(value).lower(), f"bo.TokenLiteral not {value}. got={exp.TokenLiteral()}"
    return True

def test_infix_expression(exp, left , operator , right):
    assert isinstance(exp, InfixExpression) , f"exp not InfixExpression. got={type(exp)}"
    if not test_literal_expression(exp.Left , left):
        return False
    if exp.Operator != operator:
        return False
    if not test_literal_expression(exp.Right , right):
        return False
    return True


'''
class ParserTest(unittest.TestCase):

    def test_let_statements(self):
        tests = [
            {"input": "let x = 5;", "expected_identifier": "x", "expected_value": 5},
            {"input": "let y = true;", "expected_identifier": "y", "expected_value": True},
            {"input": "let foobar = y;", "expected_identifier": "foobar", "expected_value": "y"}
        ]
        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()
            check_parser_errors(parser)

            self.assertEqual(len(program.Statements), 1, f"Program should have 1 statement, got {len(program.Statements)}")

            stmt = program.Statements[0]
            self.assertTrue(test_let_statement(stmt, tt["expected_identifier"]))

            val = stmt.Value
            self.assertTrue(test_literal_expression(val, tt["expected_value"]))

    def test_return_statements(self):
        tests = [
            {"input" : "return 5;" , "expected_value" : 5},
            {"input" : "return true;" , "expected_value" : True},
            {"input" : "return foobar;" , "expected_value" : "foobar"},
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()
            check_parser_errors(parser)
            self.assertEqual(len(program.Statements), 1, f"Program should have 1 statement, got {len(program.Statements)}")
            stmt = program.Statements[0]
            self.assertEqual(stmt.TokenLiteral(), "return", f"returnStmt.TokenLiteral not 'return', got={stmt.TokenLiteral()}")
            self.assertTrue(test_literal_expression(stmt.ReturnValue, tt["expected_value"]))

    def test_identifier_expression(self):
        input = "foobar;"

        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.ParseProgram()

        self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")

        stmt = program.Statements[0]
        self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

        ident = stmt.Expression
        self.assertIsInstance(ident, Identifier, f"exp not Identifier. got={type(ident)}")

        self.assertEqual(ident.Value, "foobar", f"ident.value not 'foobar'. got={ident.Value}")
        self.assertEqual(ident.TokenLiteral(), "foobar", f"ident.TokenLiteral not 'foobar'. got={ident.TokenLiteral()}")

    def test_integer_literal_expression(self):
        input = "5;"
        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.ParseProgram()
        check_parser_errors(parser)
        self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")
        stmt = program.Statements[0]
        self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

        literal = stmt.Expression
        self.assertIsInstance(literal, IntegerLiteral, f"exp not Identifier. got={type(literal)}")

        self.assertEqual(literal.Value, 5, f"literal.value not 5. got={literal.Value}")
        self.assertEqual(literal.TokenLiteral(), "5", f"literal.TokenLiteral not '5'. got={literal.TokenLiteral()}")

    def test_parsing_prefix_expressions(self):
        tests = [
            {"input" : "!5;", "operator" : "!", "value" : 5},
            {"input" : "-15;", "operator" : "-", "value" : 15},
            {"input" : "!foobar;", "operator" : "!", "value" : "foobar"},
            {"input" : "-foobar;", "operator" : "-", "value" : "foobar"},
            {"input" : "!true;", "operator" : "!", "value" : True},
            {"input" : "!false;", "operator" : "!", "value" : False}
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()
            check_parser_errors(parser)

            self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")
            
            stmt = program.Statements[0]
            self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

            exp = stmt.Expression
            self.assertIsInstance(exp, PrefixExpression, f"exp not PrefixExpression. got={type(exp)}")

            self.assertEqual(exp.Operator , tt["operator"] , f"Operator is not {tt["operator"]} got {exp.Operator}")
            self.assertTrue(test_literal_expression(exp.Right , tt["value"]))

    def test_parsing_infix_expressions(self):
        tests = [

            {"input" : "5 + 5;" , "leftValue" : 5 , "operator" : "+" , "rightValue" : 5},
            {"input" : "5 - 5;" , "leftValue" : 5 , "operator" : "-" , "rightValue" : 5},
            {"input" : "5 * 5;" , "leftValue" : 5 , "operator" : "*" , "rightValue" : 5},
            {"input" : "5 / 5;" , "leftValue" : 5 , "operator" : "/" , "rightValue" : 5},
            {"input" : "5 > 5;" , "leftValue" : 5 , "operator" : ">" , "rightValue" : 5},
            {"input" : "5 < 5;" , "leftValue" : 5 , "operator" : "<" , "rightValue" : 5},
            {"input" : "5 == 5;" , "leftValue" : 5 , "operator" : "==" , "rightValue" : 5},
            {"input" : "5 != 5;" , "leftValue" : 5 , "operator" : "!=" , "rightValue" : 5},
            {"input" : "foobar + barfoo;" , "leftValue" : "foobar" , "operator" : "+" , "rightValue" : "barfoo"},
            {"input" : "foobar - barfoo;" , "leftValue" : "foobar" , "operator" : "-" , "rightValue" : "barfoo"},
            {"input" : "foobar * barfoo;" , "leftValue" : "foobar" , "operator" : "*" , "rightValue" : "barfoo"},
            {"input" : "foobar / barfoo;" , "leftValue" : "foobar" , "operator" : "/" , "rightValue" : "barfoo"},
            {"input" : "foobar > barfoo;" , "leftValue" : "foobar" , "operator" : ">" , "rightValue" : "barfoo"},
            {"input" : "foobar < barfoo;" , "leftValue" : "foobar" , "operator" : "<" , "rightValue" : "barfoo"},
            {"input" : "foobar == barfoo;" , "leftValue" : "foobar" , "operator" : "==" , "rightValue" : "barfoo"},
            {"input" : "foobar != barfoo;" , "leftValue" : "foobar" , "operator" : "!=" , "rightValue" : "barfoo"},
            {"input" : "true == true" , "leftValue" : True , "operator" : "==" , "rightValue" : True},
            {"input" : "true != false" , "leftValue" : True , "operator" : "!=" , "rightValue" : False},
            {"input" : "false == false" , "leftValue" : False , "operator" : "==" , "rightValue" : False}
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()
            check_parser_errors(parser)

            self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")
            
            stmt = program.Statements[0]
            self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")
            
            self.assertTrue(test_infix_expression(stmt.Expression , tt["leftValue"] , tt["operator"] , tt["rightValue"]))

    def test_operator_precedence_parsing(self):
        tests = [
            {"input" : "-a * b" , "expected" : "((-a) * b)"},
            {"input" : "!-a" , "expected" : "(!(-a))"},
            {"input" : "a + b + c" , "expected" : "((a + b) + c)"},
            {"input" : "a + b - c" , "expected" : "((a + b) - c)"},
            {"input" : "a * b * c" , "expected" : "((a * b) * c)"},
            {"input" : "a * b / c" , "expected" : "((a * b) / c)"},
            {"input" : "a + b / c" , "expected" : "(a + (b / c))"},
            {"input" : "a + b * c + d / e - f" , "expected" : "(((a + (b * c)) + (d / e)) - f)"},
            {"input" : "3 + 4; -5 * 5" , "expected" : "(3 + 4)((-5) * 5)"},
            {"input" : "5 > 4 == 3 < 4" , "expected" : "((5 > 4) == (3 < 4))"},
            {"input" : "5 < 4 != 3 > 4" , "expected" : "((5 < 4) != (3 > 4))"},
            {"input" : "3 + 4 * 5 == 3 * 1 + 4 * 5" , "expected" : "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"},
            {"input" : "true" , "expected" : "true"},
            {"input" : "false" , "expected" : "false"},
            {"input" : "3 > 5 == false", "expected" : "((3 > 5) == false)"},
            {"input" : "3 < 5 == true" , "expected" : "((3 < 5) == true)"},
            {"input" : "1 + (2 + 3) + 4" , "expected" : "((1 + (2 + 3)) + 4)"},
            {"input" : "(5 + 5) * 2" , "expected" : "((5 + 5) * 2)"},
            {"input" : "2 / (5 + 5)" , "expected" : "(2 / (5 + 5))"},
            {"input" : "(5 + 5) * 2 * (5 + 5)" , "expected" : "(((5 + 5) * 2) * (5 + 5))"},
            {"input" : "-(5 + 5)" , "expected" : "(-(5 + 5))"},
            {"input" : "!(true == true)" , "expected" : "(!(true == true))"},
            {"input" : "a + add(b * c) + d" , "expected" : "((a + add((b * c))) + d)"},
            {"input" : "add(a, b, 1, 2 * 3, 4 + 5, add(6, 7 * 8))" , "expected" : "add(a, b, 1, (2 * 3), (4 + 5), add(6, (7 * 8)))"},
            {"input" : "add(a + b + c * d / f + g)" , "expected" : "add((((a + b) + ((c * d) / f)) + g))"}
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()
            check_parser_errors(parser)

            #self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)} , statement is = {tt['input']}")
            #special as we try to test the effect of ; as well, input = "3 + 4; -5 * 5"

            actual = program.String()
            if actual != tt["expected"]:
                self.fail(msg=f"expected = {tt["expected"]} , got = {actual}")
            
    def test_boolean_expression(self):
        tests = [
            {"input" : "true" , "expectedBoolean" : True},
            {"input" : "false" , "expectedBoolean" : False}
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()
            check_parser_errors(parser)

            self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")
            
            stmt = program.Statements[0]
            self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")
            
            boolean = stmt.Expression
            self.assertIsInstance(boolean, Boolean, f"exp not Boolean. got={type(boolean)}")
            self.assertEqual(boolean.Value, tt["expectedBoolean"], f"boolean.Value not {tt['expectedBoolean']}. got={boolean.Value}")

    def test_if_else_expression(self):
        input = 'if (x < y) {x} else {y}'
        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.ParseProgram()
        check_parser_errors(parser)
        self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")
        stmt = program.Statements[0]
        self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")
        exp = stmt.Expression
        self.assertIsInstance(exp, IfExpression, f"exp not IfExpression. got={type(exp)}")

        if not test_infix_expression(exp.Condition , "x" , "<" , "y"):
            self.fail("Condition failed")
        
        if (len(exp.Consequence.Statements) != 1):
            self.fail(f"Consequence not single statement, got = {len(exp.Consequence.Statements)}")
        
        consequence = exp.Consequence.Statements[0]
        self.assertIsInstance(consequence , ExpressionStatement , f"Consequence not an ExpressionStatement. ")

        if not test_identifier(consequence.Expression , "x"):
            self.fail(f"consequence identifier incorrect. got = {consequence.Expression}")
        
        if (len(exp.Alternative.Statements) != 1):
            self.fail(f"Alternative not single statement, got = {len(exp.Alternative.Statements)}")
        
        alternative = exp.Alternative.Statements[0]
        self.assertIsInstance(alternative , ExpressionStatement , f"Alternative not an ExpressionStatement. ")

        if not test_identifier(alternative.Expression , "y"):
            self.fail(f"alternative identifier incorrect. got = {alternative.Expression}")
    
    def test_function_literal_parsing(self):
        input = 'fn(x ,  y ) {x + y;}'
        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.ParseProgram()

        check_parser_errors(parser)
        self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")

        stmt = program.Statements[0]
        self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

        function = stmt.Expression
        self.assertIsInstance(function, FunctionLiteral, f"exp not FunctionLiteral. got={type(function)} , {function.String()}")

        self.assertEqual(2 , len(function.Parameters) , f"function literal parameters wrong, got = {len(function.Parameters)}")


        if not test_literal_expression(function.Parameters[0] , "x"):
            self.fail()
        if not test_literal_expression(function.Parameters[1] , "y"):
            self.fail()
        
        self.assertEqual(1 , len(function.Body.Statements) , f"function body statements wrong, got = {len(function.Body.Statements)}")

        body_statement = function.Body.Statements[0]

        self.assertIsInstance(body_statement , ExpressionStatement , f"bosy is not ExpressionStatement type")
        
        if not test_infix_expression(body_statement.Expression , "x" , "+" , "y"):
            self.fail()
        
    def test_function_parameter_parsing(self):
        tests = [
            {"input" : "fn() {};" , "expectedParameters" : []},
            {"input" : "fn(x) {};" , "expectedParameters" : ["x"]},
            {"input" : "fn(x,y,    z   ) {};" , "expectedParameters" : ["x" , "y" , "z"]}
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()

            check_parser_errors(parser)
            self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")

            stmt = program.Statements[0]
            self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

            function = stmt.Expression
            self.assertIsInstance(function, FunctionLiteral, f"exp not FunctionLiteral. got={type(function)} , {function.String()}")

            if len(function.Parameters) != len(tt["expectedParameters"]):
                self.fail("Length of parameters not equal.")

            for i in range (len(function.Parameters)):
                if not test_literal_expression(function.Parameters[i] , tt["expectedParameters"][i]):
                    self.fail(f"mismatched parameters, expected = { tt["expectedParameters"][i]} , got = {function.Parameters[i]}")
                
    def test_call_expression_parsing(self):
        input = 'add(1, 2 * 3, 4 + 5);'
        lexer = Lexer(input)
        parser = Parser(lexer)
        program = parser.ParseProgram()

        self.assertEqual(1 , len(program.Statements) , f"program.Statements does not contain 1 statements. got={len(program.Statements)}\n")
        stmt = program.Statements[0]
        self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

        expression_ = stmt.Expression
        self.assertIsInstance(expression_, CallExpression, f"exp not CallExpression. got={type(expression_)}")

        self.assertTrue(test_identifier(expression_.Function, "add"))
        self.assertEqual(len(expression_.Arguments) , 3)

        self.assertTrue(test_literal_expression(expression_.Arguments[0] , 1))
        self.assertTrue(test_infix_expression(expression_.Arguments[1] , 2 , "*" , 3))
        self.assertTrue(test_infix_expression(expression_.Arguments[2] , 4 , "+" , 5))

    def test_call_expression_parameter_parsing(self):
        tests = [
            {"input" : "add();" , "expectedIdent" : "add" , "exprectedArgs" : []},
            {"input" : "add(1);" , "expectedIdent" : "add" , "exprectedArgs" : ["1"]},
            {"input" : "add(1 , 2 * 3 , 4 + 5);" , "expectedIdent" : "add" , "exprectedArgs" : ["1" , "(2 * 3)" , "(4 + 5)"]}
        ]

        for tt in tests:
            lexer = Lexer(tt["input"])
            parser = Parser(lexer)
            program = parser.ParseProgram()

            check_parser_errors(parser)
            self.assertEqual(len(program.Statements), 1, f"program has not enough Statements. got={len(program.Statements)}")

            stmt = program.Statements[0]
            self.assertIsInstance(stmt, ExpressionStatement, f"program.Statements[0] is not ExpressionStatement. got={type(stmt)}")

            expression_ = stmt.Expression
            self.assertIsInstance(expression_, CallExpression, f"exp not CallExpression. got={type(expression_)}")

            self.assertTrue(test_identifier(expression_.Function , tt["expectedIdent"]))

            self.assertEqual(len(expression_.Arguments) , len(tt["exprectedArgs"]) , f"Length of arguments different")

            for i in range (len(expression_.Arguments)):
                self.assertEqual(expression_.Arguments[i].String() , tt["exprectedArgs"][i] , f"mismatched parameters, expected = { tt["exprectedArgs"][i]} , got = {expression_.Arguments[i]}")
             


if __name__ == "__main__":
    unittest.main()
'''
