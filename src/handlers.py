import sys
import questionary
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from rich import box
from src.storage import Storage
from src.models import Note

console = Console()
storage = Storage()

def print_notes_table(notes):
    """Выводит таблицу заметок."""
    if not notes:
        console.print("[yellow]📭 Заметок пока нет.[/yellow]")
        return

    table = Table(title=f"Мои Заметки ({len(notes)})", box=box.ROUNDED)
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Дата", style="magenta")
    table.add_column("Заголовок", style="bold green") 
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
        preview = (note.content[:30] + '...') if len(note.content) > 30 else note.content
        display_text = f"{note.title} | {preview}"
        choices.append(questionary.Choice(title=display_text, value=note.id))
    
    selected_id = questionary.select(
        "Выберите заметку:",
        choices=choices
    ).ask()
    
    return selected_id

def handle_add(title=None, msg=None):
    title = title or Prompt.ask("[bold green]Введите заголовок[/bold green]")
    content = msg or Prompt.ask("[bold green]Введите содержание[/bold green]")
    
    note = Note(title=title, content=content)
    storage.add_note(note)
    console.print(f"[bold blue]✅ Заметка сохранена![/bold blue] (ID: {note.id[:8]})")

def handle_list(query=None):
    if query:
        notes = storage.filter_notes(query)
        console.print(f"[bold blue]🔍 Результаты поиска по запросу '{query}':[/bold blue]")
    else:
        notes = storage.get_all_notes()
    
    print_notes_table(notes)

def handle_edit(note_id=None, title=None, msg=None):
    if not note_id:
        notes = storage.get_all_notes()
        if not notes:
            console.print("[yellow]📭 Нет заметок для редактирования.[/yellow]")
            return
        
        note_id = select_note_interactive(notes)
        if not note_id:
            return

    note = storage.get_note_by_id(note_id)
    if not note:
        console.print(f"[bold red]❌ Заметка с ID {note_id} не найдена.[/bold red]")
        return

    if not title and not msg:
        console.print(f"[dim]Редактирование: {note.title}[/dim]")
        title = Prompt.ask("Заголовок", default=note.title)
        msg = Prompt.ask("Содержание", default=note.content)

    success = storage.edit_note(note_id, title, msg)
    if success:
        console.print(f"[bold green]✏️  Заметка обновлена![/bold green]")

def handle_delete(note_id=None):
    if not note_id:
        notes = storage.get_all_notes()
        if not notes:
            console.print("[yellow]📭 Нет заметок для удаления.[/yellow]")
            return

        note_id = select_note_interactive(notes)
        if not note_id:
            return

    if questionary.confirm(f"Вы уверены, что хотите удалить заметку {note_id[:8]}?").ask():
        success = storage.delete_note(note_id)
        if success:
            console.print(f"[bold red]🗑️  Заметка удалена.[/bold red]")
        else:
            console.print(f"[bold red]❌ Ошибка: заметка не найдена.[/bold red]")
    else:
        console.print("[dim]Удаление отменено.[/dim]")