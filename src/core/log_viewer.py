import os
import time
import json
from datetime import datetime
from utils.colors import Colors

class LogViewer:
    def __init__(self):
        self.bookmarks_file = "data/log_bookmarks.json"
        self.bookmarks = self._load_bookmarks()
    
    def _load_bookmarks(self):
        """Load bookmarked log file paths"""
        if os.path.exists(self.bookmarks_file):
            try:
                with open(self.bookmarks_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_bookmarks(self):
        """Save log file bookmarks"""
        os.makedirs(os.path.dirname(self.bookmarks_file), exist_ok=True)
        with open(self.bookmarks_file, 'w') as f:
            json.dump(self.bookmarks, f, indent=2)
    
    def add_bookmark(self, name, path):
        """Bookmark a log file for quick access"""
        if not os.path.exists(path):
            print(f"{Colors.FAIL}Error: File {path} not found{Colors.RESET}")
            return False
        
        self.bookmarks[name] = path
        self._save_bookmarks()
        print(f"{Colors.GREEN}Bookmarked '{path}' as '{name}'{Colors.RESET}")
        return True
    
    def remove_bookmark(self, name):
        """Remove a log bookmark"""
        if name in self.bookmarks:
            del self.bookmarks[name]
            self._save_bookmarks()
            print(f"{Colors.GREEN}Removed bookmark '{name}'{Colors.RESET}")
            return True
        else:
            print(f"{Colors.WARNING}Bookmark '{name}' not found{Colors.RESET}")
            return False
    
    def list_bookmarks(self):
        """List all log bookmarks"""
        if not self.bookmarks:
            print(f"{Colors.WARNING}No bookmarks saved{Colors.RESET}")
            return
        
        print(f"{Colors.HEADER}=== Log Bookmarks ==={Colors.RESET}")
        for name, path in self.bookmarks.items():
            exists = "✓" if os.path.exists(path) else "✗"
            color = Colors.GREEN if os.path.exists(path) else Colors.FAIL
            print(f"{color}{exists} {name}: {path}{Colors.RESET}")
    
    def read_logs(self, file_path, keyword=None, limit=50):
        """Reads a log file with optional keyword filtering."""
        # Check if it's a bookmark name
        if file_path in self.bookmarks:
            file_path = self.bookmarks[file_path]
        
        if not os.path.exists(file_path):
            return f"Error: File {file_path} not found."
        
        try:
            with open(file_path, 'r', errors='ignore') as f:
                lines = f.readlines()
                
                total_lines = len(lines)
                
                if keyword:
                    lines = [l for l in lines if keyword.lower() in l.lower()]
                    print(f"{Colors.CYAN}Found {len(lines)} matching lines out of {total_lines}{Colors.RESET}")
                
                result = "".join(lines[-limit:])
                return result if result else f"{Colors.WARNING}No matching lines found{Colors.RESET}"
        except Exception as e:
            return f"Error reading logs: {e}"

    def tail_logs(self, file_path):
        """Follows a log file in real-time (Ctrl+C to stop)."""
        # Check if it's a bookmark name
        if file_path in self.bookmarks:
            file_path = self.bookmarks[file_path]
        
        if not os.path.exists(file_path):
            print(f"{Colors.FAIL}Error: File {file_path} not found{Colors.RESET}")
            return
        
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
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.RESET}")
    
    def parse_log_stats(self, file_path):
        """Generate statistics from log file"""
        # Check if it's a bookmark name
        if file_path in self.bookmarks:
            file_path = self.bookmarks[file_path]
        
        if not os.path.exists(file_path):
            print(f"{Colors.FAIL}Error: File {file_path} not found{Colors.RESET}")
            return
        
        try:
            with open(file_path, 'r', errors='ignore') as f:
                lines = f.readlines()
            
            total_lines = len(lines)
            errors = sum(1 for l in lines if 'error' in l.lower())
            warnings = sum(1 for l in lines if 'warning' in l.lower() or 'warn' in l.lower())
            critical = sum(1 for l in lines if 'critical' in l.lower() or 'fatal' in l.lower())
            
            print(f"{Colors.HEADER}=== Log Statistics ==={Colors.RESET}")
            print(f"File: {file_path}")
            print(f"Total Lines: {total_lines}")
            print(f"{Colors.FAIL}Critical/Fatal: {critical}{Colors.RESET}")
            print(f"{Colors.FAIL}Errors: {errors}{Colors.RESET}")
            print(f"{Colors.WARNING}Warnings: {warnings}{Colors.RESET}")
            print(f"{Colors.GREEN}Info: {total_lines - errors - warnings - critical}{Colors.RESET}")
            
        except Exception as e:
            print(f"{Colors.FAIL}Error parsing log: {e}{Colors.RESET}")