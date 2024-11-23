import heapq
from datetime import datetime, timedelta
import time  # For simulating periodic check
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



class System:
    def __init__(self):
        # Storage for tasks in a list
        self.tasks = []
        self.priority_queue = []  # Min-heap for notifications

    def add_task_sorted(self, new_task):
        """
        Add a single task to the system in its correct position
        based on starting date and time using binary search.
        """
        # Find the correct index using binary search
        index = self._find_insert_position(new_task)
        # Insert the task at the identified index
        self.tasks.insert(index, new_task)
        heapq.heappush(self.priority_queue, (new_task.task_start, "start", new_task))
        heapq.heappush(self.priority_queue, (new_task.deadline, "deadline", new_task))


    def _find_insert_position(self, new_task):
        """
        Perform a binary search to find the correct index for a new task
        based on starting date and time.
        """
        low, high = 0, len(self.tasks) - 1

        while low <= high:
            mid = (low + high) // 2
            if self.tasks[mid].task_start < new_task.task_start:
                low = mid + 1
            else:
                high = mid - 1

        return low
    
    def check_notifications(self):
            """
            Check notifications for upcoming events or deadlines.
            """
            current_time = datetime.now()
            print(current_time)
            while self.priority_queue:
                # Get the time for the next event
                event_time, event_type, task = self.priority_queue[0]
                current_time = datetime.now()

                if event_time <= current_time:
                    # Pop and process the event if it's time
                    heapq.heappop(self.priority_queue)
                    if event_type == "start":
                        print(f"Notification: '{task.task_name}' has started")
                        task.status = "ongoing"
                    elif event_type == "deadline":
                            print(f"Warning: '{task.task_name}' has reached its deadline!")
                else:
                    # Calculate the total time difference in seconds
                    time_diff_seconds = (event_time - current_time).total_seconds()

                    # Calculate days, hours, and minutes from the total time difference
                    days = time_diff_seconds // (24 * 3600)  # 1 day = 24 hours = 86400 seconds
                    time_diff_seconds %= (24 * 3600)  # Remainder after extracting days
                    hours = time_diff_seconds // 3600  # 1 hour = 3600 seconds
                    time_diff_seconds %= 3600  # Remainder after extracting hours
                    minutes = time_diff_seconds // 60  # 1 minute = 60 seconds

                    # Display the time to the next event in days, hours, and minutes
                    print(f"Sleeping for {int(days)} day(s), {int(hours)} hour(s), and {int(minutes)} minute(s) until the next event...\n")

                    # Sleep until the next event (in seconds)
                    time_to_next_event = (event_time - current_time).total_seconds()
                    answer=input("would you like to exit (y/n): ")
                    if answer == "y":
                        return
                    elif answer != "y" and answer != "n":
                        print("Invalid input")
                    sleep_time = min(300, time_to_next_event)  # 300 seconds = 5 minutes
                    time.sleep(sleep_time)
                    
    
                
    def update_statuses(self):
        """
        Update task statuses based on current time.
        """
        current_time = datetime.now()
        for task in self.tasks:
            if task.task_start <= current_time < task.task_start + timedelta(hours=task.duration):
                task.status = "ongoing"
            elif current_time >= task.deadline:
                    print(f"Task selected: {task.task_name}, Type: {task.task_type}, Duration: {task.duration} hours, Priority: {task.priority}")
                    answer = input("Have you completed the task(y/n)")
                    if answer == "y":
                        task.status = "completed" 
                    elif answer == "n":
                        task.status == "missed"
                    else:
                        print("Invalid input")

    def quick_sort(self, tasks, answer):
        """
        Sort tasks in descending order based on the specified criteria using Quick Sort.
        """
        if len(tasks) <= 1:
            return tasks

        # Choose the middle element as the pivot
        middle_index = len(tasks) // 2
        pivot = tasks[middle_index]

        if answer == "priority":
            # Split tasks into lower and higher based on priority
            lower = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.priority > pivot.priority]
            higher = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.priority <= pivot.priority]

        elif answer == "type":
            # Split tasks into lower and higher based on task type (alphabetical comparison)
            lower = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.task_type > pivot.task_type]
            higher = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.task_type <= pivot.task_type]

        elif answer == "start":
            # Split tasks into lower and higher based on start time
            lower = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.task_start < pivot.task_start]
            higher = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.task_start >= pivot.task_start]

        elif answer == "end":
            # Split tasks into lower and higher based on start time
            lower = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.deadline < pivot.deadline]
            higher = [task for task in tasks[:middle_index] + tasks[middle_index+1:] if task.deadline >= pivot.deadline]

        # Recursively apply quick sort to the lower and higher sublists
        return self.quick_sort(lower, answer) + [pivot] + self.quick_sort(higher, answer)

    def sort_tasks(self, answer):
        """
        Wrapper method to start sorting with the initial tasks list.
        """
        self.tasks = self.quick_sort(self.tasks, answer)
        for task in self.tasks:
            print(f"Task: {task.task_name}, Type: {task.task_type} Start: {task.task_start}, Deadline: {task.deadline}, Priority: {task.priority}, Duration: {task.duration} hours")
    
    # Method to schedule tasks based on available time
    def schedule_tasks(self, available_time):
        n = len(self.tasks)
        
        # DP table to store maximum priority at each step
        dp = [[0 for _ in range(available_time + 1)] for _ in range(n + 1)]
        
        # Table to store which tasks were selected
        selected_tasks = [[[] for _ in range(available_time + 1)] for _ in range(n + 1)]

        # Function to calculate the adjusted priority based on task type
        def get_priority(task):
            # Academic tasks have higher priority, personal tasks have half priority
            return task.priority if task.task_type == 'academic' else task.priority // 2

        # Process each task
        for i in range(1, n + 1):
            for t in range(available_time + 1):
                task = self.tasks[i - 1]  # Current task being considered
                
                # Adjusted priority based on task type
                adjusted_priority = get_priority(task)

                if task.duration <= t:
                    # Check if we get a higher priority by including the task
                    if dp[i - 1][t] < dp[i - 1][t - task.duration] + adjusted_priority:
                        dp[i][t] = dp[i - 1][t - task.duration] + adjusted_priority
                        selected_tasks[i][t] = selected_tasks[i - 1][t - task.duration] + [task]
                    else:
                        dp[i][t] = dp[i - 1][t]
                        selected_tasks[i][t] = selected_tasks[i - 1][t]
                else:
                    # If the task duration is more than the available time, don't include it
                    dp[i][t] = dp[i - 1][t]
                    selected_tasks[i][t] = selected_tasks[i - 1][t]
        
        return selected_tasks[n][available_time]

    
    # Create Gantt chart
    def gantt_chart(self):
        """
        Create a Gantt chart to visualize the task schedules with starting and ending times on the x-axis.
        """
        fig, ax = plt.subplots(figsize=(16, 8))  # Increased width for more space between intervals

        # Plot each task on the Gantt chart
        for i, task in enumerate(self.tasks):
            # Use different colors for academic and personal tasks
            color = "skyblue" if task.task_type == "academic" else "lightgreen"
            
            # Calculate task duration in hours
            bar_duration = (task.deadline - task.task_start).seconds / 3600  # Duration in hours
            
            # Plot the task on the chart
            ax.barh(task.task_name, bar_duration, left=task.task_start, color=color)

        # Set the x-axis to show time with intervals based on task start and end time
        self.set_dynamic_intervals(ax)
        
        # Major formatter for the x-axis: Showing the date and time
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d, %H:%M'))  # Show month, day, and time (e.g., Nov 20, 10:00)

        # Minor formatter for the x-axis: Showing only time within the day
        # ax.xaxis.set_minor_formatter(mdates.DateFormatter('%H:%M'))  # Hour:Minute format for minor ticks

        # Rotate the x-axis labels for better readability
        plt.xticks(rotation=45, ha='right', fontsize=9)

        # Title and labels
        ax.set_xlabel('Time')
        plt.title('Task Schedule')

        # Adjust layout for better spacing
        plt.subplots_adjust(bottom=0.2)
        plt.tight_layout()

        # Show the chart
        plt.show()

    def set_dynamic_intervals(self, ax):
        """
        Dynamically update the hour intervals based on the visible time range.
        """
        # Get the current visible range of time on the x-axis
        xlim = ax.get_xlim()

        # Convert xlim values to datetime
        start_time = mdates.num2date(xlim[0])
        end_time = mdates.num2date(xlim[1])

        # Calculate the time difference as a timedelta object
        time_range = end_time - start_time

        # Adjust the interval based on the visible time range
        if time_range > timedelta(days=7):  # More than a week
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=5))  # Every 5 hours
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=3))  # Minor ticks every 3 hours
        elif time_range > timedelta(days=1):  # More than a day but less than a week
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))  # Every 3 hours
            ax.xaxis.set_minor_locator(mdates.HourLocator(interval=2))  # Minor ticks every 2 hours
        elif time_range > timedelta(hours=6):  # More than 6 hours but less than a day
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=1))  # Every 1 hour
            ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=30))  # Minor ticks every 30 minutes
        else:  # Less than 6 hours
            ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))  # Every 30 minutes
            ax.xaxis.set_minor_locator(mdates.MinuteLocator(interval=15))  # Minor ticks every 15 minutes

    

class Task:
    def __init__(self, task_name, task_type,starting, deadline, priority, duration):
            self.task_name = task_name
            self.task_type = task_type  # (personal) / (academic)
            self.task_start= starting
            self.deadline = deadline  # datetime object
            self.priority = priority  # The Higher number is equivalent to higher priority
            self.duration = duration  # in hours
            self.status = 'upcoming'  # Status is upcoming,completed or missed

# # Example system
system = System()
# Additional example tasks for testing
task8 = Task("Task 8", "academic", datetime(2024, 11, 22, 14, 30), datetime(2024, 11, 22, 16, 0), 5, 1)
task9 = Task("Task 9", "personal", datetime(2024, 11, 20, 10, 0), datetime(2024, 11, 23, 12, 0), 3, 4)
task10 = Task("Task 10", "personal", datetime(2024, 11, 24, 7, 0), datetime(2024, 11, 24, 8, 0), 2, 2)
task11 = Task("Task 11", "academic", datetime(2024, 11, 24, 8, 30), datetime(2024, 11, 20, 9, 57), 1, 1)
task12 = Task("Task 12", "personal", datetime(2024, 11, 25, 12, 0), datetime(2024, 11, 25, 14, 0), 4, 2)
task13 = Task("Task 13", "academic", datetime(2024, 11, 25, 15, 0), datetime(2024, 11, 25, 17, 0), 6, 3)
task14 = Task("Task 14", "personal", datetime(2024, 11, 20, 9, 56), datetime(2024, 11, 26, 10, 0), 3, 1)
task15 = Task("Task 15", "academic", datetime(2024, 11, 27, 13, 0), datetime(2024, 11, 27, 15, 0), 4, 2)

# Add the new tasks to the system
system.add_task_sorted(task8)
system.add_task_sorted(task9)
system.add_task_sorted(task10)
system.add_task_sorted(task11)
system.add_task_sorted(task12)
system.add_task_sorted(task13)
system.add_task_sorted(task14)
system.add_task_sorted(task15)

# print(system.sort_tasks("priority"))
# print(system.sort_tasks("type"))
# print(system.sort_tasks("time"))
# system.gantt_chart()

# # Available time (in hours)
# available_time = 3  # Total time available for tasks

# # Schedule tasks based on available time
# selected_tasks = system.schedule_tasks(available_time)
# # Print selected tasks

# print("***************Task Optimisation*********************")
# for task in selected_tasks:
#     print(f"Task selected: {task.task_name}, Type: {task.task_type}, Duration: {task.duration} hours, Priority: {task.priority}")

# while True:
#     print("\n--- Checking Notifications and Updating Statuses ---")
    
#     # Check for notifications
#     system.check_notifications()
    
#     # Update task statuses
#     system.update_statuses()
#     time.sleep(10)


