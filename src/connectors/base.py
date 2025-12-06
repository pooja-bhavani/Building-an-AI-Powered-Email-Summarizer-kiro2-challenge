"""Abstract base class for email connectors."""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from src.models import Email


class EmailConnector(ABC):
    """Abstract base class for email provider connectors."""
    
    def __init__(self):
        """Initialize the connector."""
        self.connected = False
        self.session = None
    
    @abstractmethod
    def connect(self, credentials: Dict) -> bool:
        """
        Establish connection to email provider.
        
        Args:
            credentials: Dictionary containing authentication credentials
            
        Returns:
            True if connection successful, False otherwise
            
        Raises:
            ConnectionError: If connection fails
            ValueError: If credentials are invalid
        """
        pass
    
    @abstractmethod
    def fetch_emails(
        self,
        folder: str = "INBOX",
        date_range: Optional[Tuple[datetime, datetime]] = None,
        limit: Optional[int] = None
    ) -> List[Email]:
        """
        Retrieve emails from specified folder and date range.
        
        Args:
            folder: Folder name to fetch from (default: INBOX)
            date_range: Optional tuple of (start_date, end_date)
            limit: Optional maximum number of emails to fetch
            
        Returns:
            List of Email objects
            
        Raises:
            ConnectionError: If not connected
            ValueError: If folder doesn't exist
        """
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """
        Close connection to email provider.
        
        Raises:
            ConnectionError: If disconnection fails
        """
        pass
    
    def is_connected(self) -> bool:
        """Check if connector is currently connected."""
        return self.connected
