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
    "Time Estimator", 
    "Priority Analysis Machine",
    "Centralized Task Manager",
])

if page == "Home":
    st.title("AI Study App")
    st.write("Welcome to our AI Study App. Use the sidebar to switch between segments.")
    
    column_1, column_2, column_3 = st.columns(3)
    with column_1:
        st.subheader("Time Estimator")
        st.write("Predicts the time taken to complete a task.")
    with column_2:
        st.subheader("Priority Analysis Machine")
        st.write("Calculates the priority score of a particular task.")
    with column_3:
        st.subheader("Task Manager")
        st.write("Acts as a centralized dashboard for viewing all your tasks.")

elif page == "Time Estimator":
    st.title("AI Time Estimator")
    subject_options = ["Science", "Biology", "Physics", "Chemistry", "Maths", "SST", "English", "Other"]
    
    task_name = st.text_input("Enter task name:", placeholder="e.g., Physics Revision")
    subject_completed = st.selectbox("Select Subject:", subject_options).lower()
    student_subject_difficulty = st.slider("Subject difficulty (1-10):", 1.0, 10.0, 5.0)
    task_type = st.selectbox("Task type:", ["Homework", "Project", "Exam"]).lower()
    student_task_difficulty = st.slider(f"Task difficulty:", 1.0, 10.0, 5.0)

    column_5, column_6 = st.columns(2)
    time_unit = column_5.radio("Time Unit:", ["Minutes", "Hours"]).lower()
    time_input = column_6.number_input(f"Avg time spent:", min_value=0.0, value=60.0)
        
    if st.button("Generate & Save to Manager"):
        time_multiplier = ((student_subject_difficulty/5) + (student_task_difficulty/5))/2
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
        
        st.session_state['shared_time'] = predicted_total_time if time_unit == "hours" else predicted_total_time / 60
        st.session_state['shared_task_name'] = task_name if task_name else "Untitled Task"

        new_task = {
            "Task": st.session_state['shared_task_name'],
            "Subject": subject_completed.title(),
            "Time (Hrs)": round(st.session_state['shared_time'], 2),
            "Priority": 0.0,
            "User Priority": 0.0,
            "Actual Time": 0.0,
            "Status": "Pending"
        }

        column_7, column_8, column_9 = st.columns(3)
        column_7.metric("Subject", subject_completed.title())
        column_8.metric("Difficulty Level", f"{difficulty_level:.1f}/10")
        column_9.metric("Focus Level", f"{focus_level:.1f}")

        st.subheader(f"Predicted Total Time: {predicted_total_time:.2f} {time_unit}")
        st.info(f"Estimated Completion Range: {estimation_range_low:.2f} to {estimation_range_high:.2f} {time_unit}")
    
        st.write(f"Working Time: {working_total_time:.2f} {time_unit}")
        st.write(f"Break Time: {break_total_time:.2f} {time_unit}")
        st.session_state.task_db.append(new_task)
        st.success("Task successfully saved in Task Manager.")

elif page == "Priority Analysis Machine":

    st.set_page_config(page_title="AI Priority Engine", layout="centered")
    st.markdown("---")

    st.sidebar.header("Task Details")
    task_type = st.sidebar.selectbox("Task Nature", ["Academic", "Co-Curricular", "Personal", "Other"])
    importance = st.sidebar.slider("Task Importance", 1, 10, 5)
    impact = st.sidebar.slider("Consequences and Impact", 1, 10, 5)
    completion = st.sidebar.slider("Current Completion %", 0, 100, 0)

    st.sidebar.subheader("Time Value")
    est_val = st.sidebar.number_input("Estimated Time Value", min_value=0.1, value=float(st.session_state['shared_time']))
    est_unit = st.sidebar.selectbox("Estimated Unit", ["Minutes", "Hours", "Days"])

    dead_val = st.sidebar.number_input("Deadline Time Value", min_value=0.1, value=24.0)
    dead_unit = st.sidebar.selectbox("Deadline Unit", ["Minutes", "Hours", "Days"])

    st.header("Human Capacity Level")
    column_10, column_11 = st.columns(2)

    with column_10:
        mood = st.slider("Mental State (1: Optimal, 10: Burnout)", 1, 10, 3)
        energy = st.slider("Energy Level (1: Low, 10: Peak)", 1, 10, 7)
    with column_11:
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
    urgency_level = min(urgency, 100)
    capacity_level = max(capacity, (capacity * -1), 1)

    if estimated_priority > 75:
        priority_setting = "Crunch setting"
    elif estimated_priority < 25:
        priority_setting = "Relaxed setting"
    else:
        priority_setting = "Comfortable setting"
    
    st.markdown("---")
    st.subheader("Priority Analysis Details")

    st.text("-" * 30)
    st.write(f"Task: {task_type}")
    st.write(f"AI Mode: {priority_setting}")
    st.write(f"Value: {value:.2f}/100")
    st.write(f"Urgency: {urgency_level:.2f}%")
    st.write(f"Capacity: {capacity_level:.2f}")
    st.text("-" * 30)

    st.metric(label="AI PRIORITY SCORE", value=f"{estimated_priority:.2f}/100")

    if estimated_priority > 75:
        st.error(f"SETTING: CRUNCH MODE - High urgency detected.")
    elif estimated_priority < 25:
        st.success(f"SETTING: RELAXED MODE - Low pressure detected.")
    else:
        st.info(f"SETTING: COMFORTABLE MODE.")

    if st.button("Update Priority in Manager"):
        if st.session_state.task_db:
            st.session_state.task_db[-1]["Priority"] = priority
            st.success("Priority score saved to the Task Manager!")
        else:
            st.error("Please un the Time Estimator and Priority Analysis Machine first")

    st.text("-" * 50)

elif page == "Task Manager":
    st.title("Task Manager")
    
    if not st.session_state.task_db:
        st.info("No task data currently inputted.")
    else:
        st.subheader("Stored Task Data")
        st.table(pd.DataFrame(st.session_state.task_db))
        
        st.divider()
        st.subheader("User Confirmation & Calibration")
        
        task_names = [t["Task"] for t in st.session_state.task_db]
        selected = st.selectbox("Select Task to Calibrate:", task_names)
        
        for t in st.session_state.task_db:
            if t["Task"] == selected:
                c1, c2 = st.columns(2)
                with c1:
                    act_time = st.number_input("Actual Time Taken (Hrs):", value=float(t['Time (Hrs)']))
                with c2:
                    user_prio = st.slider("User Perceived Priority (0-100):", 0, 100, int(t['Priority']))

                if st.button("Confirm"):
                    time_delta = act_time - t["Time (Hrs)"]
                    prio_delta = user_prio - t["Priority"]
                    
                    t["Actual Time"] = act_time
                    t["User Priority"] = user_prio
                    t["Status"] = "Calibrated"
                    
                    st.success("Log Updated!")
                    st.write(f"**Time Variance:** {time_delta:+.2f} hrs | **Priority Variance:** {prio_delta:+.1f} pts")

    if st.button("Clear All Data"):
        st.session_state.task_db = []
        st.rerun()
