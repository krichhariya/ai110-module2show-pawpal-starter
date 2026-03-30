import uuid
from dataclasses import dataclass, field
from typing import List

@dataclass
class Task:
    """Represents a single care activity."""
    description: str
    duration_mins: int
    priority: str  # e.g., 'high', 'medium', 'low'
    frequency: str
    due_time: str
    is_completed: bool = False
    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    def mark_complete(self) -> None:
        """Updates the task status to done."""
        self.is_completed = True

@dataclass
class Pet:
    """Represents a pet profile."""
    name: str
    species: str
    age: int
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Appends a new care task to the pet's list."""
        self.tasks.append(task)

@dataclass
class Owner:
    """Represents the user managing the schedule."""
    name: str
    available_time_mins: int
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Links a pet profile to the owner."""
        self.pets.append(pet)

class Scheduler:
    """
    Manages scheduling logic, conflict detection, and task retrieval.
    This is the 'Brain' of the system.
    """
    def __init__(self, owner: Owner):
        # The scheduler takes an Owner so it can access their pets and time constraints
        self.owner = owner
        self.schedule: List[Task] = []

    def get_all_tasks(self) -> List[Task]:
        """Helper: Retrieves a flattened list of all tasks across all pets."""
        all_tasks = []
        for pet in self.owner.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

    def get_upcoming_tasks(self) -> List[Task]:
        """Returns tasks that are not yet completed."""
        return [task for task in self.get_all_tasks() if not task.is_completed]

    def generate_daily_schedule(self) -> List[Task]:
        """Sorts tasks by priority and fits them into the day based on available time."""
        # 1. Get all incomplete tasks
        pending_tasks = self.get_upcoming_tasks()

        # 2. Define a priority mapping for sorting (1 is highest priority)
        priority_map = {"high": 1, "medium": 2, "low": 3}

        # 3. Sort tasks: primarily by priority, secondarily by shortest duration
        pending_tasks.sort(key=lambda x: (
            priority_map.get(x.priority.lower(), 4), 
            x.duration_mins
        ))

        # 4. Build the schedule based on the owner's available time
        daily_plan = []
        time_used = 0

        for task in pending_tasks:
            if time_used + task.duration_mins <= self.owner.available_time_mins:
                daily_plan.append(task)
                time_used += task.duration_mins

        self.schedule = daily_plan
        return self.schedule
        
    def check_conflicts(self, new_task: Task) -> bool:
        """Ensures new tasks don't overlap or exceed constraints."""
        # TODO: Implement specific time-conflict logic if dealing with exact start times.
        pass

    def generate_recurring_tasks(self) -> None:
        """Handles logic for tasks on a set schedule."""
        # TODO: Implement recurrence logic for 'Daily' or 'Weekly' tasks.
        pass