import streamlit as st

st.set_page_config(page_title="AI Priority Engine", layout="centered")
st.title("AI Priority Analysis Machine")
st.markdown("---")

st.sidebar.header("Task Details")
task_type = st.sidebar.selectbox("Task Nature", ["Academic", "Co-Curricular", "Personal", "Other"])
importance = st.sidebar.slider("Task Importance", 1, 10, 5)
impact = st.sidebar.slider("Consequences and Impact", 1, 10, 5)
completion = st.sidebar.slider("Current Completion %", 0, 100, 0)

st.sidebar.subheader("Time Value")
est_val = st.sidebar.number_input("Estimated Time Value", min_value=0.1, value=1.0)
est_unit = st.sidebar.selectbox("Estimated Unit", ["Minutes", "Hours", "Days"])

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

setting, weight = get_ai_setting(energy, mood, stress, dead_hrs)

st.markdown("---")
st.subheader("📋 AI Priority Details")

st.text("-" * 30)
st.write(f"**Task:** {task_type}")
st.write(f"**AI Mode:** {setting}")
st.write(f"**Value:** {value:.2f}/100")
st.write(f"**Urgency:** {urgency:.2f}%")
st.write(f"**Capacity:** {capacity:.2f}")
st.text("-" * 30)

st.metric(label="ESTIMATED PRIORITY SCORE", value=f"{estimated_priority}/100")

if estimated_priority > 75:
    st.error(f"SETTING: CRUNCH MODE - High urgency detected.")
elif estimated_priority < 25:
    st.success(f"SETTING: RELAXED MODE - Low pressure detected.")
else:
    st.info(f"SETTING: COMFORTABLE MODE.")

st.text("-" * 50)
