import streamlit as st

st.set_page_config(page_title="Cgpa Calculator", layout="centered")

st.title("Cgpa Calculator")

if 'cgpa' not in st.session_state:
    st.session_state.cgpa = 0

if 'form_type' not in st.session_state:
    st.session_state.form_type = None


def calculate(mark, credit):
    if 90 <= mark <= 100:
        point = credit * 10
    elif 80 <= mark < 90:
        point = credit * 9
    elif 70 <= mark < 74:
        point = credit * 8
    elif 60 <= mark < 70:
        point = credit * 7
    elif 50 <= mark < 60:
        point = credit * 6
    else:
        point = credit * 5
    return point

def run():
    st.write("Welcome to CGPA Calculator")
    col1, col2 = st.columns(2)

    with col1:
        if st.button("GPA"):
            st.session_state.form_type = "gpa"
    
    with col2:
        if st.button("CGPA"):
            st.session_state.form_type = "cgpa"
    
    
    if st.session_state.form_type == "cgpa":
        st.subheader("Cgpa Calculator")
        total = 0
        no_of_semester = int(st.number_input("Enter no. of semester",min_value=1))
        for i in range(1, int(no_of_semester)+ 1):
            gpa = st.number_input(f"Enter GPA for Semester{i}")
            total+=gpa
        st.success(f"Your CGPA ia {total/no_of_semester:.2f}")

        
    if st.session_state.form_type == "gpa":
        
        total_points = 0
        total_credits= 0
        st.subheader("GPA Calculator")
        no_of_subject = st.number_input("Enter the number of Subjects:",min_value=1)
        for i in range(int(no_of_subject)):
            mark = st.number_input(f"Marks for Subject{i+1}",min_value=50,max_value=100)
            credits = st.number_input(f"Credit for subject {i+1}",min_value = 1, max_value = 10)

            total_points += calculate(mark, credits)
            total_credits += (credits*10)
            gpa = (total_points/total_credits)*10
        st.success("Your GPA is: {:.2f}".format(gpa))

if __name__ == "__main__":
    run()