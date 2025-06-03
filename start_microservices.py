# start_microservices.py
import subprocess
import time
import sys
import os
import signal
import threading
import requests

class MicroserviceManager:
    def __init__(self):
        self.processes = []
        self.microservices = [
            {
                'name': 'Due Date Calculator (Microservice B)',
                'file': 'microservice_b_due_date_calculator.py',
                'port': 5001,
                'health_endpoint': '/health'
            },
            {
                'name': 'Email Reminder Service (Microservice C)',
                'file': 'microservice_c_email_reminder_service.py',
                'port': 5002,
                'health_endpoint': '/health'
            },
            {
                'name': 'Task Stats Service (Microservice D)',
                'file': 'microservice_d_task_stats_service.py',
                'port': 5003,
                'health_endpoint': '/health'
            }
        ]
    
    def start_microservice(self, service):
        """Start a single microservice"""
        print(f"Starting {service['name']} on port {service['port']}...")
        
        try:
            # Check if file exists
            if not os.path.exists(service['file']):
                print(f"❌ Error: {service['file']} not found!")
                return None
            
            # Start the process
            process = subprocess.Popen(
                [sys.executable, service['file']],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print(f"✅ {service['name']} started (PID: {process.pid})")
            return process
            
        except Exception as e:
            print(f"❌ Failed to start {service['name']}: {e}")
            return None
    
    def check_health(self, service, timeout=30):
        """Check if a microservice is healthy"""
        url = f"http://localhost:{service['port']}{service['health_endpoint']}"
        
        for attempt in range(timeout):
            try:
                response = requests.get(url, timeout=1)
                if response.status_code == 200:
                    data = response.json()
                    print(f"✅ {service['name']} is healthy: {data.get('status', 'unknown')}")
                    return True
            except:
                pass
            
            if attempt < timeout - 1:
                time.sleep(1)
        
        print(f"❌ {service['name']} health check failed after {timeout} seconds")
        return False
    
    def start_all(self):
        """Start all microservices"""
        print("TaskPro Microservices Startup Manager")
        print("=" * 50)
        
        # Start all microservices
        for service in self.microservices:
            process = self.start_microservice(service)
            if process:
                self.processes.append({
                    'service': service,
                    'process': process
                })
            else:
                print(f"❌ Failed to start {service['name']}")
                return False
        
        print(f"\n⏳ Waiting for microservices to initialize...")
        time.sleep(3)
        
        # Check health of all services
        print(f"\n🔍 Performing health checks...")
        all_healthy = True
        for service in self.microservices:
            if not self.check_health(service):
                all_healthy = False
        
        if all_healthy:
            print(f"\n🎉 All microservices are running and healthy!")
            print(f"\nMicroservice URLs:")
            for service in self.microservices:
                print(f"• {service['name']}: http://localhost:{service['port']}")
            
            print(f"\n📋 You can now:")
            print(f"• Run the test suite: python test_all_microservices.py")
            print(f"• Open the main application: index.html")
            print(f"• Press Ctrl+C to stop all microservices")
            
            return True
        else:
            print(f"\n❌ Some microservices failed to start properly")
            self.stop_all()
            return False
    
    def stop_all(self):
        """Stop all microservices"""
        print(f"\n🛑 Stopping all microservices...")
        
        for item in self.processes:
            try:
                service = item['service']
                process = item['process']
                
                print(f"Stopping {service['name']} (PID: {process.pid})...")
                process.terminate()
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=5)
                    print(f"✅ {service['name']} stopped gracefully")
                except subprocess.TimeoutExpired:
                    print(f"⚠️  Force killing {service['name']}...")
                    process.kill()
                    process.wait()
                    print(f"✅ {service['name']} force stopped")
                    
            except Exception as e:
                print(f"❌ Error stopping {service['name']}: {e}")
        
        self.processes.clear()
        print(f"🏁 All microservices stopped")
    
    def monitor_processes(self):
        """Monitor running processes"""
        while True:
            time.sleep(5)
            
            for item in self.processes:
                service = item['service']
                process = item['process']
                
                if process.poll() is not None:
                    print(f"⚠️  {service['name']} has stopped unexpectedly!")
                    # Attempt to restart
                    print(f"🔄 Attempting to restart {service['name']}...")
                    new_process = self.start_microservice(service)
                    if new_process:
                        item['process'] = new_process
                        time.sleep(2)
                        if self.check_health(service, timeout=10):
                            print(f"✅ {service['name']} restarted successfully")
                        else:
                            print(f"❌ Failed to restart {service['name']}")
                    else:
                        print(f"❌ Failed to restart {service['name']}")
    
    def signal_handler(self, signum, frame):
        """Handle Ctrl+C gracefully"""
        print(f"\n\n🛑 Received interrupt signal...")
        self.stop_all()
        sys.exit(0)

def print_requirements():
    """Print setup requirements"""
    print("📋 Setup Requirements:")
    print("=" * 30)
    print("Make sure you have the following files in the current directory:")
    print("• microservice_b_due_date_calculator.py")
    print("• microservice_c_email_reminder_service.py") 
    print("• microservice_d_task_stats_service.py")
    print("• index.html (main application)")
    print("\nRequired Python packages:")
    print("• flask")
    print("• requests")
    print("\nInstall with: pip install flask requests")
    print()

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import flask
        import requests
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install required packages: pip install flask requests")
        return False

def main():
    print_requirements()
    
    if not check_dependencies():
        return
    
    # Create manager instance
    manager = MicroserviceManager()
    
    # Set up signal handler for graceful shutdown
    signal.signal(signal.SIGINT, manager.signal_handler)
    signal.signal(signal.SIGTERM, manager.signal_handler)
    
    # Start all microservices
    if manager.start_all():
        try:
            # Start monitoring in a separate thread
            monitor_thread = threading.Thread(target=manager.monitor_processes, daemon=True)
            monitor_thread.start()
            
            # Keep main thread alive
            while True:
                time.sleep(1)
                
        except KeyboardInterrupt:
            manager.signal_handler(signal.SIGINT, None)
    else:
        print("❌ Failed to start microservices")
        sys.exit(1)

if __name__ == "__main__":
    main()