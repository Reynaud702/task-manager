TaskPro - Microservices Task Management System
A comprehensive web-based task management application built with microservices architecture. TaskPro helps students and professionals efficiently manage their academic and work tasks with intelligent features including automated due date analysis, email reminders, and productivity tracking.

🚀 Features
Core Task Management
Task Creation: Add tasks with title, due date, class/category, and priority levels
Task Tracking: View, edit, and mark tasks as complete with an intuitive interface
Priority Management: Visual priority indicators (High, Medium, Low) with color coding
Category Organization: Organize tasks by class or project categories
User Authentication
Secure Login: User credential validation through dedicated authentication service
Account Management: User registration and login functionality
Session Security: Secure authentication handling and user session management
Due Date Analysis: Smart calculation of task urgency and optimal scheduling
Email Reminders: Automated reminder system with customizable preferences
Productivity Statistics: Comprehensive analytics on task completion patterns
Data Integration: Seamless communication between all system components

🏗️ Microservices Architecture
Main Program (Port 8000)
Technology: HTML5, CSS3, JavaScript
Purpose: User interface and orchestration of microservices
Features: Responsive design, real-time updates, intuitive task management
Microservice A - Credential Validation Service (Port 5000)
Purpose: User authentication and credential validation
Technology: Python Flask
Features:
Validate user login credentials
Secure authentication handling
User session management
Endpoints:
POST /api/auth/login - Validate user credentials
POST /api/auth/signup - Register new users
GET /health - Service health check
Microservice B - Due Date Calculator (Port 5001)
Purpose: Intelligent due date analysis and priority calculation
Technology: Python Flask
Features:
Calculates days until due date
Suggests optimal priority levels based on urgency
Provides time management recommendations
Endpoints:
POST /api/calculate-due-date - Analyze task due dates
GET /health - Service health check
Microservice C - Email Reminder Service (Port 5002)
Purpose: Automated email reminder scheduling and management
Technology: Python Flask
Features:
Schedule email reminders for upcoming tasks
Manage user email preferences
Support for multiple reminder frequencies
Endpoints:
POST /api/reminders/schedule - Schedule new reminders
GET /api/reminders/preferences - Get user preferences
POST /api/reminders/preferences - Update preferences
GET /health - Service health check
Microservice D - Task Statistics Service (Port 5003)
Purpose: Productivity analytics and task completion insights
Technology: Python Flask
Features:
Track task completion patterns
Generate productivity reports
Analyze performance by category
Calculate completion rates and trends
Endpoints:
POST /api/stats/record-completion - Record task completion
GET /api/stats/summary - Get user statistics summary
GET /api/stats/by-category - Category-based analytics
GET /api/stats/productivity-report - Comprehensive productivity report
GET /api/stats/dashboard-data - Dashboard statistics
GET /health - Service health check
🛠️ Installation & Setup
Prerequisites
Python 3.7 or higher
pip (Python package installer)
Modern web browser
Dependencies
bash
pip install flask flask-cors
Quick Start
Clone the repository:
bash
git clone https://github.com/Reynaud702/taskpro.git
cd taskpro
Install dependencies:
bash
pip install flask flask-cors
Start all microservices (each in a separate terminal):
bash
# Terminal 1 - Credential Validation Service
python microservice_a_credential_validation.py

# Terminal 2 - Due Date Calculator
python microservice_b_due_date_calculator.py

# Terminal 3 - Email Reminder Service
python microservice_c_email_reminder_service.py

# Terminal 4 - Task Statistics Service
python microservice_d_task_stats_service.py
Serve the web application:
bash
# Terminal 5 - Web Server
python -m http.server 8000
Access the application: Open your browser to http://localhost:8000

🔧 Usage
User Authentication
Open the application at http://localhost:8000
Enter your username and password on the welcome page
Click "Login" to authenticate or "Sign Up" to create a new account
The credential validation service securely processes your authentication
Adding Tasks
Click "Add Task" in the navigation
Fill in task details (title, due date, class, priority)
Submit to create the task
Managing Tasks
View all tasks on the Dashboard
Check the checkbox to mark tasks complete
Use the priority indicators to organize your workflow
Viewing Statistics
Check the Statistics widget on the Dashboard
Click "Refresh" to update analytics
Monitor your productivity trends and completion rates
Setting Email Preferences
Navigate to email preferences (if implemented)
Configure reminder frequency and timing
Save preferences for automatic reminders

🌐 API Documentation
Health Checks
All microservices provide health check endpoints:
GET http://localhost:5000/health
GET http://localhost:5001/health
GET http://localhost:5002/health
GET http://localhost:5003/health
Example API Calls
Authenticate User:
javascript
fetch('http://localhost:5000/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        username: 'user123',
        password: 'securepassword'
    })
})
Calculate Due Date Priority:
javascript
fetch('http://localhost:5001/api/calculate-due-date', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        due_date: '2024-12-15',
        current_priority: 'medium'
    })
})
Record Task Completion:
javascript
fetch('http://localhost:5003/api/stats/record-completion', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        task_id: 'task_123',
        user_email: 'user@example.com',
        task_title: 'Complete Project',
        category: 'CS361'
    })
})

🏛️ Architecture Principles
Microservices Communication
HTTP REST APIs: All inter-service communication via HTTP requests
No Direct Imports: Services are completely decoupled
Process Isolation: Each service runs in its own process
Port-based Separation: Each service operates on a unique port
Data Flow
User interacts with the web interface
JavaScript makes HTTP requests to appropriate microservices
Microservices process requests independently
Results are returned and displayed in the UI
Statistics are automatically tracked and updated

🎯 Project Value
TaskPro demonstrates:
Microservices Architecture: Proper service decomposition and communication
Full-Stack Development: Frontend and backend integration
API Design: RESTful service interfaces
Process Management: Multiple service orchestration
User Experience: Intuitive task management interface

📝 Development Notes
This project was developed as part of CS361 Software Engineering coursework, demonstrating:
Microservices design patterns
Service-oriented architecture
HTTP-based inter-process communication
Modular application development

🤝 Contributing
This is an academic project, but contributions and suggestions are welcome for portfolio enhancement.

📄 License
This project is available for educational and portfolio purposes.
