# Task Tracker CLI

A Python command-line task tracker that stores tasks in a JSON file.

## Setup

Install Python 3, open a terminal in this project directory, and run:

```bash
python3 task_cli.py list
```

No external packages are required. If your system uses `python` for Python 3,
you can use that command instead of `python3`.

## Commands

Put descriptions containing spaces in quotes. Replace example IDs with an
existing task ID from `list`.

```bash
# Add a task (starts with status todo)
python3 task_cli.py add "Buy groceries"

# Update a description
python3 task_cli.py update 1 "Buy groceries and cook dinner"

# Change a task status
python3 task_cli.py mark-in-progress 1
python3 task_cli.py mark-done 1

# List all tasks or filter by status
python3 task_cli.py list
python3 task_cli.py list todo
python3 task_cli.py list in-progress
python3 task_cli.py list done

# Delete a task
python3 task_cli.py delete 1
```

## Storage

Tasks are saved in `tasks.json` in the current working directory. The file is
created automatically if it is missing. Running the script from another
directory uses a separate `tasks.json` in that directory.

Each task has an integer `id`, a `description`, a `status`, and ISO-formatted
`createdAt` and `updatedAt` timestamps. Updating a description or status changes
`updatedAt` and preserves `createdAt`. Deleting a task leaves the other tasks
and their IDs unchanged. New IDs are the highest existing ID plus one, or 1
when the list is empty; a deleted highest ID can therefore be reused.

## Errors

Missing or extra arguments, blank descriptions, invalid IDs, unknown commands,
and unknown status filters produce an error and a nonzero exit code.
Malformed JSON produces an error without overwriting the file. Correct the JSON
or restore a backup before running another command.

`tasks.json` and Python cache files are listed in `.gitignore` to keep local
data out of new Git commits. Ignore rules do not untrack files already in Git.
