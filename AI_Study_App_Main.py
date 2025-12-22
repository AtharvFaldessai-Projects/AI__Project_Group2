import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Study App", layout="wide")

if 'task_db' not in st.session_state:
    st.session_state.task_db = []
if 'shared_time' not in st.session_state:
    st.session_state['shared_time'] = 1.0
if 'shared_task_name' not in st.session_state:
    st.session_state['shared_task_name'] = ""

st.sidebar.title("AI Study App")
page = st.sidebar.selectbox("Platforms:", [
    "Home", 
    "Time Estimator (Model 1)", 
    "Priority Analysis Machine (Model 2)",
    "Centralized Task Manager",
    "Timetable Generator",
])

if page == "Home":
    st.title("AI Study App")
    st.write("Welcome to our AI Study App.")
    st.info("Please select a model from the sidebar:")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Time Estimator (Model 1)")
        st.write("Predicts task duration based on subject and difficulty.")
    with col2:
        st.subheader("Priority Analysis Machine (Model 2)")
        st.write("Calculates priority score based on deadlines and energy.")
    with col3:
        st.subheader("Task Manager")
        st.write("Centralised platform for task management.")
    with col4:
        st.subheader("Timetable Generator")
        st.write("Generates a schedule based on your tasks.")

elif page == "Time Estimator (Model 1)":
    st.title("AI Time Estimator")
    subject_options = ["Science", "Biology", "Physics", "Chemistry", "Maths", "SST", 
                       "History", "Geography", "Civics", "Economics", "English", "Other"]
    task_options = ["Homework", "Project", "Exam"]

    task_name = st.text_input("Enter task name:", placeholder="e.g., Science Homework")
    subject_completed = st.selectbox("Select Subject:", subject_options).lower()
    student_subject_difficulty = st.slider("Rate subject difficulty (1-10):", 1.0, 10.0, 5.0)
    task_type = st.selectbox("Enter task type:", task_options).lower()
    student_task_difficulty = st.slider(f"How difficult is this {task_type}?", 1.0, 10.0, 5.0)

    col1, col2, col3 = st.columns(3)
    with col1:
        time_unit = st.radio("Time Unit:", ["Minutes", "Hours"]).lower()
    with col2:
        time_input = st.number_input(f"Avg time spent on this {task_type}:", min_value=0.0, value=60.0)
        
    if st.button("Generate & Save to Manager"):
        time_multiplier = ((student_subject_difficulty/5) + (student_task_difficulty/5))/2
        predicted_time = time_input * time_multiplier
        difficulty_level = ((student_subject_difficulty + student_task_difficulty)/2)
        break_level = ((difficulty_level/10) + 0.35)/2
        focus_level = (difficulty_level + 10)/2 - 1.5
        break_time = (predicted_time * (break_level/10))
        predicted_total_time = (predicted_time + break_time) * 0.75
        
        st.session_state['shared_time'] = predicted_total_time if time_unit == "hours" else predicted_total_time / 60
        st.session_state['shared_task_name'] = task_name if task_name else "Untitled Task"

        st.divider()
        st.header("Task Estimation Details")
        c1, c2, c3 = st.columns(3)
        c1.metric("Subject", subject_completed.title())
        c2.metric("Difficulty Level", f"{difficulty_level:.1f}/10")
        c3.metric("Focus Level", f"{focus_level:.1f}")
        st.subheader(f"Predicted Total Time: {predicted_total_time:.2f} {time_unit}")

        new_task = {
            "Task": st.session_state['shared_task_name'],
            "Subject": subject_completed.title(),
            "Time (Hrs)": round(st.session_state['shared_time'], 2),
            "Priority": "Not Calculated",
            "Status": "Pending"
        }
        st.session_state.task_db.append(new_task)
        st.success("Task Saved!")

elif page == "Priority Analysis Machine (Model 2)":
    st.title("AI Priority Analysis Machine")
    st.sidebar.header("Task Details")
    task_nature = st.sidebar.selectbox("Task Nature", ["Academic", "Co-Curricular", "Personal", "Other"])
    importance = st.sidebar.slider("Task Importance", 1, 10, 5)
    impact = st.sidebar.slider("Consequences and Impact", 1, 10, 5)
    completion = st.sidebar.slider("Current Completion %", 0, 100, 0)

    est_val = st.sidebar.number_input("Estimated Time Value (from Model 1)", value=float(st.session_state['shared_time']))
    est_unit = st.sidebar.selectbox("Estimated Unit", ["Hours", "Minutes", "Days"])
    dead_val = st.sidebar.number_input("Deadline Time Value", min_value=0.1, value=24.0)
    dead_unit = st.sidebar.selectbox("Deadline Unit", ["Minutes", "Hours", "Days"])

    st.header("Human Capacity Level")
    col1, col2 = st.columns(2)
    mood = col1.slider("Mental State (1: Optimal, 10: Burnout)", 1, 10, 3)
    energy = col1.slider("Energy Level (1: Low, 10: Peak)", 1, 10, 7)
    motivation = col2.slider("Motivation (1: Bored, 10: Dedicated)", 1, 10, 5)
    stress = col2.slider("Stress Level (1: None, 10: Max)", 1, 10, 2)

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
    priority = min(max(round((urgency + value/2) + (capacity * 1.5), 1), 0), 100)

    st.metric(label="ESTIMATED PRIORITY SCORE", value=f"{priority}/100")

    if st.button("Click here to UPDATE LAST TASK PRIORITY"):
        if st.session_state.task_db:
            st.session_state.task_db[-1]["Priority"] = priority
            st.success("Priority Updated in Manager!")
        else:
            st.error("No task found to update!")

elif page == "Centralized Task Manager":
    st.title("Centralized Task Manager")
    if not st.session_state.task_db:
        st.info("No tasks analyzed yet.")
    else:
        st.table(pd.DataFrame(st.session_state.task_db))
    if st.button("Clear Manager"):
        st.session_state.task_db = []
        st.rerun()

elif page == "Timetable Generator":
    st.title("AI Timetable Generator")
    if not st.session_state.task_db:
        st.warning("No tasks found!")
    else:
        start_time = st.number_input("Start Hour (0-23):", 0, 23, 9)
        schedule_data = []
        current_hour = float(start_time)
        for task in st.session_state.task_db:
            duration = task["Time (Hrs)"]
            end_hour = current_hour + duration
            schedule_data.append({
                "Slot": f"{int(current_hour):02d}:00 - {int(end_hour):02d}:{(int((end_hour%1)*60)):02d}",
                "Task": task["Task"],
                "Duration": f"{duration} hrs"
            })
            current_hour = end_hour
        st.table(pd.DataFrame(schedule_data))
