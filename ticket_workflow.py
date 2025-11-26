class TicketWorkflow:
    def __init__(self):
        self.access_control = {
            'default_user': ['PROJ-123', 'PROJ-456'],  # Tickets user can access
            'admin_user': ['PROJ-*']  # All tickets
        }
    
    def get_ticket_status(self, ticket_key):
        """Get latest status and comments for a ticket"""
        # Mock implementation - would fetch from Jira
        return {
            'key': ticket_key,
            'status': 'In Progress',
            'assignee': 'developer@company.com',
            'priority': 'High',
            'last_updated': '2024-01-17T09:00:00Z',
            'comments': [
                {
                    'author': 'Product Manager',
                    'timestamp': '2024-01-16T14:30:00Z', 
                    'body': 'This is critical for next release'
                },
                {
                    'author': 'Developer',
                    'timestamp': '2024-01-17T09:00:00Z',
                    'body': 'Working on the fix, ETA tomorrow'
                }
            ]
        }
    
    def search_tickets(self, query, user_id):
        """Search tickets across organization with access control"""
        accessible_tickets = self.access_control.get(user_id, [])
        
        # Mock search - in real scenario, uses Jira API with JQL
        all_tickets = [
            {'key': 'PROJ-123', 'summary': 'Login page crashes on mobile', 'status': 'In Progress'},
            {'key': 'PROJ-456', 'summary': 'Add dark mode theme', 'status': 'Backlog'},
            {'key': 'TEAM-A-789', 'summary': 'Database optimization', 'status': 'Done'},
            {'key': 'TEAM-B-101', 'summary': 'API rate limiting', 'status': 'To Do'}
        ]
        
        # Filter by access and search query
        results = []
        for ticket in all_tickets:
            if self._has_access(ticket['key'], accessible_tickets):
                if query.lower() in ticket['summary'].lower():
                    results.append(ticket)
        
        return results
    
    def add_comment(self, ticket_key, comment, user_id):
        """Add comment to ticket if user has access"""
        accessible_tickets = self.access_control.get(user_id, [])
        
        if not self._has_access(ticket_key, accessible_tickets):
            return {'success': False, 'error': 'Access denied'}
        
        # Mock implementation - would call Jira API
        print(f"💬 [COMMENT ADDED] to {ticket_key} by {user_id}: {comment}")
        
        return {
            'success': True,
            'message': f'Comment added to {ticket_key}',
            'comment_id': f'comment_{ticket_key}_{hash(comment)}'
        }
    
    def _has_access(self, ticket_key, accessible_tickets):
        """Check if user has access to specific ticket"""
        if '*' in accessible_tickets:
            return True
        
        for pattern in accessible_tickets:
            if pattern.endswith('*') and ticket_key.startswith(pattern.replace('*', '')):
                return True
            if pattern == ticket_key:
                return True
        
        return False