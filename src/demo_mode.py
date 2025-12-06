"""Demo mode - generates realistic demo emails for testing."""

from datetime import datetime, timedelta
from typing import List
import random

from src.models import Email


def generate_demo_emails(count: int = 20) -> List[Email]:
    """
    Generate realistic demo emails for testing.
    
    Args:
        count: Number of demo emails to generate
        
    Returns:
        List of Email objects
    """
    senders = [
        "john.smith@company.com",
        "sarah.johnson@client.com",
        "mike.wilson@vendor.com",
        "emily.brown@partner.com",
        "david.lee@company.com",
        "lisa.garcia@client.com",
        "james.martinez@vendor.com",
        "jennifer.davis@partner.com",
        "robert.rodriguez@company.com",
        "maria.hernandez@client.com",
        "william.lopez@vendor.com",
        "patricia.gonzalez@partner.com",
        "richard.wilson@company.com",
        "linda.anderson@client.com",
        "thomas.taylor@vendor.com"
    ]
    
    subjects = [
        "Q4 Budget Review Meeting",
        "Project Status Update - Urgent",
        "Client Feedback on Proposal",
        "Team Sync - Weekly Update",
        "Server Maintenance Window",
        "Contract Renewal Discussion",
        "Performance Review Schedule",
        "New Feature Requirements",
        "Security Audit Results",
        "Marketing Campaign Results",
        "Vendor Contract Negotiation",
        "Technical Documentation Update",
        "Customer Support Escalation",
        "Strategic Planning Session",
        "Resource Allocation Request",
        "Compliance Training Reminder",
        "Product Launch Timeline",
        "Infrastructure Upgrade Plan",
        "Quarterly Goals Review",
        "Partnership Opportunity"
    ]
    
    body_templates = [
        "Hi Team,\n\nI wanted to provide an update on {topic}. We've made significant progress on {detail} and need to discuss {action}.\n\nKey points:\n- {point1}\n- {point2}\n- {point3}\n\nPlease review and let me know your thoughts.\n\nBest regards",
        "Hello,\n\nFollowing up on our discussion about {topic}. The current status is {detail} and we need to {action}.\n\nImportant items:\n- {point1}\n- {point2}\n- {point3}\n\nLooking forward to your feedback.\n\nThanks",
        "Team,\n\nQuick update on {topic}. We've identified {detail} and require {action}.\n\nAction items:\n- {point1}\n- {point2}\n- {point3}\n\nPlease prioritize accordingly.\n\nRegards",
        "Hi,\n\nRegarding {topic}, I wanted to share that {detail}. We should {action}.\n\nNext steps:\n- {point1}\n- {point2}\n- {point3}\n\nLet's connect soon.\n\nBest",
        "Hello Team,\n\nImportant update about {topic}. Current situation: {detail}. Recommended action: {action}.\n\nHighlights:\n- {point1}\n- {point2}\n- {point3}\n\nYour input is appreciated.\n\nThanks"
    ]
    
    topics = [
        "the project timeline",
        "budget allocation",
        "resource planning",
        "client requirements",
        "technical implementation",
        "team capacity",
        "vendor selection",
        "quality assurance",
        "risk management",
        "stakeholder alignment"
    ]
    
    details = [
        "we're ahead of schedule",
        "there are some blockers",
        "everything is on track",
        "we need additional resources",
        "the scope has changed",
        "priorities have shifted",
        "we've received approval",
        "there are dependencies",
        "we're under budget",
        "timeline needs adjustment"
    ]
    
    actions = [
        "schedule a review meeting",
        "get stakeholder approval",
        "allocate additional budget",
        "adjust the timeline",
        "coordinate with other teams",
        "update the documentation",
        "prepare a status report",
        "escalate to leadership",
        "revise the plan",
        "confirm next steps"
    ]
    
    points = [
        "Milestone completed successfully",
        "Budget review pending",
        "Team meeting scheduled for next week",
        "Client feedback incorporated",
        "Technical debt addressed",
        "Documentation updated",
        "Risk assessment completed",
        "Resource allocation approved",
        "Timeline adjusted accordingly",
        "Stakeholder alignment achieved",
        "Quality metrics improved",
        "Vendor contract finalized",
        "Compliance requirements met",
        "Performance targets exceeded",
        "Strategic goals aligned"
    ]
    
    emails = []
    base_date = datetime.now()
    
    for i in range(count):
        # Generate email details
        sender = random.choice(senders)
        subject = random.choice(subjects)
        template = random.choice(body_templates)
        
        # Generate body content
        body = template.format(
            topic=random.choice(topics),
            detail=random.choice(details),
            action=random.choice(actions),
            point1=random.choice(points),
            point2=random.choice([p for p in points if p != random.choice(points)]),
            point3=random.choice([p for p in points if p != random.choice(points)])
        )
        
        # Generate timestamp (spread over last 7 days)
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        email_date = base_date - timedelta(days=days_ago, hours=hours_ago)
        
        # Random attachments
        has_attachments = random.random() < 0.3  # 30% chance
        attachment_types = []
        if has_attachments:
            attachment_types = random.sample(['pdf', 'docx', 'xlsx', 'pptx'], random.randint(1, 2))
        
        email = Email(
            id=f"email_{i+1:03d}",
            sender=sender,
            subject=subject,
            date=email_date,
            body=body,
            folder="INBOX",
            has_attachments=has_attachments,
            attachment_types=attachment_types
        )
        
        emails.append(email)
    
    # Sort by date (newest first)
    emails.sort(key=lambda x: x.date, reverse=True)
    
    return emails
