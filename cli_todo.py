"""
To-Do List Application - Command Line Interface (CLI) Version
Task 1 - Internship Project
"""

import json
import os
from datetime import datetime

# ─────────────────────────────────────────────
# FILE STORAGE
# ─────────────────────────────────────────────
TASKS_FILE = "tasks.json"

def load_tasks():
    """Load tasks from JSON file. Returns empty list if file doesn't exist."""
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    return []

def save_tasks(tasks):
    """Save tasks list to JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

# ─────────────────────────────────────────────
# TASK OPERATIONS
# ─────────────────────────────────────────────
def add_task(tasks):
    """Add a new task."""
    title = input("\nEnter task title: ").strip()
    if not title:
        print("❌ Task title cannot be empty!")
        return

    due_date = input("Enter due date (DD-MM-YYYY) or press Enter to skip: ").strip()

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": "Pending",
        "due_date": due_date if due_date else "No due date",
        "created_at": datetime.now().strftime("%d-%m-%Y %H:%M")
    }

    tasks.append(task)
    save_tasks(tasks)
    print(f"\n✅ Task '{title}' added successfully!")


def view_tasks(tasks):
    """Display all tasks."""
    if not tasks:
        print("\n📭 No tasks found. Start by adding one!")
        return

    print("\n" + "=" * 60)
    print(f"{'ID':<5} {'TITLE':<25} {'STATUS':<12} {'DUE DATE'}")
    print("=" * 60)

    for task in tasks:
        status_icon = "✅" if task["status"] == "Completed" else "⏳"
        print(f"{task['id']:<5} {task['title']:<25} {status_icon} {task['status']:<10} {task['due_date']}")

    print("=" * 60)
    print(f"Total: {len(tasks)} task(s) | "
          f"Completed: {sum(1 for t in tasks if t['status'] == 'Completed')} | "
          f"Pending: {sum(1 for t in tasks if t['status'] == 'Pending')}")


def complete_task(tasks):
    """Mark a task as completed."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("\nEnter Task ID to mark as complete: "))
        task = next((t for t in tasks if t["id"] == task_id), None)

        if not task:
            print("❌ Task not found!")
        elif task["status"] == "Completed":
            print("ℹ️  Task is already completed!")
        else:
            task["status"] = "Completed"
            save_tasks(tasks)
            print(f"✅ Task '{task['title']}' marked as completed!")

    except ValueError:
        print("❌ Please enter a valid number!")


def delete_task(tasks):
    """Delete a task by ID."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("\nEnter Task ID to delete: "))
        task = next((t for t in tasks if t["id"] == task_id), None)

        if not task:
            print("❌ Task not found!")
        else:
            confirm = input(f"⚠️  Delete '{task['title']}'? (yes/no): ").lower()
            if confirm == "yes":
                tasks.remove(task)
                # Re-assign IDs after deletion
                for i, t in enumerate(tasks, start=1):
                    t["id"] = i
                save_tasks(tasks)
                print(f"🗑️  Task deleted successfully!")
            else:
                print("❎ Deletion cancelled.")

    except ValueError:
        print("❌ Please enter a valid number!")


def update_task(tasks):
    """Update the title of an existing task."""
    view_tasks(tasks)
    if not tasks:
        return

    try:
        task_id = int(input("\nEnter Task ID to update: "))
        task = next((t for t in tasks if t["id"] == task_id), None)

        if not task:
            print("❌ Task not found!")
        else:
            new_title = input(f"Enter new title (current: '{task['title']}'): ").strip()
            if new_title:
                task["title"] = new_title
                save_tasks(tasks)
                print(f"✏️  Task updated to '{new_title}'!")
            else:
                print("❌ Title cannot be empty!")

    except ValueError:
        print("❌ Please enter a valid number!")


def clear_completed(tasks):
    """Remove all completed tasks."""
    completed = [t for t in tasks if t["status"] == "Completed"]
    if not completed:
        print("\nℹ️  No completed tasks to clear.")
        return

    confirm = input(f"⚠️  Remove all {len(completed)} completed task(s)? (yes/no): ").lower()
    if confirm == "yes":
        tasks[:] = [t for t in tasks if t["status"] == "Pending"]
        for i, t in enumerate(tasks, start=1):
            t["id"] = i
        save_tasks(tasks)
        print(f"🗑️  {len(completed)} completed task(s) cleared!")
    else:
        print("❎ Operation cancelled.")


# ─────────────────────────────────────────────
# MENU
# ─────────────────────────────────────────────
def show_menu():
    print("\n" + "╔" + "═" * 36 + "╗")
    print("║       📝  TO-DO LIST APP           ║")
    print("╠" + "═" * 36 + "╣")
    print("║  1. ➕ Add Task                    ║")
    print("║  2. 📋 View All Tasks              ║")
    print("║  3. ✅ Mark Task as Complete       ║")
    print("║  4. ✏️  Update Task Title           ║")
    print("║  5. 🗑️  Delete a Task               ║")
    print("║  6. 🧹 Clear Completed Tasks       ║")
    print("║  7. 🚪 Exit                        ║")
    print("╚" + "═" * 36 + "╝")


def main():
    print("\n🎉 Welcome to the To-Do List App!")
    tasks = load_tasks()

    while True:
        show_menu()
        choice = input("\nEnter your choice (1-7): ").strip()

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            update_task(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            clear_completed(tasks)
        elif choice == "7":
            print("\n👋 Goodbye! Stay productive!\n")
            break
        else:
            print("❌ Invalid choice! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
