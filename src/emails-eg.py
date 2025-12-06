"""Demo mode with mock data for showcasing the application."""

from datetime import datetime, timedelta
from typing import List
from src.models import Email, Summary, SummaryConfig
import random

def generate_demo_emails(count: int = 20) -> List[Email]:
    """Generate realistic demo emails."""
    
    senders = [
        "boss@company.com",
        "client@example.com", 
        "hr@company.com",
        "team.lead@company.com",
        "support@vendor.com",
        "marketing@company.com",
        "finance@company.com",
        "john.doe@partner.com",
        "sarah.smith@client.com",
        "tech.support@service.com"
    ]
    
    subjects = [
        "Q4 Project Review Meeting",
        "Urgent: Contract Renewal Needed",
        "New Employee Onboarding Schedule",
        "Budget Approval Request",
        "Weekly Team Sync - Action Items",
        "Client Feedback on Latest Release",
        "Server Maintenance Window",
        "Training Session Next Week",
        "Invoice #12345 - Payment Due",
        "Product Launch Timeline",
        "Security Update Required",
        "Performance Review Schedule",
        "Holiday Schedule Announcement",
        "New Feature Request from Client",
        "Bug Report - Priority High",
        "Team Building Event",
        "Quarterly Goals Review",
        "Vendor Contract Expiring",
        "System Upgrade Notification",
        "Meeting Notes - Action Required"
    ]
    
    bodies = [
        "Hi team, we need to schedule our Q4 project review. Please prepare your quarterly reports and presentation slides. The meeting will be on Friday at 2 PM. Budget approval is still pending from finance. Let me know if you have any questions.",
        
        "Hello, our current contract expires next week. We need to discuss renewal terms and pricing. Can we schedule a call this week? This is time-sensitive and requires immediate attention from the legal team.",
        
        "Welcome our new team members! Please help them get set up with accounts and introduce them to the team. Onboarding schedule is attached. First day orientation starts at 9 AM on Monday.",
        
        "The budget request for Q1 has been submitted. We're waiting for approval from the finance department. Expected timeline is 2-3 business days. Please hold off on any major purchases until we get confirmation.",
        
        "Following up on our weekly sync. Key action items: 1) Complete code review by Wednesday, 2) Update documentation, 3) Schedule client demo for next week. Please confirm you can meet these deadlines.",
        
        "Client has provided feedback on the latest release. Overall positive, but they've requested some UI improvements and bug fixes. Priority items are listed in the attached document. Let's discuss in tomorrow's standup.",
        
        "Scheduled maintenance window this Saturday from 2 AM to 6 AM. All services will be temporarily unavailable. Please plan accordingly and notify your teams. Emergency contact information is included below.",
        
        "Reminder: Training session on the new CRM system next Tuesday at 10 AM. Attendance is mandatory for all sales team members. Materials will be shared beforehand. Please come prepared with questions.",
        
        "Invoice #12345 for $5,000 is due by end of month. Please process payment at your earliest convenience. Contact accounting if you have any questions about the charges or need additional documentation.",
        
        "Product launch timeline has been finalized. Marketing campaign starts in 2 weeks. All teams need to be ready with their deliverables. Final review meeting scheduled for next Friday at 3 PM.",
        
        "Critical security update available for our infrastructure. Please apply patches during the next maintenance window. This addresses several high-priority vulnerabilities. IT team will coordinate the rollout.",
        
        "Performance review cycle begins next month. Please start preparing your self-assessments and gathering feedback from peers. HR will send detailed instructions and templates by end of week.",
        
        "Holiday schedule for December has been finalized. Office will be closed from Dec 24-26 and Jan 1. Please plan your work accordingly and set up out-of-office messages. Emergency contacts will be provided.",
        
        "Client has requested a new feature for the dashboard. They need real-time analytics and custom reporting capabilities. This is a high-priority request that could lead to contract expansion. Let's discuss feasibility.",
        
        "High priority bug reported in production. Users are experiencing login issues. Engineering team is investigating. ETA for fix is 2-3 hours. Will provide updates every 30 minutes until resolved.",
        
        "Team building event scheduled for next month! We're planning an outdoor activity day followed by dinner. Please RSVP by end of week so we can finalize headcount and arrangements.",
        
        "Time to review our quarterly goals. Please prepare a summary of your progress and any blockers you're facing. We'll discuss in our 1-on-1 meetings next week. Be ready to set goals for next quarter.",
        
        "Vendor contract for cloud services expires in 30 days. We need to decide whether to renew or switch providers. Cost comparison and feature analysis attached. Let's schedule a meeting to discuss options.",
        
        "System upgrade scheduled for next weekend. This will include new features and performance improvements. Downtime expected to be minimal. Detailed release notes will be shared on Friday.",
        
        "Meeting notes from yesterday's session. Key decisions made and action items assigned. Please review and confirm your tasks. Next meeting scheduled for same time next week. Let me know if you have conflicts."
    ]
    
    emails = []
    base_date = datetime.now()
    
    for i in range(min(count, len(subjects))):
        email_date = base_date - timedelta(days=random.randint(0, 7), hours=random.randint(0, 23))
        has_attachments = random.choice([True, False, False])  # 33% chance
        
        attachment_types = []
        if has_attachments:
            possible_types = ['pdf', 'xlsx', 'docx', 'pptx', 'jpg', 'png']
            attachment_types = random.sample(possible_types, random.randint(1, 3))
        
        email = Email(
            id=f"demo_{i+1}",
            sender=random.choice(senders),
            subject=subjects[i],
            date=email_date,
            body=bodies[i],
            folder="INBOX",
            has_attachments=has_attachments,
            attachment_types=attachment_types
        )
        emails.append(email)
    
    # Sort by date (newest first)
    emails.sort(key=lambda e: e.date, reverse=True)
    
    return emails


def generate_demo_summary(email: Email) -> Summary:
    """Generate a realistic demo summary for an email."""
    
    # Extract first 2-3 sentences as summary
    sentences = email.body.split('. ')
    summary_text = '. '.join(sentences[:3]).strip()
    if not summary_text.endswith('.'):
        summary_text += '.'
    
    # Generate contextual key points based on email content
    key_points = []
    body_lower = email.body.lower()
    subject_lower = email.subject.lower()
    
    # Extract specific details from the email
    if 'meeting' in body_lower or 'meeting' in subject_lower:
        if 'friday' in body_lower:
            key_points.append("Meeting scheduled for Friday")
        elif 'next week' in body_lower:
            key_points.append("Meeting scheduled for next week")
        else:
            key_points.append("Meeting scheduled")
    
    if 'budget' in body_lower or 'budget' in subject_lower:
        key_points.append("Budget approval or planning required")
    
    if 'contract' in body_lower or 'contract' in subject_lower:
        if 'expir' in body_lower:
            key_points.append("Contract expiring soon")
        else:
            key_points.append("Contract-related matter")
    
    if 'urgent' in body_lower or 'urgent' in subject_lower or 'priority' in body_lower:
        key_points.append("High priority - immediate attention needed")
    
    if 'deadline' in body_lower or 'due' in body_lower:
        key_points.append("Time-sensitive deadline approaching")
    
    if 'report' in body_lower or 'report' in subject_lower:
        key_points.append("Report preparation or review required")
    
    if 'client' in body_lower or 'client' in subject_lower:
        key_points.append("Client communication or feedback")
    
    if 'team' in body_lower or 'team' in subject_lower:
        key_points.append("Team coordination required")
    
    if 'maintenance' in body_lower or 'maintenance' in subject_lower:
        key_points.append("System maintenance scheduled")
    
    if 'training' in body_lower or 'training' in subject_lower:
        key_points.append("Training session scheduled")
    
    # Ensure we have at least 2 key points
    if len(key_points) < 2:
        key_points.append("Important information shared")
        key_points.append("Review and acknowledgment needed")
    
    # Generate specific action items based on content
    action_items = []
    
    if 'please' in body_lower or 'need' in body_lower:
        if 'prepare' in body_lower:
            action_items.append("Prepare required materials or documents")
        if 'review' in body_lower:
            action_items.append("Review and provide feedback")
        if 'confirm' in body_lower or 'rsvp' in body_lower:
            action_items.append("Confirm attendance or availability")
        if 'schedule' in body_lower:
            action_items.append("Schedule meeting or call")
    
    if 'approval' in body_lower:
        action_items.append("Provide approval or sign-off")
    
    if 'update' in body_lower:
        action_items.append("Provide status update")
    
    if 'contact' in body_lower or 'reach out' in body_lower:
        action_items.append("Contact relevant stakeholders")
    
    if 'follow up' in body_lower or 'follow-up' in body_lower:
        action_items.append("Follow up on pending items")
    
    # Ensure we have at least 1-2 action items
    if len(action_items) == 0:
        if 'meeting' in body_lower:
            action_items.append("Attend scheduled meeting")
        action_items.append("Review email and take appropriate action")
    
    return Summary(
        email_id=email.id,
        summary_text=summary_text,
        key_points=key_points[:5],
        action_items=action_items[:4],
        timestamp=datetime.now(),
        model_used="demo-mode"
    )
