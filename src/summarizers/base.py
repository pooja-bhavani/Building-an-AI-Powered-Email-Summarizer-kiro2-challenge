"""Abstract base class for summarizers."""

from abc import ABC, abstractmethod
from typing import List
from src.models import Email, Summary, BatchSummary, SummaryConfig


class Summarizer(ABC):
    """Abstract base class for AI summarization engines."""
    
    def __init__(self):
        """Initialize the summarizer."""
        self.model_name = "unknown"
    
    @abstractmethod
    def summarize_email(self, email: Email, config: SummaryConfig) -> Summary:
        """
        Generate summary for a single email.
        
        Args:
            email: Email object to summarize
            config: Configuration for summarization
            
        Returns:
            Summary object
            
        Raises:
            Exception: If summarization fails
        """
        pass
    
    @abstractmethod
    def summarize_batch(self, emails: List[Email], config: SummaryConfig) -> BatchSummary:
        """
        Generate consolidated summary for multiple emails.
        
        Args:
            emails: List of Email objects to summarize
            config: Configuration for summarization
            
        Returns:
            BatchSummary object
            
        Raises:
            Exception: If summarization fails
        """
        pass
