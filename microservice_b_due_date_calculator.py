# microservice_b_due_date_calculator.py
from flask import Flask, request, jsonify
from flask_cors import CORS  # Add this import
from datetime import datetime, timedelta
import json

app = Flask(__name__)
CORS(app) 

sample_tasks = {
    1: {"title": "CS361 Assignment 3", "due_date": "2025-06-05", "priority": "high"},
    2: {"title": "Math Homework", "due_date": "2025-06-03", "priority": "medium"},
    3: {"title": "History Essay", "due_date": "2025-06-10", "priority": "low"}
}

@app.route('/api/duedate/calculate/<int:task_id>', methods=['GET'])
def calculate_due_date(task_id):
    """
    Calculate days remaining and status for a specific task
    Returns: days remaining, status (overdue/urgent/normal), and priority suggestion
    """
    
   
    due_date_str = request.args.get('due_date')
    
    if not due_date_str and task_id not in sample_tasks:
        return jsonify({
            'success': False,
            'error': 'Task not found and no due_date provided'
        }), 404
    
    if due_date_str:
        # Use provided due date
        try:
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d')
        except ValueError:
            return jsonify({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }), 400
    else:
        # Use sample task data
        task = sample_tasks[task_id]
        due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
    
    current_date = datetime.now()
    days_remaining = (due_date - current_date).days
    
    # Determine status and priority
    if days_remaining < 0:
        status = "overdue"
        urgency = "critical"
        suggested_priority = "high"
        days_past_due = abs(days_remaining)
        message = f"Task is {days_past_due} day(s) overdue"
    elif days_remaining <= 2:
        status = "urgent"
        urgency = "high"
        suggested_priority = "high"
        message = f"Task is due in {days_remaining} day(s) - URGENT"
    elif days_remaining <= 7:
        status = "due_soon"
        urgency = "medium"
        suggested_priority = "medium"
        message = f"Task is due in {days_remaining} day(s)"
    else:
        status = "normal"
        urgency = "low"
        suggested_priority = "low"
        message = f"Task is due in {days_remaining} day(s)"
    
    return jsonify({
        'success': True,
        'task_id': task_id,
        'days_remaining': days_remaining,
        'status': status,
        'urgency': urgency,
        'suggested_priority': suggested_priority,
        'due_date': due_date.strftime('%Y-%m-%d'),
        'message': message
    })

@app.route('/api/duedate/upcoming', methods=['GET'])
def get_upcoming_tasks():
    """
    List all upcoming due dates in the next 7 days
    Can accept POST data with multiple tasks or use sample data
    """
    
    # Check if tasks data is provided in request body
    if request.is_json and request.get_json():
        tasks_data = request.get_json().get('tasks', [])
    else:
        # Use sample data for demonstration
        tasks_data = [
            {'id': tid, 'title': task['title'], 'due_date': task['due_date']} 
            for tid, task in sample_tasks.items()
        ]
    
    current_date = datetime.now()
    seven_days_from_now = current_date + timedelta(days=7)
    
    upcoming_tasks = []
    
    for task in tasks_data:
        try:
            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
            days_remaining = (due_date - current_date).days
            
            # Include tasks due in next 7 days or overdue
            if days_remaining <= 7:
                if days_remaining < 0:
                    status = "overdue"
                    urgency = "critical"
                elif days_remaining <= 2:
                    status = "urgent"
                    urgency = "high"
                elif days_remaining <= 7:
                    status = "due_soon"
                    urgency = "medium"
                
                upcoming_tasks.append({
                    'id': task.get('id', 'unknown'),
                    'title': task.get('title', 'Untitled Task'),
                    'due_date': task['due_date'],
                    'days_remaining': days_remaining,
                    'status': status,
                    'urgency': urgency
                })
        
        except (ValueError, KeyError) as e:
            continue  # Skip invalid tasks
    
    # Sort by days remaining (overdue first, then by urgency)
    upcoming_tasks.sort(key=lambda x: (x['days_remaining'] if x['days_remaining'] >= 0 else -999, x['urgency']))
    
    # Generate summary statistics
    overdue_count = len([t for t in upcoming_tasks if t['status'] == 'overdue'])
    urgent_count = len([t for t in upcoming_tasks if t['status'] == 'urgent'])
    due_soon_count = len([t for t in upcoming_tasks if t['status'] == 'due_soon'])
    
    return jsonify({
        'success': True,
        'upcoming_tasks': upcoming_tasks,
        'total_upcoming': len(upcoming_tasks),
        'summary': {
            'overdue': overdue_count,
            'urgent': urgent_count,
            'due_soon': due_soon_count
        },
        'generated_at': current_date.isoformat()
    })

@app.route('/api/duedate/batch-calculate', methods=['POST'])
def batch_calculate():
    """
    Calculate due dates for multiple tasks at once
    Expects JSON with 'tasks' array containing task objects with due_date field
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    tasks = data.get('tasks', [])
    
    if not tasks:
        return jsonify({
            'success': False,
            'error': 'No tasks provided'
        }), 400
    
    results = []
    current_date = datetime.now()
    
    for task in tasks:
        try:
            task_id = task.get('id', 'unknown')
            due_date = datetime.strptime(task['due_date'], '%Y-%m-%d')
            days_remaining = (due_date - current_date).days
            
            # Determine priority based on due date
            if days_remaining < 3:
                suggested_priority = "high"
            elif days_remaining <= 7:
                suggested_priority = "medium"
            else:
                suggested_priority = "low"
            
            results.append({
                'task_id': task_id,
                'title': task.get('title', 'Untitled'),
                'days_remaining': days_remaining,
                'suggested_priority': suggested_priority,
                'due_date': task['due_date']
            })
            
        except (ValueError, KeyError) as e:
            results.append({
                'task_id': task.get('id', 'unknown'),
                'error': f'Invalid task data: {str(e)}'
            })
    
    return jsonify({
        'success': True,
        'results': results,
        'processed_count': len(results)
    })

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'service': 'due-date-calculator',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)