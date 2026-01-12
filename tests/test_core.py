import unittest
import os
import json
from src.models import Note
from src.storage import Storage

class TestNoteModel(unittest.TestCase):
    def test_note_creation(self):
        """Проверяем, что заметка создается корректно."""
        note = Note("Test Title", "Test Content")
        self.assertEqual(note.title, "Test Title")
        self.assertEqual(note.content, "Test Content")
        self.assertIsNotNone(note.id)
        self.assertIsNotNone(note.created_at)

    def test_note_serialization(self):
        """Проверяем перевод в словарь и обратно."""
        note = Note("A", "B")
        data = note.to_dict()
        self.assertEqual(data["title"], "A")
        
        note_restored = Note.from_dict(data)
        self.assertEqual(note_restored.id, note.id)
        self.assertEqual(note_restored.title, "A")

class TestStorage(unittest.TestCase):
    def setUp(self):
        """Создаем временный файл для тестов перед каждым тестом."""
        self.test_file = "test_notes.json"
        self.storage = Storage(self.test_file)

    def tearDown(self):
        """Удаляем временный файл после каждого теста."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_and_get_note(self):
        """Проверяем добавление и чтение."""
        note = Note("Test", "Content")
        self.storage.add_note(note)
        
        notes = self.storage.get_all_notes()
        self.assertEqual(len(notes), 1)
        self.assertEqual(notes[0].title, "Test")

    def test_delete_note(self):
        """Проверяем удаление."""
        note = Note("To Delete", "...")
        self.storage.add_note(note)
        
        result = self.storage.delete_note(note.id)
        self.assertTrue(result)
        self.assertEqual(len(self.storage.get_all_notes()), 0)

    def test_filter_notes(self):
        """Проверяем поиск."""
        n1 = Note("Apple", "Green")
        n2 = Note("Banana", "Yellow")
        self.storage.add_note(n1)
        self.storage.add_note(n2)
        
        results = self.storage.filter_notes("apple")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Apple")

if __name__ == '__main__':
    unittest.main()