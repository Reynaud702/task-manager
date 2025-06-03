# test_all_microservices.py
import requests
import json
from datetime import datetime, timedelta

def test_microservice(base_url, service_name):
    print(f"\n{'='*50}")
    print(f"Testing {service_name}")
    print(f"Base URL: {base_url}")
    print(f"{'='*50}")
    
    # Health check
    try:
        health_response = requests.get(f"{base_url}/health")
        print(f"✓ Health Check - Status: {health_response.status_code}")
        print(f"  Response: {health_response.json()}")
    except Exception as e:
        print(f"✗ Health Check Failed: {e}")
        return False
    
    return True

def test_username_generator():
    """Test Microservice A - Username Generator"""
    base_url = "http://localhost:5000"
    
    if not test_microservice(base_url, "Username Generator (Microservice A)"):
        return
    
    print("\nTest 1: Generate username with full information")
    full_data = {
        "first_name": "John",
        "last_name": "Smith",
        "favorite_genre": "rock"
    }
    try:
        response = requests.post(
            f"{base_url}/generate", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(full_data)
        )
        print(f"✓ Full Info Test - Status: {response.status_code}")
        print(f"  Request: {full_data}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Full Info Test Failed: {e}")
    
    print("\nTest 2: Generate username with partial information")
    partial_data = {"first_name": "Alice"}
    try:
        response = requests.post(
            f"{base_url}/generate", 
            headers={"Content-Type": "application/json"},
            data=json.dumps(partial_data)
        )
        print(f"✓ Partial Info Test - Status: {response.status_code}")
        print(f"  Request: {partial_data}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Partial Info Test Failed: {e}")

def test_due_date_calculator():
    """Test Microservice B - Due Date Calculator"""
    base_url = "http://localhost:5001"
    
    if not test_microservice(base_url, "Due Date Calculator (Microservice B)"):
        return
    
    print("\nTest 1: Calculate due date for single task")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
    try:
        response = requests.get(f"{base_url}/api/duedate/calculate/1?due_date={tomorrow}")
        print(f"✓ Single Task Test - Status: {response.status_code}")
        print(f"  Due Date: {tomorrow}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Single Task Test Failed: {e}")
    
    print("\nTest 2: Get upcoming tasks")
    try:
        response = requests.get(f"{base_url}/api/duedate/upcoming")
        print(f"✓ Upcoming Tasks Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Upcoming Tasks Test Failed: {e}")
    
    print("\nTest 3: Batch calculate multiple tasks")
    batch_data = {
        "tasks": [
            {"id": 1, "title": "Task 1", "due_date": tomorrow},
            {"id": 2, "title": "Task 2", "due_date": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d')},
            {"id": 3, "title": "Task 3", "due_date": (datetime.now() + timedelta(days=10)).strftime('%Y-%m-%d')}
        ]
    }
    try:
        response = requests.post(
            f"{base_url}/api/duedate/batch-calculate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(batch_data)
        )
        print(f"✓ Batch Calculate Test - Status: {response.status_code}")
        print(f"  Request: {len(batch_data['tasks'])} tasks")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Batch Calculate Test Failed: {e}")

def test_email_reminder_service():
    """Test Microservice C - Email Reminder Service"""
    base_url = "http://localhost:5002"
    
    if not test_microservice(base_url, "Email Reminder Service (Microservice C)"):
        return
    
    user_email = "test@oregonstate.edu"
    
    print("\nTest 1: Get reminder settings (default)")
    try:
        response = requests.get(f"{base_url}/api/reminder/settings?user_email={user_email}")
        print(f"✓ Get Settings Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Get Settings Test Failed: {e}")
    
    print("\nTest 2: Update reminder settings")
    settings_data = {
        "user_email": user_email,
        "reminders_enabled": True,
        "reminder_timing": 3,
        "email_notifications": True
    }
    try:
        response = requests.put(
            f"{base_url}/api/reminder/settings",
            headers={"Content-Type": "application/json"},
            data=json.dumps(settings_data)
        )
        print(f"✓ Update Settings Test - Status: {response.status_code}")
        print(f"  Request: {settings_data}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Update Settings Test Failed: {e}")
    
    print("\nTest 3: Schedule a reminder")
    reminder_data = {
        "user_email": user_email,
        "task_id": 1,
        "task_title": "CS361 Assignment 3",
        "due_date": (datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d'),
        "priority": "high"
    }
    try:
        response = requests.post(
            f"{base_url}/api/reminder/schedule",
            headers={"Content-Type": "application/json"},
            data=json.dumps(reminder_data)
        )
        print(f"✓ Schedule Reminder Test - Status: {response.status_code}")
        print(f"  Request: {reminder_data}")
        print(f"  Response: {response.json()}")
        
        # Store reminder ID for status check
        if response.status_code == 200:
            reminder_id = response.json().get('reminder_id')
            
            print("\nTest 4: Check reminder status")
            status_response = requests.get(f"{base_url}/api/reminder/status/{reminder_id}")
            print(f"✓ Reminder Status Test - Status: {status_response.status_code}")
            print(f"  Response: {status_response.json()}")
            
    except Exception as e:
        print(f"✗ Schedule Reminder Test Failed: {e}")
    
    print("\nTest 5: List user reminders")
    try:
        response = requests.get(f"{base_url}/api/reminder/list?user_email={user_email}")
        print(f"✓ List Reminders Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ List Reminders Test Failed: {e}")

def test_task_stats_service():
    """Test Microservice D - Task Stats Service"""
    base_url = "http://localhost:5003"
    
    if not test_microservice(base_url, "Task Stats Service (Microservice D)"):
        return
    
    user_email = "test@oregonstate.edu"
    
    print("\nTest 1: Record task completion")
    completion_data = {
        "task_id": 1,
        "user_email": user_email,
        "task_title": "CS361 Assignment 3",
        "category": "CS361",
        "completion_date": datetime.now().strftime('%Y-%m-%d'),
        "created_date": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d')
    }
    try:
        response = requests.post(
            f"{base_url}/api/stats/record-completion",
            headers={"Content-Type": "application/json"},
            data=json.dumps(completion_data)
        )
        print(f"✓ Record Completion Test - Status: {response.status_code}")
        print(f"  Request: {completion_data}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Record Completion Test Failed: {e}")
    
    # Record a few more completions for better testing
    for i in range(2, 5):
        completion_data = {
            "task_id": i,
            "user_email": user_email,
            "task_title": f"Task {i}",
            "category": "MATH241" if i % 2 == 0 else "CS361",
            "completion_date": (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d'),
            "created_date": (datetime.now() - timedelta(days=i+2)).strftime('%Y-%m-%d')
        }
        try:
            requests.post(
                f"{base_url}/api/stats/record-completion",
                headers={"Content-Type": "application/json"},
                data=json.dumps(completion_data)
            )
        except:
            pass
    
    print("\nTest 2: Get summary statistics")
    try:
        response = requests.get(f"{base_url}/api/stats/summary?user_email={user_email}")
        print(f"✓ Summary Stats Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Summary Stats Test Failed: {e}")
    
    print("\nTest 3: Get statistics by category")
    try:
        response = requests.get(f"{base_url}/api/stats/by-category?user_email={user_email}")
        print(f"✓ Category Stats Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Category Stats Test Failed: {e}")
    
    print("\nTest 4: Get productivity report")
    try:
        response = requests.get(f"{base_url}/api/stats/productivity-report?user_email={user_email}&time_period=30")
        print(f"✓ Productivity Report Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Productivity Report Test Failed: {e}")
    
    print("\nTest 5: Get dashboard data")
    try:
        response = requests.get(f"{base_url}/api/stats/dashboard-data?user_email={user_email}")
        print(f"✓ Dashboard Data Test - Status: {response.status_code}")
        print(f"  Response: {response.json()}")
    except Exception as e:
        print(f"✗ Dashboard Data Test Failed: {e}")

def test_integration_scenario():
    """Test a complete integration scenario across all microservices"""
    print(f"\n{'='*50}")
    print("INTEGRATION SCENARIO TEST")
    print("Simulating complete task workflow")
    print(f"{'='*50}")
    
    user_email = "integration@oregonstate.edu"
    
    # Step 1: Create and analyze task due dates
    print("\nStep 1: Analyze due dates for new tasks")
    task_data = {
        "tasks": [
            {"id": 101, "title": "Final Project", "due_date": (datetime.now() + timedelta(days=2)).strftime('%Y-%m-%d')},
            {"id": 102, "title": "Research Paper", "due_date": (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')},
        ]
    }
    try:
        due_date_response = requests.post(
            "http://localhost:5001/api/duedate/batch-calculate",
            headers={"Content-Type": "application/json"},
            data=json.dumps(task_data)
        )
        print(f"✓ Due date analysis: {due_date_response.json()}")
    except Exception as e:
        print(f"✗ Due date analysis failed: {e}")
    
    # Step 2: Schedule reminders
    print("\nStep 2: Schedule email reminders")
    for task in task_data["tasks"]:
        reminder_data = {
            "user_email": user_email,
            "task_id": task["id"],
            "task_title": task["title"],
            "due_date": task["due_date"],
            "priority": "high"
        }
        try:
            reminder_response = requests.post(
                "http://localhost:5002/api/reminder/schedule",
                headers={"Content-Type": "application/json"},
                data=json.dumps(reminder_data)
            )
            print(f"✓ Reminder scheduled for {task['title']}: {reminder_response.json()}")
        except Exception as e:
            print(f"✗ Reminder scheduling failed for {task['title']}: {e}")
    
    # Step 3: Complete a task and record statistics
    print("\nStep 3: Complete task and record statistics")
    completion_data = {
        "task_id": 101,
        "user_email": user_email,
        "task_title": "Final Project",
        "category": "CS361",
        "completion_date": datetime.now().strftime('%Y-%m-%d'),
        "created_date": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
    }
    try:
        stats_response = requests.post(
            "http://localhost:5003/api/stats/record-completion",
            headers={"Content-Type": "application/json"},
            data=json.dumps(completion_data)
        )
        print(f"✓ Task completion recorded: {stats_response.json()}")
    except Exception as e:
        print(f"✗ Task completion recording failed: {e}")
    
    # Step 4: Get updated statistics
    print("\nStep 4: Get updated user statistics")
    try:
        stats_response = requests.get(f"http://localhost:5003/api/stats/dashboard-data?user_email={user_email}")
        print(f"✓ Updated statistics: {stats_response.json()}")
    except Exception as e:
        print(f"✗ Statistics retrieval failed: {e}")
    
    print("\n✓ Integration scenario completed successfully!")

def main():
    """Run all microservice tests"""
    print("TaskPro Microservices Test Suite")
    print("================================")
    print("This script tests the three microservices:")
    print("• Microservice B: Due Date Calculator (Port 5001)")
    print("• Microservice C: Email Reminder Service (Port 5002)")
    print("• Microservice D: Task Stats Service (Port 5003)")
    print("\nMake sure all microservices are running before proceeding!")
    
    input("\nPress Enter to start testing...")
    
    # Test each microservice individually
    test_due_date_calculator()
    test_email_reminder_service()
    test_task_stats_service()
    
    # Test integration scenario
    test_integration_scenario()
    
    print(f"\n{'='*50}")
    print("ALL TESTS COMPLETED")
    print("Check the output above for any failures.")
    print("If all tests show ✓, your microservices are working correctly!")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()