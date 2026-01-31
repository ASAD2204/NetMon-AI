def format_bytes(size):
    """Converts bytes to human-readable format (MB, GB)."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

def validate_pid(pid_str):
    """Ensures input is a valid process ID."""
    return pid_str.isdigit() and int(pid_str) > 0