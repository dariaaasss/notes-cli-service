import argparse
import sys
import questionary
from rich.prompt import Prompt
from src.handlers import (
    console, storage, 
    handle_add, handle_list, handle_edit, handle_delete
)

def run_interactive_mode():
    """Бесконечный цикл работы приложения."""
    while True:
        console.clear()
        console.rule("[bold blue]Notes CLI Service[/bold blue]")
        

        action = questionary.select(
            "Что вы хотите сделать?",
            choices=[
                questionary.Choice("📜 Показать все", value="list"),
                questionary.Choice("🔍 Поиск", value="search"),
                questionary.Choice("➕ Добавить новую", value="add"),
                questionary.Choice("✏️ Редактировать", value="edit"),
                questionary.Choice("🗑️ Удалить", value="delete"),
                questionary.Choice("🚪 Выход", value="exit"),
            ]
        ).ask()

        if action == "exit":
            console.print("[bold blue]До свидания! 👋[/bold blue]")
            sys.exit(0)
        
        elif action == "list":
            handle_list()
        
        elif action == "search":
            query = Prompt.ask("Введите текст для поиска")
            handle_list(query) 
        
        elif action == "add":
            handle_add()
        
        elif action == "edit":
            handle_edit()
        
        elif action == "delete":
            handle_delete()
        
        # Пауза, чтобы пользователь увидел результат перед очисткой
        print()
        Prompt.ask("[dim]Нажмите Enter, чтобы продолжить...[/dim]")

def main():
    parser = argparse.ArgumentParser(description="CLI Сервис Заметок")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # Настройка аргументов
    add_parser = subparsers.add_parser("add", help="Создать заметку")
    add_parser.add_argument("--title")
    add_parser.add_argument("--msg")

    list_parser = subparsers.add_parser("list", help="Список заметок")
    list_parser.add_argument("--query", "-q")

    edit_parser = subparsers.add_parser("edit", help="Редактировать заметку")
    edit_parser.add_argument("--id")
    edit_parser.add_argument("--title")
    edit_parser.add_argument("--msg")

    del_parser = subparsers.add_parser("delete", help="Удалить заметку")
    del_parser.add_argument("--id")

    # Интерактивный режим
    if len(sys.argv) == 1:
        try:
            run_interactive_mode()
        except KeyboardInterrupt:
            console.print("\n[bold blue]Выход...[/bold blue]")
            sys.exit(0)
    
    # Обычный режим (CLI флаги)
    args = parser.parse_args()

    if args.command == "add":
        handle_add(args.title, args.msg)
    elif args.command == "list":
        handle_list(args.query)
    elif args.command == "edit":
        handle_edit(args.id, args.title, args.msg)
    elif args.command == "delete":
        handle_delete(args.id)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()