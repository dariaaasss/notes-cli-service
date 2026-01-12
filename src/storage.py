import json
import os
from typing import List, Optional
from src.models import Note


class Storage:
    def __init__(self, filename: str = "notes.json"):
        self.filename = filename
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def get_all_notes(self) -> List[Note]:
        with open(self.filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return [Note.from_dict(item) for item in data]

    def add_note(self, note: Note):
        notes = self.get_all_notes()
        notes.append(note)
        self._save_notes(notes)

    def delete_note(self, note_id: str) -> bool:
        notes = self.get_all_notes()
        initial_count = len(notes)
        notes = [n for n in notes if n.id != note_id]

        if len(notes) < initial_count:
            self._save_notes(notes)
            return True
        return False

    def edit_note(self, note_id: str, title: str = None, content: str = None) -> bool:
        notes = self.get_all_notes()
        updated = False

        for note in notes:
            if note.id == note_id:
                if title:
                    note.title = title
                if content:
                    note.content = content
                updated = True
                break

        if updated:
            self._save_notes(notes)
            return True
        return False

    def filter_notes(self, query: str) -> List[Note]:
        notes = self.get_all_notes()
        query = query.lower()
        return [
            note for note in notes
            if query in note.title.lower() or query in note.content.lower()
        ]

    def _save_notes(self, notes: List[Note]):
        data = [n.to_dict() for n in notes]
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def get_note_by_id(self, note_id: str) -> Optional[Note]:
        """Find a note by ID and return it, or None."""
        notes = self.get_all_notes()
        for note in notes:
            if note.id == note_id:
                return note
        return None