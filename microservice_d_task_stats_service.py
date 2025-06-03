# microservice_d_task_stats_service.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, timedelta
import json
from collections import defaultdict, Counter

app = Flask(__name__)
CORS(app)


completion_events = []
task_data = {}

@app.route('/api/stats/record-completion', methods=['POST'])
def record_completion():
    """
    Record a task completion event
    Expects: task_id, user_email, task_title, category/class, completion_date, created_date
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['task_id', 'user_email', 'task_title']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'success': False,
                'error': f'Missing required field: {field}'
            }), 400
    
    task_id = data['task_id']
    user_email = data['user_email']
    task_title = data['task_title']
    category = data.get('category', 'General')
    completion_date_str = data.get('completion_date', datetime.now().strftime('%Y-%m-%d'))
    created_date_str = data.get('created_date', completion_date_str)
    
    try:
        completion_date = datetime.strptime(completion_date_str, '%Y-%m-%d')
        created_date = datetime.strptime(created_date_str, '%Y-%m-%d')
    except ValueError:
        return jsonify({
            'success': False,
            'error': 'Invalid date format. Use YYYY-MM-DD'
        }), 400
    
    # Calculate completion time in days
    completion_time_days = (completion_date - created_date).days
    
    # Create completion event record
    event_id = len(completion_events) + 1
    completion_event = {
        'event_id': event_id,
        'task_id': task_id,
        'user_email': user_email,
        'task_title': task_title,
        'category': category,
        'completion_date': completion_date_str,
        'created_date': created_date_str,
        'completion_time_days': max(1, completion_time_days),  # Minimum 1 day
        'recorded_at': datetime.now().isoformat()
    }
    
    completion_events.append(completion_event)
    
    return jsonify({
        'success': True,
        'event_id': event_id,
        'completion_time_days': completion_time_days,
        'message': 'Task completion recorded successfully'
    })

@app.route('/api/stats/summary', methods=['GET'])
def get_summary_stats():
    """
    Get basic task statistics summary for a user
    Requires user_email as query parameter
    """
    user_email = request.args.get('user_email')
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email parameter is required'
        }), 400
    
    # Filter events for this user
    user_events = [e for e in completion_events if e['user_email'] == user_email]
    
    if not user_events:
        return jsonify({
            'success': True,
            'user_email': user_email,
            'stats': {
                'total_completed': 0,
                'average_completion_time': 0,
                'total_categories': 0,
                'completion_rate': 0,
                'message': 'No completed tasks found'
            }
        })
    
    # Calculate basic statistics
    total_completed = len(user_events)
    completion_times = [e['completion_time_days'] for e in user_events]
    average_completion_time = sum(completion_times) / len(completion_times)
    
    # Count unique categories
    categories = set(e['category'] for e in user_events)
    total_categories = len(categories)
    
    # Calculate recent activity (last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    recent_events = [
        e for e in user_events 
        if datetime.strptime(e['completion_date'], '%Y-%m-%d') >= thirty_days_ago
    ]
    recent_completed = len(recent_events)
    
    # Calculate completion trend
    if len(user_events) >= 2:
        # Compare last 2 weeks vs previous 2 weeks
        two_weeks_ago = datetime.now() - timedelta(days=14)
        four_weeks_ago = datetime.now() - timedelta(days=28)
        
        last_two_weeks = len([
            e for e in user_events 
            if datetime.strptime(e['completion_date'], '%Y-%m-%d') >= two_weeks_ago
        ])
        
        prev_two_weeks = len([
            e for e in user_events 
            if four_weeks_ago <= datetime.strptime(e['completion_date'], '%Y-%m-%d') < two_weeks_ago
        ])
        
        if prev_two_weeks > 0:
            trend_percentage = ((last_two_weeks - prev_two_weeks) / prev_two_weeks) * 100
        else:
            trend_percentage = 100 if last_two_weeks > 0 else 0
    else:
        trend_percentage = 0
    
    return jsonify({
        'success': True,
        'user_email': user_email,
        'stats': {
            'total_completed': total_completed,
            'average_completion_time_days': round(average_completion_time, 1),
            'total_categories': total_categories,
            'recent_completed_30_days': recent_completed,
            'trend_percentage': round(trend_percentage, 1),
            'fastest_completion': min(completion_times),
            'slowest_completion': max(completion_times),
            'most_active_category': Counter(e['category'] for e in user_events).most_common(1)[0][0] if user_events else None
        },
        'generated_at': datetime.now().isoformat()
    })

@app.route('/api/stats/by-category', methods=['GET'])
def get_stats_by_category():
    """
    Get task completion statistics grouped by category/class
    Requires user_email as query parameter
    """
    user_email = request.args.get('user_email')
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email parameter is required'
        }), 400
    
    # Filter events for this user
    user_events = [e for e in completion_events if e['user_email'] == user_email]
    
    if not user_events:
        return jsonify({
            'success': True,
            'user_email': user_email,
            'categories': [],
            'message': 'No completed tasks found'
        })
    
    # Group by category
    category_stats = defaultdict(list)
    for event in user_events:
        category_stats[event['category']].append(event)
    
    # Calculate statistics for each category
    category_results = []
    for category, events in category_stats.items():
        completion_times = [e['completion_time_days'] for e in events]
        
        category_data = {
            'category': category,
            'total_completed': len(events),
            'average_completion_time': round(sum(completion_times) / len(completion_times), 1),
            'fastest_completion': min(completion_times),
            'slowest_completion': max(completion_times),
            'recent_tasks': [
                {
                    'task_title': e['task_title'],
                    'completion_date': e['completion_date'],
                    'completion_time_days': e['completion_time_days']
                }
                for e in sorted(events, key=lambda x: x['completion_date'], reverse=True)[:3]
            ]
        }
        
        category_results.append(category_data)
    
    # Sort by total completed (most active categories first)
    category_results.sort(key=lambda x: x['total_completed'], reverse=True)
    
    return jsonify({
        'success': True,
        'user_email': user_email,
        'categories': category_results,
        'total_categories': len(category_results)
    })

@app.route('/api/stats/productivity-report', methods=['GET'])
def get_productivity_report():
    """
    Generate a comprehensive productivity report for a user
    Requires user_email as query parameter
    """
    user_email = request.args.get('user_email')
    time_period = request.args.get('time_period', '30')  # days
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email parameter is required'
        }), 400
    
    try:
        days = int(time_period)
    except ValueError:
        days = 30
    
    # Filter events for this user and time period
    cutoff_date = datetime.now() - timedelta(days=days)
    user_events = [
        e for e in completion_events 
        if e['user_email'] == user_email 
        and datetime.strptime(e['completion_date'], '%Y-%m-%d') >= cutoff_date
    ]
    
    if not user_events:
        return jsonify({
            'success': True,
            'user_email': user_email,
            'time_period_days': days,
            'report': {
                'summary': 'No tasks completed in this time period',
                'total_completed': 0
            }
        })
    
    # Calculate daily completion pattern
    daily_completions = defaultdict(int)
    for event in user_events:
        date = event['completion_date']
        daily_completions[date] += 1
    
    # Find most productive day
    most_productive_day = max(daily_completions.items(), key=lambda x: x[1]) if daily_completions else None
    
    # Calculate completion rate per week
    weeks_in_period = max(1, days // 7)
    completion_rate_per_week = len(user_events) / weeks_in_period
    
    # Category performance
    category_performance = defaultdict(list)
    for event in user_events:
        category_performance[event['category']].append(event['completion_time_days'])
    
    top_categories = [
        {
            'category': cat,
            'completed': len(times),
            'avg_completion_time': round(sum(times) / len(times), 1)
        }
        for cat, times in category_performance.items()
    ]
    top_categories.sort(key=lambda x: x['completed'], reverse=True)
    
    # Performance insights
    insights = generate_performance_insights(user_events, days)
    
    return jsonify({
        'success': True,
        'user_email': user_email,
        'time_period_days': days,
        'report': {
            'total_completed': len(user_events),
            'completion_rate_per_week': round(completion_rate_per_week, 1),
            'average_completion_time': round(sum(e['completion_time_days'] for e in user_events) / len(user_events), 1),
            'most_productive_day': {
                'date': most_productive_day[0] if most_productive_day else None,
                'tasks_completed': most_productive_day[1] if most_productive_day else 0
            },
            'top_categories': top_categories[:5],  # Top 5 categories
            'daily_breakdown': dict(daily_completions),
            'insights': insights
        },
        'generated_at': datetime.now().isoformat()
    })

def generate_performance_insights(events, days):
    """Generate insights about user's task completion performance"""
    insights = []
    
    if not events:
        return ["No tasks completed in this period."]
    
    total_completed = len(events)
    avg_completion_time = sum(e['completion_time_days'] for e in events) / len(events)
    
    # Productivity insights
    tasks_per_week = total_completed / max(1, days // 7)
    if tasks_per_week >= 5:
        insights.append("Excellent productivity! You're completing 5+ tasks per week.")
    elif tasks_per_week >= 3:
        insights.append("Good productivity level - consistently completing tasks.")
    else:
        insights.append("Consider setting more frequent task completion goals.")
    
    # Completion time insights
    if avg_completion_time <= 2:
        insights.append("Great efficiency! You complete tasks quickly.")
    elif avg_completion_time <= 5:
        insights.append("Good task completion speed.")
    else:
        insights.append("Consider breaking large tasks into smaller, manageable pieces.")
    
    # Category diversity
    categories = set(e['category'] for e in events)
    if len(categories) >= 3:
        insights.append("Well-balanced workload across multiple categories.")
    elif len(categories) == 2:
        insights.append("Good balance between different types of tasks.")
    else:
        insights.append("Consider diversifying your task categories for better skill development.")
    
    return insights

@app.route('/api/stats/incomplete-tasks', methods=['POST'])
def track_incomplete_tasks():
    """
    Track current incomplete tasks for statistics
    This helps calculate completion rates
    """
    if not request.is_json:
        return jsonify({
            'success': False,
            'error': 'Content-Type must be application/json'
        }), 400
    
    data = request.get_json()
    user_email = data.get('user_email')
    incomplete_tasks = data.get('incomplete_tasks', [])
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email is required'
        }), 400
    
    
    current_snapshot = {
        'user_email': user_email,
        'incomplete_count': len(incomplete_tasks),
        'categories': Counter(task.get('category', 'General') for task in incomplete_tasks),
        'snapshot_date': datetime.now().strftime('%Y-%m-%d'),
        'tasks': incomplete_tasks
    }
    
    # Calculate completion rate
    completed_in_period = len([
        e for e in completion_events 
        if e['user_email'] == user_email
    ])
    
    total_tasks = completed_in_period + len(incomplete_tasks)
    completion_rate = (completed_in_period / total_tasks * 100) if total_tasks > 0 else 0
    
    return jsonify({
        'success': True,
        'incomplete_count': len(incomplete_tasks),
        'completed_count': completed_in_period,
        'completion_rate_percentage': round(completion_rate, 1),
        'total_tasks': total_tasks
    })

@app.route('/api/stats/dashboard-data', methods=['GET'])
def get_dashboard_data():
    """
    Get all statistics data for dashboard display
    Requires user_email as query parameter
    """
    user_email = request.args.get('user_email')
    
    if not user_email:
        return jsonify({
            'success': False,
            'error': 'user_email parameter is required'
        }), 400
    
    # Get all user events
    user_events = [e for e in completion_events if e['user_email'] == user_email]
    
    # Calculate this week's stats
    week_ago = datetime.now() - timedelta(days=7)
    this_week_events = [
        e for e in user_events 
        if datetime.strptime(e['completion_date'], '%Y-%m-%d') >= week_ago
    ]
    
    # Calculate this month's stats
    month_ago = datetime.now() - timedelta(days=30)
    this_month_events = [
        e for e in user_events 
        if datetime.strptime(e['completion_date'], '%Y-%m-%d') >= month_ago
    ]
    
    # Category breakdown
    category_breakdown = Counter(e['category'] for e in user_events)
    
    # Recent achievements
    recent_tasks = sorted(user_events, key=lambda x: x['completion_date'], reverse=True)[:5]
    
    dashboard_data = {
        'overall_stats': {
            'total_completed': len(user_events),
            'this_week': len(this_week_events),
            'this_month': len(this_month_events),
            'average_completion_time': round(
                sum(e['completion_time_days'] for e in user_events) / len(user_events), 1
            ) if user_events else 0
        },
        'category_breakdown': dict(category_breakdown),
        'recent_completions': [
            {
                'task_title': task['task_title'],
                'category': task['category'],
                'completion_date': task['completion_date'],
                'completion_time_days': task['completion_time_days']
            }
            for task in recent_tasks
        ],
        'performance_trend': calculate_performance_trend(user_events)
    }
    
    return jsonify({
        'success': True,
        'user_email': user_email,
        'dashboard': dashboard_data,
        'generated_at': datetime.now().isoformat()
    })

def calculate_performance_trend(events):
    """Calculate performance trend over time"""
    if len(events) < 4:
        return {'trend': 'insufficient_data', 'message': 'Need more completed tasks to show trend'}
    
    # Split events into two halves by date
    sorted_events = sorted(events, key=lambda x: x['completion_date'])
    mid_point = len(sorted_events) // 2
    
    first_half = sorted_events[:mid_point]
    second_half = sorted_events[mid_point:]
    
    # Calculate average completion times
    first_half_avg = sum(e['completion_time_days'] for e in first_half) / len(first_half)
    second_half_avg = sum(e['completion_time_days'] for e in second_half) / len(second_half)
    
    # Calculate trend
    if second_half_avg < first_half_avg * 0.9:  # 10% improvement
        trend = 'improving'
        message = 'Your task completion speed is improving!'
    elif second_half_avg > first_half_avg * 1.1:  # 10% slower
        trend = 'declining'
        message = 'Consider strategies to improve completion speed.'
    else:
        trend = 'stable'
        message = 'Consistent performance - maintaining steady pace.'
    
    return {
        'trend': trend,
        'message': message,
        'first_half_avg': round(first_half_avg, 1),
        'second_half_avg': round(second_half_avg, 1)
    }

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy', 
        'service': 'task-stats-service',
        'timestamp': datetime.now().isoformat(),
        'total_events': len(completion_events)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5003)