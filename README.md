# Task Manager

A task management application built with Python. This project allows users to create, view, edit, complete, delete, search, and filter tasks through a command-line interface.

## Features

- Add new tasks with a title, description, priority, and due date.
- List all registered tasks.
- Edit existing tasks.
- Mark tasks as completed.
- Delete tasks.
- Filter tasks by status or priority.
- Search tasks by title.
- View statistics about total, completed, and pending tasks.
- Save and load tasks using a JSON file.
- Validate user input.
- Handle invalid JSON data and report storage errors.
- Run automated tests using `unittest`.

## Technologies

- Python 3.10 or newer
- JSON for data persistence
- `unittest` for automated testing

No external Python packages are required.

## Project Structure

```text
task_manager_api/
├── main.py
├── task.py
├── task_manager.py
├── storage.py
├── tasks.json
├── README.md
└── tests/
    ├── test_task_manager.py
    └── test_storage.py
```

### Main Files

- `main.py`: Runs the application and handles user interaction.
- `task.py`: Defines the `Task` class.
- `task_manager.py`: Contains the task management operations.
- `storage.py`: Saves and loads tasks from the JSON file and handles storage errors.
- `tasks.json`: Stores the task data.
- `tests/`: Contains the automated tests.

## Getting Started

### Requirements

Install Python 3.10 or newer.

### Run the Application

Open a terminal in the project folder and run:

```bash
python main.py
```

On Windows, you can also use:

```bash
py main.py
```

Follow the menu displayed in the terminal to manage your tasks.

## Running the Tests

Run all automated tests from the project root:

```bash
python -m unittest discover -s tests -v
```

The tests cover task management operations, searching, filtering, statistics, editing, and JSON storage.

## Data Storage

Tasks are stored locally in `tasks.json`. The application loads existing tasks when it starts and saves changes when tasks are added, edited, completed, or deleted.

Keep a backup of `tasks.json` if you need to preserve your task data.

## Learning Objectives

This project demonstrates practical use of:

- Object-oriented programming (OOP)
- Classes and objects
- CRUD operations
- Functions and methods
- Lists and list comprehensions
- Type hints
- Exception handling
- JSON file operations
- Input validation
- Automated testing and mocking
- Separation of responsibilities between modules

## Future Improvements

- Add sorting by due date.
- Improve task editing so existing values can be kept.
- Add recurring tasks and reminders.
- Develop a graphical user interface.
- Add database support.
- Add more automated tests for input validation and storage failures.

## Author

Developed as a Python learning project.
