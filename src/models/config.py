"""Configuration data models."""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any


@dataclass
class SummaryConfig:
    """Configuration for email summarization."""
    
    length: str = "standard"  # "brief", "standard", "detailed"
    focus_areas: List[str] = field(default_factory=lambda: ["action_items", "decisions"])
    language: str = "en"
    model: str = "gpt-4"
    
    def validate(self) -> bool:
        """Validate configuration values."""
        valid_lengths = ["brief", "standard", "detailed"]
        if self.length not in valid_lengths:
            return False
        
        valid_focus_areas = ["action_items", "decisions", "questions", "deadlines", "people"]
        if not isinstance(self.focus_areas, list):
            return False
        for area in self.focus_areas:
            if area not in valid_focus_areas:
                return False
        
        if not self.language or not isinstance(self.language, str):
            return False
        
        if not self.model or not isinstance(self.model, str):
            return False
        
        return True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SummaryConfig':
        """Create config from dictionary."""
        return cls(**data)
    
    @classmethod
    def default(cls) -> 'SummaryConfig':
        """Return default configuration."""
        return cls(
            length="standard",
            focus_areas=["action_items", "decisions"],
            language="en",
            model="gpt-4"
        )
