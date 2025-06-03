# TaskPro - Microservices Task Management System

A comprehensive web-based task management application built with microservices architecture. TaskPro helps students and professionals efficiently manage their academic and work tasks with intelligent features including automated due date analysis, email reminders, and productivity tracking.

## 🚀 Features

### Core Task Management
- **Task Creation**: Add tasks with title, due date, class/category, and priority levels
- **Task Tracking**: View, edit, and mark tasks as complete with an intuitive interface
- **Priority Management**: Visual priority indicators (High, Medium, Low) with color coding
- **Category Organization**: Organize tasks by class or project categories

### User Authentication
- **Simple Login**: Basic client-side authentication for demonstration
- **Account Access**: Username and password entry with immediate dashboard access
- **Demo Purpose**: Authentication is simplified for academic project showcase
- **Due Date Analysis**: Smart calculation of task urgency and optimal scheduling
- **Email Reminders**: Automated reminder system with customizable preferences
- **Productivity Statistics**: Comprehensive analytics on task completion patterns
- **Data Integration**: Seamless communication between all system components

## 🏗️ Microservices Architecture

### Main Program (Port 8000)
- **Technology**: HTML5, CSS3, JavaScript
- **Purpose**: User interface and orchestration of microservices
- **Features**: Responsive design, real-time updates, intuitive task management

### Microservice A - Credential Validation Service (Port 5000)
- **Status**: Not implemented in current version
- **Purpose**: User authentication and credential validation
- **Note**: Authentication is currently handled client-side for demonstration purposes

### Microservice B - Due Date Calculator (Port 5001)
- **Purpose**: Intelligent due date analysis and priority calculation
- **Technology**: Python Flask
- **Features**:
  - Calculates days until due date
  - Suggests optimal priority levels based on urgency
  - Provides time management recommendations
- **Endpoints**:
  - `POST /api/calculate-due-date` - Analyze task due dates
  - `GET /health` - Service health check

### Microservice C - Email Reminder Service (Port 5002)
- **Purpose**: Automated email reminder scheduling and management
- **Technology**: Python Flask
- **Features**:
  - Schedule email reminders for upcoming tasks
  - Manage user email preferences
  - Support for multiple reminder frequencies
- **Endpoints**:
  - `POST /api/reminders/schedule` - Schedule new reminders
  - `GET /api/reminders/preferences` - Get user preferences
  - `POST /api/reminders/preferences` - Update preferences
  - `GET /health` - Service health check

### Microservice D - Task Statistics Service (Port 5003)
- **Purpose**: Productivity analytics and task completion insights
- **Technology**: Python Flask
- **Features**:
  - Track task completion patterns
  - Generate productivity reports
  - Analyze performance by category
  - Calculate completion rates and trends
- **Endpoints**:
  - `POST /api/stats/record-completion` - Record task completion
  - `GET /api/stats/summary` - Get user statistics summary
  - `GET /api/stats/by-category` - Category-based analytics
  - `GET /api/stats/productivity-report` - Comprehensive productivity report
  - `GET /api/stats/dashboard-data` - Dashboard statistics
  - `GET /health` - Service health check

## 🛠️ Development Tools

### Automatic Microservice Management
Use the included startup script for easy development:
```bash
python start_microservices.py
```
This script will:
- Start all microservices automatically
- Monitor their health status
- Provide restart capabilities
- Show service URLs and status

### Testing Suite
Comprehensive test suite for all microservices:
```bash
python test_all_microservices.py
```
Tests include:
- Individual microservice functionality
- API endpoint validation
- Integration scenario testing
- Error handling verification

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser

### Dependencies
```bash
pip install flask flask-cors requests
```

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Reynaud702/taskpro.git
   cd taskpro
   ```

2. **Install dependencies**:
   ```bash
   pip install flask flask-cors requests
   ```

3. **Start all microservices** (choose one method):

   **Option A - Automatic startup (recommended):**
   ```bash
   python start_microservices.py
   ```

   **Option B - Manual startup (each in a separate terminal):**
   ```bash
   # Terminal 1 - Due Date Calculator
   python microservice_b_due_date_calculator.py

   # Terminal 2 - Email Reminder Service
   python microservice_c_email_reminder_service.py

   # Terminal 3 - Task Statistics Service
   python microservice_d_task_stats_service.py
   ```

4. **Serve the web application**:
   ```bash
   # Terminal 5 - Web Server
   python -m http.server 8000
   ```

5. **Access the application**:
   Open your browser to `http://localhost:8000`

## 🔧 Usage

### User Authentication
1. Open the application at `http://localhost:8000`
2. Enter any username and password on the welcome page
3. Click "Login" to access the dashboard (authentication is client-side only for demo)

### Adding Tasks
1. Click "Add Task" in the navigation
2. Fill in task details (title, due date, class, priority)
3. Submit to create the task

### Managing Tasks
1. View all tasks on the Dashboard
2. Check the checkbox to mark tasks complete
3. Use the priority indicators to organize your workflow

### Viewing Statistics
1. Check the Statistics widget on the Dashboard
2. Click "Refresh" to update analytics
3. Monitor your productivity trends and completion rates

### Setting Email Preferences
1. Navigate to email preferences (if implemented)
2. Configure reminder frequency and timing
3. Save preferences for automatic reminders

## 🌐 API Documentation

### Health Checks
All microservices provide health check endpoints:
- `GET http://localhost:5001/health` - Due Date Calculator
- `GET http://localhost:5002/health` - Email Reminder Service
- `GET http://localhost:5003/health` - Task Statistics Service

### Example API Calls

**Calculate Due Date Priority**:
```javascript
fetch('http://localhost:5001/api/duedate/batch-calculate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        tasks: [
            { id: 1, title: 'Assignment', due_date: '2025-06-15' }
        ]
    })
})
```

**Schedule Email Reminder**:
```javascript
fetch('http://localhost:5002/api/reminder/schedule', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        user_email: 'student@oregonstate.edu',
        task_id: 'task_123',
        task_title: 'Complete Project',
        due_date: '2025-06-15',
        priority: 'high'
    })
})
```

**Record Task Completion**:
```javascript
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
```

## 🏛️ Architecture Principles

### Microservices Communication
- **HTTP REST APIs**: All inter-service communication via HTTP requests
- **No Direct Imports**: Services are completely decoupled
- **Process Isolation**: Each service runs in its own process
- **Port-based Separation**: Each service operates on a unique port

### Data Flow
1. User interacts with the web interface
2. JavaScript makes HTTP requests to appropriate microservices
3. Microservices process requests independently
4. Results are returned and displayed in the UI
5. Statistics are automatically tracked and updated

## 🎯 Project Value

TaskPro demonstrates:
- **Microservices Architecture**: Proper service decomposition and communication
- **Full-Stack Development**: Frontend and backend integration
- **API Design**: RESTful service interfaces
- **Process Management**: Multiple service orchestration
- **User Experience**: Intuitive task management interface

## 📝 Development Notes

This project was developed as part of CS361 Software Engineering coursework, demonstrating:
- Microservices design patterns
- Service-oriented architecture
- HTTP-based inter-process communication
- Modular application development

## 🤝 Contributing

This is an academic project, but contributions and suggestions are welcome for portfolio enhancement.

## 📄 License

This project is available for educational and portfolio purposes.

---

**Note**: This application is designed for demonstration of microservices architecture and may require additional security and scalability considerations for production use.
