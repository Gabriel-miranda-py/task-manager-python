
from task import Task
from storage import load_tasks, save_tasks


class TaskManager:
    def __init__(self) -> None:
        self.tasks: list[Task] = load_tasks()

    def add_task(
        self,
        title: str,
        description: str,
        priority: str,
        due_date: str
    ) -> Task:
        task_id = max(
            (task.task_id for task in self.tasks),
            default=0
        ) + 1

        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date
        )

        self.tasks.append(task)
        save_tasks(self.tasks)

        return task

    def get_tasks(self) -> list[Task]:
        return self.tasks.copy()

    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                task.completed = True
                save_tasks(self.tasks)
                return True

        return False

    def delete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                self.tasks.remove(task)
                save_tasks(self.tasks)
                return True

        return False

    def edit_task(
        self,
        task_id: int,
        title: str,
        description: str,
        priority: str,
        due_date: str
    ) -> bool:
        for task in self.tasks:
            if task.task_id == task_id:
                task.title = title
                task.description = description
                task.priority = priority
                task.due_date = due_date

                save_tasks(self.tasks)
                return True

        return False

    def get_tasks_by_status(self, completed: bool) -> list[Task]:
        return [
            task for task in self.tasks
            if task.completed == completed
        ]

    def get_tasks_by_priority(self, priority: str) -> list[Task]:
        return [
            task for task in self.tasks
            if task.priority.casefold() == priority.casefold()
        ]

    def search_tasks(self, query: str) -> list[Task]:
        query = query.strip().casefold()

        return [
            task for task in self.tasks
            if query in task.title.casefold()
        ]

    def get_statistics(self) -> dict[str, int]:
        total = len(self.tasks)

        completed = sum(
            1 for task in self.tasks
            if task.completed
        )

        pending = total - completed

        return {
            "total": total,
            "completed": completed,
            "pending": pending
        }

    def get_tasks_sorted_by_due_date(self) -> list[Task]:
        return sorted(
            self.tasks,
            key=lambda task: task.due_date
        )
