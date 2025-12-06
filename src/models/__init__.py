"""Data models for the email summarizer."""

from src.models.email import Email
from src.models.summary import Summary, BatchSummary
from src.models.config import SummaryConfig

__all__ = ['Email', 'Summary', 'BatchSummary', 'SummaryConfig']
