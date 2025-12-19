import streamlit as st

subject_options = ["Science", "Biology", "Physics", "Chemistry", "Maths", "SST", 
                   "History", "Geography", "Civics", "Economics", "English", "Other"]
task_options = ["Homework", "Project", "Exam"]

st.title("AI Task Estimator")
st.markdown("Enter your task details below to get a predicted study schedule.")

subject_completed = st.selectbox("Select Subject:", subject_options).lower()
student_subject_difficulty = st.slider("Rate subject difficulty (1-10):", 1.0, 10.0, 5.0)
task_type = st.selectbox("Enter task type:", task_options).lower()
student_task_difficulty = st.slider(f"How difficult is this {task_type}?", 1.0, 10.0, 5.0)

col1, col2 = st.columns(2)
with col1:
    time_unit = st.radio("Time Unit:", ["Minutes", "Hours"]).lower()
with col2:
    time_input = st.number_input(f"Avg time spent on this {task_type}:", min_value=0.0, value=60.0)

if st.button("Generate Prediction"):
    # Everything inside the IF must be indented by exactly 4 spaces (or 1 tab)
    task_multiplier = student_task_difficulty
    time_multiplier = ((student_subject_difficulty/5) + (task_multiplier/5))/2
    
    predicted_time = time_input * time_multiplier
    difficulty_level = ((student_subject_difficulty + student_task_difficulty)/2)
    
    break_level = ((difficulty_level/10) + 0.25)/2
    focus_level = (difficulty_level + 10)/2
    break_time = (predicted_time * (break_level/10))
    
    predicted_total_time = (predicted_time + break_time) * 0.85
    estimation_range_low = predicted_total_time * 0.85
    estimation_range_high = predicted_total_time * 1.15

    # FIX: These lines below were indented too much in your previous version
    st.divider()
    st.header("📊 Task Estimation Details")
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Subject", subject_completed.title())
    c2.metric("Difficulty", f"{difficulty_level:.1f}/10")
    c3.metric("Focus Level", f"{focus_level:.1f}")

    st.subheader(f"Predicted Total Time: {predicted_total_time:.2f} {time_unit}")
    st.info(f"Estimated Completion Range: {estimation_range_low:.2f} to {estimation_range_high:.2f} {time_unit}")
    
    st.write(f"Working Time: {predicted_time:.2f} {time_unit}")
    st.write(f"Break Time: {break_time:.2f} {time_unit}")
