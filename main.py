from pawpal_system import Task, Pet, Owner, Scheduler

def run_demo():
    # 1. Create the Owner with a specific time constraint
    # Let's give the owner 90 minutes of available time today
    owner = Owner(name="Jordan", available_time_mins=90)

    # 2. Create the Pets
    mochi = Pet(name="Mochi", species="Dog", age=3)
    luna = Pet(name="Luna", species="Cat", age=2)

    # 3. Create the Tasks with different durations and priorities
    task1 = Task(description="Morning Walk", duration_mins=30, priority="high", frequency="Daily", due_time="08:00")
    task2 = Task(description="Brush Fur", duration_mins=15, priority="low", frequency="Weekly", due_time="18:00")
    task3 = Task(description="Vet Visit", duration_mins=60, priority="high", frequency="Once", due_time="14:00")
    task4 = Task(description="Playtime", duration_mins=20, priority="medium", frequency="Daily", due_time="16:00")

    # 4. Assign Tasks to Pets
    mochi.add_task(task1)
    mochi.add_task(task3)
    mochi.add_task(task4)
    luna.add_task(task2)

    # 5. Link Pets to Owner
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # 6. Initialize the Scheduler and Generate the Plan
    scheduler = Scheduler(owner=owner)
    daily_plan = scheduler.generate_daily_schedule()

    # 7. Print the output clearly to the terminal
    print(f"\n🐾 --- Today's Schedule for {owner.name}'s Pets --- 🐾")
    print(f"Total time available: {owner.available_time_mins} mins\n")
    
    if not daily_plan:
        print("No tasks scheduled for today.")
    else:
        total_time_used = 0
        for i, task in enumerate(daily_plan, start=1):
            print(f"{i}. {task.description}")
            print(f"   Priority: {task.priority.capitalize()} | Duration: {task.duration_mins} mins | Due: {task.due_time}")
            total_time_used += task.duration_mins
            
        print("-" * 40)
        print(f"Total time scheduled: {total_time_used} mins")
        print(f"Time remaining: {owner.available_time_mins - total_time_used} mins\n")

if __name__ == "__main__":
    run_demo()