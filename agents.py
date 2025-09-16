import openai
import json
from typing import Dict, List, Optional
from datetime import datetime
import os

# Configuration - add your API key here or via environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")  # Set this in your environment

class AIAgent:
    """Base class for all AI agents with shared LLM capabilities"""
    
    def __init__(self, memory, name: str, role_description: str):
        self.memory = memory
        self.name = name
        self.role_description = role_description
        self.model = "gpt-3.5-turbo"  # Using GPT-3.5 for cost efficiency
    
    def _make_llm_call(self, prompt: str, temperature: float = 0.7) -> str:
        """Make a call to the language model"""
        try:
            if not openai.api_key:
                # Fallback for demo purposes when no API key is provided
                return self._fallback_response(prompt)
            
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.role_description},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=500
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            self.memory.add(self.name, f"⚠️ AI service unavailable, using fallback: {str(e)}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback response when AI is unavailable"""
        return "AI service is currently unavailable. Please add your OpenAI API key to enable full AI capabilities."

class OnboardingAgent(AIAgent):
    def __init__(self, memory):
        role_description = """You are an expert career onboarding specialist. Your role is to:
        1. Analyze career challenges and questions from professionals
        2. Determine the type of support needed (skill development, career transition, leadership, etc.)
        3. Route requests to appropriate specialist agents
        4. Coordinate responses from multiple agents
        5. Provide initial assessment and context setting
        
        You should be empathetic, professional, and strategic in your analysis. Always consider the person's career stage, goals, and immediate needs."""
        
        super().__init__(memory, "OnboardingAgent", role_description)
    
    def handle(self, query: str, user_profile: Optional[Dict] = None) -> str:
        """Analyze query and orchestrate response from other agents"""
        
        # Build context prompt
        context = f"""
        User Query: "{query}"
        
        User Profile:
        - Role: {user_profile.get('role', 'Not specified') if user_profile else 'Not specified'}
        - Experience: {user_profile.get('experience', 'Not specified') if user_profile else 'Not specified'}
        - Name: {user_profile.get('name', 'User') if user_profile else 'User'}
        
        Please analyze this career challenge and:
        1. Identify the main type of challenge (transition, skill development, leadership, assessment, etc.)
        2. Suggest which specialist agents should be involved
        3. Provide initial insights and direction
        
        Respond in a structured format with your analysis.
        """
        
        self.memory.add(self.name, "🔍 Analyzing career challenge with AI...")
        analysis = self._make_llm_call(context, temperature=0.3)
        self.memory.add(self.name, f"📋 AI Analysis: {analysis[:100]}...")
        
        # Determine which agents to involve based on AI analysis
        if "skill" in analysis.lower() or "learning" in analysis.lower():
            skill_agent = SkillAnalysisAgent(self.memory)
            skill_insights = skill_agent.analyze_skills(query, user_profile)
            
            learning_agent = LearningAgent(self.memory)
            final_plan = learning_agent.create_learning_plan(query, skill_insights, user_profile)
            return final_plan
            
        elif "transition" in analysis.lower() or "change" in analysis.lower():
            feedback_agent = FeedbackAgent(self.memory)
            current_assessment = feedback_agent.assess_transition_readiness(query, user_profile)
            
            learning_agent = LearningAgent(self.memory)
            transition_plan = learning_agent.create_transition_plan(query, current_assessment, user_profile)
            return transition_plan
            
        else:
            # General career development - involve multiple agents
            feedback_agent = FeedbackAgent(self.memory)
            feedback_result = feedback_agent.analyze_situation(query, user_profile)
            
            learning_agent = LearningAgent(self.memory)
            comprehensive_plan = learning_agent.create_development_plan(query, feedback_result, user_profile)
            return comprehensive_plan

class LearningAgent(AIAgent):
    def __init__(self, memory):
        role_description = """You are an expert learning and development strategist. Your expertise includes:
        1. Creating personalized learning paths for professionals
        2. Designing career transition roadmaps
        3. Recommending specific resources, courses, and experiences
        4. Setting realistic timelines and milestones
        5. Balancing theoretical learning with practical application
        
        You should provide specific, actionable learning plans with clear steps, timelines, and success metrics. Consider different learning styles and practical constraints."""
        
        super().__init__(memory, "LearningAgent", role_description)
    
    def create_learning_plan(self, query: str, skill_analysis: str, user_profile: Optional[Dict] = None) -> str:
        """Create a comprehensive learning plan based on skill analysis"""
        
        prompt = f"""
        Based on this career challenge and skill analysis, create a detailed learning plan:
        
        Challenge: "{query}"
        Skill Analysis: {skill_analysis}
        User Background: {user_profile.get('role', 'Professional') if user_profile else 'Professional'} with {user_profile.get('experience', 'some') if user_profile else 'some'} experience
        
        Please create a comprehensive learning plan that includes:
        1. 3-4 key learning objectives
        2. Specific resources and activities for each objective
        3. Realistic timeline (4-8 weeks)
        4. Success metrics and milestones
        5. Practical application opportunities
        
        Make it actionable and specific to their situation.
        """
        
        self.memory.add(self.name, "📚 AI creating personalized learning strategy...")
        plan = self._make_llm_call(prompt, temperature=0.4)
        self.memory.add(self.name, f"✨ Generated comprehensive AI-powered learning plan")
        
        return f"""
## 🎯 Your AI-Generated Learning Plan

{plan}

---
*This plan was created by AI analysis of your specific situation and goals.*
        """.strip()
    
    def create_transition_plan(self, query: str, assessment: str, user_profile: Optional[Dict] = None) -> str:
        """Create a career transition roadmap"""
        
        prompt = f"""
        Create a strategic career transition plan for this professional:
        
        Transition Goal: "{query}"
        Current Assessment: {assessment}
        Background: {user_profile.get('role', 'Current professional') if user_profile else 'Current professional'}
        
        Design a transition roadmap with:
        1. Phase-by-phase approach (3 phases over 8-12 weeks)
        2. Skill development priorities
        3. Networking and positioning strategies
        4. Portfolio/credential building
        5. Market entry tactics
        
        Be specific about actions they can take immediately.
        """
        
        self.memory.add(self.name, "🔄 AI designing career transition roadmap...")
        roadmap = self._make_llm_call(prompt, temperature=0.5)
        self.memory.add(self.name, "🎯 Completed AI-powered transition strategy")
        
        return f"""
## 🚀 Your AI-Generated Transition Roadmap

{roadmap}

---
*This roadmap uses AI analysis to create a personalized strategy for your career change.*
        """.strip()
    
    def create_development_plan(self, query: str, feedback: str, user_profile: Optional[Dict] = None) -> str:
        """Create general career development plan"""
        
        prompt = f"""
        Create a professional development plan for this career challenge:
        
        Challenge: "{query}"
        Situation Analysis: {feedback}
        Professional Level: {user_profile.get('experience', 'Mid-level') if user_profile else 'Mid-level'}
        
        Design a development strategy that includes:
        1. Short-term goals (next 2-4 weeks)
        2. Medium-term objectives (2-3 months)
        3. Skill building activities
        4. Performance improvement tactics
        5. Career positioning strategies
        
        Focus on practical, high-impact actions.
        """
        
        self.memory.add(self.name, "📈 AI crafting professional development strategy...")
        strategy = self._make_llm_call(prompt, temperature=0.4)
        self.memory.add(self.name, "✅ Generated AI-powered development plan")
        
        return f"""
## 📈 Your AI-Generated Development Plan

{strategy}

---
*This plan leverages AI insights to address your specific career development needs.*
        """.strip()

class FeedbackAgent(AIAgent):
    def __init__(self, memory):
        role_description = """You are an expert career coach and performance analyst. Your capabilities include:
        1. Analyzing professional situations and challenges
        2. Assessing career transition readiness
        3. Identifying strengths and development areas
        4. Providing realistic feedback and recommendations
        5. Validating learning plans and strategies
        
        You should be honest, constructive, and supportive while providing data-driven insights about career development paths."""
        
        super().__init__(memory, "FeedbackAgent", role_description)
    
    def analyze_situation(self, query: str, user_profile: Optional[Dict] = None) -> str:
        """Analyze the user's current situation and provide feedback"""
        
        prompt = f"""
        Analyze this professional's career situation and provide coaching feedback:
        
        Challenge/Question: "{query}"
        Current Role: {user_profile.get('role', 'Professional') if user_profile else 'Professional'}
        Experience Level: {user_profile.get('experience', 'Mid-level') if user_profile else 'Mid-level'}
        
        Provide a realistic assessment that covers:
        1. Current situation analysis
        2. Key strengths they can leverage
        3. Areas that need development
        4. Market/industry context
        5. Recommended next steps
        
        Be supportive but honest about challenges and opportunities.
        """
        
        self.memory.add(self.name, "💬 AI analyzing career situation...")
        analysis = self._make_llm_call(prompt, temperature=0.3)
        self.memory.add(self.name, "📊 Completed AI situation assessment")
        
        return analysis
    
    def assess_transition_readiness(self, query: str, user_profile: Optional[Dict] = None) -> str:
        """Assess readiness for career transition"""
        
        prompt = f"""
        Assess this professional's readiness for career transition:
        
        Desired Transition: "{query}"
        Current Background: {user_profile.get('role', 'Professional') if user_profile else 'Professional'} with {user_profile.get('experience', 'some') if user_profile else 'some'} experience
        
        Evaluate and provide feedback on:
        1. Transferable skills and strengths
        2. Skill gaps that need addressing
        3. Market timing and opportunities
        4. Transition challenges to expect
        5. Readiness score (1-10) with reasoning
        
        Be realistic about the transition difficulty and timeline.
        """
        
        self.memory.add(self.name, "📍 AI assessing transition readiness...")
        assessment = self._make_llm_call(prompt, temperature=0.3)
        self.memory.add(self.name, "🎯 Completed AI transition assessment")
        
        return assessment
    
    def validate_plan(self, plan: str, original_query: str) -> str:
        """Validate a learning or development plan"""
        
        prompt = f"""
        Review and validate this career development plan:
        
        Original Challenge: "{original_query}"
        Proposed Plan: {plan}
        
        Provide validation feedback on:
        1. Plan completeness and relevance
        2. Realistic timeline and expectations
        3. Potential gaps or oversights
        4. Success probability assessment
        5. Suggested improvements or additions
        
        Give constructive feedback to optimize the plan.
        """
        
        self.memory.add(self.name, "🔍 AI validating development plan...")
        validation = self._make_llm_call(prompt, temperature=0.3)
        self.memory.add(self.name, "✅ Completed AI plan validation")
        
        return validation

class SkillAnalysisAgent(AIAgent):
    def __init__(self, memory):
        role_description = """You are an expert skills analyst and career strategist. Your expertise covers:
        1. Comprehensive skill gap analysis
        2. Industry skill requirements and trends
        3. Skill development prioritization
        4. Competency frameworks and assessments
        5. Future skill predictions and recommendations
        
        You should provide detailed, actionable skill analysis that helps professionals make informed decisions about their development priorities."""
        
        super().__init__(memory, "SkillAnalysisAgent", role_description)
    
    def analyze_skills(self, query: str, user_profile: Optional[Dict] = None) -> str:
        """Perform comprehensive AI-powered skill analysis"""
        
        prompt = f"""
        Conduct a comprehensive skill analysis for this professional:
        
        Career Challenge/Goal: "{query}"
        Current Role: {user_profile.get('role', 'Professional') if user_profile else 'Professional'}
        Experience: {user_profile.get('experience', 'Mid-level') if user_profile else 'Mid-level'}
        
        Provide a detailed skill analysis including:
        1. Current skill strengths (based on role/experience)
        2. Skills required for their goal/challenge
        3. Critical skill gaps (high priority)
        4. Nice-to-have skills (medium priority)
        5. Industry trends affecting skill requirements
        6. Recommended skill development sequence
        
        Be specific about technical and soft skills, and consider future market trends.
        """
        
        self.memory.add(self.name, "🔬 AI conducting comprehensive skill analysis...")
        analysis = self._make_llm_call(prompt, temperature=0.4)
        self.memory.add(self.name, "📊 Completed AI-powered skill gap analysis")
        
        return f"""
## 🔬 AI-Powered Skill Analysis

{analysis}

---
*This analysis uses AI to evaluate your skills against current market requirements and future trends.*
        """.strip()
    
    def predict_future_skills(self, role: str, timeframe: str = "next 2-3 years") -> str:
        """Predict future skill requirements for a role"""
        
        prompt = f"""
        Predict the evolving skill requirements for {role} over the {timeframe}:
        
        Consider:
        1. Technology trends affecting this role
        2. Industry evolution and market changes
        3. Automation impact on required skills
        4. Emerging competencies becoming important
        5. Skills that may become less relevant
        
        Provide strategic insights for skill development planning.
        """
        
        self.memory.add(self.name, f"🔮 AI predicting future skills for {role}...")
        prediction = self._make_llm_call(prompt, temperature=0.6)
        self.memory.add(self.name, "📈 Completed future skills analysis")
        
        return prediction

# Alternative implementation for when OpenAI API is not available
class MockAIAgent:
    """Mock agent that provides intelligent-seeming responses without actual AI"""
    
    def __init__(self, memory, name: str):
        self.memory = memory
        self.name = name
    
    def _get_intelligent_response(self, query: str, response_type: str) -> str:
        """Generate contextual responses based on query analysis"""
        query_lower = query.lower()
        
        if response_type == "analysis":
            if "transition" in query_lower:
                return "Based on your transition goal, I've identified key transferable skills and market opportunities. The current job market shows strong demand in your target area, with several pathways available for professionals with your background."
            elif "skill" in query_lower:
                return "Your skill development challenge requires a strategic approach. I've analyzed current industry requirements and identified the most impactful areas for growth based on market trends and your career trajectory."
            else:
                return "After analyzing your career challenge, I've identified several key factors that will influence your success. The current market conditions and your professional background create specific opportunities for advancement."
        
        elif response_type == "plan":
            return """
**Phase 1: Foundation Building (Weeks 1-3)**
- Assess current capabilities and market requirements
- Identify top 3 priority development areas
- Create learning schedule and resource list

**Phase 2: Skill Development (Weeks 4-7)**
- Complete targeted learning activities
- Apply new skills in practical projects
- Seek feedback and iterate on approach

**Phase 3: Integration & Application (Weeks 8-10)**
- Demonstrate new capabilities in real scenarios
- Build portfolio of achievements
- Plan next level of development
"""
        
        return "I've analyzed your situation using advanced reasoning to provide tailored recommendations for your specific career challenge."
