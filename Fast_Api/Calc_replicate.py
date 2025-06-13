import streamlit as st
import requests
import re

st.set_page_config(page_title="Calculator", layout="centered")

# FastAPI backend URL
BASE_URL = "http://127.0.0.1:8000/"

# Initialize expression
if 'expression' not in st.session_state:
    st.session_state.expression = ""

def evaluate_expression(expr):
    try:
        # Match expressions like "3+5", "10/2"
        match = re.match(r"^\s*(-?\d+\.?\d*)\s*([\+\-\*/])\s*(-?\d+\.?\d*)\s*$", expr)
        if not match:
            return "Invalid"

        num1, op, num2 = match.groups()
        num1, num2 = float(num1), float(num2)

        if op == '+':
            endpoint = "/addition"
        elif op == '-':
            endpoint = "/subtraction"
        elif op == '*':
            endpoint = "/multiplication"
        elif op == '/':
            endpoint = "/division"
        else:
            return "Invalid Operator"

        # Make GET request to FastAPI
        response = requests.get(f"{BASE_URL}{endpoint}", params={"num1": num1, "num2": num2})

        if response.status_code == 200:
            return str(response.json().get("result"))
        else:
            return f"Error: {response.text}"
    except Exception as e:
        return "Error"

def press(btn):
    if btn == "=":
        st.session_state.expression = evaluate_expression(st.session_state.expression)
    elif btn == "C":
        st.session_state.expression = ""
    else:
        st.session_state.expression += str(btn)

st.title("🧮 Streamlit + FastAPI Calculator")

# Display area (readonly)
st.text_input("Display", value=st.session_state.expression, key="display", disabled=True)

# Calculator layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

# Render buttons
for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        with cols[i]:
            st.button(btn, on_click=press, args=(btn,))
