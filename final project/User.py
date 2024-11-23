import heapq
import time
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from DAAproject import *

# Assume your System and Task classes are already imported and available as they were defined earlier

def print_menu():
    """
    Display the CLI menu to the user.
    """
    print("\nTask Management System")
    print("1. Add Task")
    print("2. Sort Tasks")
    print("3. Check Notifications")
    print("4. Update Task Statuses")
    print("5. View Gantt Chart")
    print("6.  Optimise Schedule Tasks")
    print("7. Exit")

def get_task_input():
    """
    Get task input from the user.
    """
    task_name = input("Enter task name: ")
    task_type = input("Enter task type (academic/personal): ").lower()
    task_start = datetime.strptime(input("Enter task start time (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
    deadline = datetime.strptime(input("Enter task deadline (YYYY-MM-DD HH:MM): "), "%Y-%m-%d %H:%M")
    priority = int(input("Enter task priority (higher number is higher priority): "))
    duration = int(input("Enter task duration in hours: "))
    return Task(task_name, task_type, task_start, deadline, priority, duration)

def main():
    
    while True:
        print_menu()
        choice = input("Choose an option (1-7): ")
        
        if choice == '1':
            # Add a new task
            task = get_task_input()
            system.add_task_sorted(task)
            print(f"Task '{task.task_name}' added successfully.")
        
        elif choice == '2':
            # Sort tasks by chosen criteria
            print("\nSort by:")
            print("1. Priority")
            print("2. Task Type")
            print("3. Start Time")
            print("4. End Time")
            sort_choice = input("Choose an option (1-3): ")
            if sort_choice == '1':
                system.sort_tasks("priority")
            elif sort_choice == '2':
                system.sort_tasks("type")
            elif sort_choice == '3':
                system.sort_tasks("start")

            elif sort_choice == '4':
                system.sort_tasks("end")
            else:
                print("Invalid choice.")
        
        elif choice == '3':
            # Check for notifications
            print("\nChecking notifications...\n")
            system.check_notifications()
        
        elif choice == '4':
            # Update task statuses
            print("\nUpdating task statuses...\n")
            system.update_statuses()
        
        elif choice == '5':
            # View the Gantt chart
            print("\nDisplaying Gantt chart...\n")
            system.gantt_chart()
        
        elif choice == '6':
            # Schedule tasks
            available_time = int(input("Enter the available time in hours: "))
            selected_tasks = system.schedule_tasks(available_time)
            print("\nSelected tasks based on available time:")
            for task in selected_tasks:
                print(f"Task: {task.task_name}, Type: {task.task_type}, Duration: {task.duration} hours, Priority: {task.priority}")
        
        elif choice == '7':
            # Exit the program
            print("Exiting the system.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == '__main__':
    main()
