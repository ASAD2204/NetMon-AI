import json
import os
import subprocess
from utils.colors import Colors

class PlaybookEngine:
    def run_playbook(self, playbook_path):
        """Executes a JSON-defined sequence of administrative tasks."""
        if not os.path.exists(playbook_path):
            print(f"{Colors.FAIL}Playbook not found: {playbook_path}{Colors.RESET}")
            return

        try:
            with open(playbook_path, 'r') as f:
                tasks = json.load(f)
            
            print(f"{Colors.HEADER}🚀 Executing Automation Sequence...{Colors.RESET}")
            for i, task in enumerate(tasks, 1):
                print(f"{Colors.CYAN}[{i}/{len(tasks)}] Running: {task}{Colors.RESET}")
                # shell=True is used here to allow native pipe/commands, 
                # but only from your local JSON files.
                result = subprocess.run(task, shell=True)
                if result.returncode != 0:
                    print(f"{Colors.FAIL}Critical failure in task {i}. Sequence halted.{Colors.RESET}")
                    break
            print(f"{Colors.GREEN}✔ Playbook completed.{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}Automation Error: {e}{Colors.RESET}")