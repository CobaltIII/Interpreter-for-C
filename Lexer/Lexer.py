import sys

PROMPT = "Interpreter >> "

#test code for a sample code to tokeniz, taken from 'writing an INTERPRETER in go' by Thorsten Ball
test_case = """let five = 5; 
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

class TokenType:
    # "Special" types
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

#Keywords
KEYWORDS = {
    "fn": TokenType.FUNCTION,
    "let": TokenType.LET,
    "true": TokenType.TRUE,
    "false": TokenType.FALSE,
    "if": TokenType.IF,
    "else": TokenType.ELSE,
    "return": TokenType.RETURN,
}

#Defining the look of a token, it is essentially a {type : value} pair
class Token:
    def __init__(self, type_, literal):
        self.type = type_
        self.literal = literal
    #printing for easy debugging
    def __repr__(self):
        return f"Token ( type = [ {self.type} ] , literal =  '{ self.literal }' ) "

#Checking if the word is a keyword, if it isn't returns IDENT, else, returns the keyword type of the word
def lookup_ident(ident):
    return KEYWORDS.get(ident, TokenType.IDENT)

#Defining the look of the lexer
class Lexer:
    def __init__(self, input_):
        self.input = input_
        self.position = 0
        self.read_position = 0
        self.ch = None
        self.read_char()

    #moves the reading pointer by 1 and saves the charecter it read. If we're at the end of the file, it stores None in the ch
    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = None
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1
      
    #peeks the next charecter in the input
    def peek_char(self):
        if self.read_position >= len(self.input):
            return None
        return self.input[self.read_position]

    #makes the next token (main part of the code)
    def next_token(self):
        self.skip_whitespace() #skips all the whitespaces and new lines and tabs

        if self.ch is None:
            return Token(TokenType.EOF, "") #if we have no charecter left, return end of file

        #assign tokens with if statements
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

    #function to skip all whitespaces
    def skip_whitespace(self):
        if self.ch == None:
            self.read_char()
            return
        while self.ch in ' \t\n\r':
            self.read_char()

   #read identifiers in one go
    def read_identifier(self):
        position = self.position
        while self.ch and self.ch.isalpha():
            self.read_char()
        return self.input[position:self.position]

    #read numbers in one go
    def read_number(self):
        position = self.position
        while self.ch and self.ch.isdigit():
            self.read_char()
        return self.input[position:self.position]
      
#REPL : Read Execute Print Loop of the Lexer (For testing mostly right now, it shows a prompt that  
#you can enter a valid 'monkey' command into and get the tokenized version of it

def start_repl():
    print("Type your code here ")
    while True:
        sys.stdout.write(PROMPT)
        sys.stdout.flush()
        line = sys.stdin.readline()
        if not line:
            break
        line = line.strip(" \n")
        line = test_case
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
