import streamlit as st

st.set_page_config(page_title="Calculator", layout="centered")

# Initialize expression
if 'expression' not in st.session_state:
    st.session_state.expression = ""

def press(btn):
    if btn == "=":
        try:
            st.session_state.expression = str(eval(st.session_state.expression))
        except:
            st.session_state.expression = "Error"
    elif btn == "C":
        st.session_state.expression = ""
    else:
        st.session_state.expression += str(btn)

st.title("🧮 Streamlit Calculator")

# Display area (readonly)
st.text_input("Display", value=st.session_state.expression, key="display", disabled=True)

# Calculator layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"]
]

# Render buttons with callback
for row in buttons:
    cols = st.columns(len(row))
    for i, btn in enumerate(row):
        with cols[i]:
            st.button(btn, on_click=press, args=(btn,))
