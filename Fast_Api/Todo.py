import streamlit as st
import requests
import pandas as pd

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="📋 Task Manager", layout="centered")
st.title("📋 Task Manager with FastAPI")

# Tabs for each operation
tab1, tab2, tab3, tab4 = st.tabs(["➕ Create Task", "📖 View Task", "✏️ Update Task", "❌ Delete Task"])

# ---------------------- CREATE ----------------------
with tab1:
    st.header("Create New Task")
    with st.form("create_form"):
        task_id = st.number_input("Task ID", min_value=1, step=1)
        task_name = st.text_input("Task Name")
        task_description = st.text_input("Task Description")
        completed = st.checkbox("Completed")
        submitted = st.form_submit_button("Create Task")

        if submitted:
            if not task_name or not task_description:
                st.warning("Please fill all fields.")
            else:
                payload = {
                    "task_name": task_name,
                    "task_description": task_description,
                    "Completed": completed
                }
                res = requests.post(f"{API_URL}/task/create/{task_id}", json=payload)
                if res.status_code == 200:
                    st.success("✅ Task created successfully!")
                else:
                    st.error(f"❌ {res.json().get('Error', 'Unknown error')}")

# ---------------------- READ ----------------------
with tab2:
    st.header("View Task by ID")
    view_id = st.number_input("Enter Task ID to view", min_value=1, step=1, key="view_id")
    if st.button("Fetch Task"):
        res = requests.get(f"{API_URL}/task/{view_id}")
        if res.status_code == 200 and "Error" not in res.json():
            st.json(res.json())
        else:
            st.error(f"❌ {res.json().get('Error', 'Task not found')}")

# ---------------------- UPDATE ----------------------
with tab3:
    st.header("Update Task")
    with st.form("update_form"):
        update_id = st.number_input("Task ID", min_value=1, step=1, key="update_id")
        new_name = st.text_input("New Task Name", key="name_update")
        new_desc = st.text_input("New Task Description", key="desc_update")
        new_completed = st.checkbox("Completed", key="comp_update")
        submitted_update = st.form_submit_button("Update Task")

        if submitted_update:
            payload = {
                "task_name": new_name,
                "task_description": new_desc,
                "Completed": new_completed
            }
            res = requests.put(f"{API_URL}/task/update/{update_id}", json=payload)
            if res.status_code == 200 and "Error" not in res.json():
                st.success("✅ Task updated successfully!")
            else:
                st.error(f"❌ {res.json().get('Error', 'Update failed')}")

# ---------------------- DELETE ----------------------
with tab4:
    st.header("Delete Task")
    del_id = st.number_input("Enter Task ID to delete", min_value=1, step=1, key="delete_id")
    if st.button("Delete Task"):
        res = requests.delete(f"{API_URL}/task/delete/{del_id}")
        if res.status_code == 200 and "Error" not in res.json():
            st.success("🗑️ Task deleted successfully!")
        else:
            st.error(f"❌ {res.json().get('Error', 'Delete failed')}")
