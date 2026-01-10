import argparse
import sys
from src.storage import Storage
from src.models import Note


def main():
    parser = argparse.ArgumentParser(description="Notes CLI Service")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Command: add
    add_parser = subparsers.add_parser("add", help="Add a new note")
    add_parser.add_argument("--title", required=True, help="Title of the note")
    add_parser.add_argument("--msg", required=True, help="Content of the note")

    # Command: list
    subparsers.add_parser("list", help="List all notes")

    # Command: delete
    del_parser = subparsers.add_parser("delete", help="Delete a note by ID")
    del_parser.add_argument("--id", required=True, help="ID of the note to delete")

    args = parser.parse_args()
    storage = Storage()

    if args.command == "add":
        note = Note(title=args.title, content=args.msg)
        storage.add_note(note)
        print(f"✅ Note added successfully! ID: {note.id}")

    elif args.command == "list":
        notes = storage.get_all_notes()
        if not notes:
            print("📭 No notes found.")
        else:
            print(f"Found {len(notes)} notes:\n")
            for note in notes:
                print(f"ID: {note.id} | {note.created_at[:19]}")
                print(f"Title: {note.title}")
                print(f"Content: {note.content}")
                print("-" * 40)

    elif args.command == "delete":
        success = storage.delete_note(args.id)
        if success:
            print(f"🗑️ Note {args.id} deleted.")
        else:
            print(f"❌ Note with ID {args.id} not found.")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()