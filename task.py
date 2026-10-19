class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        description: str,
        priority: str,
        due_date: str
    ) -> None:
        self.task_id = task_id
        self.title = title
        self.description = description
        self.priority = priority
        self.due_date = due_date
        self.completed = False
