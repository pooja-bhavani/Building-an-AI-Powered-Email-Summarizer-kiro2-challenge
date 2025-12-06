"""Storage manager for summaries."""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from src.models import Summary, BatchSummary


class StorageManager:
    """Manages persistence of summaries and batch summaries."""
    
    def __init__(self, base_dir: str = "summaries"):
        """
        Initialize storage manager.
        
        Args:
            base_dir: Base directory for storing summaries
        """
        self.base_dir = Path(base_dir)
        self.individual_dir = self.base_dir / "individual"
        self.batch_dir = self.base_dir / "batch"
        self.exports_dir = self.base_dir / "exports"
        
        # Create directories
        self.individual_dir.mkdir(parents=True, exist_ok=True)
        self.batch_dir.mkdir(parents=True, exist_ok=True)
        self.exports_dir.mkdir(parents=True, exist_ok=True)
    
    def save_summary(self, summary: Summary) -> str:
        """
        Save individual summary to disk.
        
        Args:
            summary: Summary object to save
            
        Returns:
            Path to saved file
        """
        timestamp_str = summary.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"summary_{summary.email_id}_{timestamp_str}.json"
        filepath = self.individual_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(summary.to_dict(), f, indent=2)
        
        return str(filepath)
    
    def save_batch_summary(self, batch_summary: BatchSummary) -> str:
        """
        Save batch summary to disk.
        
        Args:
            batch_summary: BatchSummary object to save
            
        Returns:
            Path to saved file
        """
        timestamp_str = batch_summary.timestamp.strftime("%Y%m%d_%H%M%S")
        filename = f"batch_{timestamp_str}.json"
        filepath = self.batch_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(batch_summary.to_dict(), f, indent=2)
        
        return str(filepath)
    
    def load_summaries(self, filters: Optional[Dict] = None) -> List[Summary]:
        """
        Load saved summaries with optional filtering.
        
        Args:
            filters: Optional dict with 'email_id', 'start_date', 'end_date'
            
        Returns:
            List of Summary objects
        """
        summaries = []
        
        for filepath in self.individual_dir.glob("summary_*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    summary = Summary.from_dict(data)
                    
                    # Apply filters
                    if filters:
                        if 'email_id' in filters and summary.email_id != filters['email_id']:
                            continue
                        if 'start_date' in filters and summary.timestamp < filters['start_date']:
                            continue
                        if 'end_date' in filters and summary.timestamp > filters['end_date']:
                            continue
                    
                    summaries.append(summary)
            except Exception as e:
                print(f"Warning: Failed to load {filepath}: {str(e)}")
                continue
        
        # Sort by timestamp (newest first)
        summaries.sort(key=lambda s: s.timestamp, reverse=True)
        
        return summaries
    
    def load_batch_summaries(self) -> List[BatchSummary]:
        """
        Load all batch summaries.
        
        Returns:
            List of BatchSummary objects
        """
        batch_summaries = []
        
        for filepath in self.batch_dir.glob("batch_*.json"):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    batch_summary = BatchSummary.from_dict(data)
                    batch_summaries.append(batch_summary)
            except Exception as e:
                print(f"Warning: Failed to load {filepath}: {str(e)}")
                continue
        
        # Sort by timestamp (newest first)
        batch_summaries.sort(key=lambda bs: bs.timestamp, reverse=True)
        
        return batch_summaries
    
    def export_summaries(
        self,
        summaries: List[Summary],
        format: str,
        output_path: str
    ) -> None:
        """
        Export summaries to specified format.
        
        Args:
            summaries: List of summaries to export
            format: Export format ('json', 'txt', 'md')
            output_path: Output file path
        """
        if format == 'json':
            self._export_json(summaries, output_path)
        elif format == 'txt':
            self._export_txt(summaries, output_path)
        elif format == 'md':
            self._export_markdown(summaries, output_path)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, summaries: List[Summary], output_path: str) -> None:
        """Export summaries as JSON."""
        data = [s.to_dict() for s in summaries]
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def _export_txt(self, summaries: List[Summary], output_path: str) -> None:
        """Export summaries as plain text."""
        with open(output_path, 'w') as f:
            for i, summary in enumerate(summaries, 1):
                f.write(f"{'='*80}\n")
                f.write(f"Summary {i}\n")
                f.write(f"{'='*80}\n")
                f.write(f"Email ID: {summary.email_id}\n")
                f.write(f"Timestamp: {summary.timestamp}\n")
                f.write(f"Model: {summary.model_used}\n\n")
                f.write(f"Summary:\n{summary.summary_text}\n\n")
                
                if summary.key_points:
                    f.write("Key Points:\n")
                    for point in summary.key_points:
                        f.write(f"  - {point}\n")
                    f.write("\n")
                
                if summary.action_items:
                    f.write("Action Items:\n")
                    for item in summary.action_items:
                        f.write(f"  - {item}\n")
                    f.write("\n")
                
                f.write("\n")
    
    def _export_markdown(self, summaries: List[Summary], output_path: str) -> None:
        """Export summaries as Markdown."""
        with open(output_path, 'w') as f:
            f.write("# Email Summaries\n\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write("---\n\n")
            
            for i, summary in enumerate(summaries, 1):
                f.write(f"## Summary {i}\n\n")
                f.write(f"**Email ID:** {summary.email_id}  \n")
                f.write(f"**Timestamp:** {summary.timestamp}  \n")
                f.write(f"**Model:** {summary.model_used}\n\n")
                f.write(f"### Summary\n\n{summary.summary_text}\n\n")
                
                if summary.key_points:
                    f.write("### Key Points\n\n")
                    for point in summary.key_points:
                        f.write(f"- {point}\n")
                    f.write("\n")
                
                if summary.action_items:
                    f.write("### Action Items\n\n")
                    for item in summary.action_items:
                        f.write(f"- {item}\n")
                    f.write("\n")
                
                f.write("---\n\n")
