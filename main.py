
from storage import StorageError
from task import Task
from datetime import datetime

from task_manager import TaskManager

try:
    manager = TaskManager()

except StorageError as error:
    print(f"\nErro ao carregar as tarefas: {error}")
    raise SystemExit(1)


def show_tasks(tasks: list[Task] | None = None) -> None:
    if tasks is None:
        tasks = manager.get_tasks()

    if not tasks:
        print("\nNão existem tarefas para mostrar.")
        return

    print("\n========== AS TUAS TAREFAS ==========")

    for task in tasks:
        status = "Concluída" if task.completed else "Pendente"

        print(f"\nID: {task.task_id}")
        print(f"Título: {task.title}")
        print(f"Descrição: {task.description}")
        print(f"Prioridade: {task.priority}")
        print(f"Prazo: {task.due_date}")
        print(f"Estado: {status}")


def get_non_empty_text(message: str) -> str:
    while True:
        value = input(message).strip()

        if value:
            return value

        print("Este campo não pode ficar vazio.")


def get_priority() -> str:
    priorities = {
        "alta": "Alta",
        "media": "Média",
        "média": "Média",
        "baixa": "Baixa"
    }

    while True:
        value = input(
            "Prioridade (Alta/Média/Baixa): "
        ).strip().casefold()

        if value in priorities:
            return priorities[value]

        print("Prioridade inválida. Escolhe Alta, Média ou Baixa.")


def get_due_date() -> str:
    while True:
        due_date = input("Prazo (AAAA-MM-DD): ").strip()

        try:
            parsed_date = datetime.strptime(
                due_date,
                "%Y-%m-%d"
            )

            if parsed_date.strftime("%Y-%m-%d") == due_date:
                return due_date

        except ValueError:
            pass

        print("Data inválida. Usa uma data real no formato AAAA-MM-DD.")



def filter_tasks_menu() -> None:
    print("\n========== FILTRAR TAREFAS ==========")
    print("1. Mostrar tarefas pendentes")
    print("2. Mostrar tarefas concluídas")
    print("3. Filtrar por prioridade")
    print("0. Voltar ao menu principal")

    option = input("Escolhe um filtro: ").strip()

    if option == "1":
        tasks = manager.get_tasks_by_status(False)
        show_tasks(tasks)

    elif option == "2":
        tasks = manager.get_tasks_by_status(True)
        show_tasks(tasks)

    elif option == "3":
        priority = get_priority()
        tasks = manager.get_tasks_by_priority(priority)
        show_tasks(tasks)

    elif option == "0":
        return

    else:
        print("Opção inválida. Tenta novamente.")


def search_tasks_menu() -> None:
    query = get_non_empty_text(
        "Escreve o título ou a parte do título: "
    )

    results = manager.search_tasks(query)

    print(f"\nForam encontradas {len(results)} tarefa(s). ")

    show_tasks(results)


def show_statistics() -> None:
    stats = manager.get_statistics()

    print("\n========== ESTATÍSTICAS ==========")
    print(f"Total de tarefas: {stats['total']}")
    print(f"Tarefas concluídas: {stats['completed']}")
    print(f"Tarefas pendentes: {stats['pending']}")



def edit_task_menu() -> None:
    show_tasks()

    try:
        task_id = int(input("\nID da tarefa a editar: "))
    except ValueError:
        print("Erro: introduz um ID numérico válido.")
        return

    current_task = next(
        (
            task for task in manager.get_tasks()
            if task.task_id == task_id
        ),
        None
    )

    if current_task is None:
        print("Não foi encontrada nenhuma tarefa com esse ID.")
        return

    print("\nIntroduz os novos dados da tarefa.")

    title = get_non_empty_text("Novo título: ")
    description = input("Nova descrição: ").strip()
    priority = get_priority()
    due_date = get_due_date()

    success = manager.edit_task(
        task_id,
        title,
        description,
        priority,
        due_date
    )

    if success:
        print("\nTarefa editada com sucesso!")


while True:
    print("\n========== TASK MANAGER ==========")
    print("1. Adicionar tarefa")
    print("2. Listar tarefas")
    print("3. Concluir tarefa")
    print("4. Excluir tarefa")
    print("5. Filtrar tarefas")
    print("6. Pesquisar tarefa por título")
    print("7. Ver estatísticas")
    print("8. Editar tarefa")
    print("9. Ordenar tarefas por prazo")
    print("0. Sair")

    option = input("Escolhe uma opção: ").strip()

    if option == "1":
        title = get_non_empty_text("Título: ")

        description = input("Descrição: ").strip()

        priority = get_priority()

        due_date = get_due_date()

        task = manager.add_task(
            title,
            description,
            priority,
            due_date
        )

        print(f"\nTarefa '{task.title}' adicionada com sucesso!")
        print(f"ID da tarefa: {task.task_id}")

    elif option == "2":
        show_tasks()

    elif option == "3":
        show_tasks()

        try:
            task_id = int(input("\nID da tarefa a concluir: "))
        except ValueError:
            print("Erro: introduz um ID numérico válido.")
            continue

        if manager.complete_task(task_id):
            print("Tarefa concluída com sucesso!")
        else:
            print("Não foi encontrada nenhuma tarefa com esse ID.")

    elif option == "4":
        show_tasks()

        try:
            task_id = int(input("\nID da tarefa a excluir: "))
        except ValueError:
            print("Erro: introduz um ID numérico válido.")
            continue

        if manager.delete_task(task_id):
            print("Tarefa excluída com sucesso!")
        else:
            print("Não foi encontrada nenhuma tarefa com esse ID.")

    elif option == "5":
            filter_tasks_menu()

    elif option == "6":
        search_tasks_menu()

    elif option == "7":
        show_statistics()

    elif option == "8":
        edit_task_menu()

    elif option == "9":
        tasks = manager.get_tasks_sorted_by_due_date()
        show_tasks(tasks)

    elif option == "0":
            print("A sair do Task Manager...")
            break

    else:
        print("Opção inválida. Tenta novamente.")
