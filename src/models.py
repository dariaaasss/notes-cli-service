import uuid
from datetime import datetime


class Note:
    def __init__(self, title: str, content: str, note_id: str = None, created_at: str = None):
        self.id = note_id or str(uuid.uuid4())
        self.title = title
        self.content = content
        self.created_at = created_at or datetime.now().isoformat()

    def to_dict(self):
        """Convert note to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Create Note object from dictionary."""
        return cls(
            title=data["title"],
            content=data["content"],
            note_id=data["id"],
            created_at=data["created_at"]
        )