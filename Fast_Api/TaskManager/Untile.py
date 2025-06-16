import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Todo App", layout="centered")

st.title("📝 Todo Task Manager")

# --- Create New Todo ---
st.header("➕ Add New Todo")

with st.form("todo_form"):
    title = st.text_input("Title")
    description = st.text_area("Description")
    completed = st.checkbox("Completed", value=False)
    submit = st.form_submit_button("Add Todo")

    if submit:
        if not title or not description:
            st.warning("Please fill in all fields.")
        else:
            response = requests.post(
                f"{API_URL}/todos",
                json={
                    "title": title,
                    "description": description,
                    "completed": completed
                }
            )
            if response.status_code == 200:
                st.success("Todo added successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")

# --- View All Todos ---
st.header("📋 View All Todos")

response = requests.get(f"{API_URL}/todo/view")

if response.status_code == 200:
    todos = response.json()

    if len(todos) == 0:
        st.info("No todos found.")
    else:
        for todo in todos:
            st.markdown(f"""
                ### ✅ {todo['title']}
                **Description**: {todo['description']}  
                **Completed**: {"✔️ Yes" if todo['completed'] else "❌ No"}  
                **ID**: {todo['id']}
                ---
            """)
else:
    st.error(f"Failed to fetch todos: {response.status_code}")
