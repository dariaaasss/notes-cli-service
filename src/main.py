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

    # Command: edit
    edit_parser = subparsers.add_parser("edit", help="Edit a note")
    edit_parser.add_argument("--id", required=True, help="ID of the note to edit")
    edit_parser.add_argument("--title", help="New title")
    edit_parser.add_argument("--msg", help="New content")

    # Command: list
    list_parser = subparsers.add_parser("list", help="List all notes")
    list_parser.add_argument("--query", "-q", help="Filter notes by keyword")

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
        if args.query:
            notes = storage.filter_notes(args.query)
            print(f"🔍 Search results for '{args.query}':")
        else:
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

    elif args.command == "edit":
        if not args.title and not args.msg:
            print("⚠️  You must provide either --title or --msg to update.")
            sys.exit(1)

        success = storage.edit_note(args.id, args.title, args.msg)
        if success:
            print(f"✏️  Note {args.id} updated successfully.")
        else:
            print(f"❌ Note with ID {args.id} not found.")
            sys.exit(1)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()