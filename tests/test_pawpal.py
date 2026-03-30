from pawpal_system import Task, Pet

def test_task_mark_complete():
    """Verify that calling mark_complete() changes the task's status to True."""
    # 1. Arrange: Create a sample task
    task = Task(
        description="Morning Walk", 
        duration_mins=30, 
        priority="high", 
        frequency="Daily", 
        due_time="08:00"
    )
    
    # Verify the default state is False
    assert task.is_completed is False
    
    # 2. Act: Mark the task as complete
    task.mark_complete()
    
    # 3. Assert: Verify the state changed
    assert task.is_completed is True

def test_pet_add_task():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # 1. Arrange: Create a pet and a task
    mochi = Pet(name="Mochi", species="Dog", age=3)
    task = Task(
        description="Brush Fur", 
        duration_mins=15, 
        priority="low", 
        frequency="Weekly", 
        due_time="18:00"
    )
    
    # Verify the pet starts with no tasks
    assert len(mochi.tasks) == 0
    
    # 2. Act: Add the task to the pet
    mochi.add_task(task)
    
    # 3. Assert: Verify the task list grew and contains the right task
    assert len(mochi.tasks) == 1
    assert mochi.tasks[0].description == "Brush Fur"
    