# Email Summarizer - Design Document

## Overview

The Email Summarizer is a modular system that connects to email accounts, retrieves emails, and generates AI-powered summaries. The architecture follows a layered approach with clear separation between email connectivity, data processing, AI summarization, and user interfaces. The system supports multiple email providers (IMAP, Gmail OAuth) and can be extended to support additional providers and AI models.

## Architecture

The system follows a modular, layered architecture:

```
┌─────────────────────────────────────────────────────────┐
│              User Interfaces Layer                       │
│         (CLI Interface | Web Interface)                  │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Application Layer                           │
│    (Orchestration, Configuration, State Management)      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌──────────────────┬──────────────────┬──────────────────┐
│  Email Provider  │   Summarization  │   Storage        │
│     Layer        │      Layer       │   Layer          │
│  (IMAP, Gmail)   │   (AI Models)    │  (JSON, Files)   │
└──────────────────┴──────────────────┴──────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Data Models Layer                           │
│        (Email, Summary, Configuration)                   │
└─────────────────────────────────────────────────────────┘
```

### Key Architectural Principles

1. **Separation of Concerns**: Email retrieval, summarization, and storage are independent modules
2. **Provider Abstraction**: Email providers and AI models are abstracted behind interfaces
3. **Stateless Operations**: Core operations don't maintain state between invocations
4. **Error Isolation**: Failures in one component don't cascade to others
5. **Interface Parity**: CLI and Web UI provide equivalent functionality

## Components and Interfaces

### 1. Data Models (`models.py`)

Core data structures representing emails, summaries, and configuration.

```python
@dataclass
class Email:
    id: str
    sender: str
    subject: str
    date: datetime
    body: str
    folder: str
    has_attachments: bool
    attachment_types: List[str]

@dataclass
class Summary:
    email_id: str
    summary_text: str
    key_points: List[str]
    action_items: List[str]
    timestamp: datetime
    model_used: str

@dataclass
class BatchSummary:
    email_ids: List[str]
    consolidated_summary: str
    common_themes: List[str]
    urgent_items: List[str]
    timestamp: datetime

@dataclass
class SummaryConfig:
    length: str  # "brief", "standard", "detailed"
    focus_areas: List[str]  # ["action_items", "decisions", "questions"]
    language: str
    model: str
```

### 2. Email Connector (`connector.py`)

Abstract interface for email providers with concrete implementations.

```python
class EmailConnector(ABC):
    @abstractmethod
    def connect(self, credentials: Dict) -> bool:
        """Establish connection to email provider"""
        pass
    
    @abstractmethod
    def fetch_emails(self, folder: str, date_range: Optional[Tuple[datetime, datetime]]) -> List[Email]:
        """Retrieve emails from specified folder and date range"""
        pass
    
    @abstractmethod
    def disconnect(self) -> None:
        """Close connection to email provider"""
        pass

class IMAPConnector(EmailConnector):
    """IMAP email provider implementation"""
    pass

class GmailConnector(EmailConnector):
    """Gmail OAuth provider implementation"""
    pass
```

### 3. Summarizer (`summarizer.py`)

AI-powered summarization engine with model abstraction.

```python
class Summarizer(ABC):
    @abstractmethod
    def summarize_email(self, email: Email, config: SummaryConfig) -> Summary:
        """Generate summary for a single email"""
        pass
    
    @abstractmethod
    def summarize_batch(self, emails: List[Email], config: SummaryConfig) -> BatchSummary:
        """Generate consolidated summary for multiple emails"""
        pass

class OpenAISummarizer(Summarizer):
    """OpenAI GPT-based summarization"""
    pass

class LocalModelSummarizer(Summarizer):
    """Local model-based summarization (future extension)"""
    pass
```

### 4. Storage Manager (`storage.py`)

Handles persistence of summaries and configuration.

```python
class StorageManager:
    def save_summary(self, summary: Summary) -> str:
        """Save individual summary and return file path"""
        pass
    
    def save_batch_summary(self, batch_summary: BatchSummary) -> str:
        """Save batch summary and return file path"""
        pass
    
    def load_summaries(self, filters: Optional[Dict]) -> List[Summary]:
        """Load saved summaries with optional filtering"""
        pass
    
    def export_summaries(self, summaries: List[Summary], format: str, output_path: str) -> None:
        """Export summaries to specified format (JSON, TXT, MD)"""
        pass
```

### 5. Application Orchestrator (`app.py`)

Coordinates operations between components.

```python
class EmailSummarizerApp:
    def __init__(self, connector: EmailConnector, summarizer: Summarizer, storage: StorageManager):
        self.connector = connector
        self.summarizer = summarizer
        self.storage = storage
        self.config = SummaryConfig()
    
    def connect_email(self, provider: str, credentials: Dict) -> bool:
        """Connect to email account"""
        pass
    
    def get_emails(self, folder: str, date_range: Optional[Tuple]) -> List[Email]:
        """Retrieve emails from account"""
        pass
    
    def generate_summaries(self, emails: List[Email]) -> List[Summary]:
        """Generate individual summaries for selected emails"""
        pass
    
    def generate_batch_summary(self, emails: List[Email]) -> BatchSummary:
        """Generate consolidated summary for email batch"""
        pass
    
    def save_and_export(self, summaries: List[Summary], export_format: str, path: str) -> None:
        """Save summaries and export to file"""
        pass
```

### 6. CLI Interface (`cli.py`)

Command-line interface for all operations.

```python
# Commands:
# - connect: Connect to email account
# - fetch: Retrieve emails
# - summarize: Generate summaries for selected emails
# - batch-summarize: Generate batch summary
# - export: Export summaries to file
# - config: Configure summarization preferences
```

### 7. Web Interface (`web_ui.py`)

Flask-based web application providing visual interface.

```python
# Routes:
# - /: Home page with connection form
# - /emails: Display fetched emails with selection
# - /summarize: Generate and display summaries
# - /batch: Generate batch summary
# - /saved: View saved summaries
# - /export: Export summaries
# - /config: Configuration page
```

## Data Models

### Email Data Flow

```
Email Provider → Email Object → Summarizer → Summary Object → Storage
```

### Storage Structure

```
summaries/
├── individual/
│   ├── summary_<email_id>_<timestamp>.json
│   └── ...
├── batch/
│   ├── batch_<timestamp>.json
│   └── ...
└── exports/
    ├── export_<timestamp>.json
    ├── export_<timestamp>.txt
    └── export_<timestamp>.md
```

### Configuration File

```json
{
  "email_provider": "imap",
  "credentials": {
    "encrypted": true,
    "data": "..."
  },
  "summarization": {
    "length": "standard",
    "focus_areas": ["action_items", "decisions"],
    "language": "en",
    "model": "gpt-4"
  }
}
```


## Correctness Properties

*A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.*

### Property 1: Valid credentials establish connection

*For any* valid IMAP or Gmail OAuth credentials, attempting to connect should result in a successful connection to the email server.
**Validates: Requirements 1.1, 1.2**

### Property 2: Invalid credentials are rejected

*For any* invalid or malformed credentials, the connection attempt should be rejected with a clear error message.
**Validates: Requirements 1.3**

### Property 3: Session persistence

*For any* established connection, subsequent operations should be able to use that connection without re-authenticating.
**Validates: Requirements 1.4**

### Property 4: Date range filtering

*For any* date range and collection of emails, fetching with that date range should return only emails with dates within the specified range.
**Validates: Requirements 2.3**

### Property 5: Folder filtering

*For any* folder name and collection of emails, fetching from that folder should return only emails belonging to that folder.
**Validates: Requirements 2.4**

### Property 6: Email metadata completeness

*For any* retrieved email, it should contain all required fields: sender, subject, date, body, folder, and attachment information.
**Validates: Requirements 2.2**

### Property 7: Selection tracking

*For any* set of emails, selecting multiple emails should result in all selected emails being tracked in the selection state.
**Validates: Requirements 3.2**

### Property 8: Selection and deselection are inverses

*For any* email, selecting it and then deselecting it should result in the email not being in the selected state.
**Validates: Requirements 3.3**

### Property 9: Select all completeness

*For any* displayed set of emails, the select-all operation should mark every email as selected.
**Validates: Requirements 3.4**

### Property 10: Clear selection empties selection

*For any* selection state, clearing the selection should result in zero emails being selected.
**Validates: Requirements 3.5**

### Property 11: Summary generation completeness

*For any* set of selected emails, generating summaries should produce exactly one summary per email.
**Validates: Requirements 4.1**

### Property 12: Summary structure completeness

*For any* generated summary, it should contain key_points, action_items, and main topics fields.
**Validates: Requirements 4.2**

### Property 13: Attachment information preservation

*For any* email with attachments, the generated summary should include information about the presence and types of attachments.
**Validates: Requirements 4.3**

### Property 14: Summary-email linkage

*For any* generated summary, it should contain the metadata (id, sender, subject, date) of the source email.
**Validates: Requirements 4.4**

### Property 15: Error isolation in batch processing

*For any* batch of emails where one fails summarization, all other emails should still be processed and produce summaries.
**Validates: Requirements 4.5**

### Property 16: Batch summary singularity

*For any* set of selected emails, generating a batch summary should produce exactly one consolidated summary object.
**Validates: Requirements 5.1**

### Property 17: Batch summary structure

*For any* generated batch summary, it should contain common_themes, urgent_items, and key action points fields.
**Validates: Requirements 5.2**

### Property 18: Batch summary email references

*For any* batch summary, it should contain references (email IDs) to all source emails that were summarized.
**Validates: Requirements 5.4**

### Property 19: Saved summary metadata

*For any* saved summary, the stored version should include a timestamp and all associated email metadata.
**Validates: Requirements 6.2**

### Property 20: Export format validity

*For any* requested export format (JSON, TXT, MD), the exported file should be valid and parseable in that format.
**Validates: Requirements 6.3**

### Property 21: Export completeness

*For any* exported summary, the file should contain both the original email metadata and the generated summary text.
**Validates: Requirements 6.4**

### Property 22: Saved summaries chronological ordering

*For any* collection of saved summaries, retrieving them should return them ordered by timestamp (newest first or oldest first consistently).
**Validates: Requirements 6.5**

### Property 23: Configuration affects summary length

*For any* length configuration (brief, standard, detailed), summaries generated with that configuration should reflect the relative length preference (brief < standard < detailed in character count).
**Validates: Requirements 7.1**

### Property 24: Configuration persistence

*For any* configuration change, all summaries generated after the change should use the new configuration settings.
**Validates: Requirements 7.4**

### Property 25: Component error isolation

*For any* component failure (connector, summarizer, storage), other components should continue to function independently.
**Validates: Requirements 8.4**

### Property 26: CLI output completeness

*For any* CLI operation, the output should include status information and results in a structured text format.
**Validates: Requirements 9.3**

### Property 27: Interface parity

*For any* operation performed through both CLI and Web UI with identical inputs, both interfaces should produce identical results.
**Validates: Requirements 9.5**

## Error Handling

### Connection Errors

- **Invalid Credentials**: Return clear error message indicating authentication failure
- **Network Timeout**: Retry with exponential backoff, fail after 3 attempts
- **Server Unavailable**: Return error with suggestion to check server status

### Email Retrieval Errors

- **Empty Folder**: Return empty list with informational message
- **Malformed Email**: Skip malformed email, log error, continue processing others
- **Permission Denied**: Return error indicating insufficient permissions for folder

### Summarization Errors

- **API Rate Limit**: Queue requests and retry with delay
- **Model Unavailable**: Return error with suggestion to check API key or model availability
- **Content Too Large**: Truncate content to model limits, add note in summary
- **Individual Email Failure**: Log error, continue with other emails, report failed email IDs

### Storage Errors

- **Disk Full**: Return error indicating insufficient storage space
- **Permission Denied**: Return error indicating write permission issues
- **Invalid Export Format**: Return error listing supported formats

### General Error Handling Principles

1. **Fail Gracefully**: Never crash the application; always return meaningful errors
2. **Error Isolation**: Errors in one email/operation don't affect others
3. **User Feedback**: All errors include actionable information for users
4. **Logging**: All errors are logged with context for debugging
5. **Recovery**: Where possible, provide automatic retry or recovery mechanisms

## Testing Strategy

### Unit Testing

The system will use **pytest** as the testing framework for Python.

Unit tests will cover:
- Individual component functionality (connector, summarizer, storage)
- Data model validation and serialization
- Configuration loading and validation
- Error handling for specific scenarios
- CLI command parsing and output formatting
- Web UI route handlers

### Property-Based Testing

The system will use **Hypothesis** for property-based testing in Python.

Property-based tests will:
- Run a minimum of 100 iterations per property
- Be tagged with comments referencing the design document property
- Use the format: `# Feature: email-summarizer, Property {number}: {property_text}`
- Generate random but valid test data (emails, credentials, configurations)
- Verify universal properties hold across all generated inputs

Each correctness property listed above will be implemented as a property-based test.

### Integration Testing

- Test complete workflows: connect → fetch → summarize → save → export
- Test interface parity between CLI and Web UI
- Test error recovery and isolation across components
- Test with real email providers (using test accounts)

### Test Data Generation

Property-based tests will use smart generators:
- **Email Generator**: Creates valid email objects with random but realistic data
- **Credential Generator**: Creates valid and invalid credential formats
- **Date Range Generator**: Creates valid date ranges for filtering
- **Configuration Generator**: Creates valid configuration combinations

### Testing Approach

1. **Implementation First**: Implement features before writing tests
2. **Property Tests for Core Logic**: Use property-based testing for business logic and data transformations
3. **Unit Tests for Edge Cases**: Use unit tests for specific scenarios and error conditions
4. **Integration Tests for Workflows**: Test complete user workflows end-to-end

## Security Considerations

### Credential Storage

- Credentials are encrypted at rest using `cryptography` library
- Encryption key is stored separately from credentials
- OAuth tokens are refreshed automatically before expiration

### API Key Management

- AI model API keys stored in environment variables
- Never logged or displayed in UI
- Validated before use

### Email Content Privacy

- Email content is not stored permanently unless user explicitly saves summaries
- Summaries can be configured to exclude sensitive information
- All network communication uses TLS/SSL

## Performance Considerations

### Batch Processing

- Emails processed in parallel where possible (thread pool)
- Batch size limited to prevent memory issues
- Progress indicators for long-running operations

### Caching

- Email metadata cached to reduce API calls
- Summaries cached to avoid regeneration
- Configuration cached in memory

### Rate Limiting

- Respect email provider rate limits
- Implement exponential backoff for API calls
- Queue requests when approaching limits

## Future Extensions

1. **Additional Email Providers**: Microsoft Exchange, Yahoo Mail
2. **Additional AI Models**: Anthropic Claude, local models (Llama)
3. **Advanced Filtering**: Search by sender, keywords, importance
4. **Summary Templates**: Customizable summary formats
5. **Scheduled Summarization**: Automatic daily/weekly summaries
6. **Email Actions**: Reply, forward, archive based on summaries
7. **Multi-language Support**: Automatic language detection and translation
8. **Mobile Interface**: Responsive web design or native mobile app
