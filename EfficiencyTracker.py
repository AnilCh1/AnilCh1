# analytics/efficiency_tracker.py
from datetime import datetime, timedelta
import sqlite3

class EfficiencyTracker:
    def __init__(self, db_path: str = 'efficiency_metrics.db'):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database for tracking efficiency metrics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ticket_metrics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_key TEXT,
                chat_space TEXT,
                created_at TIMESTAMP,
                creation_time_seconds REAL,
                manual_time_saved_seconds REAL,
                issue_type TEXT,
                priority TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def record_ticket_creation(self, ticket_data: Dict):
        """Record metrics for each ticket creation"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO ticket_metrics 
            (ticket_key, chat_space, created_at, creation_time_seconds, 
             manual_time_saved_seconds, issue_type, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            ticket_data['ticket_key'],
            ticket_data['chat_space'],
            datetime.now(),
            ticket_data.get('creation_time', 30),  # Default 30 seconds automated
            ticket_data.get('time_saved', 300),    # Default 5 minutes saved vs manual
            ticket_data.get('issue_type', 'Task'),
            ticket_data.get('priority', 'Medium')
        ))
        
        conn.commit()
        conn.close()
    
    def get_efficiency_report(self) -> Dict:
        """Generate efficiency report for teams"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Calculate total time saved
        cursor.execute('''
            SELECT 
                COUNT(*) as total_tickets,
                SUM(manual_time_saved_seconds) as total_time_saved_seconds,
                AVG(creation_time_seconds) as avg_creation_time
            FROM ticket_metrics
        ''')
        
        result = cursor.fetchone()
        conn.close()
        
        total_time_saved_hours = result[1] / 3600 if result[1] else 0
        
        return {
            'total_tickets_created': result[0] or 0,
            'total_time_saved_hours': round(total_time_saved_hours, 2),
            'average_creation_time_seconds': round(result[2] or 0, 2),
            'estimated_productivity_gain': f"{round((total_time_saved_hours / 8) * 100, 2)}%"  # Based on 8-hour day
        }