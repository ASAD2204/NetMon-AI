import subprocess
import os
from utils.colors import Colors

class UserManager:
    def _run(self, cmd):
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.returncode == 0, res.stdout, res.stderr

    def add_user(self, username):
        if os.name == 'nt':
            cmd = f"net user {username} /add"
        else:
            cmd = f"sudo useradd -m {username}"
        
        success, _, err = self._run(cmd)
        if success:
            print(f"{Colors.GREEN}User '{username}' added.{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}Error: {err}{Colors.RESET}")

    def list_users(self):
        print(f"{Colors.HEADER}--- System Users ---{Colors.RESET}")
        if os.name == 'nt':
            _, out, _ = self._run("net user")
            print(out)
        else:
            with open('/etc/passwd', 'r') as f:
                for line in f:
                    print(line.split(':')[0])