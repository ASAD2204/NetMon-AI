import subprocess
import os
from utils.colors import Colors

class ServiceManager:
    def __init__(self):
        self.os_type = os.name # 'nt' for Windows, 'posix' for Linux/macOS

    def _run_command(self, cmd):
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip(), result.stderr.strip(), result.returncode
        except Exception as e:
            return "", str(e), 1

    def manage_service(self, service_name, action):
        """
        Actions: start, stop, restart, status, enable, disable
        """
        if self.os_type == 'posix':
            # Linux systemd implementation
            cmd = f"sudo systemctl {action} {service_name}"
        else:
            # Windows Service Control (sc) implementation
            win_actions = {"start": "start", "stop": "stop", "status": "query", "restart": "restart"}
            action = win_actions.get(action, action)
            cmd = f"sc {action} {service_name}"

        print(f"{Colors.CYAN}Executing {action} on {service_name}...{Colors.RESET}")
        out, err, code = self._run_command(cmd)
        
        if code == 0:
            print(f"{Colors.GREEN}✓ Success:{Colors.RESET} {out if out else 'Action completed.'}")
        else:
            print(f"{Colors.FAIL}✗ Error:{Colors.RESET} {err}")

    def get_logs(self, service_name, lines=50):
        """Fetches the last N lines of logs for a service (Linux only)."""
        if self.os_type != 'posix':
            print(f"{Colors.WARNING}Service logs via journalctl are only supported on Linux.{Colors.RESET}")
            return
        
        cmd = f"sudo journalctl -u {service_name} -n {lines} --no-pager"
        out, err, _ = self._run_command(cmd)
        print(f"\n{Colors.BOLD}--- Logs for {service_name} ---{Colors.RESET}")
        print(out if out else err)