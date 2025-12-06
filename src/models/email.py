"""Email data models."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class Email:
    """Represents an email message."""
    
    id: str
    sender: str
    subject: str
    date: datetime
    body: str
    folder: str
    has_attachments: bool
    attachment_types: List[str] = field(default_factory=list)
    
    def validate(self) -> bool:
        """Validate that all required fields are present and valid."""
        if not self.id or not isinstance(self.id, str):
            return False
        if not self.sender or not isinstance(self.sender, str):
            return False
        if not self.subject or not isinstance(self.subject, str):
            return False
        if not isinstance(self.date, datetime):
            return False
        if not self.body or not isinstance(self.body, str):
            return False
        if not self.folder or not isinstance(self.folder, str):
            return False
        if not isinstance(self.has_attachments, bool):
            return False
        if not isinstance(self.attachment_types, list):
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert email to dictionary."""
        data = asdict(self)
        data['date'] = self.date.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Email':
        """Create email from dictionary."""
        data = data.copy()
        if isinstance(data.get('date'), str):
            data['date'] = datetime.fromisoformat(data['date'])
        return cls(**data)
