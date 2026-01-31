import json
import os
import subprocess
import shlex
import re
from utils.colors import Colors

class PlaybookEngine:
    def __init__(self):
        # Whitelist of allowed commands
        self.ALLOWED_COMMANDS = {
            'ls', 'dir', 'echo', 'cat', 'grep', 'find', 
            'systemctl', 'service', 'ping', 'curl',
            'mkdir', 'touch', 'cp', 'mv', 'pwd',
            'whoami', 'hostname', 'date', 'ps'
        }
        
        # Patterns that should never be executed
        self.FORBIDDEN_PATTERNS = [
            r'rm\s+-rf\s+/',
            r'mkfs',
            r'dd\s+if=',
            r':(){:|:&};:',  # Fork bomb
            r'chmod\s+777',
            r'>\s*/dev/sd',
            r'eval\s',
            r'exec\s',
            r'shutdown',
            r'reboot',
            r'init\s+0',
            r'init\s+6',
            r';\s*rm\s',
            r'\|\s*rm\s',
            r'&&\s*rm\s'
        ]
    
    def _validate_command(self, command):
        """Validates a single command against security rules"""
        # Check forbidden patterns
        for pattern in self.FORBIDDEN_PATTERNS:
            if re.search(pattern, command, re.IGNORECASE):
                return False, f"Forbidden pattern detected: {pattern}"
        
        # Parse command to get base command
        try:
            parts = shlex.split(command)
            if not parts:
                return False, "Empty command"
            
            base_cmd = parts[0]
            
            # Check if base command is whitelisted
            if base_cmd not in self.ALLOWED_COMMANDS:
                return False, f"Command '{base_cmd}' not in whitelist"
            
            return True, "Command validated"
        except ValueError as e:
            return False, f"Invalid command syntax: {e}"
    
    def _safe_execute(self, command):
        """Executes a command safely without shell=True"""
        try:
            # Parse command safely
            args = shlex.split(command)
            
            # Execute without shell
            result = subprocess.run(
                args,
                capture_output=True,
                text=True,
                timeout=30  # Prevent hanging
            )
            return result
        except subprocess.TimeoutExpired:
            print(f"{Colors.FAIL}Command timed out after 30 seconds{Colors.RESET}")
            return None
        except Exception as e:
            print(f"{Colors.FAIL}Execution error: {e}{Colors.RESET}")
            return None
    
    def run_playbook(self, playbook_path):
        """Executes a JSON-defined sequence of administrative tasks."""
        # Validate playbook file path
        if not os.path.exists(playbook_path):
            print(f"{Colors.FAIL}Playbook not found: {playbook_path}{Colors.RESET}")
            return
        
        # Only allow playbooks from trusted directory
        abs_path = os.path.abspath(playbook_path)
        trusted_dir = os.path.abspath("playbooks/")
        
        # Create trusted directory if it doesn't exist
        os.makedirs(trusted_dir, exist_ok=True)
        
        if not abs_path.startswith(trusted_dir):
            print(f"{Colors.FAIL}Playbook must be in trusted directory: {trusted_dir}{Colors.RESET}")
            return

        try:
            with open(playbook_path, 'r') as f:
                tasks = json.load(f)
            
            # Validate it's a list
            if not isinstance(tasks, list):
                print(f"{Colors.FAIL}Invalid playbook format: must be a JSON array{Colors.RESET}")
                return
            
            # Validate each task
            print(f"{Colors.CYAN}Validating playbook...{Colors.RESET}")
            for i, task in enumerate(tasks, 1):
                valid, msg = self._validate_command(task)
                if not valid:
                    print(f"{Colors.FAIL}Task {i} validation failed: {msg}{Colors.RESET}")
                    print(f"Problematic command: {task}")
                    return
            
            print(f"{Colors.GREEN}✓ Playbook validated{Colors.RESET}")
            print(f"{Colors.HEADER}🚀 Executing Automation Sequence...{Colors.RESET}")
            
            successful = 0
            for i, task in enumerate(tasks, 1):
                print(f"{Colors.CYAN}[{i}/{len(tasks)}] Running: {task}{Colors.RESET}")
                
                result = self._safe_execute(task)
                
                if result is None or result.returncode != 0:
                    error_msg = result.stderr if result else "Execution failed"
                    print(f"{Colors.FAIL}Task {i} failed: {error_msg}{Colors.RESET}")
                    print(f"{Colors.WARNING}Halting sequence. {successful}/{i} tasks completed.{Colors.RESET}")
                    break
                else:
                    successful += 1
                    if result.stdout:
                        print(result.stdout)
            
            if successful == len(tasks):
                print(f"{Colors.GREEN}✔ Playbook completed successfully ({successful} tasks){Colors.RESET}")
            
        except json.JSONDecodeError as e:
            print(f"{Colors.FAIL}Invalid JSON in playbook: {e}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}Automation Error: {e}{Colors.RESET}")
