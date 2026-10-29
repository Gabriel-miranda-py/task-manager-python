
from datetime import date 
import unittest
from unittest.mock import patch

from task_manager import TaskManager


class TestTaskManager(unittest.TestCase):

    def setUp(self) -> None:
        self.load_patcher = patch(
            "task_manager.load_tasks",
            return_value=[]
        )

        self.save_patcher = patch(
            "task_manager.save_tasks"
        )

        self.mock_load = self.load_patcher.start()
        self.mock_save = self.save_patcher.start()

        self.addCleanup(self.load_patcher.stop)
        self.addCleanup(self.save_patcher.stop)

        self.manager = TaskManager()

    def test_add_task(self) -> None:
        task = self.manager.add_task(
            "Estudar Python",
            "Praticar OOP",
            "Alta",
            "2026-10-25"
        )

        self.assertEqual(task.task_id, 1)
        self.assertEqual(task.title, "Estudar Python")
        self.assertFalse(task.completed)
        self.mock_save.assert_called_once()

    def test_task_ids_increase(self) -> None:
        first = self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        second = self.manager.add_task(
            "Estudar inglês",
            "Vocabulário",
            "Média",
            "2026-10-26"
        )

        self.assertEqual(first.task_id, 1)
        self.assertEqual(second.task_id, 2)

    def test_get_tasks_returns_copy(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        tasks = self.manager.get_tasks()
        tasks.clear()

        self.assertEqual(
            len(self.manager.get_tasks()),
            1
        )

    def test_complete_task(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.mock_save.reset_mock()

        result = self.manager.complete_task(1)

        self.assertTrue(result)
        self.assertTrue(
            self.manager.get_tasks()[0].completed
        )
        self.mock_save.assert_called_once()

    def test_complete_nonexistent_task(self) -> None:
        result = self.manager.complete_task(99)

        self.assertFalse(result)

    def test_delete_task(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.mock_save.reset_mock()

        result = self.manager.delete_task(1)

        self.assertTrue(result)
        self.assertEqual(self.manager.get_tasks(), [])
        self.mock_save.assert_called_once()

    def test_filter_by_status(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.manager.add_task(
            "Estudar inglês",
            "Vocabulário",
            "Média",
            "2026-10-26"
        )

        self.manager.complete_task(1)

        completed = self.manager.get_tasks_by_status(True)
        pending = self.manager.get_tasks_by_status(False)

        self.assertEqual(
            [task.task_id for task in completed],
            [1]
        )
        self.assertEqual(
            [task.task_id for task in pending],
            [2]
        )

    def test_filter_by_priority(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.manager.add_task(
            "Estudar inglês",
            "Vocabulário",
            "Baixa",
            "2026-10-26"
        )

        results = self.manager.get_tasks_by_priority("alta")

        self.assertEqual(
            [task.task_id for task in results],
            [1]
        )

    def test_search_by_title(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.manager.add_task(
            "Ir ao ginásio",
            "Fazer exercício",
            "Baixa",
            "2026-10-26"
        )

        results = self.manager.search_tasks("PYTHON")

        self.assertEqual(
            [task.task_id for task in results],
            [1]
        )

    def test_statistics(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.manager.add_task(
            "Estudar inglês",
            "Vocabulário",
            "Média",
            "2026-10-26"
        )

        self.manager.add_task(
            "Ir ao ginásio",
            "Exercício",
            "Baixa",
            "2026-10-27"
        )

        self.manager.complete_task(2)

        stats = self.manager.get_statistics()

        self.assertEqual(stats["total"], 3)
        self.assertEqual(stats["completed"], 1)
        self.assertEqual(stats["pending"], 2)

    def test_edit_task(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-25"
        )

        self.mock_save.reset_mock()

        result = self.manager.edit_task(
            1,
            "Aprender Python",
            "Praticar classes",
            "Baixa",
            "2026-10-28"
        )

        task = self.manager.get_tasks()[0]

        self.assertTrue(result)
        self.assertEqual(task.title, "Aprender Python")
        self.assertEqual(task.description, "Praticar classes")
        self.assertEqual(task.priority, "Baixa")
        self.assertEqual(task.due_date, "2026-10-28")
        self.mock_save.assert_called_once()

    def test_edit_nonexistent_task(self) -> None:
        result = self.manager.edit_task(
            99,
            "Novo título",
            "Nova descrição",
            "Alta",
            "2026-10-25"
        )

        self.assertFalse(result)

    def test_sort_tasks_by_due_date(self) -> None:
        self.manager.add_task(
            "Estudar Python",
            "Programação",
            "Alta",
            "2026-10-30"
        )

        self.manager.add_task(
            "Fazer trabalho",
            "Trabalho escolar",
            "Média",
            "2026-10-25"
        )

        self.manager.add_task(
            "Estudar inglês",
            "Vocabulário",
            "Baixa",
            "2026-10-28"
        )

        sorted_tasks = self.manager.get_tasks_sorted_by_due_date()

        self.assertEqual(
            [task.task_id for task in sorted_tasks],
            [2, 3, 1]
        )

        # A ordenação não deve alterar a lista original.
        self.assertEqual(
            [task.task_id for task in self.manager.get_tasks()],
            [1, 2, 3]
        )


if __name__ == "__main__":
    unittest.main()
