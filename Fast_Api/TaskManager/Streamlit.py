import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="Todo Task Manager")
st.title("📝 Todo Task Manager")

# Session state for managing user action
if 'clicked' not in st.session_state:
    st.session_state.clicked = None

# Header buttons
col1, col2, col3, col4 = st.columns(4)
if col1.button("➕ Add Task"):
    st.session_state.clicked = "Add"
if col2.button("📄 View Tasks"):
    st.session_state.clicked = "View"
if col3.button("✏️ Update Task"):
    st.session_state.clicked = "Update"
if col4.button("❌ Delete Task"):
    st.session_state.clicked = "Delete"

# Utility function to fetch tasks
def fetch_tasks():
    try:
        response = requests.get(f"{API_URL}/todo/view")
        if response.status_code == 200:
            return pd.DataFrame(response.json())
        else:
            st.error("Failed to fetch tasks.")
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Error: {e}")
        return pd.DataFrame()

# Add Task
if st.session_state.clicked == "Add":
    st.subheader("Add New Task")
    with st.form("add_task"):
        title = st.text_input("Title")
        description = st.text_input("Description")
        completed = st.checkbox("Completed", value=False)
        submit = st.form_submit_button("Create Task")

    if submit:
        if not title or not description:
            st.warning("Please fill in all fields.")
        else:
            res = requests.post(f"{API_URL}/todo/create", json={
                "title": title,
                "description": description,
                "completed": completed
            })
            if res.status_code == 200:
                st.success("✅ Task added successfully.")
            else:
                st.error(f"❌ Failed to add task. Status: {res.status_code}")

# View / Update / Delete Tasks
if st.session_state.clicked in ["View", "Update", "Delete"]:
    df = fetch_tasks()
    if not df.empty:
        df_display = df.rename(columns={
            "id": "ID", 
            "title": "Title", 
            "description": "Description", 
            "completed": "Completed"
        })[["ID", "Title", "Description", "Completed"]]

        st.subheader("📋 Current Tasks")
        st.dataframe(df_display.set_index("ID"), use_container_width=True)

        # --- Update Task ---
        if st.session_state.clicked == "Update":
            selected_id = st.selectbox("Select a task to update (by ID):", df["id"])
            task = df[df["id"] == selected_id].iloc[0]

            with st.form("update_task_form"):
                title = st.text_input("Title", task["title"])
                description = st.text_input("Description", task["description"])
                completed = st.checkbox("Completed", task["completed"])
                submit = st.form_submit_button("Update Task")

            if submit:
                response = requests.put(
                    f"{API_URL}/todo/update/{selected_id}",
                    json={
                        "title": title,
                        "description": description,
                        "completed": completed
                    }
                )
                if response.status_code == 200:
                    st.success("✅ Task updated successfully.")
                    st.rerun()
                else:
                    st.error(f"❌ Failed to update task. Status: {response.status_code}")

        # --- Delete Task ---
        elif st.session_state.clicked == "Delete":
            selected_id = st.selectbox("Select a task to delete (by ID):", df["id"])
            if st.button("Confirm Delete"):
                res = requests.delete(f"{API_URL}/todo/delete/{selected_id}")
                if res.status_code == 200:
                    st.success("🗑️ Task deleted successfully.")
                    # Keep delete mode active and refresh the app
                    st.session_state.clicked = "Delete"
                    st.rerun()
                else:
                    st.error(f"❌ Failed to delete task. Status: {res.status_code}")

    else:
        st.info("No tasks found.")
