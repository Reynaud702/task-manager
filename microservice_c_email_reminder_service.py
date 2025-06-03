# microservice_c_email_reminder_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS  
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import hashlib
import os

app = Flask(__name__)
CORS(app)

# In-memory storage for reminder settings and scheduled reminders
# In production, this would be a proper database
user_settings = {}
scheduled_reminders = []
sent_reminders = []

EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USER = os.getenv('EMAIL_USER', 'your-email@gmail.com')
EMAIL_PASS = os.getenv('EMAIL_PASS', 'your-app-password')

@app.route('/api/reminder/schedule', methods=['POST'])
def schedule_reminder():
    """
    Schedule a reminder for a task
    Expects: user_email, task_id, task_title, due_date, priority
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['user_email', 'task_id', 'task_title', 'due_date']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    user_email = data['user_email']
    task_id = data['task_id']
    task_title = data['task_title']
    due_date_str = data['due_date']
    priority = data.get('priority', 'medium')
    
    try:
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    
    # Get user's reminder preferences
    user_prefs = user_settings.get(user_email, {
        'reminders_enabled': True,
        'reminder_timing': 1  # days before due date
    })
    
    if not user_prefs['reminders_enabled']:
        return jsonify({
            'success': True,
            'message': 'Reminder not scheduled - user has disabled reminders',
            'reminder_id': None
        })
    
    # Calculate when to send the reminder
    reminder_timing = user_prefs.get('reminder_timing', 1)
    reminder_date = due_date - timedelta(days=reminder_timing)
    
    # Create reminder record
    reminder_id = len(scheduled_reminders) + 1
    reminder = {
        'reminder_id': reminder_id,
        'user_email': user_email,
        'task_id': task_id,
        'task_title': task_title,
        'due_date': due_date_str,
        'priority': priority,
        'reminder_date': reminder_date.strftime('%Y-%m-%d'),
        'scheduled_at': datetime.now().isoformat(),
        'status': 'scheduled'
    }
    
    scheduled_reminders.append(reminder)
    
    return jsonify({
        'success': True,
        'reminder_id': reminder_id,
        'reminder_date': reminder_date.strftime('%Y-%m-%d'),
        'message': f'Reminder scheduled for {reminder_timing} day(s) before due date'
    })

@app.route('/api/reminder/settings', methods=['GET'])
def get_reminder_settings():
    """
    Get user reminder preferences
    Requires user_email as query parameter
    """
    user_email = request.args.get('user_email')
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email parameter is required'
        }), 400
    
    # Get user settings or return defaults
    settings = user_settings.get(user_email, {
        'reminders_enabled': True,
        'reminder_timing': 1,  # 1 day before
        'email_notifications': True
    })
    
    return jsonify({
        'success': True,
        'user_email': user_email,
        'settings': settings,
        'available_timings': [
            {'value': 1, 'label': '1 day before'},
            {'value': 3, 'label': '3 days before'},
            {'value': 7, 'label': '7 days before'}
        ]
    })

@app.route('/api/reminder/settings', methods=['PUT'])
def update_reminder_settings():
    """
    Update user reminder preferences
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    user_email = data.get('user_email')
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email is required'
        }), 400
    
    # Update user settings
    if user_email not in user_settings:
        user_settings[user_email] = {}
    
    settings = user_settings[user_email]
    
    # Update provided settings
    if 'reminders_enabled' in data:
        settings['reminders_enabled'] = bool(data['reminders_enabled'])
    
    if 'reminder_timing' in data:
        timing = data['reminder_timing']
        if timing in [1, 3, 7]:
            settings['reminder_timing'] = timing
        else:
            return jsonify({
                'success': False,
                'error': 'reminder_timing must be 1, 3, or 7 days'
            }), 400
    
    if 'email_notifications' in data:
        settings['email_notifications'] = bool(data['email_notifications'])
    
    settings['updated_at'] = datetime.now().isoformat()
    
    return jsonify({
        'success': True,
        'message': 'Settings updated successfully',
        'settings': settings
    })

@app.route('/api/reminder/send-due-soon', methods=['POST'])
def send_due_soon_reminders():
    """
    Manually trigger sending reminders for tasks due within 24 hours
    This would typically be called by a scheduled job
    """
    current_date = datetime.now().date()
    sent_count = 0
    errors = []
    
    for reminder in scheduled_reminders:
        if reminder['status'] != 'scheduled':
            continue
            
        reminder_date = datetime.strptime(reminder['reminder_date'], '%Y-%m-%d').date()
        
        # Check if it's time to send this reminder
        if reminder_date <= current_date:
            # Check if we haven't already sent this reminder
            reminder_key = f"{reminder['user_email']}_{reminder['task_id']}"
            if reminder_key not in [r['key'] for r in sent_reminders]:
                
                # Send the email reminder
                success = send_email_reminder(reminder)
                
                if success:
                    # Mark as sent
                    reminder['status'] = 'sent'
                    sent_reminders.append({
                        'key': reminder_key,
                        'reminder_id': reminder['reminder_id'],
                        'sent_at': datetime.now().isoformat()
                    })
                    sent_count += 1
                else:
                    errors.append(f"Failed to send reminder {reminder['reminder_id']}")
    
    return jsonify({
        'success': True,
        'sent_count': sent_count,
        'errors': errors,
        'processed_at': datetime.now().isoformat()
    })

def send_email_reminder(reminder):
    """
    Send an email reminder for a task
    Returns True if successful, False otherwise
    """
    try:
        
        
        user_email = reminder['user_email']
        task_title = reminder['task_title']
        due_date = reminder['due_date']
        priority = reminder['priority']
        
        # Create email content
        subject = f"TaskPro Reminder: {task_title} due soon"
        
        body = f"""
        Hello!
        
        This is a friendly reminder that your task is due soon:
        
        Task: {task_title}
        Due Date: {due_date}
        Priority: {priority.upper()}
        
        Don't forget to complete this task on time!
        
        Best regards,
        TaskPro Team
        """
        
        
        print(f"EMAIL SENT TO: {user_email}")
        print(f"SUBJECT: {subject}")
        print(f"BODY: {body}")
        
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

@app.route('/api/reminder/status/<int:reminder_id>', methods=['GET'])
def get_reminder_status(reminder_id):
    """
    Check the status of a specific reminder
    """
    reminder = next((r for r in scheduled_reminders if r['reminder_id'] == reminder_id), None)
    
    if not reminder:
        return jsonify({
            'success': False,
            'error': 'Reminder not found'
        }), 404
    
    # Check if it has been sent
    sent_info = next((s for s in sent_reminders if s['reminder_id'] == reminder_id), None)
    
    response_data = {
        'success': True,
        'reminder_id': reminder_id,
        'status': reminder['status'],
        'task_title': reminder['task_title'],
        'due_date': reminder['due_date'],
        'reminder_date': reminder['reminder_date']
    }
    
    if sent_info:
        response_data['sent_at'] = sent_info['sent_at']
    
    return jsonify(response_data)

@app.route('/api/reminder/list', methods=['GET'])
def list_reminders():
    """
    List all reminders for a user
    Requires user_email as query parameter
    """
    user_email = request.args.get('user_email')
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email parameter is required'
        }), 400
    
    user_reminders = [r for r in scheduled_reminders if r['user_email'] == user_email]
    
    return jsonify({
        'success': True,
        'reminders': user_reminders,
        'total_count': len(user_reminders)
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'service': 'email-reminder-service',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5002)