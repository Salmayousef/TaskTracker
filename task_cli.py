import json
import sys
from datetime import datetime

TASK_FILE = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]


def create_task(task_id, description, status, created_at, updated_at):
    return {
        "id": task_id,
        "description": description,
        "status": status,
        "createdAt": created_at,
        "updatedAt": updated_at,
    }


def add_task(tasks, task):
    tasks.append(task)
    save_tasks(tasks)
    print(f"Task added successfully (ID: {task['id']})")


def parse_task_id(value):
    try:
        return int(value)
    except ValueError:
        print("Error: task_id must be an integer.")
        sys.exit(1)


def validate_description(description):
    if not description.strip():
        print("Error: Description cannot be empty.")
        sys.exit(1)


def find_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            return task
    print(f"Error: Task with ID {task_id} not found.")
    sys.exit(1)


def update_task(tasks, task_id, description):
    task = find_task(tasks, task_id)
    task["description"] = description
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"Task ID {task_id} updated successfully to description '{description}'")


def delete_task(tasks, task_id):
    task = find_task(tasks, task_id)
    tasks.remove(task)
    save_tasks(tasks)
    print(f"Task ID {task_id} deleted successfully")


def mark_task(tasks, task_id, status):
    task = find_task(tasks, task_id)
    task["status"] = status
    task["updatedAt"] = datetime.now().isoformat()
    save_tasks(tasks)
    print(f"Task ID {task_id} marked as {status} successfully")


def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    for task in tasks:
        print(
            f"ID: {task['id']}, Description: {task['description']}, "
            f"Status: {task['status']}, Created At: {task['createdAt']}, "
            f"Updated At: {task['updatedAt']}"
        )


def load_tasks():
    try:
        with open(TASK_FILE, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except FileNotFoundError:
        tasks = []
        save_tasks(tasks)
    except json.JSONDecodeError:
        print(f"Error: {TASK_FILE} is not a valid JSON file.")
        sys.exit(1)
    return tasks


def save_tasks(tasks):
    with open(TASK_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


def main():
    if len(sys.argv) < 2:
        print("Usage: python task_cli.py <command>")
        sys.exit(1)

    command = sys.argv[1]
    tasks = load_tasks()
    if command == "add":
        if len(sys.argv) != 3:
            print('Usage: python task_cli.py add "<description>"')
            sys.exit(1)
        description = sys.argv[2]
        validate_description(description)
        task_id = max((task["id"] for task in tasks), default=0) + 1
        now = datetime.now().isoformat()
        task = create_task(task_id, description, "todo", now, now)
        add_task(tasks, task)
    elif command == "list":
        if len(sys.argv) == 3:
            status = sys.argv[2]
            if status not in VALID_STATUSES:
                print(f"Unknown status filter: {status}")
                sys.exit(1)
            tasks = [task for task in tasks if task["status"] == status]
        elif len(sys.argv) > 3:
            print("Usage: python task_cli.py list [status]")
            sys.exit(1)

        list_tasks(tasks)
    elif command == "update":
        if len(sys.argv) != 4:
            print('Usage: python task_cli.py update <task_id> "<new_description>"')
            sys.exit(1)
        task_id = parse_task_id(sys.argv[2])
        description = sys.argv[3]
        validate_description(description)
        update_task(tasks, task_id, description)
    elif command == "delete":
        if len(sys.argv) != 3:
            print("Usage: python task_cli.py delete <task_id>")
            sys.exit(1)
        task_id = parse_task_id(sys.argv[2])
        delete_task(tasks, task_id)
    elif command in ("mark-done", "mark-in-progress"):
        if len(sys.argv) != 3:
            print(f"Usage: python task_cli.py {command} <task_id>")
            sys.exit(1)
        task_id = parse_task_id(sys.argv[2])
        status = "done" if command == "mark-done" else "in-progress"
        mark_task(tasks, task_id, status)
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == "__main__":
    main()
