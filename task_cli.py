import sys
from datetime import datetime
import json

TASK_FILE = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]

def create_task(task_id, description, status, created_at, updated_at):
    return {
        "id": task_id,
        "description": description,
        "status": status,
        "createdAt": created_at,
        "updatedAt": updated_at
    }

def add_task(tasks, task, task_id):
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task_id})")

def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(f"ID: {task['id']}, Description: {task['description']}, Status: {task['status']}, Created At: {task['createdAt']}, Updated At: {task['updatedAt']}")

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []
        save_tasks(tasks)
    except json.JSONDecodeError:
        print("Error: tasks.json is not a valid JSON file. Starting with an empty task list.")
        sys.exit(1)
    return tasks

def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump(tasks, f, indent=4)

def main():

    tasks = load_tasks()

    if len(sys.argv) < 2:
        print("Usage: python task_cli.py <command>")
        sys.exit(1)

    command = sys.argv[1]
    if command == "add":
        if len(sys.argv) < 3:
            print("Usage: python task_cli.py add <task>")
            sys.exit(1)
        task_id = max((task["id"] for task in tasks), default=0) + 1
        task_status = "todo"
        task_description = sys.argv[2]
        now = datetime.now().isoformat()
        task_created_at = now
        task_updated_at = now
        task = create_task(task_id, task_description, task_status, task_created_at, task_updated_at)
        add_task(tasks, task, task_id)
    elif command == "list":
        if len(sys.argv) == 3:
            if sys.argv[2] == "todo":
                tasks = [task for task in tasks if task["status"] == "todo"]
            elif sys.argv[2] == "in-progress":
                tasks = [task for task in tasks if task["status"] == "in-progress"]
            elif sys.argv[2] == "done":
                tasks = [task for task in tasks if task["status"] == "done"]
            else:
                print(f"Unknown status filter: {sys.argv[2]}")
                sys.exit(1)
        elif len(sys.argv) > 3:
            print("Usage: python task_cli.py list [status]")
            sys.exit(1)
            
        list_tasks(tasks)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()