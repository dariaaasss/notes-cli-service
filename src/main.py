import argparse
import sys
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from src.storage import Storage
from src.models import Note

# Инициализация Rich консоли
console = Console()


def print_notes_table(notes):
    """Helper function to print notes in a nice table."""
    if not notes:
        console.print("[yellow]📭 Заметок не найдено.[/yellow]")
        return

    table = Table(title=f"Мои Заметки ({len(notes)})", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Дата", style="magenta")
    table.add_column("Заголовок", style="green")
    table.add_column("Содержание")

    for note in notes:
        # Обрезаем ID и дату для красоты
        table.add_row(note.id[:8], note.created_at[:10], note.title, note.content)

    console.print(table)


def main():
    parser = argparse.ArgumentParser(description="Сервис CLI для заметок")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # --- ADD COMMAND ---
    # Убрали required=True, чтобы можно было запускать интерактивно
    add_parser = subparsers.add_parser("add", help="Добавить новую заметку")
    add_parser.add_argument("--title", help="Заголовок заметки")
    add_parser.add_argument("--msg", help="Содержание заметки")

    # --- LIST COMMAND ---
    list_parser = subparsers.add_parser("list", help="Вывести все заметки")
    list_parser.add_argument("--query", "-q", help="Фильтр заметок по ключевому слову")

    # --- EDIT COMMAND ---
    edit_parser = subparsers.add_parser("edit", help="Редактировать заметку")
    edit_parser.add_argument("--id", help="ID заметки для редактирования")
    edit_parser.add_argument("--title", help="Новый заголовок")
    edit_parser.add_argument("--msg", help="Новое содержание")

    # --- DELETE COMMAND ---
    del_parser = subparsers.add_parser("delete", help="Удалить заметку по ID")
    del_parser.add_argument("--id", help="ID заметки для удаления")

    args = parser.parse_args()
    storage = Storage()

    # LOGIC
    if args.command == "add":
        # Интерактивный режим: если флагов нет, спрашиваем через Prompt
        title = args.title or Prompt.ask("[bold green]Введите заголовок[/bold green]")
        content = args.msg or Prompt.ask("[bold green]Введите содержание[/bold green]")

        note = Note(title=title, content=content)
        storage.add_note(note)
        console.print(f"[bold blue]✅ Заметка успешно добавлена![/bold blue] (ID: {note.id[:8]})")

    elif args.command == "list":
        if args.query:
            notes = storage.filter_notes(args.query)
            console.print(f"[bold blue]🔍 Результаты поиска по '{args.query}':[/bold blue]")
        else:
            notes = storage.get_all_notes()
        print_notes_table(notes)

    elif args.command == "edit":
        # Если ID не передан, показываем список и просим ввести ID
        if not args.id:
            print_notes_table(storage.get_all_notes())
            args.id = Prompt.ask("[bold orange1]Введите ID заметки для редактирования[/bold orange1]")

        # Проверяем существование заметки сразу
        note = storage.get_note_by_id(args.id)  # Предполагаем, что такой метод существует в Storage; если нет, добавьте его
        if not note:
            console.print(f"[bold red]❌ Заметка с ID {args.id} не найдена.[/bold red]")
            sys.exit(1)

        new_title = args.title
        new_content = args.msg

        # Если пользователь не передал ни заголовка, ни текста флагами, спрашиваем, что менять
        if not new_title and not new_content:
            console.print("[dim]Оставьте пустым, чтобы сохранить текущее значение[/dim]")
            new_title = Prompt.ask("Новый заголовок", default=note.title)
            new_content = Prompt.ask("Новое содержание", default=note.content)

        success = storage.edit_note(args.id, new_title, new_content)
        if success:
            console.print(f"[bold green]✏️  Заметка обновлена![/bold green]")
        else:
            console.print(f"[bold red]❌ Заметка с ID {args.id} не найдена.[/bold red]")
            sys.exit(1)

    elif args.command == "delete":
        if not args.id:
            print_notes_table(storage.get_all_notes())
            args.id = Prompt.ask("[bold red]Введите ID заметки для удаления[/bold red]")

        # Проверяем существование заметки сразу
        note = storage.get_note_by_id(args.id)  # Предполагаем, что такой метод существует в Storage; если нет, добавьте его
        if not note:
            console.print(f"[bold red]❌ Заметка с ID {args.id} не найдена.[/bold red]")
            sys.exit(1)

        success = storage.delete_note(args.id)
        if success:
            console.print(f"[bold red]🗑️ Заметка удалена.[/bold red]")
        else:
            console.print(f"[bold red]❌ Заметка с ID {args.id} не найдена.[/bold red]")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()