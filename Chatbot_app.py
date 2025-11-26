from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Initialize data storage
tickets = []
ticket_counter = 1000

# Common suggestions for quick ticket creation
COMMON_SUGGESTIONS = {
    'bug': [
        "App crashes on startup",
        "API unavailable",
        "Login not working", 
        "Mobile app performance slow",
        "Interactive element has no hover state",
        "Broken layout on specific screen sizes",
        "Animation has low performance",
        "Page not loading",
        "Other"
    ],
    'feature': [
        "Version Control on Git",
        "Responsive Design",
        "Asset Optimization",
        "API Integration", 
        "Design System Integration",
        "TypeScript Support",
        "API integration",
        "Other"
    ],
    'task': [
        "Update documentation",
        "cross-browser compatibility",
        "Database optimization",
        "Integrate with backend APIs",
        "components for performance",
        "Performance testing",
        "validate design specifications",
        "Deploy features in staging environments",
        "debug performance issues",
        "UI functionality across devices", 
        "Other"
    ]
}

# Demo tickets for status tracking
DEMO_TICKETS = [
    {
        'key': 'BUG-1001',
        'summary': 'Mobile app crashes on login page',
        'description': 'App crashes immediately when users try to login on iOS devices',
        'issue_type': 'Bug',
        'status': 'In Progress',
        'priority': 'High',
        'reporter': 'qa-team@company.com',
        'assignee': 'mobile-dev@company.com',
        'created': '2024-01-15T10:00:00',
        'updated': '2024-01-17T14:30:00',
        'comments': [
            {
                'author': 'QA Team',
                'timestamp': '2024-01-15T10:00:00',
                'body': 'Issue reproduced on iOS 15 and 16 devices'
            },
            {
                'author': 'Mobile Developer',
                'timestamp': '2024-01-17T14:30:00',
                'body': 'Identified the root cause - memory leak in authentication module. Working on fix.'
            }
        ]
    }
]

@app.route('/')
def home():
    """Main ChatBot Interface"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Jira ChatBot - Complete System</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            margin: 40px; 
            background: #f5f5f5; 
        }
        .container { 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            padding: 30px; 
            border-radius: 10px; 
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .dashboard { 
            display: grid; 
            grid-template-columns: 1fr 1fr; 
            gap: 20px; 
            margin: 20px 0; 
        }
        .panel { 
            background: #f8f9fa; 
            padding: 20px; 
            border-radius: 8px; 
            border: 1px solid #e1e5e9;
        }
        .chat-container { 
            background: white; 
            padding: 15px; 
            border-radius: 8px; 
            margin: 15px 0; 
            max-height: 400px; 
            overflow-y: auto;
            border: 1px solid #e1e5e9;
        }
        .message { 
            background: white; 
            padding: 12px 15px; 
            margin: 8px 0; 
            border-radius: 8px; 
            border-left: 4px solid #2196f3; 
        }
        .bot-message { 
            border-left-color: #4caf50; 
            background: #e8f5e8; 
        }
        .user-message { 
            border-left-color: #ffc107; 
            background: #fff3cd; 
        }
        .button { 
            background: #2196f3; 
            color: white; 
            padding: 12px 20px; 
            border: none; 
            border-radius: 6px; 
            cursor: pointer; 
            margin: 5px; 
            font-size: 14px;
        }
        .button:hover { 
            background: #1976d2; 
        }
        .suggestion-btn { 
            background: #666; 
            color: white; 
            padding: 8px 12px; 
            border: none; 
            border-radius: 4px; 
            cursor: pointer; 
            margin: 3px; 
            font-size: 12px;
        }
        .suggestion-btn:hover { 
            background: #555; 
        }
        .other-btn { 
            background: #ff9800; 
        }
        .other-btn:hover { 
            background: #f57c00; 
        }
        .ticket-card { 
            background: white; 
            padding: 15px; 
            margin: 10px 0; 
            border-radius: 8px; 
            border: 1px solid #e1e5e9;
        }
        .input-group { 
            margin: 15px 0; 
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .user-input { 
            flex: 1; 
            padding: 12px; 
            border: 2px solid #e1e5e9; 
            border-radius: 6px; 
            font-size: 14px;
        }
        .user-input:focus {
            border-color: #2196f3;
            outline: none;
        }
        .suggestions-container {
            margin: 10px 0;
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        .calendar-container {
            margin: 10px 0;
            padding: 15px;
            background: #f8f9fa;
            border-radius: 8px;
            border: 1px solid #e1e5e9;
        }
        .calendar-grid {
            display: grid;
            grid-template-columns: repeat(7, 1fr);
            gap: 5px;
            margin: 10px 0;
        }
        .calendar-header {
            grid-column: 1 / -1;
            text-align: center;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .calendar-day {
            padding: 8px;
            text-align: center;
            border: 1px solid #e1e5e9;
            border-radius: 4px;
            cursor: pointer;
            background: white;
            font-size: 12px;
        }
        .calendar-day:hover {
            background: #2196f3;
            color: white;
        }
        .calendar-day.disabled {
            background: #f5f5f5;
            color: #ccc;
            cursor: not-allowed;
        }
        .calendar-day.today {
            background: #ffeb3b;
            font-weight: bold;
        }
        .calendar-day.selected {
            background: #2196f3;
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Jira ChatBot</h1>
        <p>Create tickets, track status, and get updates - all in one place!</p>
        
        <div class="dashboard">
            <!-- Left Panel: Ticket Creation -->
            <div class="panel">
                <h3>🎫 Create New Ticket</h3>
                <div style="text-align: center; margin-bottom: 15px;">
                    <button class="button" onclick="startWorkflow('bug')">🐛 Report Bug</button>
                    <button class="button" onclick="startWorkflow('feature')">✨ Request Feature</button>
                    <button class="button" onclick="startWorkflow('task')">📋 Create Task</button>
                </div>
                
                <div class="chat-container" id="chatContainer">
                    <div class="message bot-message">
                        <strong>Jira Bot:</strong> Hello! Click a button or type directly to create tickets.
                    </div>
                </div>
                
                <div class="suggestions-container" id="suggestionsArea"></div>
                
                <div class="input-group">
                    <input type="text" class="user-input" id="userInput" placeholder="Type your message here...">
                    <button class="button" id="submitBtn" onclick="processUserResponse()">Submit</button>
                    <button class="button" onclick="cancelWorkflow()" style="background: #f44336;">Cancel</button>
                </div>
            </div>

            <!-- Right Panel: Status & Updates -->
            <div class="panel">
                <h3>📊 Track & Search</h3>
                <div style="text-align: center; margin-bottom: 15px;">
                    <button class="button" onclick="loadLatestUpdates()">🔄 Latest Updates</button>
                    <button class="button" onclick="showAllTickets()">📋 All Tickets</button>
                </div>
                
                <div class="input-group">
                    <input type="text" class="user-input" id="searchInput" placeholder="Search tickets...">
                    <button class="button" onclick="searchTickets()">🔍 Search</button>
                </div>
                
                <div id="statusResults">
                    <div class="message bot-message">
                        Use buttons above to check status or search tickets.
                    </div>
                </div>
            </div>
        </div>

        <!-- Results Area -->
        <div id="resultsArea"></div>
    </div>

    <script>
        // === VARIABLE DEFINITIONS ===
        let currentWorkflow = null;
        let currentStep = 0;
        let workflowData = {};

        const COMMON_SUGGESTIONS = {
            bug: [
                "App crashes on startup",
                "API unavailable",
                "Login not working", 
                "Mobile app performance slow",
                "Interactive element has no hover state",
                "Broken layout on specific screen sizes",
                "Animation has low performance",
                "Page not loading",
                "Other"
            ],
            feature: [
                "Version Control on Git",
                "Responsive Design",
                "Asset Optimization",
                "API Integration", 
                "Design System Integration",
                "TypeScript Support",
                "API integration",
                "Other"
            ],
            task: [
                "Update documentation",
                "cross-browser compatibility",
                "Database optimization",
                "Integrate with backend APIs",
                "components for performance",
                "Performance testing",
                "validate design specifications",
                "Deploy features in staging environments",
                "debug performance issues",
                "UI functionality across devices", 
                "Other"
            ]
        };

        const workflows = {
            bug: {
                name: "Bug Report",
                steps: [
                    { 
                        question: "What's the issue? Choose from common bugs or describe your own:",
                        field: "title", 
                        suggestions: COMMON_SUGGESTIONS.bug 
                    },
                    { 
                        question: "Please describe the bug in detail:",
                        field: "description" 
                    },
                    { 
                        question: "What are the steps to reproduce this issue?",
                        field: "steps" 
                    },
                    { 
                        question: "What's the priority level?",
                        field: "priority",
                        suggestions: ["High - System down/critical", "Medium - Major functionality affected", "Low - Minor issue"] 
                    }
                ]
            },
            feature: {
                name: "Feature Request", 
                steps: [
                    { 
                        question: "What feature would you like? Choose from common requests or describe your own:",
                        field: "title",
                        suggestions: COMMON_SUGGESTIONS.feature 
                    },
                    { 
                        question: "Please describe the feature in detail:",
                        field: "description" 
                    },
                    { 
                        question: "What business value does this provide?",
                        field: "business_value" 
                    }
                ]
            },
            task: {
                name: "Task",
                steps: [
                    { 
                        question: "What task needs to be done? Choose from common tasks or describe your own:",
                        field: "title", 
                        suggestions: COMMON_SUGGESTIONS.task 
                    },
                    { 
                        question: "Please describe the task:",
                        field: "description" 
                    },
                    { 
                        question: "When is this due? (YYYY-MM-DD)",
                        field: "due_date"
                    }
                ]
            }
        };

        // === NATURAL LANGUAGE PROCESSING ===
        function processNaturalLanguage(input) {
            const text = input.toLowerCase().trim();
            console.log("Processing:", text);
            
            if (text.includes('bug') || text.includes('error') || text.includes('crash') || text.includes('not working')) {
                startWorkflow('bug');
                addBotMessage("I'll help you report a bug. Let me ask a few questions...");
            }
            else if (text.includes('feature') || text.includes('new') || text.includes('add')) {
                startWorkflow('feature');
                addBotMessage("Great! Let's create a feature request...");
            }
            else if (text.includes('task') || text.includes('todo') || text.includes('work')) {
                startWorkflow('task');
                addBotMessage("I'll help you create a task. Let's get the details...");
            }
            else if (text.includes('status') || text.includes('check')) {
                addBotMessage("Use the search box to check ticket status.");
            }
            else if (text.includes('search') || text.includes('find')) {
                addBotMessage("Use the search box to find tickets.");
            }
            else if (text.includes('help')) {
                showHelp();
            }
            else {
                addBotMessage("I can help you create tickets! Try: 'report a bug', 'new feature', or 'create task'.");
            }
        }

        function showHelp() {
            addBotMessage(`I can help you with:
🎫 Create Tickets: "report a bug", "new feature", "create task"
📊 Check Status: Use search box
🔍 Search: Use search box to find tickets`);
        }

        // === CORE WORKFLOW FUNCTIONS ===
        function startWorkflow(type) {
            currentWorkflow = type;
            currentStep = 0;
            workflowData = {};
            addBotMessage(`Starting ${workflows[type].name} workflow...`);
            askNextQuestion();
        }

        function askNextQuestion() {
            const step = workflows[currentWorkflow].steps[currentStep];
            addBotMessage(step.question);
            
            if (step.suggestions) {
                showSuggestions(step.suggestions, step.field);
            } else {
                enableTextInput();
            }
        }

        function showSuggestions(suggestions, field) {
            const area = document.getElementById('suggestionsArea');
            area.innerHTML = '';
            
            suggestions.forEach(suggestion => {
                const button = document.createElement('button');
                button.className = suggestion === 'Other' ? 'suggestion-btn other-btn' : 'suggestion-btn';
                button.textContent = suggestion;
                button.onclick = () => {
                    if (suggestion === 'Other') {
                        enableTextInput();
                        addBotMessage("Please describe in your own words:");
                    } else {
                        handleSuggestionSelection(suggestion, field);
                    }
                };
                area.appendChild(button);
            });
        }

        function handleSuggestionSelection(suggestion, field) {
            workflowData[field] = suggestion;
            addUserMessage(suggestion);
            document.getElementById('suggestionsArea').innerHTML = '';
            moveToNextStep();
        }

        function enableTextInput() {
            document.getElementById('userInput').disabled = false;
            document.getElementById('submitBtn').disabled = false;
            document.getElementById('userInput').focus();
            document.getElementById('suggestionsArea').innerHTML = '';
        }

        function processUserResponse() {
            const input = document.getElementById('userInput').value.trim();
            if (!input) {
                alert('Please enter a response');
                return;
            }

            addUserMessage(input);
            document.getElementById('userInput').value = '';
            
            if (currentWorkflow) {
                const step = workflows[currentWorkflow].steps[currentStep];
                workflowData[step.field] = input;
                moveToNextStep();
            } else {
                processNaturalLanguage(input);
            }
        }

        function moveToNextStep() {
            currentStep++;
            if (currentStep < workflows[currentWorkflow].steps.length) {
                askNextQuestion();
            } else {
                completeWorkflow();
            }
        }

        function completeWorkflow() {
            addBotMessage("Creating your ticket...");
            
            fetch('/complete-workflow', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    workflow_type: currentWorkflow,
                    data: workflowData
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showTicketResult(data.ticket);
                    addBotMessage(data.message);
                } else {
                    addBotMessage("❌ Failed to create ticket");
                }
            })
            .catch(error => {
                addBotMessage("❌ Error creating ticket");
            });
        }

        function showTicketResult(ticket) {
            const resultsArea = document.getElementById('resultsArea');
            resultsArea.innerHTML = `
                <div class="ticket-card" style="background: #e8f5e8; border-left: 4px solid #4caf50;">
                    <h3>✅ Ticket Created Successfully!</h3>
                    <p><strong>Ticket ID:</strong> ${ticket.key}</p>
                    <p><strong>Title:</strong> ${ticket.summary}</p>
                    <p><strong>Type:</strong> ${ticket.issue_type}</p>
                    <p><strong>Status:</strong> ${ticket.status}</p>
                    <p><strong>Priority:</strong> ${ticket.priority}</p>
                    <p><strong>Reporter:</strong> ${ticket.reporter}</p>
                    <p>📧 Email notification sent to your team!</p>
                </div>
            `;
            resetWorkflow();
        }

        // === STATUS & SEARCH FUNCTIONS ===
        function loadLatestUpdates() {
            fetch('/latest-updates')
            .then(response => response.json())
            .then(data => {
                let html = '<h4>🔄 Recently Updated Tickets:</h4>';
                data.tickets.forEach(ticket => {
                    html += `
                        <div class="ticket-card">
                            <strong>${ticket.key}</strong>: ${ticket.summary}<br>
                            <small>Status: ${ticket.status} | Updated: ${new Date(ticket.updated).toLocaleDateString()}</small>
                        </div>
                    `;
                });
                document.getElementById('statusResults').innerHTML = html;
            });
        }

        function showAllTickets() {
            fetch('/search-tickets?q=')
            .then(response => response.json())
            .then(data => {
                let html = '<h4>📋 All Tickets:</h4>';
                data.tickets.forEach(ticket => {
                    html += `
                        <div class="ticket-card">
                            <strong>${ticket.key}</strong>: ${ticket.summary}<br>
                            <small>Type: ${ticket.issue_type} | Status: ${ticket.status}</small>
                        </div>
                    `;
                });
                document.getElementById('statusResults').innerHTML = html;
            });
        }

        function searchTickets() {
            const query = document.getElementById('searchInput').value;
            fetch('/search-tickets?q=' + encodeURIComponent(query))
            .then(response => response.json())
            .then(data => {
                let html = `<h4>🔍 Search Results (${data.count} tickets):</h4>`;
                data.tickets.forEach(ticket => {
                    html += `
                        <div class="ticket-card">
                            <strong>${ticket.key}</strong>: ${ticket.summary}<br>
                            <small>Status: ${ticket.status} | Priority: ${ticket.priority}</small>
                        </div>
                    `;
                });
                document.getElementById('statusResults').innerHTML = html;
            });
        }

        // === UTILITY FUNCTIONS ===
        function cancelWorkflow() {
            resetWorkflow();
            addBotMessage("Workflow cancelled.");
        }

        function resetWorkflow() {
            currentWorkflow = null;
            currentStep = 0;
            workflowData = {};
            document.getElementById('userInput').disabled = false;
            document.getElementById('submitBtn').disabled = false;
            document.getElementById('userInput').value = '';
            document.getElementById('suggestionsArea').innerHTML = '';
        }

        function addBotMessage(text) {
            addMessage(text, 'bot-message');
        }

        function addUserMessage(text) {
            addMessage(text, 'user-message');
        }

        function addMessage(text, className) {
            const container = document.getElementById('chatContainer');
            const div = document.createElement('div');
            div.className = `message ${className}`;
            div.innerHTML = `<strong>${className === 'bot-message' ? 'Jira Bot' : 'You'}:</strong> ${text}`;
            container.appendChild(div);
            container.scrollTop = container.scrollHeight;
        }

        // === INITIALIZATION ===
        document.addEventListener('DOMContentLoaded', function() {
            addBotMessage("Ready to help! Type 'bug', 'feature', or 'task' to start, or click buttons.");
            
            // Enter key support
            document.getElementById('userInput').addEventListener('keypress', function(event) {
                if (event.key === 'Enter') {
                    event.preventDefault();
                    processUserResponse();
                }
            });
        });
    </script>
</body>
</html>
'''

@app.route('/complete-workflow', methods=['POST'])
def complete_workflow():
    global ticket_counter
    ticket_counter += 1
    
    data = request.json
    workflow_type = data.get('workflow_type')
    user_data = data.get('data', {})
    
    print(f"🎫 Creating ticket - Type: {workflow_type}")
    
    # Generate ticket based on workflow type
    if workflow_type == 'bug':
        ticket_key = f'BUG-{ticket_counter}'
        issue_type = 'Bug'
        priority = 'High' if 'High' in user_data.get('priority', '') else 'Medium'
    elif workflow_type == 'feature':
        ticket_key = f'FEAT-{ticket_counter}'
        issue_type = 'Story'
        priority = 'Medium'
    else:
        ticket_key = f'TASK-{ticket_counter}'
        issue_type = 'Task'
        priority = 'Low'
    
    # Create ticket data
    ticket_data = {
        'key': ticket_key,
        'summary': user_data.get('title', 'Untitled'),
        'description': user_data.get('description', 'No description'),
        'issue_type': issue_type,
        'status': 'To Do',
        'priority': priority,
        'reporter': 'user@company.com',
        'created': datetime.datetime.now().isoformat(),
        'updated': datetime.datetime.now().isoformat()
    }
    
    # Store the ticket
    tickets.append(ticket_data)
    
    print(f"✅ TICKET CREATED: {ticket_key}")
    print(f"   Title: {ticket_data['summary']}")
    
    return jsonify({
        'success': True,
        'ticket': ticket_data,
        'message': f"✅ Ticket {ticket_key} Created!\\n\\n📋 **{ticket_data['summary']}**\\n• Type: {issue_type}\\n• Status: {ticket_data['status']}\\n• Priority: {priority}\\n• Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\\n\\n📧 Email notification sent to your team!"
    })

@app.route('/latest-updates')
def get_latest_updates():
    all_tickets = tickets + DEMO_TICKETS
    recent_tickets = sorted(all_tickets, key=lambda x: x['updated'], reverse=True)[:5]
    return jsonify({'tickets': recent_tickets})

@app.route('/search-tickets')
def search_tickets():
    query = request.args.get('q', '').lower()
    all_tickets = tickets + DEMO_TICKETS
    
    if query:
        matching_tickets = [t for t in all_tickets if query in t['summary'].lower() or query in t['key'].lower()]
    else:
        matching_tickets = all_tickets
    
    return jsonify({'tickets': matching_tickets, 'count': len(matching_tickets)})

@app.route('/ticket-status/<ticket_key>')
def get_ticket_status(ticket_key):
    all_tickets = tickets + DEMO_TICKETS
    ticket = next((t for t in all_tickets if t['key'].upper() == ticket_key.upper()), None)
    
    if ticket:
        return jsonify({'success': True, 'ticket': ticket})
    else:
        return jsonify({'success': False, 'error': f'Ticket {ticket_key} not found'})

if __name__ == '__main__':
    print("🚀 Jira ChatBot Starting...")
    print("📍 Open: http://localhost:5000")
    print("✅ Features: Ticket creation, status tracking, search")
    app.run(debug=True, port=5000)