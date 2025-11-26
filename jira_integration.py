import requests
import os
from datetime import datetime

class JiraManager:
    def __init__(self):
        self.jira_url = os.getenv('JIRA_URL', 'https://your-company.atlassian.net')
        self.auth = (os.getenv('JIRA_EMAIL'), os.getenv('JIRA_API_TOKEN'))
        self.ticket_counter = 1000
    
    def create_ticket(self, ticket_data):
        """Create actual Jira ticket via REST API"""
        # For demo purposes - in real implementation, this calls actual Jira API
        ticket_key = f"PROJ-{self.ticket_counter}"
        self.ticket_counter += 1
        
        payload = {
            "fields": {
                "project": {"key": "PROJ"},
                "summary": ticket_data['summary'],
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [{
                        "type": "paragraph", 
                        "content": [{"type": "text", "text": ticket_data['description']}]
                    }]
                },
                "issuetype": {"name": ticket_data.get('issuetype', 'Bug')}
            }
        }
        
        # Actual API call would be:
        # response = requests.post(
        #     f"{self.jira_url}/rest/api/3/issue",
        #     json=payload,
        #     auth=self.auth,
        #     headers={'Content-Type': 'application/json'}
        # )
        
        return {
            'key': ticket_key,
            'id': str(self.ticket_counter),
            'summary': ticket_data['summary'],
            'status': 'To Do',
            'created': datetime.now().isoformat(),
            'url': f"{self.jira_url}/browse/{ticket_key}"
        }
    
    def search_tickets(self, query, user_id):
        """Search tickets user has access to"""
        # Mock implementation - would use JQL in real scenario
        search_payload = {
            "jql": f'text ~ "{query}" AND (project = PROJ OR participants = {user_id})',
            "maxResults": 10
        }
        
        # Mock search results
        return [
            {
                'key': 'PROJ-123',
                'summary': 'Login page performance issues',
                'status': 'In Progress',
                'assignee': 'john.doe@company.com'
            },
            {
                'key': 'PROJ-456', 
                'summary': 'Add dark mode feature',
                'status': 'Backlog',
                'assignee': 'jane.smith@company.com'
            }
        ]
    
    def get_ticket_details(self, ticket_key):
        """Get full ticket details including comments"""
        # Mock implementation
        return {
            'key': ticket_key,
            'summary': 'Sample Ticket',
            'status': 'In Progress',
            'description': 'Ticket description here',
            'comments': [
                {'author': 'user1', 'body': 'Working on this', 'created': '2024-01-15T10:00:00Z'},
                {'author': 'user2', 'body': 'Any updates?', 'created': '2024-01-16T14:30:00Z'}
            ],
            'assignee': 'developer@company.com',
            'reporter': 'reporter@company.com'
        }
    
    def add_comment(self, ticket_key, comment, user_id):
        """Add comment to existing ticket"""
        # Mock implementation
        return {
            'success': True,
            'comment_id': '12345',
            'message': f'Comment added to {ticket_key}'
        }