"""Summary data models."""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Dict, Any


@dataclass
class Summary:
    """Represents a summary of a single email."""
    
    email_id: str
    summary_text: str
    key_points: List[str]
    action_items: List[str]
    timestamp: datetime
    model_used: str
    
    def validate(self) -> bool:
        """Validate that all required fields are present and valid."""
        if not self.email_id or not isinstance(self.email_id, str):
            return False
        if not self.summary_text or not isinstance(self.summary_text, str):
            return False
        if not isinstance(self.key_points, list):
            return False
        if not isinstance(self.action_items, list):
            return False
        if not isinstance(self.timestamp, datetime):
            return False
        if not self.model_used or not isinstance(self.model_used, str):
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert summary to dictionary."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Summary':
        """Create summary from dictionary."""
        data = data.copy()
        if isinstance(data.get('timestamp'), str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)


@dataclass
class BatchSummary:
    """Represents a consolidated summary of multiple emails."""
    
    email_ids: List[str]
    consolidated_summary: str
    common_themes: List[str]
    urgent_items: List[str]
    timestamp: datetime
    
    def validate(self) -> bool:
        """Validate that all required fields are present and valid."""
        if not isinstance(self.email_ids, list) or len(self.email_ids) == 0:
            return False
        if not self.consolidated_summary or not isinstance(self.consolidated_summary, str):
            return False
        if not isinstance(self.common_themes, list):
            return False
        if not isinstance(self.urgent_items, list):
            return False
        if not isinstance(self.timestamp, datetime):
            return False
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert batch summary to dictionary."""
        data = asdict(self)
        data['timestamp'] = self.timestamp.isoformat()
        return data
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'BatchSummary':
        """Create batch summary from dictionary."""
        data = data.copy()
        if isinstance(data.get('timestamp'), str):
            data['timestamp'] = datetime.fromisoformat(data['timestamp'])
        return cls(**data)
