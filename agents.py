from random import choice

class OnboardingAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle(self, query):
        self.memory.add("OnboardingAgent", "Detected onboarding/learning issue.")
        response = LearningAgent(self.memory).handle(query)
        return response

class LearningAgent:
    def __init__(self, memory):
        self.memory = memory

    def handle(self, query):
        self.memory.add("LearningAgent", "Suggesting a learning sprint for skill gap.")
        feedback_result = FeedbackAgent(self.memory).analyze(query)
        final = f"Plan: Complete 2-week sprint on '{query}' with mentor support.\nFeedback: {feedback_result}"
        self.memory.add("LearningAgent", final)
        return final

class FeedbackAgent:
    def __init__(self, memory):
        self.memory = memory

    def analyze(self, query):
        result = choice([
            "Recent peer reviews confirm this skill gap.",
            "Performance data shows need for improvement.",
            "No strong evidence, but upskilling recommended."
        ])
        self.memory.add("FeedbackAgent", result)
        return result
