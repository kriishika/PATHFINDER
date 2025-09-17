from datetime import datetime
import json

class Memory:
    """Enhanced memory system for AI agents with conversation context and insights"""
    def __init__(self):
        self.log = []
        self.detailed_log = []
        self.conversation_context = {}
        self.user_insights = {}
        self.session_start = datetime.now()

    def add(self, agent, message, metadata=None):
        """Add a message to both simple and detailed logs"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        # Simple log for backward compatibility
        self.log.append(f"{agent}: {message}")
        
        # Detailed log with metadata
        log_entry = {
            'agent': agent,
            'message': message,
            'timestamp': timestamp,
            'full_timestamp': datetime.now().isoformat(),
            'metadata': metadata or {}
        }
        self.detailed_log.append(log_entry)

    def get_log(self):
        """Get simple log for backward compatibility"""
        return self.log

    def get_detailed_log(self):
        """Get detailed log with timestamps and metadata"""
        return self.detailed_log

    def add_user_insight(self, key, value):
        """Store insights about the user for personalization"""
        self.user_insights[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }

    def get_user_insights(self):
        """Get stored user insights"""
        return self.user_insights

    def set_conversation_context(self, key, value):
        """Set context for the current conversation"""
        self.conversation_context[key] = value

    def get_conversation_context(self, key=None):
        """Get conversation context"""
        if key:
            return self.conversation_context.get(key)
        return self.conversation_context

    def get_session_summary(self):
        """Get a summary of the current session"""
        agent_activity = {}
        for entry in self.detailed_log:
            agent = entry['agent']
            agent_activity[agent] = agent_activity.get(agent, 0) + 1

        return {
            'session_duration': str(datetime.now() - self.session_start),
            'total_interactions': len(self.detailed_log),
            'agent_activity': agent_activity,
            'user_insights_count': len(self.user_insights)
        }

    def clear_session(self):
        """Clear current session but preserve user insights"""
        self.log = []
        self.detailed_log = []
        self.conversation_context = {}
        self.session_start = datetime.now()

    def export_session(self):
        """Export session data as JSON"""
        return json.dumps({
            'session_summary': self.get_session_summary(),
            'detailed_log': self.detailed_log,
            'user_insights': self.user_insights,
            'conversation_context': self.conversation_context
        }, indent=2)

    def search_log(self, keyword):
        """Search through the conversation log"""
        results = []
        for entry in self.detailed_log:
            if keyword.lower() in entry['message'].lower():
                results.append(entry)
        return results

    def get_agent_interactions(self, agent_name):
        """Get all interactions from a specific agent"""
        return [entry for entry in self.detailed_log if entry['agent'] == agent_name]

    def get_recent_interactions(self, count=5):
        """Get the most recent interactions"""
        return self.detailed_log[-count:] if self.detailed_log else []
