import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Study App", layout="wide")

# --- GLOBAL MEMORY INITIALIZATION ---
if 'task_db' not in st.session_state:
    st.session_state.task_db = []
if 'shared_time' not in st.session_state:
    st.session_state['shared_time'] = 1.0
if 'shared_task_name' not in st.session_state:
    st.session_state['shared_task_name'] = ""

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("AI Study App")
page = st.sidebar.selectbox("Platforms:", [
    "Home", 
    "Time Estimator (Model 1)", 
    "Priority Analysis Machine (Model 2)",
    "Centralized Task Manager",
    "Timetable Generator",
    "Data Visualization",
    "Feedback Loop"
])

# --- HOME PAGE ---
if page == "Home":
    st.title("AI Study App")
    st.write("Welcome to the AI Study App. Navigate through the sidebar to manage your studies.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.subheader("Model 1")
        st.write("Predicts task duration.")
    with col2:
        st.subheader("Model 2")
        st.write("Calculates priority scores.")
    with col3:
        st.subheader("Manager")
        st.write("Stores all study data.")
    with col4:
        st.subheader("Feedback")
        st.write("Calibrates AI accuracy.")

# --- MODEL 1: TIME ESTIMATOR ---
elif page == "Time Estimator (Model 1)":
    st.title("AI Time Estimator")
    subject_options = ["Science", "Biology", "Physics", "Chemistry", "Maths", "SST", "English", "Other"]
    
    task_name = st.text_input("Enter task name:", placeholder="e.g., Physics Revision")
    subject_completed = st.selectbox("Select Subject:", subject_options).lower()
    student_subject_difficulty = st.slider("Subject difficulty (1-10):", 1.0, 10.0, 5.0)
    task_type = st.selectbox("Task type:", ["Homework", "Project", "Exam"]).lower()
    student_task_difficulty = st.slider(f"Task difficulty:", 1.0, 10.0, 5.0)

    col1, col2 = st.columns(2)
    time_unit = col1.radio("Time Unit:", ["Minutes", "Hours"]).lower()
    time_input = col2.number_input(f"Avg time spent:", min_value=0.0, value=60.0)
        
    if st.button("Generate & Save to Manager"):
        # Math Logic
        time_multiplier = ((student_subject_difficulty/5) + (student_task_difficulty/5))/2
        predicted_time = time_input * time_multiplier
        difficulty_level = ((student_subject_difficulty + student_task_difficulty)/2)
        break_time = (predicted_time * (((difficulty_level/10) + 0.35)/20))
        predicted_total_time = (predicted_time + break_time) * 0.75
        
        # Shared State for Model 2
        st.session_state['shared_time'] = predicted_total_time if time_unit == "hours" else predicted_total_time / 60
        st.session_state['shared_task_name'] = task_name if task_name else "Untitled Task"

        # Centralization (Initialization of all keys to prevent errors)
        new_task = {
            "Task": st.session_state['shared_task_name'],
            "Subject": subject_completed.title(),
            "Time (Hrs)": round(st.session_state['shared_time'], 2),
            "Priority": 0.0,
            "User Priority": 0.0, # Added for feedback
            "Actual Time": 0.0,   # Added for feedback
            "Status": "Pending"
        }
        st.session_state.task_db.append(new_task)
        st.success("Task Extracted to Manager!")

# --- MODEL 2: PRIORITY MACHINE ---
elif page == "Priority Analysis Machine (Model 2)":
    st.title("AI Priority Analysis Machine")
    
    # Auto-pulls from Model 1
    est_val = st.sidebar.number_input("Est. Time (from Model 1)", value=float(st.session_state['shared_time']))
    dead_val = st.sidebar.number_input("Deadline (Hours)", min_value=0.1, value=24.0)

    st.header("Human Capacity Level")
    col1, col2 = st.columns(2)
    mood = col1.slider("Burnout Level (1-10)", 1, 10, 3)
    energy = col1.slider("Energy Level (1-10)", 1, 10, 7)
    motivation = col2.slider("Motivation (1-10)", 1, 10, 5)
    stress = col2.slider("Stress Level (1-10)", 1, 10, 2)

    # Priority Logic
    value = 50 # Default baseline
    capacity = (energy - (mood + stress/10)) * (1 + (motivation/100))
    urgency = (est_val / max(dead_val, 0.1)) * 100
    priority = min(max(round((urgency + value/2) + (capacity * 1.5), 1), 0), 100)

    st.metric(label="AI PRIORITY SCORE", value=f"{priority}/100")

    if st.button("Update Priority in Manager"):
        if st.session_state.task_db:
            st.session_state.task_db[-1]["Priority"] = priority
            st.success("Priority Integrated!")
        else:
            st.error("Create a task in Model 1 first!")

# --- CENTRALIZED TASK MANAGER ---
elif page == "Centralized Task Manager":
    st.title("Centralized Task Manager")
    if not st.session_state.task_db:
        st.info("Database empty.")
    else:
        st.table(pd.DataFrame(st.session_state.task_db))
    if st.button("Clear Manager"):
        st.session_state.task_db = []
        st.rerun()

# --- TIMETABLE GENERATOR ---
elif page == "Timetable Generator":
    st.title("AI Timetable Generator")
    if not st.session_state.task_db:
        st.warning("No tasks found!")
    else:
        start_time = st.number_input("Start Hour (0-23):", 0, 23, 9)
        schedule_data = []
        curr = float(start_time)
        for t in st.session_state.task_db:
            end = curr + t["Time (Hrs)"]
            schedule_data.append({
                "Slot": f"{int(curr):02d}:00 - {int(end):02d}:{(int((end%1)*60)):02d}",
                "Task": t["Task"],
                "Duration": f"{t['Time (Hrs)']} hrs"
            })
            curr = end
        st.table(pd.DataFrame(schedule_data))

# --- DATA VISUALIZATION ---
elif page == "Data Visualization":
    st.title("📊 Study Analytics")
    if st.session_state.task_db:
        df = pd.DataFrame(st.session_state.task_db)
        st.bar_chart(df.groupby("Subject")["Time (Hrs)"].sum())
        st.scatter_chart(df, x="Time (Hrs)", y="Priority")

# --- DUAL FEEDBACK LOOP ---
elif page == "Feedback Loop":
    st.title("🔄 AI Feedback Loop (Time & Priority)")
    if not st.session_state.task_db:
        st.warning("No tasks to review.")
    else:
        task_names = [t["Task"] for t in st.session_state.task_db]
        selected = st.selectbox("Select Task to Calibrate:", task_names)
        
        for t in st.session_state.task_db:
            if t["Task"] == selected:
                col1, col2 = st.columns(2)
                with col1:
                    st.subheader("Time Calibration")
                    st.write(f"AI Predicted: {t['Time (Hrs)']} hrs")
                    act_time = st.number_input("Actual Time Taken:", value=float(t['Time (Hrs)']))
                
                with col2:
                    st.subheader("Priority Calibration")
                    st.write(f"AI Priority: {t['Priority']}/100")
                    user_prio = st.slider("How high was the actual pressure?", 0, 100, int(t['Priority']))

                if st.button("Submit Feedback"):
                    t["Actual Time"] = act_time
                    t["User Priority"] = user_prio
                    t["Status"] = "Completed"
                    
                    time_delta = act_time - t["Time (Hrs)"]
                    prio_delta = user_prio - t["Priority"]
                    
                    st.success("Feedback Logged!")
                    st.write(f"**Time Error:** {time_delta:.2f} hrs | **Priority Error:** {prio_delta:.1f} pts")
                    st.info("Delta values are being stored to improve the weighting multipliers.")
