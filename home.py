import streamlit as st
import io
from evaluator import *
from tokens import * 
from parser import *
from contextlib import redirect_stdout


st.set_page_config(page_title="Custom Code Interpreter", layout="wide")

st.title("Custom Code Interpreter")
st.subheader("Made by Dhruv Jaiswal", divider = "blue")
st.subheader("A simple code interpreter with a custom language")
st.markdown("This is a custom code interpreter built using Python. You can write and run code snippets in a custom language called Monkey.")
st.markdown("The interpreter supports basic operations, functions, and built-ins.")
st.markdown("You can also load sample code snippets to test the interpreter. Do this by clicking the buttons to load pre-written code.")
st.markdown("The interpreter will evaluate the code and display the output.")
st.markdown("You can also write your own code in the text area below.")

st.write("Click a button to load a sample code snippet.")

snippet_1 = """let fibcalc = fn(x){
    if (x < 2) { 1 }
    else {fibcalc(x - 2) + fibcalc(x - 1)}
};
print(fibcalc(4));
print(fibcalc(5));
print(fibcalc(6));
print(fibcalc(7));
print(fibcalc(8));
"""

snippet_2 = '''let x = 15;
if (x < 10) {
    print("x is less than 10");
    } else if (x < 20) {
    print("x is less than 20, but greater than or equal to 10");
    } else {
    print("x is greater than or equal to 20");'''

snippet_3 = '''let add = fn(x, y) {x + y;};
let array = [1, 2, 3 + 3, add(2, 2)];
print(array);

let arr = push(array, "Hello");
print(arr);

print(rest(arr));'''

snippet_4 = """let newAdder = fn(x) { fn(n) { x + n } };
let addThree = newAdder(3);
print(addThree(3));
let addTwo = newAdder(2);
addTwo(2);"""

snippet_5 = """let firstName = "Dhruv";
let lastName = "Jaiswal";
let fullName = fn(first, last) { first + " " + last };
print(fullName(firstName, lastName));"""

snippet_6 = """let add = fn(x, y) {x + y;};
let hasher = {"why" : "not" , "2 + 3" : add(2 , 3)};
print("hash value of why ->" , hasher["why"]);
print("==========================");
print("hash value of not->" , hasher["not"]);
print("==========================");
print("hash value of 2 + 3 ->" , hasher["2 + 3"]);
print("==========================");"""

snippet_7 = """print("it's paradoxical, yet it works.");
print("They won’t fear it until they understand it. And they won’t understand it until they’ve used it.");
print("why so serious?");"""

snippet_8 = """let a = 10;
let b = 5;

let sum = a + b;
let diff = a - b;
let product = a * b;
let quotient = a / b;
let mod = a % b;

print("Sum: ", sum);
print("Difference: ", diff);
print("Product: ", product);
print("Quotient: ", quotient);"""

if "code_input" not in st.session_state:
    st.session_state.code_input = ""

col1, col2, col3, col4 = st.columns(4)

with col1: #done
    if st.button("⭐ Fib recursive"):
        st.session_state.code_input = snippet_1
    if st.button("📝 High order function"):
        st.session_state.code_input = snippet_4

with col2: #done
    if st.button("🔀 Conditional demo"):
        st.session_state.code_input = snippet_2
    if st.button("🧶 String demo"):
        st.session_state.code_input = snippet_5

with col3:
    if st.button("🔡 Array demo"):
        st.session_state.code_input = snippet_3
    if st.button("#️⃣ Hash demo"):
        st.session_state.code_input = snippet_6

with col4:
    if st.button("🖨️ Print demo"):
        st.session_state.code_input = snippet_7
    if st.button("➗ Arithmetic"):
        st.session_state.code_input = snippet_8

col1, col2 = st.columns([3, 2])
with col1:
    code = st.text_area("Write your code here:", value=st.session_state.code_input, height=300, key="code_area")
with col2:
    st.markdown("##### Some syntax:")
    syntaxHelp = """
        - Variables: let x = 5;
        - Functions: let add = fn(x, y) { x + y; };
        - Conditionals: if (x < 10) { return true; } else { return false; }
        - Print: print(x);
        - Strings: let y = "Hello, World!";
        - Arrays: let z = [1, 2, 3];
        - Hashes: let a = {"key": "value"};
        - Operators: '+', '-', '*', '/', '==', '!=', '<', '>'
        - Built-in array functions: 'len', 'rest', 'push'"""
    st.code(syntaxHelp, language="python")

if st.button("▶️ Run Code"):
    try:
        f = io.StringIO()
        with redirect_stdout(f):
            env = Environment()
            lexer = Lexer(code)
            parser = Parser(lexer)  
            program = parser.ParseProgram()
            evaluated = Eval(program , env)

        output = f.getvalue()
        if output.strip():
            st.markdown("### 🖨️ Printed Output:")
            st.code(output)

        if evaluated is not None:
            st.markdown("### 🔎 Final Evaluation:")
            st.code(evaluated.inspect())

    except Exception as e:
        st.error(f"❌ Error running code:\n{e}")
