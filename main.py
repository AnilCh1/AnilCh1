# main.py
from core.bot_integration import EnhancedJiraChatBot
from integrations.google_chat_handler import GoogleChatHandler
from analytics.efficiency_tracker import EfficiencyTracker

def main():
    # Initialize components
    jira_bot = EnhancedJiraChatBot()
    chat_handler = GoogleChatHandler(jira_bot)
    analytics = EfficiencyTracker()
    
    print("🚀 Enhanced Jira-Chat Bot Started!")
    print("Features:")
    print("✅ AI-powered ticket classification")
    print("✅ Interactive Google Chat cards") 
    print("✅ Real-time Jira integration")
    print("✅ Efficiency analytics and reporting")
    print("✅ Automated workflow optimization")
    
    # Start Flask app for Google Chat webhooks
    if __name__ == '__main__':
        chat_handler.app.run(host='0.0.0.0', port=8080, debug=True)

if __name__ == '__main__':
    main()