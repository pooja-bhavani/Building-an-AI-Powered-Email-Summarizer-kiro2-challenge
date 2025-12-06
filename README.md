# ✨ Email Summarizer - AI-Powered Email Management

<img width="1470" height="956" alt="Screenshot 2025-12-06 at 8 20 46 PM" src="https://github.com/user-attachments/assets/a6fe68a2-30b3-4f0d-9c2f-294b965d872f" />


> **AI for Bharat - Week 2: Lazy Automation Challenge**  
> "I hate manually reading through hundreds of emails, so I built this."

An intelligent email management system that uses AI to automatically summarize emails, create tasks, and help you stay organized without the manual effort.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-3.0+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎯 Problem Statement

Email overload is real. Professionals receive 100+ emails daily, spending hours reading, categorizing, and extracting action items. This manual process is:
- ⏰ **Time-consuming** - Hours wasted on email triage
- 😰 **Stressful** - Fear of missing important information
- 🔄 **Repetitive** - Same categorization tasks daily
- 📊 **Inefficient** - No quick overview of inbox status

## 💡 Solution

Email Summarizer automates the boring parts of email management:
- 🤖 **AI-Powered Summaries** - Instant email summaries with key points and action items
- 📊 **Batch Analysis** - Analyze multiple emails at once to identify themes and priorities
- 🔍 **Smart Search** - Quickly find emails by sender, subject, or content
- ✉️ **Email Composition** - Compose and send emails directly from the app
- ✅ **Task Creation** - Convert emails into actionable tasks with priorities and due dates
- 🎨 **Modern UI** - Clean, professional dark theme interface

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd email-summarizer
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
python3 app.py
```

4. **Open your browser**
```
http://localhost:8080
```

That's it! The app comes with 20 demo emails pre-loaded and uses Mock AI (no API key needed).

## 🎮 Features

### 1. Email Summarization
- Select one or multiple emails
- Click "✨ Summarize" to get AI-generated summaries
- Each summary includes:
  - 📝 Concise overview of email content
  - 🔑 3-5 key points extracted
  - ✅ 2-4 actionable items identified

### 2. Batch Analysis
- Select multiple emails
- Click "📊 Batch" for consolidated analysis
- Get comprehensive overview with:
  - 📊 Overall summary of all emails
  - 🎯 Common themes across emails
  - 🚨 Urgent items requiring attention

### 3. Smart Search
- Real-time search as you type
- Search across sender, subject, and content
- Shows "Found X of Y emails"
- Works with all other features (select, summarize, etc.)

### 4. Email Composition
- Click "✉️ Compose" to write new emails
- Fill in recipient, subject, and message
- Simulated sending (demo mode)

### 5. Task Management
- Click "📋 Create Task" on any email
- Set task title, description, due date, and priority
- Tasks are stored and can be tracked

## 🏗️ Architecture

### Tech Stack
- **Backend**: Python 3.8+, Flask 3.0
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **AI**: Mock AI Summarizer (no external API needed)
- **Storage**: JSON-based file storage

### Project Structure
```
email-summarizer/
├── app.py                          # Main Flask application
├── requirements.txt                # Python dependencies
├── .env.example                    # Environment configuration template
├── templates/
│   └── index.html                  # Web UI
├── src/
│   ├── models/
│   │   ├── email.py               # Email data model
│   │   ├── summary.py             # Summary data model
│   │   └── config.py              # Configuration model
│   ├── summarizers/
│   │   ├── base.py                # Summarizer interface
│   │   └── mock_summarizer.py    # Mock AI implementation
│   ├── demo_mode.py               # Demo email generator
│   └── storage.py                 # Storage manager
├── summaries/                      # Saved summaries
│   ├── individual/                # Individual email summaries
│   ├── batch/                     # Batch summaries
│   └── exports/                   # Exported summaries
├── .kiro/
│   └── specs/email-summarizer/    # Feature specifications
│       ├── requirements.md        # Requirements document
│       ├── design.md              # Design document
│       └── tasks.md               # Implementation tasks
└── tests/
    └── property/                   # Property-based tests
```

## 🎨 UI Features

### Professional Dark Theme
- Dark navy background (#0f172a)
- Subtle blue/purple gradients
- Clean card-based layout
- Smooth animations and transitions

### Responsive Design
- Works on desktop and tablet
- Adaptive layout
- Touch-friendly controls

### User Experience
- No login required
- Instant load with demo data
- Real-time search filtering
- Clear visual feedback
- Intuitive controls

## 🔧 Configuration

### Optional: OpenAI Integration

If you want to use real OpenAI GPT-4 instead of Mock AI:

1. Get an API key from https://platform.openai.com/api-keys

2. Create a `.env` file:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

3. Restart the app - it will automatically use OpenAI

### Environment Variables

```bash
# OpenAI Configuration (Optional)
OPENAI_API_KEY=your-api-key-here

# Summarization Settings
SUMMARY_LENGTH=standard          # brief, standard, or detailed
SUMMARY_LANGUAGE=en             # Language code
AI_MODEL=gpt-4                  # gpt-4 or gpt-3.5-turbo

# Storage
SUMMARIES_DIR=summaries         # Directory for saved summaries
```

## 📊 How It Works

### Mock AI Summarizer

The app includes a sophisticated Mock AI that generates realistic summaries without external API calls:

1. **Personalization** - Uses sender name in summaries
2. **Consistency** - Same email always gets same summary (hash-based seeding)
3. **Detail** - Generates comprehensive summaries with:
   - Topic identification
   - Specific details
   - Required actions
   - Business context
4. **Variety** - 16+ topics, 10+ details, 10+ actions, 10+ contexts
5. **Realism** - Professional business communication style

### Demo Mode

- 20 pre-generated realistic emails
- Various senders, subjects, and content
- Mix of priorities and topics
- Some with attachments
- Timestamps spread across recent days

## 🧪 Testing

The project includes comprehensive property-based tests using Hypothesis:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src tests/

# Run specific test file
pytest tests/property/test_models_property.py
```

## 📝 Development with Kiro

This project was built using **Kiro AI IDE** following spec-driven development:

### Spec-Driven Development Process

1. **Requirements** - Defined 9 requirements with 45+ acceptance criteria
2. **Design** - Created comprehensive design with 27 correctness properties
3. **Tasks** - Broke down into 70+ implementation tasks
4. **Implementation** - Built incrementally with testing at each step

### Key Benefits

- ✅ Clear requirements from the start
- ✅ Systematic design process
- ✅ Property-based testing for correctness
- ✅ Incremental development
- ✅ Complete documentation

See `.kiro/specs/email-summarizer/` for full specifications.

## 🎯 Use Cases

### For Professionals
- Quickly scan inbox without reading every email
- Identify urgent items requiring immediate attention
- Extract action items automatically
- Stay organized with task creation

### For Teams
- Batch analyze team communications
- Identify common themes and priorities
- Track action items across projects
- Improve response times

### For Executives
- Get high-level overview of communications
- Identify strategic priorities
- Delegate tasks efficiently
- Save hours of email reading time

## 🚀 Future Enhancements

- [ ] Real IMAP/SMTP integration for actual email accounts
- [ ] Email categorization and auto-labeling
- [ ] Calendar integration for scheduling
- [ ] Email templates and quick replies
- [ ] Advanced search with filters
- [ ] Email threading and conversation view
- [ ] Mobile app version
- [ ] Browser extension
- [ ] Slack/Teams integration
- [ ] Analytics dashboard

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built for **AI for Bharat - Week 2: Lazy Automation Challenge**
- Developed using **Kiro AI IDE**
- Inspired by the need to automate boring email tasks

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Made with ❤️ using Kiro AI IDE**

*"Automate the boring stuff, focus on what matters."*
