import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel

console = Console()

class SystemMonitor:
    def get_metrics(self):
        """Standardized metric collection for both AI context and TUI display."""
        return {
            "cpu": psutil.cpu_percent(interval=None),
            "mem": psutil.virtual_memory().percent,
            "disk": psutil.disk_usage('/').percent,
            "boot_time": psutil.boot_time()
        }

    def display_dashboard(self):
        """Professional TUI Dashboard using the Rich Live library."""
        def generate_table():
            stats = self.get_metrics()
            table = Table(show_header=True, header_style="bold magenta", expand=True)
            table.add_column("Resource")
            table.add_column("Usage %", justify="right")
            table.add_column("Status", justify="center")

            for label, val in [("CPU", stats['cpu']), ("RAM", stats['mem']), ("Disk", stats['disk'])]:
                color = "red" if val > 85 else "yellow" if val > 60 else "green"
                status = "CRITICAL" if val > 85 else "WARNING" if val > 60 else "HEALTHY"
                table.add_row(label, f"[{color}]{val}%[/]", f"[{color}]{status}[/]")
            return table

        console.print(Panel("[bold cyan]NetMon-AI Live Dashboard[/]\n[italic]Monitoring system vitals...[/]", border_style="blue"))
        try:
            with Live(generate_table(), refresh_per_second=2) as live:
                while True:
                    time.sleep(0.5)
                    live.update(generate_table())
        except KeyboardInterrupt:
            console.print("\n[yellow]Dashboard suspended.[/]")