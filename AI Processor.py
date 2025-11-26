# core/ai_processor.py
import re
from collections import Counter

class AIChatProcessor:
    def __init__(self):
        self.bug_keywords = ['bug', 'error', 'broken', 'fix', 'issue', 'crash', 'fail']
        self.feature_keywords = ['feature', 'enhancement', 'improve', 'add', 'new functionality']
        self.priority_keywords = {
            'high': ['urgent', 'critical', 'blocker', 'asap', 'emergency'],
            'medium': ['important', 'should have', 'priority'],
            'low': ['nice to have', 'when possible', 'low priority']
        }
    
    def analyze_message_intent(self, message: str) -> Dict:
        """Analyze chat message to determine ticket type, priority, and components"""
        message_lower = message.lower()
        
        # Determine issue type
        issue_type = self._classify_issue_type(message_lower)
        
        # Extract priority
        priority = self._extract_priority(message_lower)
        
        # Identify potential components/labels
        labels = self._extract_labels(message_lower)
        
        # Suggest project based on content
        project = self._suggest_project(message_lower)
        
        return {
            'issue_type': issue_type,
            'priority': priority,
            'labels': labels,
            'project': project,
            'confidence_score': self._calculate_confidence(message_lower)
        }
    
    def _classify_issue_type(self, message: str) -> str:
        bug_count = sum(1 for keyword in self.bug_keywords if keyword in message)
        feature_count = sum(1 for keyword in self.feature_keywords if keyword in keyword in message)
        
        if bug_count > feature_count:
            return 'Bug'
        elif feature_count > bug_count:
            return 'Story'
        else:
            return 'Task'