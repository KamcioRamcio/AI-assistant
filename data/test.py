from functions import *

def main():
    while True:
        print("\nTo-Do List")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Complete")
        print("4. Delete Task")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task = input("Enter the task: ")
            deadline = None
            location = None

            if input("Is there a deadline for this task? (y/n) ").lower() == "y":
                deadline = input("Enter the deadline: ")

            if input("Is there a location for this task? (y/n) ").lower() == "y":
                location = input("Enter the location: ")

            add_task(task, deadline, location)
        elif choice == "2":
            tasks = get_tasks()
            for task in tasks:
                status = "Completed" if task[4] else "Pending"
                print(f"{task[0]}: {task[1]} - {status}, Deadline: {task[2]}, Location: {task[3]}")
        elif choice == "3":
            task_id = int(input("Enter the task ID to mark as complete: "))
            update_task(task_id, True)
        elif choice == "4":
            task_id = int(input("Enter the task ID to delete: "))
            delete_task(task_id)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
