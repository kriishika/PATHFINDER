import streamlit as st
from agents import OnboardingAgent, LearningAgent, FeedbackAgent
from memory import Memory

st.set_page_config(page_title="Pathfinder AI", layout="wide")

st.title("🤖 Pathfinder – Agentic Career Co-Pilot")

# Shared memory
memory = Memory()

# Initialize agents
onboarding = OnboardingAgent(memory)
learning = LearningAgent(memory)
feedback = FeedbackAgent(memory)

user_input = st.text_input("Enter your challenge:", "")

if st.button("Run Agents"):
    if user_input:
        st.markdown(f"**User:** {user_input}")
        response = onboarding.handle(user_input)
        st.markdown("### 🧠 Agent Conversation")
        for step in memory.get_log():
            st.write(step)
        st.markdown("### ✅ Final Recommendation")
        st.success(response)
    else:
        st.warning("Please enter something first.")
