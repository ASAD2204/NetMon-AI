#!/usr/bin/env python3
import os
import shlex
import sys
import time
import subprocess
from pathlib import Path

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
        
        # Security Configuration
        self._setup_security_rules()
        
        if os.name == 'nt':
            os.system('color')

    def _setup_security_rules(self):
        """Initialize security rules and restrictions"""
        # Define safe commands that can be passed to OS
        self.SAFE_NATIVE_COMMANDS = {
            'ls', 'dir', 'pwd', 'whoami', 'hostname', 
            'date', 'uptime', 'df', 'free', 'top',
            'netstat', 'ipconfig', 'ifconfig', 'route',
            'clear', 'cls'
        }
        
        # Define restricted paths
        self.FORBIDDEN_PATHS = [
            "/etc/shadow",
            "/etc/sudoers", 
            "/etc/passwd",
            "/boot",
            "/sys",
            "/proc",
            "C:\\Windows\\System32",
            "C:\\Windows\\SysWOW64",
            "/root",
            "/var/run"
        ]
        
        # Define allowed base directories (optional - can be commented out)
        self.ALLOWED_BASES = [
            str(Path.home()),  # User's home directory
            "/tmp",
            "/var/log",
            "C:\\temp",
            "C:\\Users\\Public"
        ]

    def _sanitize_and_validate_path(self, path_str):
        """
        Sanitizes and validates a path for security.
        Returns (is_safe, sanitized_path, error_message)
        """
        if not path_str or path_str.lower() == "none":
            return True, None, None
        
        # Remove quotes and whitespace
        cleaned = path_str.strip().replace('"', '').replace("'", "")
        
        # Resolve to absolute path
        try:
            abs_path = os.path.abspath(cleaned)
        except Exception as e:
            return False, None, f"Invalid path: {e}"
        
        # Check forbidden paths
        for forbidden in self.FORBIDDEN_PATHS:
            if os.name == 'nt':
                # Case-insensitive on Windows
                if abs_path.lower().startswith(forbidden.lower()):
                    return False, None, f"Access to {forbidden} is forbidden"
            else:
                if abs_path.startswith(forbidden):
                    return False, None, f"Access to {forbidden} is forbidden"
        
        return True, abs_path, None

    def welcome_banner(self):
        banner = Panel.fit(
            "[bold cyan]NetMon-AI: Intelligent Network Monitoring Platform[/]\n"
            "[italic green]Context Awareness: ACTIVE | Audit Logging: ENABLED | Security: ENHANCED[/]",
            border_style="magenta"
        )
        console.print(banner)
        print(f"Type {Colors.GREEN}'ask <query>'{Colors.RESET} for AI help or use native commands.")
        print(f"Type {Colors.GREEN}'help'{Colors.RESET} for available commands.\n")

    def show_help(self):
        """Display available commands"""
        help_text = f"""
{Colors.BOLD}{Colors.HEADER}=== NetMon-AI Command Reference ==={Colors.RESET}

{Colors.CYAN}AI Commands:{Colors.RESET}
  ask <query>              Ask AI for help (e.g., "ask show CPU usage")

{Colors.CYAN}System Monitoring:{Colors.RESET}
  monitor                  Open live system dashboard
  pslist                   List running processes
  pskill <pid>             Terminate a process by PID
  connections              Show active network connections

{Colors.CYAN}Security & Integrity:{Colors.RESET}
  register <file>          Register file for integrity monitoring
  audit                    Check registered files for tampering
  analyze <logfile>        AI-powered log analysis

{Colors.CYAN}Automation:{Colors.RESET}
  run-script <file>        Execute automation playbook

{Colors.CYAN}Network Tools:{Colors.RESET}
  (Use 'ask' for network operations like ping, port scan)

{Colors.CYAN}General:{Colors.RESET}
  help                     Show this help message
  clear / cls              Clear screen
  exit / quit              Exit NetMon-AI

{Colors.WARNING}Note: Many destructive operations require confirmation for safety.{Colors.RESET}
"""
        print(help_text)

    def run(self):
        self.welcome_banner()
        
        while True:
            try:
                # Dynamic prompt showing current directory
                prompt = f"{Colors.CYAN}{os.getcwd()} $ {Colors.RESET}"
                cmd_input = input(prompt).strip()
                
                if not cmd_input: 
                    continue
                    
                if cmd_input.lower() in ["exit", "quit"]: 
                    print(f"{Colors.GREEN}Shutting down NetMon-AI...{Colors.RESET}")
                    break

                parts = shlex.split(cmd_input)
                cmd = parts[0].lower()

                # --- COMMAND ROUTING ---

                if cmd == "help":
                    self.show_help()
                
                elif cmd == "ask":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: ask <your question>{Colors.RESET}")
                        continue
                    query = " ".join(parts[1:])
                    intent = self.ai_nlp.process_query(query)
                    self.route_ai_intent(query, intent)
                
                elif cmd == "monitor":
                    self.monitor.display_dashboard()
                
                elif cmd == "pslist":
                    procs = self.proc_mgr.list_processes()
                    print(f"\n{Colors.BOLD}{'PID':<10} {'Name':<25} {'CPU %':<10} {'Mem %':<10}{Colors.RESET}")
                    for p in procs:
                        print(f"{p['pid']:<10} {p['name']:<25} {p.get('cpu_percent', 0):<10} {p.get('memory_percent', 0):10.2f}")
                
                elif cmd == "pskill":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: pskill <pid>{Colors.RESET}")
                        continue
                    try:
                        pid = int(parts[1])
                        success, msg = self.proc_mgr.kill_process(pid)
                        print(f"{Colors.GREEN if success else Colors.FAIL}{msg}{Colors.RESET}")
                    except ValueError:
                        print(f"{Colors.FAIL}Error: PID must be a number{Colors.RESET}")

                elif cmd == "connections":
                    self.net_tools.show_connections()
                
                elif cmd == "register":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: register <filepath>{Colors.RESET}")
                        continue
                    self.integrity.register_file(parts[1])
                
                elif cmd == "audit":
                    self.integrity.check_integrity()
                
                elif cmd == "run-script":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: run-script <playbook_path>{Colors.RESET}")
                        continue
                    self.playbook.run_playbook(parts[1])
                
                elif cmd == "analyze":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: analyze <logfile>{Colors.RESET}")
                        continue
                    self.ai_logs.analyze_file(parts[1])
                
                elif cmd in ["clear", "cls"]:
                    os.system('cls' if os.name == 'nt' else 'clear')

                else:
                    # Check if command is in safe list
                    if cmd in self.SAFE_NATIVE_COMMANDS:
                        os.system(cmd_input)
                    else:
                        print(f"{Colors.WARNING}Command '{cmd}' not recognized.{Colors.RESET}")
                        print(f"Use {Colors.GREEN}'ask <query>'{Colors.RESET} for AI assistance")
                        print(f"or try: {Colors.CYAN}'help'{Colors.RESET} for available commands")

            except KeyboardInterrupt:
                print(f"\n{Colors.WARNING}Use 'exit' to quit.{Colors.RESET}")
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

        # --- PATH VALIDATION ---
        if target and target.lower() != "none":
            is_safe, clean_target, error = self._sanitize_and_validate_path(target)
            if not is_safe:
                print(f"{Colors.FAIL}Security Violation: {error}{Colors.RESET}")
                self.auditor.log_intent(query, intent, False)
                return
        else:
            clean_target = None

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
            if action == "MONITOR_MEM":
                stats = self.monitor.get_metrics()
                mem = stats.get('mem')
                try:
                    mem_val = float(mem)
                except Exception:
                    mem_val = mem
                if isinstance(mem_val, (int, float)):
                    color = Colors.FAIL if mem_val > 85 else Colors.WARNING if mem_val > 60 else Colors.GREEN
                    print(f"{Colors.BOLD}Memory Usage:{Colors.RESET} {color}{mem_val}%{Colors.RESET}")
                else:
                    print(f"Memory Usage: {mem}")

            elif action == "MONITOR_CPU":
                stats = self.monitor.get_metrics()
                cpu = stats.get('cpu')
                try:
                    cpu_val = float(cpu)
                except Exception:
                    cpu_val = cpu
                if isinstance(cpu_val, (int, float)):
                    color = Colors.FAIL if cpu_val > 85 else Colors.WARNING if cpu_val > 60 else Colors.GREEN
                    print(f"{Colors.BOLD}CPU Usage:{Colors.RESET} {color}{cpu_val}%{Colors.RESET}")
                else:
                    print(f"CPU Usage: {cpu}")

            elif action == "MONITOR_DISK":
                stats = self.monitor.get_metrics()
                disk = stats.get('disk')
                try:
                    disk_val = float(disk)
                except Exception:
                    disk_val = disk
                if isinstance(disk_val, (int, float)):
                    color = Colors.FAIL if disk_val > 85 else Colors.WARNING if disk_val > 60 else Colors.GREEN
                    print(f"{Colors.BOLD}Disk Usage:{Colors.RESET} {color}{disk_val}%{Colors.RESET}")
                else:
                    print(f"Disk Usage: {disk}")

            elif action == "MONITOR_DASHBOARD":
                # AI requested the full live dashboard
                self.monitor.display_dashboard()

            elif action == "LIST_FILES":
                search_term = clean_target if clean_target else "."
                # Use safe subprocess instead of os.system
                if os.name == 'nt':
                    subprocess.run(['dir', search_term], shell=False)
                else:
                    subprocess.run(['ls', '-la', search_term], shell=False)

            elif action == "MOVE_DIR":
                if clean_target and os.path.exists(clean_target):
                    os.chdir(clean_target)
                    print(f"{Colors.GREEN}Directory Changed: {os.getcwd()}{Colors.RESET}")
                else:
                    print(f"{Colors.FAIL}Directory does not exist: {clean_target}{Colors.RESET}")

            elif action == "MOVE_AND_LIST":
                if clean_target and os.path.exists(clean_target):
                    os.chdir(clean_target)
                    print(f"{Colors.GREEN}Moved to: {os.getcwd()}{Colors.RESET}")
                    if os.name == 'nt':
                        subprocess.run(['dir'], shell=False)
                    else:
                        subprocess.run(['ls', '-la'], shell=False)
                else:
                    print(f"{Colors.FAIL}Directory does not exist: {clean_target}{Colors.RESET}")

            elif action == "SERVICE_OP":
                if clean_target and value:
                    self.svc_mgr.manage_service(clean_target, value)
                else:
                    print(f"{Colors.FAIL}Service operation requires service name and action{Colors.RESET}")

            elif action == "KILL_PROC":
                try:
                    pid = int(clean_target)
                    if pid <= 0:
                        print(f"{Colors.FAIL}Invalid PID{Colors.RESET}")
                    else:
                        success, msg = self.proc_mgr.kill_process(pid)
                        print(f"{Colors.GREEN if success else Colors.FAIL}{msg}{Colors.RESET}")
                except (ValueError, TypeError):
                    print(f"{Colors.FAIL}Invalid PID: must be a number{Colors.RESET}")

            elif action == "PORT_SCAN":
                if clean_target:
                    # Add basic validation to prevent scanning arbitrary hosts
                    print(f"{Colors.CYAN}Scanning {clean_target}...{Colors.RESET}")
                    self.net_tools.port_scan(clean_target)
                else:
                    print(f"{Colors.FAIL}Port scan requires a target host{Colors.RESET}")

            elif action == "PING":
                if clean_target:
                    self.net_tools.ping(clean_target)
                else:
                    print(f"{Colors.FAIL}Ping requires a target host{Colors.RESET}")

            elif action == "BANDWIDTH":
                self.net_tools.get_bandwidth()

            elif action == "CONNECTIONS":
                self.net_tools.show_connections()

            elif action == "MONITOR_SUMMARY":
                stats = self.monitor.get_metrics()
                # Format CPU / MEM / DISK in one concise block
                cpu = stats.get('cpu')
                mem = stats.get('mem')
                disk = stats.get('disk')
                def fmt(label, val):
                    try:
                        v = float(val)
                        color = Colors.FAIL if v > 85 else Colors.WARNING if v > 60 else Colors.GREEN
                        return f"{label}: {color}{v}%{Colors.RESET}"
                    except Exception:
                        return f"{label}: {val}"

                print(fmt('CPU', cpu) + '  |  ' + fmt('MEM', mem) + '  |  ' + fmt('DISK', disk))

            elif action == "UNKNOWN":
                print(f"{Colors.WARNING}AI Analysis: {intent.get('message', 'Unable to understand query')}{Colors.RESET}")

            else:
                print(f"{Colors.WARNING}Action '{action}' is not implemented yet.{Colors.RESET}")

        except Exception as e:
            print(f"{Colors.FAIL}Execution Error: {e}{Colors.RESET}")

if __name__ == "__main__":
    shell = NetMonShell()
    shell.run()
