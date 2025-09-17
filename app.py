import streamlit as st
import time
import os
from datetime import datetime
from agents import OnboardingAgent, LearningAgent, FeedbackAgent, SkillAnalysisAgent
from memory import Memory
import plotly.express as px
import pandas as pd

# Page config with better styling
st.set_page_config(
    page_title="Pathfinder AI", 
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🧭"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .agent-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
    }
    .ai-indicator {
        background: linear-gradient(135deg, #00c851 0%, #007e33 100%);
        padding: 0.5rem 1rem;
        border-radius: 20px;
        color: white;
        font-size: 0.8rem;
        display: inline-block;
        margin: 0.5rem 0;
    }
    .recommendation-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 2rem;
        font-weight: bold;
    }
    .api-warning {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        padding: 1rem;
        border-radius: 8px;
        color: white;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧭 Pathfinder AI</h1>
    <p>Your Intelligent Agentic Career Co-Pilot</p>
    <p><em>Powered by AI Agents with Real Language Model Intelligence</em></p>
</div>
""", unsafe_allow_html=True)

# API Key Check and Configuration
api_key_available = bool(os.getenv("OPENAI_API_KEY"))

if not api_key_available:
    st.markdown("""
    <div class="api-warning">
        <h4>⚙️ AI Configuration</h4>
        <p>For full AI capabilities, add your OpenAI API key:</p>
        <p><code>export OPENAI_API_KEY="your-key-here"</code></p>
        <p><em>Currently running in demo mode with intelligent fallback responses.</em></p>
    </div>
    """, unsafe_allow_html=True)

# Initialize session state
if 'memory' not in st.session_state:
    st.session_state.memory = Memory()
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'user_profile' not in st.session_state:
    st.session_state.user_profile = {
        'name': '',
        'role': '',
        'experience': '',
        'goals': []
    }

# Sidebar for user profile and settings
with st.sidebar:
    st.header("👤 Your Profile")
    
    # AI Status Indicator
    if api_key_available:
        st.markdown('<div class="ai-indicator">🧠 AI Agents: ACTIVE</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="ai-indicator" style="background: linear-gradient(135deg, #ffa500 0%, #ff6347 100%);">🤖 AI Agents: DEMO MODE</div>', unsafe_allow_html=True)
    
    with st.expander("Setup Your Profile", expanded=True):
        name = st.text_input("Name", value=st.session_state.user_profile['name'])
        role = st.selectbox("Current Role", 
            ["Software Engineer", "Data Scientist", "Product Manager", 
             "Designer", "Marketing", "Sales", "Student", "Other"])
        experience = st.selectbox("Experience Level", 
            ["Fresh Graduate", "1-2 years", "3-5 years", "5+ years"])
        
        if st.button("Update Profile"):
            st.session_state.user_profile.update({
                'name': name, 'role': role, 'experience': experience
            })
            st.success("Profile updated! AI agents will personalize responses.")
    
    st.markdown("---")
    
    # AI Agent Status
    st.header("🤖 AI Agent Status")
    agents = [
        ("OnboardingAgent", "🚪", "Routing & Analysis"),
        ("LearningAgent", "📚", "Strategy & Planning"), 
        ("FeedbackAgent", "💬", "Assessment & Validation"),
        ("SkillAnalysisAgent", "🔬", "Skill Intelligence")
    ]
    
    for agent_name, icon, description in agents:
        status = "READY" if api_key_available else "DEMO"
        color = "#00c851" if api_key_available else "#ffa500"
        st.markdown(f"""
        **{icon} {agent_name}**  
        <span style="color: {color};">● {status}</span> - {description}
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.header("🎯 Quick Actions")
    if st.button("🚀 Career Assessment"):
        st.session_state.quick_action = "career_assessment"
    if st.button("📚 Skill Gap Analysis"):
        st.session_state.quick_action = "skill_analysis"
    if st.button("🎓 Learning Path"):
        st.session_state.quick_action = "learning_path"
    
    st.markdown("---")
    st.header("📊 Your Progress")
    # Mock progress data
    progress_data = pd.DataFrame({
        'Skill': ['Python', 'Leadership', 'Communication', 'Data Analysis'],
        'Progress': [85, 60, 75, 40]
    })
    fig = px.bar(progress_data, x='Skill', y='Progress', 
                color='Progress', color_continuous_scale='viridis')
    fig.update_layout(height=300, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("💬 Chat with Your AI Agent Team")
    
    # AI Capability Notice
    if api_key_available:
        st.success("🧠 **Full AI Mode**: Your agents are powered by advanced language models for intelligent, personalized responses.")
    else:
        st.info("🤖 **Demo Mode**: Agents use intelligent fallback responses. Add OpenAI API key for full AI capabilities.")
    
    # Quick action handling
    if hasattr(st.session_state, 'quick_action'):
        if st.session_state.quick_action == "career_assessment":
            user_input = "I want a comprehensive AI-powered career assessment"
        elif st.session_state.quick_action == "skill_analysis":
            user_input = "Use AI to analyze my current skills and identify gaps"
        elif st.session_state.quick_action == "learning_path":
            user_input = "Create an AI-generated personalized learning path for me"
        else:
            user_input = ""
        delattr(st.session_state, 'quick_action')
    else:
        user_input = st.text_input(
            "What career challenge should our AI agents solve?", 
            placeholder="e.g., 'I want to transition to AI/ML engineering' or 'Help me develop leadership skills'"
        )
    
    # Example prompts with AI focus
    st.markdown("**💡 Try these AI-powered examples:**")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("🎯 AI Career Strategy"):
            user_input = "Use AI to create a career transition strategy from marketing to product management"
    with example_col2:
        if st.button("📈 AI Skill Planning"):
            user_input = "I need AI analysis of data science skills and a learning roadmap"
    with example_col3:
        if st.button("💼 AI Leadership Coach"):
            user_input = "How can AI help me develop better leadership and management skills?"

    if st.button("🚀 Activate AI Agent Team", type="primary") or user_input:
        if user_input:
            # Clear previous memory for new conversation
            st.session_state.memory = Memory()
            
            # Display user input
            st.markdown(f"**You:** {user_input}")
            
            # Progress bar for AI processing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate AI processing with progress updates
            ai_steps = [
                "🧠 Initializing AI agents...",
                "🔍 AI analyzing your challenge...",
                "🤖 Agents consulting language models...",
                "📊 AI generating personalized insights...",
                "✨ Finalizing AI recommendations..."
            ]
            
            for i, status in enumerate(ai_steps):
                status_text.text(status)
                progress_bar.progress((i + 1) * 20)
                time.sleep(0.8)  # Longer delay to show AI processing
            
            # Initialize AI agents
            onboarding = OnboardingAgent(st.session_state.memory)
            
            # Process with AI agents
            with st.spinner("🤖 AI agents collaborating..."):
                response = onboarding.handle(user_input, st.session_state.user_profile)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display AI agent conversation
            st.markdown("### 🤖 AI Agent Intelligence Network")
            
            agent_logs = st.session_state.memory.get_detailed_log()
            for log_entry in agent_logs:
                agent_name = log_entry['agent']
                message = log_entry['message']
                timestamp = log_entry['timestamp']
                
                # Different styling for different agents
                if agent_name == "OnboardingAgent":
                    icon = "🚪"
                    color = "#e74c3c"
                elif agent_name == "LearningAgent":
                    icon = "📚"
                    color = "#3498db"
                elif agent_name == "FeedbackAgent":
                    icon = "💬"
                    color = "#f39c12"
                elif agent_name == "SkillAnalysisAgent":
                    icon = "🔬"
                    color = "#9b59b6"
                else:
                    icon = "🤖"
                    color = "#95a5a6"
                
                # Add AI indicator for actual AI responses
                ai_indicator = "🧠 AI" if api_key_available else "🤖 Demo"
                
                st.markdown(f"""
                <div class="agent-card">
                    <strong>{icon} {agent_name}</strong> <span style="color: green; font-size: 0.8em;">{ai_indicator}</span>
                    <small style="color: gray; float: right;">{timestamp}</small><br>
                    {message}
                </div>
                """, unsafe_allow_html=True)
            
            # Display final AI recommendation
            st.markdown("### 🎯 Your AI-Powered Action Plan")
            st.markdown(f"""
            <div class="recommendation-box">
                <h4>✨ AI Agent Collaboration Result</h4>
                {response}
                <br><br>
                <small>{'Generated by GPT-powered AI agents' if api_key_available else 'Generated by intelligent demo agents'}</small>
            </div>
            """, unsafe_allow_html=True)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                'user_input': user_input,
                'response': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ai_powered': api_key_available
            })
            
        else:
            st.warning("💭 Please describe your career challenge for AI analysis!")

with col2:
    st.header("📈 AI Dashboard")
    
    # AI Agent activity summary
    st.subheader("🤖 AI Agent Activity")
    if st.session_state.memory.get_log():
        agent_counts = {}
        for log in st.session_state.memory.get_detailed_log():
            agent = log['agent']
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        for agent, count in agent_counts.items():
            ai_status = "🧠 AI-Powered" if api_key_available else "🤖 Demo Mode"
            st.metric(f"{agent}", f"{count} interactions", ai_status)
    else:
        st.info("No AI agent activity yet. Start a conversation!")
    
    st.markdown("---")
    
    # AI Intelligence Metrics
    st.subheader("🧠 AI Intelligence Metrics")
    col_a, col_b = st.columns(2)
    
    with col_a:
        if api_key_available:
            st.metric("AI Model", "GPT-3.5", "Active")
            st.metric("Intelligence Level", "High", "Language Model")
        else:
            st.metric("AI Model", "Demo", "Fallback")
            st.metric("Intelligence Level", "Rule-Based", "Pattern Matching")
    
    with col_b:
        total_interactions = len(st.session_state.conversation_history)
        ai_interactions = sum(1 for conv in st.session_state.conversation_history if conv.get('ai_powered', False))
        st.metric("Total Sessions", total_interactions)
        st.metric("AI-Powered", ai_interactions, f"of {total_interactions}")
    
    st.markdown("---")
    
    # Conversation history
    st.subheader("💭 Recent AI Conversations")
    if st.session_state.conversation_history:
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-3:])):
            ai_badge = "🧠 AI" if conv.get('ai_powered', False) else "🤖 Demo"
            with st.expander(f"{ai_badge} {conv['timestamp']}", expanded=False):
                st.write(f"**You:** {conv['user_input'][:100]}...")
                st.write(f"**AI Agents:** {conv['response'][:150]}...")
    else:
        st.info("No AI conversations yet!")
    
    st.markdown("---")
    
    # System info with AI status
    st.subheader("ℹ️ AI System Status")
    if api_key_available:
        st.success("🟢 AI Agents: Fully Operational")
        st.success("🧠 Language Model: Connected")
    else:
        st.warning("🟡 AI Agents: Demo Mode")
        st.info("🔧 Add API key for full AI")
    
    st.info(f"💾 Memory: {len(st.session_state.memory.get_log())} entries")
    st.info(f"👤 Profile: {'Complete' if st.session_state.user_profile['name'] else 'Setup needed'}")

# Footer with AI emphasis
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p>🧭 <strong>Pathfinder AI</strong> - {'Powered by GPT-3.5 Agentic Intelligence' if api_key_available else 'Intelligent Demo with AI Architecture'}</p>
    <p><em>Hackathon Demo - Multi-Agent AI System for Career Development</em></p>
    {'<p style="color: green;">✅ Full AI capabilities active</p>' if api_key_available else '<p style="color: orange;">⚙️ Add OpenAI API key for full AI intelligence</p>'}
</div>
""", unsafe_allow_html=True)
