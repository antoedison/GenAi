# main.py
import streamlit as st

st.sidebar.title("Project Navigator")
selected_app = st.sidebar.radio("Choose a Service:", [
    "Project 1", "Pdf Assistant"
])

if selected_app == "Project 1":
    from CGPA import cgpa
    cgpa.run()
if selected_app == "Pdf Assistant":
    from Pdf_assistant import Pdf_assistant
    Pdf_assistant.main()

