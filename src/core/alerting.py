import os
import json
import smtplib
import subprocess
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from utils.colors import Colors

class AlertingSystem:
    """
    Alert notification system for critical events.
    Supports multiple notification channels: Console, File, Email, Webhook
    """
    def __init__(self, config_file="data/alert_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
        self.alert_history_file = "data/alert_history.json"
        self.alert_history = self._load_history()
        self.suppression_window = 300  # 5 minutes in seconds
    
    def _load_config(self):
        """Load alert configuration"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except:
                return self._get_default_config()
        return self._get_default_config()
    
    def _get_default_config(self):
        """Default alert configuration"""
        return {
            "enabled": True,
            "thresholds": {
                "cpu_critical": 90,
                "cpu_warning": 75,
                "memory_critical": 90,
                "memory_warning": 75,
                "disk_critical": 90,
                "disk_warning": 80
            },
            "channels": {
                "console": True,
                "file": True,
                "email": False,
                "webhook": False
            },
            "email": {
                "smtp_server": "smtp.gmail.com",
                "smtp_port": 587,
                "sender": "",
                "password": "",
                "recipients": []
            },
            "webhook": {
                "url": "",
                "method": "POST"
            }
        }
    
    def _save_config(self):
        """Save alert configuration"""
        os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def _load_history(self):
        """Load alert history"""
        if os.path.exists(self.alert_history_file):
            try:
                with open(self.alert_history_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_history(self):
        """Save alert history"""
        os.makedirs(os.path.dirname(self.alert_history_file), exist_ok=True)
        # Keep only last 1000 alerts
        with open(self.alert_history_file, 'w') as f:
            json.dump(self.alert_history[-1000:], f, indent=2)
    
    def _should_suppress(self, alert_type, resource):
        """Check if alert should be suppressed (deduplication)"""
        now = datetime.now()
        for alert in reversed(self.alert_history):
            if alert.get("type") == alert_type and alert.get("resource") == resource:
                alert_time = datetime.fromisoformat(alert.get("timestamp"))
                time_diff = (now - alert_time).total_seconds()
                if time_diff < self.suppression_window:
                    return True
        return False
    
    def check_system_metrics(self, metrics):
        """
        Check system metrics against thresholds and trigger alerts
        
        Args:
            metrics (dict): Dictionary containing cpu, mem, disk percentages
        """
        if not self.config.get("enabled", True):
            return
        
        thresholds = self.config.get("thresholds", {})
        
        # Check CPU
        cpu = metrics.get("cpu", 0)
        if cpu >= thresholds.get("cpu_critical", 90):
            self.trigger_alert("CRITICAL", "CPU", f"CPU usage at {cpu:.1f}%", cpu)
        elif cpu >= thresholds.get("cpu_warning", 75):
            self.trigger_alert("WARNING", "CPU", f"CPU usage at {cpu:.1f}%", cpu)
        
        # Check Memory
        mem = metrics.get("mem", 0)
        if mem >= thresholds.get("memory_critical", 90):
            self.trigger_alert("CRITICAL", "Memory", f"Memory usage at {mem:.1f}%", mem)
        elif mem >= thresholds.get("memory_warning", 75):
            self.trigger_alert("WARNING", "Memory", f"Memory usage at {mem:.1f}%", mem)
        
        # Check Disk
        disk = metrics.get("disk", 0)
        if disk >= thresholds.get("disk_critical", 90):
            self.trigger_alert("CRITICAL", "Disk", f"Disk usage at {disk:.1f}%", disk)
        elif disk >= thresholds.get("disk_warning", 80):
            self.trigger_alert("WARNING", "Disk", f"Disk usage at {disk:.1f}%", disk)
    
    def trigger_alert(self, severity, resource, message, value=None):
        """
        Trigger an alert through configured channels
        
        Args:
            severity (str): CRITICAL, WARNING, INFO
            resource (str): Resource type (CPU, Memory, Disk, etc.)
            message (str): Alert message
            value (float): Optional metric value
        """
        # Check suppression
        if self._should_suppress(severity, resource):
            return
        
        alert = {
            "timestamp": datetime.now().isoformat(),
            "severity": severity,
            "resource": resource,
            "message": message,
            "value": value
        }
        
        # Add to history
        self.alert_history.append(alert)
        self._save_history()
        
        channels = self.config.get("channels", {})
        
        # Console notification
        if channels.get("console", True):
            self._notify_console(alert)
        
        # File notification
        if channels.get("file", True):
            self._notify_file(alert)
        
        # Email notification
        if channels.get("email", False):
            self._notify_email(alert)
        
        # Webhook notification
        if channels.get("webhook", False):
            self._notify_webhook(alert)
    
    def _notify_console(self, alert):
        """Display alert in console"""
        severity = alert["severity"]
        if severity == "CRITICAL":
            color = Colors.FAIL
            icon = "🔴"
        elif severity == "WARNING":
            color = Colors.WARNING
            icon = "🟡"
        else:
            color = Colors.CYAN
            icon = "🔵"
        
        print(f"\n{color}{Colors.BOLD}{icon} ALERT [{severity}]{Colors.RESET}")
        print(f"{color}Resource: {alert['resource']}{Colors.RESET}")
        print(f"{color}Message: {alert['message']}{Colors.RESET}")
        print(f"{color}Time: {alert['timestamp']}{Colors.RESET}\n")
    
    def _notify_file(self, alert):
        """Write alert to file"""
        alert_file = "data/alerts.log"
        os.makedirs(os.path.dirname(alert_file), exist_ok=True)
        
        with open(alert_file, 'a') as f:
            log_entry = f"{alert['timestamp']} | {alert['severity']} | {alert['resource']} | {alert['message']}\n"
            f.write(log_entry)
    
    def _notify_email(self, alert):
        """Send alert via email"""
        email_config = self.config.get("email", {})
        
        if not email_config.get("sender") or not email_config.get("recipients"):
            return
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['sender']
            msg['To'] = ", ".join(email_config['recipients'])
            msg['Subject'] = f"[NetMon-AI] {alert['severity']} Alert: {alert['resource']}"
            
            body = f"""
NetMon-AI Alert Notification

Severity: {alert['severity']}
Resource: {alert['resource']}
Message: {alert['message']}
Timestamp: {alert['timestamp']}
Value: {alert.get('value', 'N/A')}

This is an automated alert from NetMon-AI monitoring system.
"""
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender'], email_config['password'])
            server.send_message(msg)
            server.quit()
        
        except Exception as e:
            print(f"{Colors.FAIL}Email notification failed: {e}{Colors.RESET}")
    
    def _notify_webhook(self, alert):
        """Send alert to webhook"""
        webhook_config = self.config.get("webhook", {})
        url = webhook_config.get("url")
        
        if not url:
            return
        
        try:
            # Use curl for webhook (cross-platform)
            payload = json.dumps(alert)
            cmd = f'curl -X POST -H "Content-Type: application/json" -d \'{payload}\' {url}'
            subprocess.run(cmd, shell=True, capture_output=True, timeout=5)
        except Exception as e:
            print(f"{Colors.FAIL}Webhook notification failed: {e}{Colors.RESET}")
    
    def get_recent_alerts(self, count=10, severity=None):
        """Get recent alerts with optional severity filter"""
        print(f"{Colors.HEADER}=== Recent Alerts ==={Colors.RESET}")
        
        filtered = self.alert_history
        if severity:
            filtered = [a for a in self.alert_history if a.get("severity") == severity]
        
        recent = filtered[-count:]
        
        if not recent:
            print(f"{Colors.GREEN}No recent alerts{Colors.RESET}")
            return
        
        for alert in reversed(recent):
            severity = alert.get("severity", "INFO")
            color = Colors.FAIL if severity == "CRITICAL" else Colors.WARNING if severity == "WARNING" else Colors.CYAN
            
            print(f"{color}[{alert['timestamp']}] {severity} - {alert['resource']}{Colors.RESET}")
            print(f"  {alert['message']}")
            print()
    
    def configure_thresholds(self, resource, warning=None, critical=None):
        """Update alert thresholds"""
        thresholds = self.config.get("thresholds", {})
        
        if warning is not None:
            thresholds[f"{resource}_warning"] = warning
        if critical is not None:
            thresholds[f"{resource}_critical"] = critical
        
        self.config["thresholds"] = thresholds
        self._save_config()
        
        print(f"{Colors.GREEN}Alert thresholds updated for {resource}{Colors.RESET}")
        if warning:
            print(f"  Warning: {warning}%")
        if critical:
            print(f"  Critical: {critical}%")
    
    def show_config(self):
        """Display current alert configuration"""
        print(f"{Colors.HEADER}=== Alert System Configuration ==={Colors.RESET}")
        print(f"Enabled: {Colors.GREEN if self.config['enabled'] else Colors.FAIL}{'Yes' if self.config['enabled'] else 'No'}{Colors.RESET}")
        
        print(f"\n{Colors.CYAN}Thresholds:{Colors.RESET}")
        for key, value in self.config.get("thresholds", {}).items():
            print(f"  {key}: {value}%")
        
        print(f"\n{Colors.CYAN}Active Channels:{Colors.RESET}")
        for channel, enabled in self.config.get("channels", {}).items():
            status = f"{Colors.GREEN}Enabled{Colors.RESET}" if enabled else f"{Colors.FAIL}Disabled{Colors.RESET}"
            print(f"  {channel.capitalize()}: {status}")
    
    def clear_history(self):
        """Clear alert history"""
        self.alert_history = []
        self._save_history()
        print(f"{Colors.GREEN}Alert history cleared{Colors.RESET}")
