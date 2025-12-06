"""Property-based tests for data models."""

from datetime import datetime, timedelta
from hypothesis import given, strategies as st
from src.models import Email, Summary, BatchSummary


# Generators for Email
@st.composite
def email_generator(draw):
    """Generate valid Email objects."""
    return Email(
        id=draw(st.text(min_size=1, max_size=50)),
        sender=draw(st.emails()),
        subject=draw(st.text(min_size=1, max_size=200)),
        date=draw(st.datetimes(
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2025, 12, 31)
        )),
        body=draw(st.text(min_size=1, max_size=5000)),
        folder=draw(st.sampled_from(['INBOX', 'Sent', 'Drafts', 'Archive'])),
        has_attachments=draw(st.booleans()),
        attachment_types=draw(st.lists(
            st.sampled_from(['pdf', 'jpg', 'png', 'doc', 'xlsx']),
            max_size=5
        ))
    )


# Feature: email-summarizer, Property 6: Email metadata completeness
@given(email_generator())
def test_email_metadata_completeness(email):
    """
    For any retrieved email, it should contain all required fields:
    sender, subject, date, body, folder, and attachment information.
    
    **Validates: Requirements 2.2**
    """
    # Verify all required fields are present and not None
    assert email.id is not None
    assert email.sender is not None
    assert email.subject is not None
    assert email.date is not None
    assert email.body is not None
    assert email.folder is not None
    assert email.has_attachments is not None
    assert email.attachment_types is not None
    
    # Verify types are correct
    assert isinstance(email.id, str)
    assert isinstance(email.sender, str)
    assert isinstance(email.subject, str)
    assert isinstance(email.date, datetime)
    assert isinstance(email.body, str)
    assert isinstance(email.folder, str)
    assert isinstance(email.has_attachments, bool)
    assert isinstance(email.attachment_types, list)
    
    # Verify validation passes
    assert email.validate() is True


# Generators for Summary
@st.composite
def summary_generator(draw):
    """Generate valid Summary objects."""
    return Summary(
        email_id=draw(st.text(min_size=1, max_size=50)),
        summary_text=draw(st.text(min_size=10, max_size=1000)),
        key_points=draw(st.lists(st.text(min_size=1, max_size=200), min_size=1, max_size=10)),
        action_items=draw(st.lists(st.text(min_size=1, max_size=200), max_size=10)),
        timestamp=draw(st.datetimes(
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2025, 12, 31)
        )),
        model_used=draw(st.sampled_from(['gpt-4', 'gpt-3.5-turbo', 'claude-3']))
    )


# Feature: email-summarizer, Property 12: Summary structure completeness
@given(summary_generator())
def test_summary_structure_completeness(summary):
    """
    For any generated summary, it should contain key_points, action_items,
    and main topics fields.
    
    **Validates: Requirements 4.2**
    """
    # Verify all required fields are present
    assert summary.email_id is not None
    assert summary.summary_text is not None
    assert summary.key_points is not None
    assert summary.action_items is not None
    assert summary.timestamp is not None
    assert summary.model_used is not None
    
    # Verify types are correct
    assert isinstance(summary.email_id, str)
    assert isinstance(summary.summary_text, str)
    assert isinstance(summary.key_points, list)
    assert isinstance(summary.action_items, list)
    assert isinstance(summary.timestamp, datetime)
    assert isinstance(summary.model_used, str)
    
    # Verify validation passes
    assert summary.validate() is True


# Generators for BatchSummary
@st.composite
def batch_summary_generator(draw):
    """Generate valid BatchSummary objects."""
    return BatchSummary(
        email_ids=draw(st.lists(st.text(min_size=1, max_size=50), min_size=1, max_size=20)),
        consolidated_summary=draw(st.text(min_size=10, max_size=2000)),
        common_themes=draw(st.lists(st.text(min_size=1, max_size=200), max_size=10)),
        urgent_items=draw(st.lists(st.text(min_size=1, max_size=200), max_size=10)),
        timestamp=draw(st.datetimes(
            min_value=datetime(2020, 1, 1),
            max_value=datetime(2025, 12, 31)
        ))
    )


# Feature: email-summarizer, Property 17: Batch summary structure
@given(batch_summary_generator())
def test_batch_summary_structure(batch_summary):
    """
    For any generated batch summary, it should contain common_themes,
    urgent_items, and key action points fields.
    
    **Validates: Requirements 5.2**
    """
    # Verify all required fields are present
    assert batch_summary.email_ids is not None
    assert batch_summary.consolidated_summary is not None
    assert batch_summary.common_themes is not None
    assert batch_summary.urgent_items is not None
    assert batch_summary.timestamp is not None
    
    # Verify types are correct
    assert isinstance(batch_summary.email_ids, list)
    assert len(batch_summary.email_ids) > 0
    assert isinstance(batch_summary.consolidated_summary, str)
    assert isinstance(batch_summary.common_themes, list)
    assert isinstance(batch_summary.urgent_items, list)
    assert isinstance(batch_summary.timestamp, datetime)
    
    # Verify validation passes
    assert batch_summary.validate() is True
