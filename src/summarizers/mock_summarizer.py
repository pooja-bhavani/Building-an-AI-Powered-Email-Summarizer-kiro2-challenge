"""Mock summarizer for demo purposes without OpenAI API."""

from typing import List
from datetime import datetime
import random
import hashlib

from src.models import Email, Summary, BatchSummary, SummaryConfig


class MockSummarizer:
    """Mock summarizer that generates detailed, realistic summaries without API calls."""
    
    def __init__(self):
        """Initialize mock summarizer."""
        self.summary_templates = [
            "This email from {sender} discusses {topic}. The main focus is on {detail} and requires {action}. {context}",
            "The sender provides comprehensive updates on {topic}, highlighting {detail}. Immediate attention needed for {action}. {context}",
            "Important communication regarding {topic} with specific emphasis on {detail}. Action required: {action}. {context}",
            "Detailed information about {topic} has been shared. Key aspect: {detail}. Next steps involve {action}. {context}",
            "Update on {topic} requiring careful consideration of {detail}. Priority action: {action}. {context}"
        ]
        
        self.topics = [
            "project deliverables and milestones", "quarterly budget planning and allocation", 
            "cross-functional team coordination", "client feedback and satisfaction metrics",
            "upcoming deadline adjustments", "resource allocation and capacity planning",
            "strategic meeting schedules", "technical infrastructure issues", 
            "organizational policy updates", "performance review cycles",
            "long-term strategic planning", "vendor contract negotiations",
            "product development roadmap", "marketing campaign performance",
            "customer support escalations", "compliance and regulatory requirements"
        ]
        
        self.details = [
            "timeline compression due to market demands",
            "budget constraints affecting project scope",
            "stakeholder alignment on key objectives",
            "technical dependencies requiring resolution",
            "resource availability and skill gaps",
            "risk factors that need mitigation strategies",
            "quality assurance and testing requirements",
            "documentation completeness and accuracy",
            "communication protocols across teams",
            "approval workflows and decision authority"
        ]
        
        self.actions = [
            "comprehensive review and formal approval by leadership",
            "immediate response with detailed analysis",
            "cross-team discussion to align on approach",
            "thorough budget review and reallocation",
            "schedule confirmation with all stakeholders",
            "complete document preparation with supporting data",
            "stakeholder notification and expectation management",
            "detailed risk assessment and mitigation planning",
            "strategic action planning with clear milestones",
            "follow-up meeting to finalize decisions"
        ]
        
        self.contexts = [
            "This aligns with our Q4 strategic objectives.",
            "Urgent attention required to meet project deadlines.",
            "This impacts multiple departments and requires coordination.",
            "Client expectations are high and timeline is critical.",
            "Budget implications need executive review.",
            "This is a high-priority initiative with board visibility.",
            "Dependencies exist with other ongoing projects.",
            "Regulatory compliance requirements must be met.",
            "This affects our competitive positioning in the market.",
            "Resource constraints may impact delivery timeline."
        ]
        
        self.key_points_templates = [
            "Critical project milestone successfully achieved ahead of schedule",
            "Budget allocation approved with additional contingency funds",
            "Cross-functional team meeting scheduled for next week",
            "Project deadline extended by two weeks due to scope changes",
            "New technical requirements identified requiring additional resources",
            "Comprehensive risk mitigation plan developed and ready for review",
            "Executive stakeholder approval required before proceeding",
            "Technical documentation update pending final review",
            "Resource constraints identified - hiring plan in progress",
            "Timeline adjustment proposed to accommodate quality assurance",
            "Client feedback incorporated into revised project scope",
            "Vendor contract negotiations progressing favorably",
            "Performance metrics exceed quarterly targets by 15%",
            "Compliance audit scheduled for end of month",
            "Strategic partnership opportunity identified for evaluation"
        ]
        
        self.action_items_templates = [
            "Review all attached documents and provide detailed feedback by Friday EOD",
            "Schedule comprehensive follow-up meeting with all stakeholders next week",
            "Prepare executive status report with metrics and recommendations",
            "Update detailed project timeline with revised milestones and dependencies",
            "Coordinate with finance, operations, and technical teams on resource allocation",
            "Submit comprehensive budget proposal with justification to leadership",
            "Confirm availability and prepare agenda for strategic planning session",
            "Provide detailed feedback on proposed changes with impact analysis",
            "Complete all assigned deliverables and submit for quality review",
            "Share progress updates with relevant parties and escalate blockers",
            "Conduct risk assessment and develop contingency plans",
            "Prepare presentation materials for executive review meeting",
            "Gather requirements from all departments and consolidate feedback",
            "Review vendor proposals and make recommendation with cost-benefit analysis",
            "Update stakeholders on progress and address any concerns raised"
        ]
    
    def summarize_email(self, email: Email, config: SummaryConfig) -> Summary:
        """
        Generate a detailed, realistic mock summary for an email.
        
        Args:
            email: Email to summarize
            config: Summary configuration
            
        Returns:
            Summary object with detailed mock data
        """
        # Use email content to seed randomization for consistency
        seed = int(hashlib.md5(email.id.encode()).hexdigest(), 16) % 10000
        random.seed(seed)
        
        # Extract sender name for personalization
        sender_name = email.sender.split('@')[0].replace('.', ' ').title()
        
        # Generate detailed summary text
        topic = random.choice(self.topics)
        detail = random.choice(self.details)
        action = random.choice(self.actions)
        context = random.choice(self.contexts)
        template = random.choice(self.summary_templates)
        
        summary_text = template.format(
            sender=sender_name,
            topic=topic,
            detail=detail,
            action=action,
            context=context
        )
        
        # Generate 3-5 detailed key points
        num_points = random.randint(3, 5)
        key_points = random.sample(self.key_points_templates, min(num_points, len(self.key_points_templates)))
        
        # Generate 2-4 specific action items
        num_actions = random.randint(2, 4)
        action_items = random.sample(self.action_items_templates, min(num_actions, len(self.action_items_templates)))
        
        # Reset random seed
        random.seed()
        
        return Summary(
            email_id=email.id,
            summary_text=summary_text,
            key_points=key_points,
            action_items=action_items,
            timestamp=datetime.now(),
            model_used='mock-ai'
        )
    
    def summarize_batch(self, emails: List[Email], config: SummaryConfig) -> BatchSummary:
        """
        Generate a detailed, comprehensive mock batch summary for multiple emails.
        
        Args:
            emails: List of emails to summarize
            config: Summary configuration
            
        Returns:
            BatchSummary object with detailed mock data
        """
        # Generate individual summaries
        summaries = [self.summarize_email(email, config) for email in emails]
        
        # Analyze email patterns for more realistic batch summary
        email_count = len(emails)
        unique_senders = len(set(email.sender for email in emails))
        has_attachments = sum(1 for email in emails if email.has_attachments)
        
        # Generate detailed consolidated summary
        theme1 = random.choice(self.topics)
        theme2 = random.choice([t for t in self.topics if t != theme1])
        theme3 = random.choice([t for t in self.topics if t not in [theme1, theme2]])
        
        consolidated = (
            f"Comprehensive analysis of {email_count} emails from {unique_senders} unique senders in your inbox. "
            f"Primary themes identified include {theme1}, {theme2}, and {theme3}. "
            f"{has_attachments} emails contain attachments requiring review. "
            f"Multiple high-priority items require immediate attention including {random.choice(self.actions)} "
            f"and {random.choice(self.actions)}. "
            f"Overall, the communication flow indicates active project progression with several decision points pending."
        )
        
        # Generate 4-6 common themes with more variety
        num_themes = random.randint(4, 6)
        common_themes = random.sample(self.topics, min(num_themes, len(self.topics)))
        
        # Generate 3-5 urgent items with priority indicators
        num_urgent = random.randint(3, 5)
        urgent_items = random.sample(self.action_items_templates, min(num_urgent, len(self.action_items_templates)))
        
        return BatchSummary(
            email_ids=[email.id for email in emails],
            consolidated_summary=consolidated,
            common_themes=common_themes,
            urgent_items=urgent_items,
            timestamp=datetime.now()
        )
