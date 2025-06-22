# main.py
import streamlit as st
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="My Projects", layout= "centered", page_icon = "https://raw.githubusercontent.com/antoedison/GenAi/main/Showcase/Images/Project_logo.png")



st.sidebar.title("Project Navigator")
selected_app = st.sidebar.radio("Choose a Service:", [
    "CGPA CALCULATOR", "Pdf Assistant", "Chatbot"
])

if selected_app == "CGPA CALCULATOR":
    from CGPA import cgpa
    cgpa.main()
if selected_app == "Pdf Assistant":
    from Pdf_assistant import Pdf_assistant
    Pdf_assistant.main()
if selected_app == "Chatbot":
    from Chatbot import Chatbot
    Chatbot.main()


