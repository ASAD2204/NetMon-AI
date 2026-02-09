import subprocess
import os
import re
import json
import hashlib
from datetime import datetime, timedelta
from utils.colors import Colors

class UserManager:
    def __init__(self):
        self.sessions_file = "data/user_sessions.json"
        self.password_policies_file = "data/password_policies.json"
        self.sessions = self._load_sessions()
        self.policies = self._load_policies()
    
    def _load_sessions(self):
        """Load active user sessions"""
        if os.path.exists(self.sessions_file):
            try:
                with open(self.sessions_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_sessions(self):
        """Save user sessions"""
        os.makedirs(os.path.dirname(self.sessions_file), exist_ok=True)
        with open(self.sessions_file, 'w') as f:
            json.dump(self.sessions, f, indent=2)
    
    def _load_policies(self):
        """Load password policies"""
        if os.path.exists(self.password_policies_file):
            try:
                with open(self.password_policies_file, 'r') as f:
                    return json.load(f)
            except:
                return self._get_default_policies()
        return self._get_default_policies()
    
    def _get_default_policies(self):
        """Default password policies"""
        return {
            "min_length": 8,
            "require_uppercase": True,
            "require_lowercase": True,
            "require_numbers": True,
            "require_special": True,
            "password_expiry_days": 90,
            "max_failed_attempts": 3
        }
    
    def _save_policies(self):
        """Save password policies"""
        os.makedirs(os.path.dirname(self.password_policies_file), exist_ok=True)
        with open(self.password_policies_file, 'w') as f:
            json.dump(self.policies, f, indent=2)
    
    def validate_password_strength(self, password):
        """
        Validate password against security policies
        Returns: (is_valid, error_messages[])
        """
        errors = []
        
        if len(password) < self.policies["min_length"]:
            errors.append(f"Password must be at least {self.policies['min_length']} characters")
        
        if self.policies["require_uppercase"] and not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.policies["require_lowercase"] and not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.policies["require_numbers"] and not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if self.policies["require_special"] and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return len(errors) == 0, errors
    
    def create_session(self, username):
        """Create a new user session"""
        session_id = hashlib.sha256(f"{username}{datetime.now()}".encode()).hexdigest()[:16]
        self.sessions[username] = {
            "session_id": session_id,
            "login_time": datetime.now().isoformat(),
            "last_activity": datetime.now().isoformat(),
            "failed_attempts": 0
        }
        self._save_sessions()
        return session_id
    
    def end_session(self, username):
        """End a user session"""
        if username in self.sessions:
            del self.sessions[username]
            self._save_sessions()
            print(f"{Colors.GREEN}Session ended for user '{username}'{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}No active session for user '{username}'{Colors.RESET}")
    
    def get_active_sessions(self):
        """Get all active sessions"""
        print(f"{Colors.HEADER}=== Active User Sessions ==={Colors.RESET}")
        if not self.sessions:
            print(f"{Colors.WARNING}No active sessions{Colors.RESET}")
            return
        
        for username, session in self.sessions.items():
            login_time = session.get("login_time", "Unknown")
            last_activity = session.get("last_activity", "Unknown")
            print(f"{Colors.CYAN}User:{Colors.RESET} {username}")
            print(f"  Session ID: {session.get('session_id', 'N/A')}")
            print(f"  Login Time: {login_time}")
            print(f"  Last Activity: {last_activity}")
            print()
    
    def check_password_expiry(self, username):
        """Check if user password has expired"""
        # This is a placeholder - actual implementation would check system password age
        # For demonstration purposes
        if username in self.sessions:
            login_time = datetime.fromisoformat(self.sessions[username]["login_time"])
            days_since_login = (datetime.now() - login_time).days
            expiry_days = self.policies["password_expiry_days"]
            
            if days_since_login >= expiry_days:
                print(f"{Colors.FAIL}⚠️ Password for '{username}' has expired!{Colors.RESET}")
                print(f"{Colors.WARNING}Please change your password.{Colors.RESET}")
                return True
            elif days_since_login >= expiry_days - 7:
                days_left = expiry_days - days_since_login
                print(f"{Colors.WARNING}Password expires in {days_left} days{Colors.RESET}")
                return False
        return False
    
    def show_password_policies(self):
        """Display current password policies"""
        print(f"{Colors.HEADER}=== Password Security Policies ==={Colors.RESET}")
        print(f"Minimum Length: {self.policies['min_length']} characters")
        print(f"Require Uppercase: {Colors.GREEN if self.policies['require_uppercase'] else Colors.FAIL}{'Yes' if self.policies['require_uppercase'] else 'No'}{Colors.RESET}")
        print(f"Require Lowercase: {Colors.GREEN if self.policies['require_lowercase'] else Colors.FAIL}{'Yes' if self.policies['require_lowercase'] else 'No'}{Colors.RESET}")
        print(f"Require Numbers: {Colors.GREEN if self.policies['require_numbers'] else Colors.FAIL}{'Yes' if self.policies['require_numbers'] else 'No'}{Colors.RESET}")
        print(f"Require Special Characters: {Colors.GREEN if self.policies['require_special'] else Colors.FAIL}{'Yes' if self.policies['require_special'] else 'No'}{Colors.RESET}")
        print(f"Password Expiry: {self.policies['password_expiry_days']} days")
        print(f"Max Failed Login Attempts: {self.policies['max_failed_attempts']}")
    
    def _run(self, cmd):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.returncode == 0, res.stdout, res.stderr

    def add_user(self, username, password=None):
        """Add a new user with password validation"""
        if password:
            is_valid, errors = self.validate_password_strength(password)
            if not is_valid:
                print(f"{Colors.FAIL}Password does not meet security requirements:{Colors.RESET}")
                for error in errors:
                    print(f"  - {error}")
                return False
        
        if os.name == 'nt':
            cmd = f"net user {username} /add"
        else:
            cmd = f"sudo useradd -m {username}"
        
        success, _, err = self._run(cmd)
        if success:
            print(f"{Colors.GREEN}User '{username}' added successfully.{Colors.RESET}")
            self.create_session(username)
            return True
        else:
            print(f"{Colors.FAIL}Error: {err}{Colors.RESET}")
            return False

    def list_users(self):
        print(f"{Colors.HEADER}--- System Users ---{Colors.RESET}")
        if os.name == 'nt':
            _, out, _ = self._run("net user")
            print(out)
        else:
            try:
                with open('/etc/passwd', 'r') as f:
                    for line in f:
                        print(line.split(':')[0])
            except PermissionError:
                print(f"{Colors.FAIL}Permission denied. Run with elevated privileges.{Colors.RESET}")