#!/usr/bin/env python3
import os
import shlex
import sys
import time

# --- EXTERNAL LIBRARIES ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm
except ImportError:
    print("Error: 'rich' library not found. Run 'pip install rich'")
    sys.exit(1)

# --- CUSTOM MODULES ---
from utils.colors import Colors
from core.monitoring import SystemMonitor
from core.process_manager import ProcessManager
from core.service_manager import ServiceManager
from core.network_tools import NetworkTools
from core.user_manager import UserManager
from core.log_viewer import LogViewer
from core.integrity import IntegrityMonitor
from core.automation import PlaybookEngine
from core.auditor import AuditLogger      
from ai.nlp_interface import NLPInterface
from ai.log_analyzer import LogAnalyzer

console = Console()

class NetMonShell:
    def __init__(self):
        # Core Infrastructure
        self.monitor = SystemMonitor()
        self.proc_mgr = ProcessManager()
        self.svc_mgr = ServiceManager()
        self.net_tools = NetworkTools()
        self.user_mgr = UserManager()
        self.log_view = LogViewer()
        
        # Security & Compliance
        self.integrity = IntegrityMonitor()
        self.playbook = PlaybookEngine()
        self.auditor = AuditLogger()      
        
        # Intelligence Layer
        self.ai_nlp = NLPInterface()
        self.ai_logs = LogAnalyzer()
        
        if os.name == 'nt':
            os.system('color')

    def welcome_banner(self):
        banner = Panel.fit(
            "[bold cyan]NetMon-AI: Intelligent Network Monitoring Platform[/]\n"
            "[italic green]Context Awareness: ACTIVE | Audit Logging: ENABLED[/]",
            border_style="magenta"
        )
        console.print(banner)
        print(f"Type {Colors.GREEN}'ask <query>'{Colors.RESET} for AI help or use native commands.")

    def run(self):
        self.welcome_banner()
        
        while True:
            try:
                # Dynamic prompt showing current directory
                prompt = f"{Colors.CYAN}{os.getcwd()} $ {Colors.RESET}"
                cmd_input = input(prompt).strip()
                
                if not cmd_input: continue
                if cmd_input.lower() in ["exit", "quit"]: 
                    print("Shutting down NetMon-AI...")
                    break

                parts = shlex.split(cmd_input)
                cmd = parts[0].lower()

                # --- COMMAND ROUTING ---

                if cmd == "ask":
                    query = " ".join(parts[1:])
                    # The NLP Interface now receives the CWD via context injection internally
                    intent = self.ai_nlp.process_query(query)
                    self.route_ai_intent(query, intent)
                
                elif cmd == "monitor":
                    self.monitor.display_dashboard()
                
                elif cmd == "pslist":
                    procs = self.proc_mgr.list_processes()
                    print(f"\n{Colors.BOLD}{'PID':<10} {'Name':<25} {'CPU %':<10} {'Mem %':<10}{Colors.RESET}")
                    for p in procs:
                        print(f"{p['pid']:<10} {p['name']:<25} {p.get('cpu_percent', 0):<10} {p.get('memory_percent', 0):10.2f}")
                
                elif cmd == "pskill" and len(parts) > 1:
                    success, msg = self.proc_mgr.kill_process(int(parts[1]))
                    print(f"{Colors.GREEN if success else Colors.FAIL}{msg}{Colors.RESET}")

                elif cmd == "connections":
                    self.net_tools.show_connections()
                
                elif cmd in ["clear", "cls"]:
                    os.system('cls' if os.name == 'nt' else 'clear')

                else:
                    # Native OS Fallback
                    os.system(cmd_input)

            except KeyboardInterrupt:
                print("\nUse 'exit' to quit.")
            except Exception as e:
                console.print(f"[bold red]Shell Error:[/] {e}")

    def route_ai_intent(self, query, intent):
        """
        Secure Intent Router with Path Sanitization and Audit Trail.
        """
        action = intent.get("action")
        target = intent.get("target")
        value = intent.get("value")
        risk = intent.get("risk_level", "GREEN")

        # --- THE SECURITY GATE ---
        authorized = True
        if risk in ["YELLOW", "RED"]:
            print(f"\n{Colors.WARNING}⚠️  SECURITY ALERT: {risk} RISK ACTION DETECTED{Colors.RESET}")
            print(f"Proposed Action: {action} on {target}")
            authorized = Confirm.ask(f"[bold yellow]Do you authorize this system change?[/]")
            
            if not authorized:
                print(f"{Colors.FAIL}Action Rejected.{Colors.RESET}")

        # --- THE AUDIT TRAIL ---
        self.auditor.log_intent(query, intent, authorized)

        if not authorized:
            return

        # --- EXECUTION ENGINE ---
        try:
            # Path Sanitization for Windows/Linux
            clean_target = target.replace('"', '').replace("'", "").strip() if target else None

            if action in ["MONITOR_CPU", "MONITOR_MEM"]:
                self.monitor.display_dashboard()

            elif action == "LIST_FILES":
                search_term = clean_target if clean_target and clean_target != "none" else "*"
                os.system(f'dir "{search_term}"' if os.name == 'nt' else f"ls -la {search_term}")

            elif action == "MOVE_DIR":
                os.chdir(clean_target)
                print(f"{Colors.GREEN}Directory Changed: {os.getcwd()}{Colors.RESET}")

            elif action == "MOVE_AND_LIST":
                os.chdir(clean_target)
                print(f"{Colors.GREEN}Moved to: {os.getcwd()}{Colors.RESET}")
                os.system('dir' if os.name == 'nt' else 'ls')

            elif action == "SERVICE_OP":
                self.svc_mgr.manage_service(clean_target, value)

            elif action == "KILL_PROC":
                self.proc_mgr.kill_process(int(clean_target))

            elif action == "UNKNOWN":
                print(f"{Colors.WARNING}AI Analysis:[/] {intent.get('message')}")

        except Exception as e:
            print(f"{Colors.FAIL}Execution Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    shell = NetMonShell()
    shell.run()