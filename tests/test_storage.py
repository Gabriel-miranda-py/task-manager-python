
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from storage import StorageError, load_tasks, save_tasks
from task import Task


class TestStorage(unittest.TestCase):

    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)

        self.data_file = Path(
            self.temp_dir.name
        ) / "tasks.json"

        self.patcher = patch(
            "storage.DATA_FILE",
            self.data_file
        )

        self.patcher.start()
        self.addCleanup(self.patcher.stop)

    def test_save_and_load_tasks(self) -> None:
        task = Task(
            task_id=1,
            title="Estudar Python",
            description="Praticar programação",
            priority="Alta",
            due_date="2026-10-25"
        )

        task.completed = True

        save_tasks([task])
        loaded_tasks = load_tasks()

        self.assertEqual(len(loaded_tasks), 1)
        self.assertEqual(
            loaded_tasks[0].title,
            "Estudar Python"
        )
        self.assertEqual(
            loaded_tasks[0].description,
            "Praticar programação"
        )
        self.assertEqual(
            loaded_tasks[0].priority,
            "Alta"
        )
        self.assertTrue(loaded_tasks[0].completed)

    def test_missing_file_returns_empty_list(self) -> None:
        tasks = load_tasks()

        self.assertEqual(tasks, [])

    def test_invalid_json_raises_storage_error(self) -> None:
        self.data_file.write_text(
            "{ invalid json",
            encoding="utf-8"
        )

        with self.assertRaisesRegex(
            StorageError,
            "dados inválidos"
        ):
            load_tasks()

    def test_json_root_must_be_a_list(self) -> None:
        self.data_file.write_text(
            '{"task_id": 1}',
            encoding="utf-8"
        )

        with self.assertRaisesRegex(
            StorageError,
            "deve conter uma lista"
        ):
            load_tasks()

    def test_missing_required_field_raises_storage_error(
        self
    ) -> None:
        self.data_file.write_text(
            """
            [
                {
                    "task_id": 1,
                    "title": "Estudar Python",
                    "priority": "Alta",
                    "due_date": "2026-10-25"
                }
            ]
            """,
            encoding="utf-8"
        )

        with self.assertRaisesRegex(
            StorageError,
            "description"
        ):
            load_tasks()


if __name__ == "__main__":
    unittest.main()
