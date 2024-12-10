# Interpreter-for-C
Writing a simple interpreter with the basics of a limited C language
![image](https://github.com/user-attachments/assets/13f1ba0a-ea6e-4535-819a-498578045c20)
Photo credits - Robert Nystrom

## 1. Lexer

## 2. Parser
A top down approach is used, we make a [Pratt Parser](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html)

## 3. Objects
Taking inspiration from the Ruby compiler, "the system does not differentiate between a byte class or a Pizza class" -Thorsten Ball.
We will try to make a similar kind of system for our interpreter where the return value of every evaluation will be an 'object', this could be a boolean, string or an object class itself.


### References 
1. [So you want to write an interpreter?](https://www.youtube.com/watch?v=LCslqgM48D4)
2. Writing an interpreter in Go by Thorsten Ball
3. [Crafting Interpreters by Robert Nystrom](https://craftinginterpreters.com/introduction.html)
4. [Simple but Powerful Pratt Parsing](https://matklad.github.io/2020/04/13/simple-but-powerful-pratt-parsing.html)
