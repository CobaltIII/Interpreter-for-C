# Interpreter for a C type language called Monkey

![image](https://github.com/user-attachments/assets/93a7dda7-b8a2-4029-bb27-24170469007e)
(credits - Robert Nystrom)

> Implementing a language is a real test of programming skill. The code is complex and performance critical. You must master recursion, dynamic arrays, trees, graphs, and hash tables. - Robert Nystrom

This project is a simple interpreter that implements the basics of a limited C-like language. 
It uses Pratt-Parsing to be able to evaluate expressions using Top Down Operator Precedence instead of context free grammar or Backus Naur Form. This helps us form ast trees to evaluate the expressions with precedence efficiently.

## Features

- **Basic Syntax Parsing**: Handles a subset of C language syntax.
- **Expression Evaluation**: Supports arithmetic and logical expressions.
- **Variable Management**: Allows declaration and manipulation of variables.
- **Control Structures**: Implements basic control flow mechanisms like loops and conditionals.

## Getting Started

### Prerequisites

- **Python 3.x**: Ensure you have Python installed on your system. You can download it from the [official website](https://www.python.org/downloads/).

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/CobaltIII/Interpreter-for-C.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Interpreter-for-C
   ```

3. **Run the Interpreter**:

   To help with running, for now there is a sample code of Recursive Fibonacci given. Running it would show the output in the stdout of your python terminal.


### Future Goals
1. Adding a text editor to be able to write your own code in monkey instead of writing a python string
2. Deploying on the internet  


## Project Structure

- **interpreter.py**: The main entry point for the interpreter.
- **lexer.py**: Handles lexical analysis, breaking down the input code into tokens.
- **parser.py**: Parses the tokens and generates the abstract syntax tree (AST).
- **evaluator.py**: Evaluates the expressions and executes the AST.
- **object.py**: Contains the various object types used by the interpreter, such as numbers, strings, and booleans.
- **builtins.py**: Implements built-in functions available in the interpreter.


## References Used 
1. [Crafting Interpreters - Robert Nystrom](https://craftinginterpreters.com/)
2. Writing an interpreter in Go -Thorsten Ball
3. [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html)
4. Writing compilers and interpreters - Ronald Mak
