# core/bot_integration.py
import os
import requests
import json
from typing import Dict, Optional
from google.cloud import dialogflow
from datetime import datetime

class EnhancedJiraChatBot:
    def __init__(self):
        self.jira_base_url = os.getenv('JIRA_BASE_URL')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_api_token = os.getenv('JIRA_API_TOKEN')
        self.dialogflow_project = os.getenv('DIALOGFLOW_PROJECT_ID')
        
    def create_jira_ticket_from_chat(self, chat_message: str, user_info: Dict, 
                                   chat_context: Dict) -> Dict:
        """
        Enhanced ticket creation with AI-powered classification
        """
        # Analyze message intent and extract entities
        analyzed_data = self._analyze_message_intent(chat_message)
        
        # Build comprehensive Jira ticket
        ticket_data = {
            "fields": {
                "project": {"key": analyzed_data.get('project', 'GENAI')},
                "summary": self._generate_ticket_summary(chat_message, analyzed_data),
                "description": self._build_ticket_description(chat_message, user_info, chat_context, analyzed_data),
                "issuetype": {"name": analyzed_data.get('issue_type', 'Task')},
                "labels": analyzed_data.get('labels', ['chat-generated']),
                "priority": {"name": analyzed_data.get('priority', 'Medium')},
                "customfield_12345": chat_context.get('chat_space_id'),  # Chat space reference
                "customfield_12346": chat_context.get('message_id')     # Original message ID
            }
        }
        
        return self._create_jira_issue(ticket_data)