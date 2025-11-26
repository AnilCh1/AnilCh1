# integrations/google_chat_handler.py
from flask import Flask, request, jsonify
import threading

app = Flask(__name__)

class GoogleChatHandler:
    def __init__(self, jira_bot):
        self.jira_bot = jira_bot
        self.app = app
        
        @app.route('/webhook/chat', methods=['POST'])
        def handle_chat_event():
            return self._process_chat_event(request.json)
    
    def _process_chat_event(self, event: Dict) -> Dict:
        """Process incoming Google Chat webhook events"""
        event_type = event.get('type')
        
        if event_type == 'MESSAGE':
            return self._handle_message_event(event)
        elif event_type == 'CARD_CLICKED':
            return self._handle_card_interaction(event)
        else:
            return jsonify({'text': 'Unsupported event type'})
    
    def _handle_message_event(self, event: Dict) -> Dict:
        """Handle regular message events with interactive cards"""
        message_text = event['message']['text']
        user = event['user']
        space = event['space']
        
        # Create interactive response card
        response_card = {
            "cards": [
                {
                    "header": {
                        "title": "Create Jira Ticket",
                        "subtitle": "Automate your workflow",
                        "imageUrl": "https://example.com/jira-icon.png"
                    },
                    "sections": [
                        {
                            "widgets": [
                                {
                                    "textParagraph": {
                                        "text": f"<b>Message:</b> {message_text[:200]}..."
                                    }
                                }
                            ]
                        },
                        {
                            "widgets": [
                                {
                                    "buttons": [
                                        {
                                            "textButton": {
                                                "text": "🔄 CREATE BUG TICKET",
                                                "onClick": {
                                                    "action": {
                                                        "actionMethodName": "create_bug_ticket",
                                                        "parameters": [
                                                            {"key": "message", "value": message_text},
                                                            {"key": "user", "value": user['name']}
                                                        ]
                                                    }
                                                }
                                            }
                                        },
                                        {
                                            "textButton": {
                                                "text": "✨ CREATE FEATURE REQUEST",
                                                "onClick": {
                                                    "action": {
                                                        "actionMethodName": "create_feature_ticket",
                                                        "parameters": [
                                                            {"key": "message", "value": message_text},
                                                            {"key": "user", "value": user['name']}
                                                        ]
                                                    }
                                                }
                                            }
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }
        
        return jsonify(response_card)