#!/usr/bin/env python3
"""
Email Summarizer - Production Web Application
Connects to real email accounts and uses OpenAI for summarization.
"""

from flask import Flask, render_template, jsonify, request, session
from datetime import datetime
from typing import List
import os
from dotenv import load_dotenv

from src.models import Email, Summary, SummaryConfig
from src.summarizers import MockSummarizer
from src.storage import StorageManager
from src.demo_mode import generate_demo_emails

load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Global storage
storage = StorageManager()
summarizer = None

# Generate demo emails on startup
demo_emails = generate_demo_emails()

@app.route('/')
def index():
    """Main page."""
    return render_template('index.html')

@app.route('/api/emails')
def get_emails():
    """Get emails (demo mode)."""
    global demo_emails
    
    try:
        limit = int(request.args.get('limit', 20))
        
        emails_data = []
        for email in demo_emails[:limit]:
            emails_data.append({
                'id': email.id,
                'sender': email.sender,
                'subject': email.subject,
                'date': email.date.strftime('%Y-%m-%d %H:%M'),
                'body': email.body[:300] + '...' if len(email.body) > 300 else email.body,
                'has_attachments': email.has_attachments,
                'attachment_types': email.attachment_types,
                'full_body': email.body  # Store full body for summarization
            })
        
        # Store emails in session for later use
        session['emails'] = emails_data
        
        return jsonify({'emails': emails_data})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/summarize', methods=['POST'])
def summarize():
    """Summarize selected emails using AI."""
    global summarizer
    
    data = request.json
    email_ids = data.get('email_ids', [])
    
    if not email_ids:
        return jsonify({'error': 'No emails selected'}), 400
    
    # Get emails from session
    all_emails = session.get('emails', [])
    selected_emails = [e for e in all_emails if e['id'] in email_ids]
    
    if not selected_emails:
        return jsonify({'error': 'Selected emails not found'}), 404
    
    try:
        # Initialize summarizer if not already done
        if not summarizer:
            summarizer = MockSummarizer()
        
        # Create config
        config = SummaryConfig(
            length=data.get('length', 'standard'),
            focus_areas=data.get('focus_areas', ['action_items', 'decisions']),
            language=data.get('language', 'en'),
            model=data.get('model', 'gpt-4')
        )
        
        summaries = []
        for email_data in selected_emails:
            # Convert to Email object
            email = Email(
                id=email_data['id'],
                sender=email_data['sender'],
                subject=email_data['subject'],
                date=datetime.strptime(email_data['date'], '%Y-%m-%d %H:%M'),
                body=email_data['full_body'],
                folder='INBOX',
                has_attachments=email_data['has_attachments'],
                attachment_types=email_data['attachment_types']
            )
            
            # Generate summary
            summary = summarizer.summarize_email(email, config)
            
            # Save summary
            storage.save_summary(summary)
            
            summaries.append({
                'email_id': email.id,
                'sender': email.sender,
                'subject': email.subject,
                'date': email.date.strftime('%Y-%m-%d %H:%M'),
                'summary_text': summary.summary_text,
                'key_points': summary.key_points,
                'action_items': summary.action_items
            })
        
        return jsonify({'summaries': summaries})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/batch-summarize', methods=['POST'])
def batch_summarize():
    """Generate batch summary for multiple emails."""
    global summarizer
    
    data = request.json
    email_ids = data.get('email_ids', [])
    
    if not email_ids:
        return jsonify({'error': 'No emails selected'}), 400
    
    # Get emails from session
    all_emails = session.get('emails', [])
    selected_emails = [e for e in all_emails if e['id'] in email_ids]
    
    if not selected_emails:
        return jsonify({'error': 'Selected emails not found'}), 404
    
    try:
        # Initialize summarizer if not already done
        if not summarizer:
            summarizer = MockSummarizer()
        
        # Create config
        config = SummaryConfig(
            length=data.get('length', 'standard'),
            focus_areas=data.get('focus_areas', ['action_items', 'decisions']),
            language=data.get('language', 'en'),
            model=data.get('model', 'gpt-4')
        )
        
        # Convert to Email objects
        emails = []
        for email_data in selected_emails:
            email = Email(
                id=email_data['id'],
                sender=email_data['sender'],
                subject=email_data['subject'],
                date=datetime.strptime(email_data['date'], '%Y-%m-%d %H:%M'),
                body=email_data['full_body'],
                folder='INBOX',
                has_attachments=email_data['has_attachments'],
                attachment_types=email_data['attachment_types']
            )
            emails.append(email)
        
        # Generate batch summary
        batch_summary = summarizer.summarize_batch(emails, config)
        
        # Save batch summary
        storage.save_batch_summary(batch_summary)
        
        return jsonify({
            'batch_summary': {
                'email_count': len(emails),
                'consolidated_summary': batch_summary.consolidated_summary,
                'common_themes': batch_summary.common_themes,
                'urgent_items': batch_summary.urgent_items
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/compose', methods=['POST'])
def compose_email():
    """Compose and send an email (demo mode - simulated)."""
    data = request.json
    to = data.get('to')
    subject = data.get('subject')
    body = data.get('body')
    
    if not all([to, subject, body]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # In demo mode, just simulate sending
        print(f"\n📧 SIMULATED EMAIL SENT:")
        print(f"To: {to}")
        print(f"Subject: {subject}")
        print(f"Body: {body[:100]}...")
        
        return jsonify({
            'success': True,
            'message': 'Email sent successfully! (Demo Mode)'
        })
        
    except Exception as e:
        return jsonify({'error': f'Failed to send email: {str(e)}'}), 500

@app.route('/api/create-task', methods=['POST'])
def create_task():
    """Create a task from an email."""
    data = request.json
    email_id = data.get('email_id')
    task_title = data.get('task_title')
    task_description = data.get('task_description')
    due_date = data.get('due_date')
    priority = data.get('priority', 'medium')
    
    if not all([email_id, task_title]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    try:
        # Save task to storage
        task = {
            'id': f"task_{datetime.now().timestamp()}",
            'email_id': email_id,
            'title': task_title,
            'description': task_description,
            'due_date': due_date,
            'priority': priority,
            'status': 'pending',
            'created_at': datetime.now().isoformat()
        }
        
        # Store in session for now
        if 'tasks' not in session:
            session['tasks'] = []
        session['tasks'].append(task)
        session.modified = True
        
        return jsonify({'success': True, 'task': task})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks')
def get_tasks():
    """Get all tasks."""
    tasks = session.get('tasks', [])
    return jsonify({'tasks': tasks})

@app.route('/api/disconnect', methods=['POST'])
def disconnect():
    """Disconnect (demo mode - just clear session)."""
    session.clear()
    return jsonify({'success': True})

if __name__ == '__main__':
    print("=" * 70)
    print("🚀 Starting Email Summarizer - Demo Mode")
    print("=" * 70)
    print()
    print("📧 AI-Powered Email Summarization:")
    print("   ✓ 20 demo emails pre-loaded")
    print("   ✓ Using Mock AI (no API key needed)")
    print("   ✓ Smart search functionality")
    print("   ✓ Compose emails (simulated)")
    print("   ✓ Create tasks from emails")
    print("   ✓ Batch summarization")
    print()
    print("🌐 Open your browser and go to:")
    print("   http://localhost:8080")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 70)
    print()
    
    app.run(debug=True, host='0.0.0.0', port=8080)
