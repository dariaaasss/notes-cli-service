import argparse
import sys
import questionary
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from src.storage import Storage
from src.models import Note

console = Console()

def print_notes_table(notes):
    """Выводит таблицу заметок."""
    if not notes:
        console.print("[yellow]📭 Заметок пока нет.[/yellow]")
        return

    table = Table(title=f"Мои Заметки ({len(notes)})", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Дата", style="magenta")
    table.add_column("Заголовок", style="green")
    table.add_column("Содержание")

    for note in notes:

        table.add_row(note.id[:8], note.created_at[:10], note.title, note.content)
    
    console.print(table)

def select_note_interactive(notes):
    """Показывает интерактивное меню для выбора заметки."""
    if not notes:
        return None
    
    choices = []
    for note in notes:
        display_text = f"{note.title} | {note.content[:20]}..."
        choices.append(questionary.Choice(title=display_text, value=note.id))
    
    selected_id = questionary.select(
        "Выберите заметку:",
        choices=choices
    ).ask()
    
    return selected_id

def main():
    parser = argparse.ArgumentParser(description="CLI Сервис Заметок")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # --- ADD ---
    add_parser = subparsers.add_parser("add", help="Создать заметку")
    add_parser.add_argument("--title", help="Заголовок")
    add_parser.add_argument("--msg", help="Текст заметки")

    # --- LIST ---
    list_parser = subparsers.add_parser("list", help="Список заметок")
    list_parser.add_argument("--query", "-q", help="Поиск по тексту")

    # --- EDIT ---
    edit_parser = subparsers.add_parser("edit", help="Редактировать заметку")
    edit_parser.add_argument("--id", help="ID заметки (необязательно в интерактивном режиме)")
    edit_parser.add_argument("--title", help="Новый заголовок")
    edit_parser.add_argument("--msg", help="Новый текст")

    # --- DELETE ---
    del_parser = subparsers.add_parser("delete", help="Удалить заметку")
    del_parser.add_argument("--id", help="ID заметки (необязательно в интерактивном режиме)")

    args = parser.parse_args()
    storage = Storage()



    if args.command == "add":
        # Если аргументы не переданы, спрашиваем интерактивно
        title = args.title or Prompt.ask("[bold green]Введите заголовок[/bold green]")
        content = args.msg or Prompt.ask("[bold green]Введите содержание[/bold green]")
        
        note = Note(title=title, content=content)
        storage.add_note(note)
        console.print(f"[bold blue]✅ Заметка сохранена![/bold blue] (ID: {note.id[:8]})")

    elif args.command == "list":
        if args.query:
            notes = storage.filter_notes(args.query)
            console.print(f"[bold blue]🔍 Результаты поиска по запросу '{args.query}':[/bold blue]")
        else:
            notes = storage.get_all_notes()
        
        print_notes_table(notes)

    elif args.command == "edit":
        # Если ID нет, даем выбрать из списка
        if not args.id:
            notes = storage.get_all_notes()
            if not notes:
                console.print("[yellow]📭 Нет заметок для редактирования.[/yellow]")
                sys.exit(0)
            
            args.id = select_note_interactive(notes)
            if not args.id: # Если пользователь отменил выбор
                return

        note = storage.get_note_by_id(args.id)
        if not note:
            console.print(f"[bold red]❌ Заметка с ID {args.id} не найдена.[/bold red]")
            sys.exit(1)

        new_title = args.title
        new_content = args.msg

        # Если данные для обновления не переданы, спрашиваем, подставляя старые значения
        if not new_title and not new_content:
            console.print(f"[dim]Редактирование: {note.title}[/dim]")
            new_title = Prompt.ask("Заголовок", default=note.title)
            new_content = Prompt.ask("Содержание", default=note.content)

        success = storage.edit_note(args.id, new_title, new_content)
        if success:
            console.print(f"[bold green]✏️  Заметка обновлена![/bold green]")

    elif args.command == "delete":
        # Если ID нет, даем выбрать
        if not args.id:
            notes = storage.get_all_notes()
            if not notes:
                console.print("[yellow]📭 Нет заметок для удаления.[/yellow]")
                sys.exit(0)

            args.id = select_note_interactive(notes)
            if not args.id:
                return

        # Подтверждение удаления
        if questionary.confirm(f"Вы уверены, что хотите удалить заметку {args.id[:8]}?").ask():
            success = storage.delete_note(args.id)
            if success:
                console.print(f"[bold red]🗑️  Заметка удалена.[/bold red]")
            else:
                console.print(f"[bold red]❌ Ошибка: заметка не найдена.[/bold red]")
        else:
            console.print("[dim]Удаление отменено.[/dim]")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()