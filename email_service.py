import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class EmailService:
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.email_user = os.getenv('EMAIL_USER')
        self.email_password = os.getenv('EMAIL_PASSWORD')
    
    def send_ticket_notification(self, ticket_data, user_id):
        """Send email notification when ticket is created"""
        # For demo - in real scenario, this sends actual emails
        print(f"📧 [EMAIL SIMULATION] Ticket notification sent for {ticket_data['key']}")
        print(f"   To: {user_id}@company.com")
        print(f"   Subject: New Jira Ticket Created: {ticket_data['key']}")
        print(f"   Body: Ticket {ticket_data['key']} - {ticket_data['summary']}")
        
        # Actual email implementation would be:
        # msg = MIMEMultipart()
        # msg['From'] = self.email_user
        # msg['To'] = f"{user_id}@company.com"
        # msg['Subject'] = f"New Jira Ticket: {ticket_data['key']}"
        # 
        # body = f"""
        # A new Jira ticket has been created:
        # 
        # Ticket: {ticket_data['key']}
        # Summary: {ticket_data['summary']}
        # Status: {ticket_data['status']}
        # URL: {ticket_data['url']}
        # 
        # Please check Jira for updates.
        # """
        # msg.attach(MIMEText(body, 'plain'))
        # 
        # with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
        #     server.starttls()
        #     server.login(self.email_user, self.email_password)
        #     server.send_message(msg)
        
        return True