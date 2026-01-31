import psutil

class ProcessManager:
    @staticmethod
    def list_processes(limit=10, sort_by='cpu'):
        """Lists top processes by CPU or Memory."""
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
        try:
            psutil.Process(pid).terminate()
            return True, f"PID {pid} terminated."
        except Exception as e:
            return False, str(e)