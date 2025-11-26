# integrations/jira_client.py
import requests
from requests.auth import HTTPBasicAuth

class AdvancedJiraClient:
    def __init__(self, base_url: str, email: str, api_token: str):
        self.base_url = base_url
        self.auth = HTTPBasicAuth(email, api_token)
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
    
    def create_issue(self, ticket_data: Dict) -> Dict:
        """Create Jira issue with enhanced error handling"""
        url = f"{self.base_url}/rest/api/3/issue"
        
        try:
            response = requests.post(
                url,
                json=ticket_data,
                headers=self.headers,
                auth=self.auth
            )
            
            if response.status_code == 201:
                issue_data = response.json()
                return {
                    'success': True,
                    'issue_key': issue_data['key'],
                    'issue_url': f"{self.base_url}/browse/{issue_data['key']}",
                    'message': f"✅ Ticket {issue_data['key']} created successfully!"
                }
            else:
                return {
                    'success': False,
                    'error': f"Jira API error: {response.status_code} - {response.text}",
                    'message': "❌ Failed to create Jira ticket"
                }
                
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': "❌ Error connecting to Jira"
            }
    
    def get_issue_status(self, issue_key: str) -> Dict:
        """Check status of created issue for feedback"""
        url = f"{self.base_url}/rest/api/3/issue/{issue_key}"
        
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            issue_data = response.json()
            return {
                'status': issue_data['fields']['status']['name'],
                'assignee': issue_data['fields'].get('assignee', {}).get('displayName', 'Unassigned'),
                'summary': issue_data['fields']['summary']
            }
        return {'status': 'Unknown'}