#!/usr/bin/env python3
import os
import shlex
import sys
import time
import subprocess
import json
import re
from pathlib import Path
from datetime import datetime

# --- EXTERNAL LIBRARIES ---
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.prompt import Confirm
except ImportError:
    print("Error: 'rich' library not found. Run 'pip install rich'")
    sys.exit(1)

# Readline for enhanced command history and autocomplete
try:
    import readline
except ImportError:
    try:
        import pyreadline3 as readline  # Windows alternative
    except ImportError:
        readline = None

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
from core.alerting import AlertingSystem
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
        self.alerting = AlertingSystem()      
        
        # Intelligence Layer
        self.ai_nlp = NLPInterface()
        self.ai_logs = LogAnalyzer()
        
        # Enhanced Features
        self.history_file = "data/command_history.json"
        self.aliases_file = "data/aliases.json"
        self.command_history = self._load_history()
        self.aliases = self._load_aliases()
        
        # Security Configuration
        self._setup_security_rules()
        
        # Setup Autocomplete
        self._setup_autocomplete()
        
        if os.name == 'nt':
            os.system('color')

    def _load_history(self):
        """Load persistent command history"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save command history to file"""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.command_history[-1000:], f, indent=2)  # Keep last 1000
        except Exception as e:
            pass
    
    def _load_aliases(self):
        """Load user-defined command aliases"""
        if os.path.exists(self.aliases_file):
            try:
                with open(self.aliases_file, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_aliases(self):
        """Save command aliases to file"""
        os.makedirs(os.path.dirname(self.aliases_file), exist_ok=True)
        try:
            with open(self.aliases_file, 'w') as f:
                json.dump(self.aliases, f, indent=2)
        except Exception as e:
            pass
    
    def _get_git_branch(self):
        """Get current Git branch if in a repository"""
        try:
            result = subprocess.run(
                ["git", "branch", "--show-current"],
                capture_output=True,
                text=True,
                stderr=subprocess.DEVNULL,
                timeout=2
            )
            if result.returncode == 0 and result.stdout.strip():
                return result.stdout.strip()
        except:
            pass
        return None
    
    def _setup_autocomplete(self):
        """Setup command autocomplete with readline"""
        if readline:
            # Load history into readline
            readline.clear_history()
            for cmd in self.command_history:
                readline.add_history(cmd)
            
            # Setup tab completion
            readline.set_completer(self._completer)
            readline.parse_and_bind("tab: complete")
            
            # Setup Ctrl+R for reverse search (works on Unix-like systems)
            if os.name != 'nt':
                readline.parse_and_bind(r"\C-r: reverse-search-history")
    
    def _completer(self, text, state):
        """Autocomplete function for commands and file paths"""
        commands = ['ask', 'monitor', 'pslist', 'pskill', 'connections', 'register',
                   'audit', 'run-script', 'analyze', 'help', 'clear', 'cls', 'exit',
                   'search', 'cat', 'touch', 'alias', 'unalias', 'aliases', 'history',
                   'export', 'health', 'pwd', 'cd', 'ls', 'dir']
        
        # Add aliases to suggestions
        commands.extend(self.aliases.keys())
        
        # Add files in current directory
        try:
            files = os.listdir('.')
            options = commands + files
        except:
            options = commands
        
        matches = [s for s in options if s.startswith(text)]
        try:
            return matches[state]
        except IndexError:
            return None
    
    def _setup_security_rules(self):
        """Initialize security rules and restrictions"""
        # Define safe commands that can be passed to OS
        self.SAFE_NATIVE_COMMANDS = {
            'ls', 'dir', 'pwd', 'whoami', 'hostname', 
            'date', 'uptime', 'df', 'free', 'top',
            'netstat', 'ipconfig', 'ifconfig', 'route',
            'clear', 'cls', 'git'
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

    def _cmd_search(self, parts):
        """Search for text in a file (grep-like)"""
        if len(parts) < 3:
            print(f"{Colors.WARNING}Usage: search <text> <filename>{Colors.RESET}")
            return
        
        text_to_find = parts[1]
        filename = parts[2]
        
        if not os.path.exists(filename):
            print(f"{Colors.FAIL}Error: File '{filename}' not found{Colors.RESET}")
            return
        
        try:
            found = False
            with open(filename, 'r', errors='ignore') as f:
                for line_num, line in enumerate(f, 1):
                    if text_to_find in line:
                        found = True
                        print(f"{Colors.CYAN}Line {line_num}:{Colors.RESET} {line.rstrip()}")
            
            if not found:
                print(f"{Colors.WARNING}Text '{text_to_find}' not found in '{filename}'{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.RESET}")
    
    def _cmd_cat(self, parts):
        """Display file contents"""
        if len(parts) < 2:
            print(f"{Colors.WARNING}Usage: cat <filename>{Colors.RESET}")
            return
        
        filename = parts[1]
        if not os.path.exists(filename):
            print(f"{Colors.FAIL}Error: File '{filename}' not found{Colors.RESET}")
            return
        
        try:
            with open(filename, 'r', errors='ignore') as f:
                print(f.read())
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.RESET}")
    
    def _cmd_touch(self, parts):
        """Create an empty file or update timestamp"""
        if len(parts) < 2:
            print(f"{Colors.WARNING}Usage: touch <filename>{Colors.RESET}")
            return
        
        filename = parts[1]
        try:
            Path(filename).touch()
            print(f"{Colors.GREEN}File '{filename}' created/updated{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.RESET}")
    
    def _cmd_pwd(self):
        """Print working directory"""
        print(f"{Colors.BOLD}{os.getcwd()}{Colors.RESET}")
    
    def _cmd_cd(self, parts):
        """Change directory"""
        if len(parts) < 2:
            print(f"{Colors.WARNING}Usage: cd <directory>{Colors.RESET}")
            return
        
        path = parts[1]
        try:
            os.chdir(path)
            print(f"{Colors.GREEN}Changed to: {os.getcwd()}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}cd: {e}{Colors.RESET}")
    
    def _cmd_ls(self, parts):
        """List directory contents with colors"""
        target_dir = parts[1] if len(parts) > 1 else '.'
        
        try:
            if not os.path.exists(target_dir):
                print(f"{Colors.FAIL}Error: Directory '{target_dir}' not found{Colors.RESET}")
                return
            
            items = sorted(os.listdir(target_dir))
            print(f"{Colors.BOLD}Contents of {target_dir}:{Colors.RESET}")
            for item in items:
                full_path = os.path.join(target_dir, item)
                if os.path.isdir(full_path):
                    print(f"{Colors.BLUE}{item}/{Colors.RESET}")
                else:
                    print(f"{Colors.GREEN}{item}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.RESET}")
    
    def _cmd_execute_piped(self, command_str):
        """Execute command with pipe or redirection support"""
        try:
            # Handle piping
            if "|" in command_str:
                pipe_parts = command_str.split("|")
                p1 = subprocess.Popen(pipe_parts[0].strip(), shell=True, stdout=subprocess.PIPE, text=True)
                p2 = subprocess.Popen(pipe_parts[1].strip(), shell=True, stdin=p1.stdout, stdout=subprocess.PIPE, text=True)
                p1.stdout.close()
                output, _ = p2.communicate()
                if output:
                    print(output, end="")
                return
            
            # Handle redirection
            if ">" in command_str:
                parts = command_str.split(">")
                cmd_part = parts[0].strip()
                file_part = parts[1].strip()
                with open(file_part, "w") as f:
                    subprocess.run(cmd_part, shell=True, stdout=f, stderr=subprocess.PIPE, text=True)
                print(f"{Colors.GREEN}Output saved to {file_part}{Colors.RESET}")
                return
            
            # Normal execution
            result = subprocess.run(command_str, shell=True, capture_output=True, text=True)
            if result.stdout:
                print(result.stdout, end="")
            if result.stderr:
                print(f"{Colors.FAIL}{result.stderr}{Colors.RESET}", end="")
        
        except Exception as e:
            print(f"{Colors.FAIL}Execution Error: {e}{Colors.RESET}")
    
    def _cmd_alias(self, parts):
        """Create command alias"""
        if len(parts) < 3:
            print(f"{Colors.WARNING}Usage: alias <name> <command>{Colors.RESET}")
            return
        
        alias_name = parts[1]
        alias_command = " ".join(parts[2:])
        self.aliases[alias_name] = alias_command
        self._save_aliases()
        print(f"{Colors.GREEN}Alias created: {alias_name} -> {alias_command}{Colors.RESET}")
    
    def _cmd_unalias(self, parts):
        """Remove command alias"""
        if len(parts) < 2:
            print(f"{Colors.WARNING}Usage: unalias <name>{Colors.RESET}")
            return
        
        alias_name = parts[1]
        if alias_name in self.aliases:
            del self.aliases[alias_name]
            self._save_aliases()
            print(f"{Colors.GREEN}Alias '{alias_name}' removed{Colors.RESET}")
        else:
            print(f"{Colors.WARNING}Alias '{alias_name}' not found{Colors.RESET}")
    
    def _cmd_show_aliases(self):
        """Display all aliases"""
        if not self.aliases:
            print(f"{Colors.WARNING}No aliases defined{Colors.RESET}")
            return
        
        print(f"{Colors.HEADER}=== Command Aliases ==={Colors.RESET}")
        for name, command in self.aliases.items():
            print(f"{Colors.CYAN}{name}{Colors.RESET} -> {command}")
    
    def _cmd_history(self):
        """Show command history"""
        print(f"{Colors.HEADER}=== Command History ==={Colors.RESET}")
        start = max(0, len(self.command_history) - 50)  # Show last 50
        for i, cmd in enumerate(self.command_history[start:], start + 1):
            print(f"{i}: {cmd}")
    
    def _cmd_export_system_state(self):
        """Export system state to JSON"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = f"data/system_snapshot_{timestamp}.json"
            
            state = {
                "timestamp": datetime.now().isoformat(),
                "metrics": self.monitor.get_metrics(),
                "processes": len(self.proc_mgr.list_processes()),
                "cwd": os.getcwd(),
                "git_branch": self._get_git_branch(),
                "aliases": self.aliases
            }
            
            os.makedirs(os.path.dirname(export_file), exist_ok=True)
            with open(export_file, 'w') as f:
                json.dump(state, f, indent=2)
            
            print(f"{Colors.GREEN}System state exported to: {export_file}{Colors.RESET}")
        except Exception as e:
            print(f"{Colors.FAIL}Export failed: {e}{Colors.RESET}")
    
    def _cmd_system_health(self):
        """Calculate and display overall system health score"""
        try:
            stats = self.monitor.get_metrics()
            cpu = float(stats.get('cpu', 0))
            mem = float(stats.get('mem', 0))
            disk = float(stats.get('disk', 0))
            
            # Check for alerts
            self.alerting.check_system_metrics(stats)
            
            # Calculate health score (100 = perfect)
            cpu_score = max(0, 100 - cpu)
            mem_score = max(0, 100 - mem)
            disk_score = max(0, 100 - disk)
            
            overall_score = (cpu_score + mem_score + disk_score) / 3
            
            # Determine health status
            if overall_score >= 85:
                status = "EXCELLENT"
                color = Colors.GREEN
            elif overall_score >= 70:
                status = "GOOD"
                color = Colors.GREEN
            elif overall_score >= 50:
                status = "FAIR"
                color = Colors.WARNING
            else:
                status = "POOR"
                color = Colors.FAIL
            
            print(f"{Colors.BOLD}{Colors.HEADER}=== System Health Report ==={Colors.RESET}")
            print(f"CPU Usage: {cpu:.1f}% (Score: {cpu_score:.1f}/100)")
            print(f"Memory Usage: {mem:.1f}% (Score: {mem_score:.1f}/100)")
            print(f"Disk Usage: {disk:.1f}% (Score: {disk_score:.1f}/100)")
            print(f"\n{Colors.BOLD}Overall Health: {color}{overall_score:.1f}/100 - {status}{Colors.RESET}")
        
        except Exception as e:
            print(f"{Colors.FAIL}Health check failed: {e}{Colors.RESET}")
    
    def show_help(self):
        """Display available commands"""
        help_text = f"""
{Colors.BOLD}{Colors.HEADER}=== NetMon-AI Command Reference ==={Colors.RESET}

{Colors.CYAN}AI Commands:{Colors.RESET}
  ask <query>              Ask AI for help (e.g., "ask show CPU usage")

{Colors.CYAN}System Monitoring:{Colors.RESET}
  monitor                  Open live system dashboard
  health                   Show overall system health score
  pslist                   List running processes
  pskill <pid>             Terminate a process by PID
  connections              Show active network connections

{Colors.CYAN}File Operations:{Colors.RESET}
  ls [dir] / dir [dir]     List directory contents
  cd <dir>                 Change directory
  pwd                      Print working directory
  cat <file>               Display file contents
  touch <file>             Create/update file
  search <text> <file>     Search text in file

{Colors.CYAN}Security & Integrity:{Colors.RESET}
  register <file>          Register file for integrity monitoring
  audit                    Check registered files for tampering
  analyze <logfile>        AI-powered log analysis
  tail <logfile>           Follow log file in real-time
  log-stats <logfile>      Generate log statistics
  bookmark-log <name> <path>  Bookmark a log file
  bookmarks                List log bookmarks

{Colors.CYAN}Automation:{Colors.RESET}
  run-script <file>        Execute automation playbook
  alias <name> <cmd>       Create command shortcut
  unalias <name>           Remove alias
  aliases                  Show all aliases

{Colors.CYAN}Utilities:{Colors.RESET}
  history                  Show command history
  export                   Export system state snapshot
  alerts [count]           Show recent alerts (default: 10)
  alert-config             Show alert configuration
  set-threshold <res>      Set alert thresholds (cpu/mem/disk)
  sessions                 Show active user sessions
  password-policy          Show password policies
  help                     Show this help message
  clear / cls              Clear screen
  exit / quit              Exit NetMon-AI

{Colors.CYAN}Advanced:{Colors.RESET}
  command | command        Pipe output between commands
  command > file           Redirect output to file

{Colors.WARNING}Note: Many destructive operations require confirmation for safety.{Colors.RESET}
"""
        print(help_text)

    def run(self):
        self.welcome_banner()
        
        while True:
            try:
                # Dynamic prompt with Git branch support
                cwd = os.getcwd()
                branch = self._get_git_branch()
                if branch:
                    prompt = f"{Colors.CYAN}{cwd} {Colors.WARNING}({branch}){Colors.RESET} $ "
                else:
                    prompt = f"{Colors.CYAN}{cwd} $ {Colors.RESET}"
                
                cmd_input = input(prompt).strip()
                
                if not cmd_input: 
                    continue
                
                # Save to history
                self.command_history.append(cmd_input)
                if readline:
                    readline.add_history(cmd_input)
                
                if cmd_input.lower() in ["exit", "quit"]: 
                    self._save_history()
                    print(f"{Colors.GREEN}Shutting down NetMon-AI...{Colors.RESET}")
                    break
                
                # Check for aliases
                if cmd_input.split()[0] in self.aliases:
                    alias_cmd = self.aliases[cmd_input.split()[0]]
                    remaining = " ".join(cmd_input.split()[1:])
                    cmd_input = f"{alias_cmd} {remaining}".strip()
                    print(f"{Colors.CYAN}Expanding alias to: {cmd_input}{Colors.RESET}")
                
                # Handle piping and redirection before parsing
                if "|" in cmd_input or ">" in cmd_input:
                    self._cmd_execute_piped(cmd_input)
                    continue
                
                try:
                    parts = shlex.split(cmd_input)
                except ValueError:
                    print(f"{Colors.FAIL}Error: Unbalanced quotes{Colors.RESET}")
                    continue
                
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
                
                elif cmd == "health":
                    self._cmd_system_health()
                
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
                
                # Log viewing
                elif cmd == "tail":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: tail <logfile|bookmark>{Colors.RESET}")
                        continue
                    self.log_view.tail_logs(parts[1])
                
                elif cmd == "log-stats":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: log-stats <logfile|bookmark>{Colors.RESET}")
                        continue
                    self.log_view.parse_log_stats(parts[1])
                
                elif cmd == "bookmark-log":
                    if len(parts) < 3:
                        print(f"{Colors.WARNING}Usage: bookmark-log <name> <path>{Colors.RESET}")
                        continue
                    self.log_view.add_bookmark(parts[1], parts[2])
                
                elif cmd == "bookmarks":
                    self.log_view.list_bookmarks()
                
                # File operations
                elif cmd in ["ls", "dir"]:
                    self._cmd_ls(parts)
                
                elif cmd == "cd":
                    self._cmd_cd(parts)
                
                elif cmd == "pwd":
                    self._cmd_pwd()
                
                elif cmd == "cat":
                    self._cmd_cat(parts)
                
                elif cmd == "touch":
                    self._cmd_touch(parts)
                
                elif cmd == "search":
                    self._cmd_search(parts)
                
                # Aliases
                elif cmd == "alias":
                    self._cmd_alias(parts)
                
                elif cmd == "unalias":
                    self._cmd_unalias(parts)
                
                elif cmd == "aliases":
                    self._cmd_show_aliases()
                
                # Utilities
                elif cmd == "history":
                    self._cmd_history()
                
                elif cmd == "export":
                    self._cmd_export_system_state()
                
                elif cmd == "alerts":
                    count = int(parts[1]) if len(parts) > 1 else 10
                    self.alerting.get_recent_alerts(count)
                
                elif cmd == "alert-config":
                    self.alerting.show_config()
                
                elif cmd == "set-threshold":
                    if len(parts) < 2:
                        print(f"{Colors.WARNING}Usage: set-threshold <resource> [warning] [critical]{Colors.RESET}")
                        print(f"Example: set-threshold cpu 75 90")
                        continue
                    resource = parts[1]
                    warning = int(parts[2]) if len(parts) > 2 else None
                    critical = int(parts[3]) if len(parts) > 3 else None
                    self.alerting.configure_thresholds(resource, warning, critical)
                
                elif cmd == "sessions":
                    self.user_mgr.get_active_sessions()
                
                elif cmd == "password-policy":
                    self.user_mgr.show_password_policies()
                
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
