import subprocess
import os
import re
from utils.colors import Colors

class ServiceManager:
    def __init__(self):
        self.os_type = os.name  # 'nt' for Windows, 'posix' for Linux/macOS

    def _validate_service_name(self, service_name):
        """Validates service name to prevent injection"""
        # Service names should only contain alphanumeric, dash, underscore, dot
        if not re.match(r'^[a-zA-Z0-9_.-]+$', service_name):
            return False
        
        # Reasonable length limit
        if len(service_name) > 100:
            return False
        
        return True

    def _run_command(self, cmd):
        """Safely runs a command without shell=True"""
        try:
            # Never use shell=True for security
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10,
                shell=False  # IMPORTANT: Never use shell=True
            )
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except subprocess.TimeoutExpired:
            return "", "Command timed out", 1
        except Exception as e:
            return "", str(e), 1

    def manage_service(self, service_name, action):
        """
        Manage system services.
        Actions: start, stop, restart, status, enable, disable
        """
        # Validate service name
        if not self._validate_service_name(service_name):
            print(f"{Colors.FAIL}Invalid service name: contains forbidden characters{Colors.RESET}")
            return
        
        # Validate action
        valid_actions = ['start', 'stop', 'restart', 'status', 'enable', 'disable']
        if action not in valid_actions:
            print(f"{Colors.FAIL}Invalid action: {action}. Valid actions: {', '.join(valid_actions)}{Colors.RESET}")
            return
        
        if self.os_type == 'posix':
            # Linux systemd implementation - use list instead of shell command
            cmd = ['sudo', 'systemctl', action, service_name]
        else:
            # Windows Service Control (sc) implementation
            win_actions = {
                "start": "start",
                "stop": "stop",
                "status": "query",
                "restart": "restart",
                "enable": "config",
                "disable": "config"
            }
            action_cmd = win_actions.get(action, action)
            
            if action == "enable":
                cmd = ['sc', 'config', service_name, 'start=', 'auto']
            elif action == "disable":
                cmd = ['sc', 'config', service_name, 'start=', 'disabled']
            else:
                cmd = ['sc', action_cmd, service_name]

        print(f"{Colors.CYAN}Executing {action} on {service_name}...{Colors.RESET}")
        out, err, code = self._run_command(cmd)
        
        if code == 0:
            print(f"{Colors.GREEN}✓ Success: {out if out else 'Action completed.'}{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}✗ Error: {err}{Colors.RESET}")

    def get_logs(self, service_name, lines=50):
        """Fetches the last N lines of logs for a service (Linux only)."""
        if self.os_type != 'posix':
            print(f"{Colors.WARNING}Service logs via journalctl are only supported on Linux.{Colors.RESET}")
            return
        
        # Validate service name
        if not self._validate_service_name(service_name):
            print(f"{Colors.FAIL}Invalid service name{Colors.RESET}")
            return
        
        # Validate lines parameter
        try:
            lines = int(lines)
            if lines < 1 or lines > 1000:
                lines = 50
        except:
            lines = 50
        
        cmd = ['sudo', 'journalctl', '-u', service_name, '-n', str(lines), '--no-pager']
        out, err, code = self._run_command(cmd)
        
        print(f"\n{Colors.BOLD}--- Logs for {service_name} (last {lines} lines) ---{Colors.RESET}")
        if code == 0:
            print(out if out else "No logs available")
        else:
            print(f"{Colors.FAIL}{err}{Colors.RESET}")
