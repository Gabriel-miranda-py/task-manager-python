
import json
from pathlib import Path

from task import Task


DATA_FILE = Path(__file__).with_name("tasks.json")


class StorageError(Exception):
    """Erro relacionado com o armazenamento das tarefas."""


def save_tasks(tasks: list[Task]) -> None:
    data = []

    for task in tasks:
        task_data = {
            "task_id": task.task_id,
            "title": task.title,
            "description": task.description,
            "priority": task.priority,
            "due_date": task.due_date,
            "completed": task.completed
        }

        data.append(task_data)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_tasks() -> list[Task]:
    try:
        with DATA_FILE.open("r", encoding="utf-8") as file:
            content = file.read()

    except FileNotFoundError:
        return []

    except OSError as error:
        raise StorageError(
            f"Não foi possível ler o ficheiro: {error}"
        ) from error

    if not content.strip():
        return []

    try:
        data = json.loads(content)

    except json.JSONDecodeError as error:
        raise StorageError(
            "O tasks.json contém dados inválidos. "
            f"Verifica a linha {error.lineno}, "
            f"coluna {error.colno}."
        ) from error

    if not isinstance(data, list):
        raise StorageError(
            "O tasks.json deve conter uma lista de tarefas."
        )

    tasks = []

    required_fields = (
        "task_id",
        "title",
        "description",
        "priority",
        "due_date"
    )

    for index, item in enumerate(data, start=1):
        if not isinstance(item, dict):
            raise StorageError(
                f"A tarefa número {index} não é um objeto válido."
            )

        missing_fields = [
            field for field in required_fields
            if field not in item
        ]

        if missing_fields:
            raise StorageError(
                f"A tarefa número {index} não contém "
                f"os campos: {', '.join(missing_fields)}."
            )

        task_id = item["task_id"]

        if not isinstance(task_id, int) or isinstance(task_id, bool):
            raise StorageError(
                f"O ID da tarefa número {index} é inválido."
            )

        for field in (
            "title",
            "description",
            "priority",
            "due_date"
        ):
            if not isinstance(item[field], str):
                raise StorageError(
                    f"O campo '{field}' da tarefa "
                    f"número {index} deve ser texto."
                )

        completed = item.get("completed", False)

        if not isinstance(completed, bool):
            raise StorageError(
                f"O estado da tarefa número {index} é inválido."
            )

        task = Task(
            task_id=task_id,
            title=item["title"],
            description=item["description"],
            priority=item["priority"],
            due_date=item["due_date"]
        )

        task.completed = completed
        tasks.append(task)

    return tasks
