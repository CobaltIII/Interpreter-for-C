import sys

PROMPT = ">> "

class TokenType:
    ILLEGAL = "ILLEGAL"
    EOF = "EOF"

    # Identifiers + literals
    IDENT = "IDENT"  # add, foobar, x, y, ...
    INT = "INT"  # 1343456

    # Operators
    ASSIGN = "="
    PLUS = "+"
    MINUS = "-"
    BANG = "!"
    ASTERISK = "*"
    SLASH = "/"

    LT = "<"
    GT = ">"

    EQ = "=="
    NOT_EQ = "!="

    # Delimiters
    COMMA = ","
    SEMICOLON = ";"

    LPAREN = "("
    RPAREN = ")"
    LBRACE = "{"
    RBRACE = "}"

    # Keywords
    FUNCTION = "FUNCTION"
    LET = "LET"
    TRUE = "TRUE"
    FALSE = "FALSE"
    IF = "IF"
    ELSE = "ELSE"
    RETURN = "RETURN"

KEYWORDS = {
    "fn": TokenType.FUNCTION,
    "let": TokenType.LET,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "return": TokenType.RETURN,
}

class Token:
    def __init__(self, type_, literal):
        self.type = type_
        self.literal = literal

    def __repr__(self):
        return f"Token ( type = [ {self.type} ] , literal =  '{ self.literal }' ) "

def lookup_ident(ident):
    return KEYWORDS.get(ident, TokenType.IDENT)

class Lexer:
    def __init__(self, input_):
        self.input = input_
        self.position = 0
        self.read_position = 0
        self.ch = None
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self):
        if self.read_position >= len(self.input):
            return None
        return self.input[self.read_position]

    def next_token(self):
        self.skip_whitespace()

        if self.ch is None:
            return Token(TokenType.EOF, "")

        tok = None
        if self.ch == '=':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(TokenType.EQ, ch + self.ch)
            else:
                tok = Token(TokenType.ASSIGN, self.ch)
        elif self.ch == '+':
            tok = Token(TokenType.PLUS, self.ch)
        elif self.ch == '-':
            tok = Token(TokenType.MINUS, self.ch)
        elif self.ch == '!':
            if self.peek_char() == '=':
                ch = self.ch
                self.read_char()
                tok = Token(TokenType.NOT_EQ, ch + self.ch)
            else:
                tok = Token(TokenType.BANG, self.ch)
        elif self.ch == '/':
            tok = Token(TokenType.SLASH, self.ch)
        elif self.ch == '*':
            tok = Token(TokenType.ASTERISK, self.ch)
        elif self.ch == '<':
            tok = Token(TokenType.LT, self.ch)
        elif self.ch == '>':
            tok = Token(TokenType.GT, self.ch)
        elif self.ch == ';':
            tok = Token(TokenType.SEMICOLON, self.ch)
        elif self.ch == ',':
            tok = Token(TokenType.COMMA, self.ch)
        elif self.ch == '{':
            tok = Token(TokenType.LBRACE, self.ch)
        elif self.ch == '}':
            tok = Token(TokenType.RBRACE, self.ch)
        elif self.ch == '(':
            tok = Token(TokenType.LPAREN, self.ch)
        elif self.ch == ')':
            tok = Token(TokenType.RPAREN, self.ch)
        elif self.ch.isalpha():
            literal = self.read_identifier()
            return Token(lookup_ident(literal), literal)
        elif self.ch.isdigit():
            return Token(TokenType.INT, self.read_number())
        else:
            tok = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()
        return tok

    def skip_whitespace(self):
        if self.ch == None:
            self.read_char()
            return
        while self.ch in ' \t\n\r':
            self.read_char()

    def read_identifier(self):
        position = self.position
        while self.ch and self.ch.isalpha():
            self.read_char()
        return self.input[position:self.position]

    def read_number(self):
        position = self.position
        while self.ch and self.ch.isdigit():
            self.read_char()
        return self.input[position:self.position]

def start_repl():
    print("Welcome to the Monkey programming language!")
    print("Feel free to type in commands.")
    while True:
        sys.stdout.write(PROMPT)
        sys.stdout.flush()
        #line = sys.stdin.readline()
        line = "x"
        if not line:
            break
        line = line.strip(" \n")
        line = """let five = 5;
let ten = 10;

let add = fn(x, y) {
  x + y;
};

let result = add(five, ten);
!-/*5;
5 < 10 > 5;

if (5 < 10) {
	return true;
} else {
	return false;
}

10 == 10;
10 != 9;"""
        lexer = Lexer(line)
        tok = lexer.next_token()
        while True:
            print(tok)
            if (tok.type == TokenType.EOF):
                break
            tok = lexer.next_token()
        break

if __name__ == "__main__":
    start_repl()
