import os
import time
from utils.colors import Colors

class LogViewer:
    @staticmethod
    def read_logs(file_path, keyword=None, limit=50):
        """Reads a log file with optional keyword filtering."""
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."
        
        try:
            with open(file_path, 'r', errors='ignore') as f:
                lines = f.readlines()
                if keyword:
                    lines = [l for l in lines if keyword.lower() in l.lower()]
                
                return "".join(lines[-limit:])
        except Exception as e:
            return f"Error reading logs: {e}"

    @staticmethod
    def tail_logs(file_path):
        """Follows a log file in real-time (Ctrl+C to stop)."""
        print(f"{Colors.CYAN}Tailing {file_path}. Press Ctrl+C to stop...{Colors.RESET}")
        try:
            with open(file_path, 'r') as f:
                f.seek(0, 2)  # Move to end of file
                while True:
                    line = f.readline()
                    if not line:
                        time.sleep(0.1)
                        continue
                    print(line, end='')
        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Stopped tailing.{Colors.RESET}")