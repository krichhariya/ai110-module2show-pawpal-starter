# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

**Core User Actions:** Before structuring the classes, I identified the primary actions a user must be able to perform within the PawPal+ system:
    1.  **Manage Profiles:** The user can enter and store basic demographic information about themselves (the owner) and their pet (e.g., name, species).
    2.  **Manage Care Tasks:** The user can add, edit, and define specific pet care tasks, ensuring they include critical constraints like task duration and priority level.
    3.  **Generate a Daily Schedule:** The user can prompt the system to evaluate the inputted tasks against constraints to build, output, and explain a logical daily care plan.

My initial design focused on four core classes to separate the responsibilities of the system:
* **Task:** Represents a single care activity. It holds the data for what needs to be done, including constraints like `duration_mins`, `priority`, and `due_time`. It is responsible for its own completion status.
* **Pet:** Represents the animal receiving care. It acts as a container for the pet's demographic info (`name`, `species`) and holds a list of `Task` objects specific to that pet.
* **Owner:** Represents the user. It holds the user's `name`, a list of their `Pet` objects, and a critical system constraint: `available_time_mins` (how much time they have to do tasks today).
* **Scheduler:** This is the "brain" of the application. It takes in the pets (and their tasks) and evaluates them against constraints to generate a prioritized daily schedule and check for conflicts.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

* **Connecting the Time Constraint:** Initially, the `Scheduler` was entirely disconnected from the `Owner` class, meaning it had no access to the `available_time_mins` constraint needed to build a realistic schedule. I modified the design so that `generate_daily_schedule(available_time_mins: int)` explicitly takes the owner's available time as an argument.
* **Task Uniqueness:** I realized that relying on a task's `description` (e.g., "Walk") could cause bugs if a pet has multiple identical tasks in a day. I updated the `Task` class to include a unique ID (`uuid`) to ensure the scheduler can accurately track, schedule, and complete specific instances of a task.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
