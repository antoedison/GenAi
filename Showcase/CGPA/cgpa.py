import streamlit as st

st.set_page_config(page_title="Cgpa Calculator", layout="centered",page_icon="https://raw.githubusercontent.com/antoedison/GenAi/main/Showcase/Images/Project_logo.png")
st.title("Cgpa Calculator")



# Grade point calculation
def calculate(mark, credit):
    if 90 <= mark <= 100:
        point = credit * 10
    elif 80 <= mark < 90:
        point = credit * 9
    elif 70 <= mark < 80:
        point = credit * 8
    elif 60 <= mark < 70:
        point = credit * 7
    elif 50 <= mark < 60:
        point = credit * 6
    else:
        point = credit * 5
    return point

# Main logic
def main():
    # Session state initialization
    if 'cgpa' not in st.session_state:
        st.session_state.cgpa = 0

    if 'form_type' not in st.session_state:
        st.session_state.form_type = None
    st.write("Welcome to CGPA Calculator")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("GPA"):
            st.session_state.form_type = "gpa"

    with col2:
        if st.button("CGPA"):
            st.session_state.form_type = "cgpa"

    if st.session_state.form_type == "cgpa":
        st.subheader("CGPA Calculator")
        no_of_semesters = st.number_input("Enter no. of semesters", min_value=1, step=1)
        total = 0

        for i in range(1, int(no_of_semesters) + 1):
            gpa = st.number_input(f"GPA for Semester {i}", min_value=0.0, max_value=10.0, step=0.01)
            total += gpa

        if no_of_semesters > 0:
            st.success(f"Your CGPA is: {total / no_of_semesters:.2f}")

    elif st.session_state.form_type == "gpa":
        st.subheader("GPA Calculator")
        no_of_subjects = st.number_input("Enter the number of Subjects", min_value=1, step=1)
        total_points = 0
        total_credits = 0

        for i in range(int(no_of_subjects)):
            mark = st.number_input(f"Marks for Subject {i+1}", min_value=0, max_value=100, step=1)
            credit = st.number_input(f"Credit for Subject {i+1}", min_value=1, max_value=10, step=1)

            total_points += calculate(mark, credit)
            total_credits += credit

        if total_credits > 0:
            gpa = total_points / total_credits
            st.success(f"Your GPA is: {gpa:.2f}")

if __name__ == "__main__":
    main()
