import streamlit as st

st.set_page_config(page_title="AI Study App", layout="wide")

if 'shared_time' not in st.session_state:
    st.session_state['shared_time'] = 1.0
if 'shared_task' not in st.session_state:
    st.session_state['shared_task'] = "Academic"

st.sidebar.title("AI Study App")
st.sidebar.markdown("Switch between analysis engines:")
page = st.sidebar.selectbox("Go to:", ["Home", "Time Estimator (Model 1)", "Priority Analysis Machine (Model 2)"])

if page == "Home":
    st.title("AI Study App")
    st.write("Welcome to your centralized task management engine.")
    st.info("Select a model from the sidebar to begin your analysis.")
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Time Estimator (Model 1)")
        st.write("Predicts how long a task will take based on subject and difficulty.")
    with col2:
        st.subheader("Priority Analysis Machine (Model 2)")
        st.write("Calculates priority score based on deadlines and your mental energy.")

elif page == "Time Estimator (Model 1)":
    subject_options = ["Science", "Biology", "Physics", "Chemistry", "Maths", "SST", 
                   "History", "Geography", "Civics", "Economics", "English", "Other"]
    task_options = ["Homework", "Project", "Exam"]

    st.title("AI Time Estimator")
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
        task_multiplier = student_task_difficulty
        time_multiplier = ((student_subject_difficulty/5) + (task_multiplier/5))/2
    
        predicted_time = time_input * time_multiplier
        difficulty_level = ((student_subject_difficulty + student_task_difficulty)/2)
    
        break_level = ((difficulty_level/10) + 0.35)/2
        focus_level = (difficulty_level + 10)/2 - 1.5
        break_time = (predicted_time * (break_level/10))
    
        predicted_total_time = (predicted_time + break_time) * 0.75
        estimation_range_low = predicted_total_time * 0.75
        estimation_range_high = predicted_total_time * 1.15
        working_total_time = predicted_total_time * 0.75
        break_total_time = predicted_total_time *0.25

        st.divider()
        st.header("Task Estimation Details")
    
        c1, c2, c3 = st.columns(3)
        c1.metric("Subject", subject_completed.title())
        c2.metric("Difficulty Level", f"{difficulty_level:.1f}/10")
        c3.metric("Focus Level", f"{focus_level:.1f}")

        st.subheader(f"Predicted Total Time: {predicted_total_time:.2f} {time_unit}")
        st.info(f"Estimated Completion Range: {estimation_range_low:.2f} to {estimation_range_high:.2f} {time_unit}")
    
        st.write(f"Working Time: {working_total_time:.2f} {time_unit}")
        st.write(f"Break Time: {break_total_time:.2f} {time_unit}")

elif page == "Priority Analysis Machine (Model 2)":
    st.title("AI Priority Analysis Machine")
    st.markdown("---")

    st.sidebar.header("Task Details")
    task_nature = st.sidebar.selectbox("Task Nature", ["Academic", "Co-Curricular", "Personal", "Other"])
    importance = st.sidebar.slider("Task Importance", 1, 10, 5)
    impact = st.sidebar.slider("Consequences and Impact", 1, 10, 5)
    completion = st.sidebar.slider("Current Completion %", 0, 100, 0)

    st.sidebar.subheader("Time Value")
    est_val = st.sidebar.number_input("Estimated Time Value (from Model 1)", 
                                     min_value=0.1, 
                                     value=float(st.session_state['shared_time']))
    est_unit = st.sidebar.selectbox("Estimated Unit", ["Hours", "Minutes", "Days"])

    dead_val = st.sidebar.number_input("Deadline Time Value", min_value=0.1, value=24.0)
    dead_unit = st.sidebar.selectbox("Deadline Unit", ["Minutes", "Hours", "Days"])

    st.header("Human Capacity Level")
    col1, col2 = st.columns(2)
    with col1:
        mood = st.slider("Mental State (1: Optimal, 10: Burnout)", 1, 10, 3)
        energy = st.slider("Energy Level (1: Low, 10: Peak)", 1, 10, 7)
    with col2:
        motivation = st.slider("Motivation (1: Bored, 10: Dedicated)", 1, 10, 5)
        stress = st.slider("Stress Level (1: None, 10: Max)", 1, 10, 2)

    def to_hours(val, unit):
        if unit == "Minutes": return val / 60
        if unit == "Days": return val * 24
        return val

    est_hrs = to_hours(est_val, est_unit)
    dead_hrs = to_hours(dead_val, dead_unit)

    value = ((importance + impact) / 2) * 10
    capacity = (energy - (mood + stress/10)) * (1 + (motivation/100))
    work_left = est_hrs * (1 - (completion/100))
    urgency = min((work_left / max(dead_hrs, 0.1)) * 100, 100)

    priority = (urgency + value/2) + (capacity * 1.5)
    estimated_priority = min(max(round(priority, 1), 0), 100)

    if estimated_priority > 75:
        priority_setting = "Crunch setting"
    elif estimated_priority < 25:
        priority_setting = "Relaxed setting"
    else:
        priority_setting = "Comfortable setting"

    st.markdown("---")
    st.subheader("Priority Analysis Details")
    st.text("-" * 30)
    st.write(f"Task: {task_nature}")
    st.write(f"AI Mode: {priority_setting}")
    st.write(f"Value: {value:.2f}/100")
    st.write(f"Urgency: {urgency:.2f}%")
    st.write(f"Capacity: {capacity:.2f}")
    st.text("-" * 30)

    st.metric(label="ESTIMATED PRIORITY SCORE", value=f"{estimated_priority}/100")

    if estimated_priority > 75:
        st.error("SETTING: CRUNCH MODE - High urgency detected.")
    elif estimated_priority < 25:
        st.success("SETTING: RELAXED MODE - Low pressure detected.")
    else:
        st.info("SETTING: COMFORTABLE MODE.")
