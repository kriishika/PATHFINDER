import streamlit as st
import time
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
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧭 Pathfinder AI</h1>
    <p>Your Intelligent Career Co-Pilot</p>
    <p><em>Multi-Agent System for Career Development & Learning</em></p>
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
            st.success("Profile updated!")
    
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
    st.header("💬 Chat with Your AI Co-Pilot")
    
    # Quick action handling
    if hasattr(st.session_state, 'quick_action'):
        if st.session_state.quick_action == "career_assessment":
            user_input = "I want a comprehensive career assessment"
        elif st.session_state.quick_action == "skill_analysis":
            user_input = "Analyze my current skills and identify gaps"
        elif st.session_state.quick_action == "learning_path":
            user_input = "Create a personalized learning path for me"
        else:
            user_input = ""
        delattr(st.session_state, 'quick_action')
    else:
        user_input = st.text_input(
            "What career challenge are you facing?", 
            placeholder="e.g., 'I'm struggling with leadership skills' or 'Need help with career transition'"
        )
    
    # Example prompts
    st.markdown("**💡 Try these examples:**")
    example_col1, example_col2, example_col3 = st.columns(3)
    
    with example_col1:
        if st.button("🎯 Career Transition"):
            user_input = "I want to transition from marketing to product management"
    with example_col2:
        if st.button("📈 Skill Development"):
            user_input = "I need to improve my data analysis skills"
    with example_col3:
        if st.button("💼 Leadership Growth"):
            user_input = "How can I develop better leadership skills?"

    if st.button("🚀 Get AI Guidance", type="primary") or user_input:
        if user_input:
            # Clear previous memory for new conversation
            st.session_state.memory = Memory()
            
            # Initialize agents
            onboarding = OnboardingAgent(st.session_state.memory)
            learning = LearningAgent(st.session_state.memory)
            feedback = FeedbackAgent(st.session_state.memory)
            skill_analysis = SkillAnalysisAgent(st.session_state.memory)
            
            # Display user input
            st.markdown(f"**You:** {user_input}")
            
            # Progress bar for processing
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Simulate processing with progress updates
            for i, status in enumerate([
                "🔍 Analyzing your challenge...",
                "🧠 Consulting AI agents...",
                "📊 Generating insights...",
                "✨ Preparing recommendations..."
            ]):
                status_text.text(status)
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.5)
            
            # Process with agents
            response = onboarding.handle(user_input, st.session_state.user_profile)
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
            # Display agent conversation
            st.markdown("### 🤖 AI Agent Analysis")
            
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
                
                st.markdown(f"""
                <div class="agent-card">
                    <strong>{icon} {agent_name}</strong>
                    <small style="color: gray; float: right;">{timestamp}</small><br>
                    {message}
                </div>
                """, unsafe_allow_html=True)
            
            # Display final recommendation
            st.markdown("### 🎯 Your Personalized Action Plan")
            st.markdown(f"""
            <div class="recommendation-box">
                <h4>✨ AI Recommendation</h4>
                {response}
            </div>
            """, unsafe_allow_html=True)
            
            # Add to conversation history
            st.session_state.conversation_history.append({
                'user_input': user_input,
                'response': response,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            })
            
        else:
            st.warning("💭 Please describe your career challenge or goal!")

with col2:
    st.header("📈 Dashboard")
    
    # Agent activity summary
    st.subheader("🤖 Agent Activity")
    if st.session_state.memory.get_log():
        agent_counts = {}
        for log in st.session_state.memory.get_detailed_log():
            agent = log['agent']
            agent_counts[agent] = agent_counts.get(agent, 0) + 1
        
        for agent, count in agent_counts.items():
            st.metric(agent, count, "interactions")
    else:
        st.info("No agent activity yet. Start a conversation!")
    
    st.markdown("---")
    
    # Conversation history
    st.subheader("💭 Recent Conversations")
    if st.session_state.conversation_history:
        for i, conv in enumerate(reversed(st.session_state.conversation_history[-3:])):
            with st.expander(f"💬 {conv['timestamp']}", expanded=False):
                st.write(f"**You:** {conv['user_input'][:100]}...")
                st.write(f"**AI:** {conv['response'][:150]}...")
    else:
        st.info("No conversations yet!")
    
    st.markdown("---")
    
    # System info
    st.subheader("ℹ️ System Status")
    st.success("🟢 All agents online")
    st.info(f"💾 Memory: {len(st.session_state.memory.get_log())} entries")
    st.info(f"👤 Profile: {'Complete' if st.session_state.user_profile['name'] else 'Setup needed'}")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: gray; padding: 1rem;">
    <p>🧭 <strong>Pathfinder AI</strong> - Powered by Multi-Agent Intelligence</p>
    <p><em>Hackathon Demo - Transforming Career Development with AI</em></p>
</div>
""", unsafe_allow_html=True)
