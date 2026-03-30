import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- 1. Initialize the Session State "Vault" ---
if 'owner' not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_time_mins=120)
    default_pet = Pet(name="Mochi", species="Dog", age=3)
    st.session_state.owner.add_pet(default_pet)
    
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

st.title("🐾 PawPal+")
st.write(f"**Owner:** {st.session_state.owner.name} | **Available Time:** {st.session_state.owner.available_time_mins} mins")
st.write(f"**Scheduling for Pet:** {st.session_state.owner.pets[0].name} ({st.session_state.owner.pets[0].species})")

st.divider()

# --- 2. Add Task Interface ---
st.markdown("### Add a Care Task")

col1, col2 = st.columns(2)
with col1:
    task_title = st.text_input("Task title", value="Morning Walk")
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=30)
with col2:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    due_time = st.text_input("Due Time (HH:MM or 'Any')", value="08:00")
    frequency = st.selectbox("Frequency", ["Once", "Daily", "Weekly"])

if st.button("Add task"):
    new_task = Task(
        description=task_title, 
        duration_mins=int(duration), 
        priority=priority,
        frequency=frequency, 
        due_time=due_time
    )
    
    # Run our lightweight conflict detection
    conflict_warning = st.session_state.scheduler.check_conflicts(new_task)
    
    if conflict_warning:
        # If a string is returned, display it as an error and don't add the task
        st.error(conflict_warning)
    else:
        # If None is returned, the coast is clear!
        st.session_state.owner.pets[0].add_task(new_task)
        st.success(f"Added '{task_title}' to the profile!")

st.divider()

# --- 3. Display & Manage Current Tasks ---
st.markdown("### Current Pending Tasks")
current_tasks = st.session_state.scheduler.get_tasks_by_status(is_completed=False)

if current_tasks:
    st.table(current_tasks) 
    
    # Add a way to complete tasks to test the recurring logic
    st.markdown("**Mark a Task Complete**")
    col3, col4 = st.columns([3, 1])
    with col3:
        task_to_complete = st.selectbox("Select a task", current_tasks, format_func=lambda t: f"{t.description} ({t.due_time})")
    with col4:
        st.write("") # Spacing alignment
        st.write("")
        if st.button("Complete Task"):
            st.session_state.scheduler.complete_task(task_to_complete.id)
            st.success(f"Marked '{task_to_complete.description}' as complete!")
            st.rerun() # Refresh the page instantly to show the updated list
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- 4. Generate the Smart Schedule ---
st.subheader("Today's Smart Schedule")

if st.button("Generate Schedule"):
    # Run the core scheduling algorithm
    daily_plan = st.session_state.scheduler.generate_daily_schedule()
    
    # Sort the generated plan chronologically
    sorted_plan = st.session_state.scheduler.sort_by_time(daily_plan)
    
    if not sorted_plan:
        st.warning("No tasks fit into the schedule today.")
    else:
        total_time = 0
        for task in sorted_plan:
            st.markdown(f"""
            **[{task.due_time}] {task.description}** *Priority: {task.priority.capitalize()} | Duration: {task.duration_mins} mins*
            """)
            total_time += task.duration_mins
            
        st.success(f"✅ Schedule generated! Total time used: {total_time}/{st.session_state.owner.available_time_mins} mins.")