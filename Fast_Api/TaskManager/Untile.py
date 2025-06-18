"""
Algorithm:
1. Import neccessary libraries.
2. Set Api url to send request to the endpoints.
3. configure the Streamlit page.
4. Add title and four buttons to add four functionalities.
5. Create a variable
"""



import streamlit as st

import requests
import pandas

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Task Manager", layout="centered")
st.title("Task Manager")

if 'clicked' not in st.session_state:
    st.session_state.clicked = None

col1, col2, col3, col4 = st.columns(4)
if col1.button("➕ Add Task"):
    st.session_state.clicked = "Add"
if col2.button("📄 View Tasks"):
    st.session_state.clicked = "View"
if col3.button("✏️ Update Task"):
    st.session_state.clicked = "Update"
if col4.button("❌ Delete Task"):
    st.session_state.clicked = "Delete"




