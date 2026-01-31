import psutil
import os

class ProcessManager:
    @staticmethod
    def list_processes(limit=10, sort_by='cpu'):
        """Lists top processes by CPU or Memory."""
        # Validate inputs
        if not isinstance(limit, int) or limit < 1 or limit > 100:
            limit = 10
        
        if sort_by not in ['cpu', 'memory']:
            sort_by = 'cpu'
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        key = 'cpu_percent' if sort_by == 'cpu' else 'memory_percent'
        processes.sort(key=lambda x: x.get(key, 0), reverse=True)
        return processes[:limit]

    @staticmethod
    def kill_process(pid):
        """Terminates a process by PID."""
        # Validate PID type
        if not isinstance(pid, int):
            try:
                pid = int(pid)
            except (ValueError, TypeError):
                return False, "Invalid PID: must be a number"
        
        # Validate PID value
        if pid <= 0:
            return False, "Invalid PID: must be positive"
        
        # Check if process exists
        if not psutil.pid_exists(pid):
            return False, f"Process {pid} does not exist"
        
        try:
            proc = psutil.Process(pid)
            
            # Don't allow killing critical system processes
            CRITICAL_PROCESSES = {
                'systemd', 'init', 'kernel', 'sshd', 
                'System', 'csrss.exe', 'smss.exe', 'wininit.exe',
                'services.exe', 'lsass.exe', 'winlogon.exe'
            }
            
            proc_name = proc.name().lower()
            for critical in CRITICAL_PROCESSES:
                if critical.lower() in proc_name:
                    return False, f"Cannot kill critical system process: {proc.name()}"
            
            # Check permissions (only on Unix-like systems)
            if os.name != 'nt':
                try:
                    current_user = psutil.Process().username()
                    target_user = proc.username()
                    
                    if current_user != target_user and os.getuid() != 0:
                        return False, "Permission denied: requires elevated privileges"
                except:
                    pass  # Skip permission check if it fails
            
            # Attempt graceful termination
            proc.terminate()
            
            # Wait for process to terminate
            try:
                proc.wait(timeout=3)
                return True, f"PID {pid} terminated successfully."
            except psutil.TimeoutExpired:
                # Force kill if terminate didn't work
                proc.kill()
                proc.wait(timeout=2)
                return True, f"PID {pid} force killed (did not respond to termination)."
                
        except psutil.NoSuchProcess:
            return False, f"Process {pid} no longer exists"
        except psutil.AccessDenied:
            return False, f"Access denied: insufficient permissions to kill PID {pid}"
        except Exception as e:
            return False, f"Error: {str(e)}"
