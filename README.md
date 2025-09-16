# Pathfinder – Agentic Career Co-Pilot

## Overview
Pathfinder is a proof-of-concept multi-agent system that helps young professionals
from onboarding to career growth. Unlike static chatbots, agents collaborate
and act autonomously.

### Agents
- **Onboarding Agent**: Detects friction and routes issues.
- **Learning Agent**: Creates adaptive learning sprints.
- **Feedback Agent**: Analyzes peer reviews and performance signals.

### Example Flow
1. User: "I'm struggling with data engineering training."
2. Onboarding Agent detects onboarding issue.
3. Learning Agent suggests a 2-week sprint.
4. Feedback Agent confirms the skill gap from reviews.
5. Final recommendation shown.

### Run Locally
```bash
pip install -r requirements.txt
streamlit run app.py
