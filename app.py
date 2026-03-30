import streamlit as st
from pawpal_system import Task, Pet, Owner, Scheduler

# --- Page Configuration ---
st.set_page_config(page_title="PawPal+ Dashboard", page_icon="🐾", layout="wide")

# --- 1. Initialize Application Memory (The "Vault") ---
if 'owner' not in st.session_state:
    # Initialize with a default owner and pet for the demo
    st.session_state.owner = Owner(name="Kamayani", available_time_mins=120)
    default_pet = Pet(name="Mochi", species="Dog", age=3)
    st.session_state.owner.add_pet(default_pet)
    
if 'scheduler' not in st.session_state:
    st.session_state.scheduler = Scheduler(owner=st.session_state.owner)

# --- Header Section ---
st.title("🐾 PawPal+ Smart Pet Care")
st.write(f"Logged in as: **{st.session_state.owner.name}** | Daily Energy Budget: **{st.session_state.owner.available_time_mins} mins**")

st.divider()

# --- 2. Sidebar: Navigation & Context ---
with st.sidebar:
    st.header("Manage Pets")
    for pet in st.session_state.owner.pets:
        st.write(f"🐶 **{pet.name}** ({pet.species})")
    
    st.divider()
    if st.button("🔄 Clear All Tasks"):
        for pet in st.session_state.owner.pets:
            pet.tasks = []
        st.rerun()

# --- 3. Main Interface: Add New Tasks ---
st.subheader("➕ Schedule a New Task")
with st.expander("Click to open task creator", expanded=True):
    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("What needs to be done?", value="Morning Walk")
        duration = st.number_input("Duration (mins)", min_value=5, max_value=180, step=5, value=30)
    with col2:
        due_time = st.text_input("Due Time (HH:MM or 'Any')", value="08:00")
        priority = st.selectbox("Priority Level", ["high", "medium", "low"], index=0)
    with col3:
        frequency = st.selectbox("Frequency", ["Once", "Daily", "Weekly"])
        target_pet = st.selectbox("Select Pet", [p.name for p in st.session_state.owner.pets])

    if st.button("Add Task to Schedule"):
        # Create the Task object
        new_task = Task(
            description=task_title,
            duration_mins=int(duration),
            priority=priority,
            frequency=frequency,
            due_time=due_time
        )
        
        # --- ALGORITHMIC CHECK: Conflict Detection ---
        conflict_msg = st.session_state.scheduler.check_conflicts(new_task)
        
        if conflict_msg:
            st.error(conflict_msg, icon="🚨")
        else:
            # Find the correct pet object and add the task
            for pet in st.session_state.owner.pets:
                if pet.name == target_pet:
                    pet.add_task(new_task)
                    st.toast(f"Success! {task_title} added for {pet.name}.", icon="✅")
                    st.rerun()

st.divider()

# --- 4. Task Management & Completion ---
col_tasks, col_schedule = st.columns([1, 1])

with col_tasks:
    st.subheader("📝 Pending Tasks")
    pending = st.session_state.scheduler.get_tasks_by_status(is_completed=False)
    
    if not pending:
        st.info("All caught up! No pending tasks.")
    else:
        # Display tasks with a "Complete" button for each
        for task in pending:
            with st.container(border=True):
                c1, c2 = st.columns([3, 1])
                with c1:
                    st.markdown(f"**{task.description}** ({task.due_time})")
                    st.caption(f"Priority: {task.priority} | Date: {task.due_date}")
                with c2:
                    # Key must be unique, so we use the task's UUID
                    if st.button("Done", key=task.id):
                        # --- ALGORITHMIC ACTION: Recurrence Trigger ---
                        st.session_state.scheduler.complete_task(task.id)
                        st.toast(f"Completed {task.description}!")
                        st.rerun()

with col_schedule:
    st.subheader("📅 Optimized Daily Plan")
    if st.button("🚀 Generate Smart Schedule"):
        # --- ALGORITHMIC ACTION: Priority Sorting & Time Fitting ---
        raw_plan = st.session_state.scheduler.generate_daily_schedule()
        sorted_plan = st.session_state.scheduler.sort_by_time(raw_plan)
        
        if not sorted_plan:
            st.warning("No tasks could fit into your available time today.")
        else:
            total_time = sum(t.duration_mins for t in sorted_plan)
            st.write(f"Plan for today ({total_time} / {st.session_state.owner.available_time_mins} mins used):")
            
            for t in sorted_plan:
                st.success(f"**{t.due_time}** - {t.description} ({t.duration_mins}m)")