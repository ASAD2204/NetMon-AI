import socket
import subprocess
import time
import os
import psutil
from utils.colors import Colors
from utils.helpers import format_bytes

class NetworkTools:
    @staticmethod
    def ping(host, count=4):
        """Performs a standard ping and displays results."""
        param = "-n" if os.name == "nt" else "-c"
        command = ["ping", param, str(count), host]
        
        print(f"{Colors.CYAN}Pinging {host}...{Colors.RESET}")
        try:
            output = subprocess.check_output(command).decode()
            print(output)
        except Exception as e:
            print(f"{Colors.FAIL}Ping failed: {e}{Colors.RESET}")

    @staticmethod
    def port_scan(host, ports=[21, 22, 80, 443, 3306, 8080]):
        """Checks if specific common ports are open on a host."""
        print(f"{Colors.HEADER}🔍 Scanning {host} for open ports...{Colors.RESET}")
        for port in ports:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"{Colors.GREEN}Port {port}: OPEN{Colors.RESET}")
            else:
                print(f"{Colors.FAIL}Port {port}: CLOSED{Colors.RESET}")
            sock.close()

    @staticmethod
    def get_bandwidth():
        """Calculates real-time network traffic throughput."""
        old_value = psutil.net_io_counters()
        time.sleep(1)
        new_value = psutil.net_io_counters()
        
        sent = new_value.bytes_sent - old_value.bytes_sent
        recv = new_value.bytes_recv - old_value.bytes_recv
        
        print(f"{Colors.BOLD}Network Usage (1s sample):{Colors.RESET}")
        print(f"📤 Sent: {format_bytes(sent)}/s")
        print(f"📥 Received: {format_bytes(recv)}/s")

    @staticmethod
    def show_connections():
        """Displays active network connections and the apps using them."""
        print(f"\n{Colors.HEADER}🌐 ACTIVE NETWORK CONNECTIONS{Colors.RESET}")
        print(f"{Colors.BOLD}{'Proto':<6} {'Local Address':<25} {'Remote Address':<25} {'Status':<15}{Colors.RESET}")
        
        try:
            for conn in psutil.net_connections(kind='inet'):
                laddr = f"{conn.laddr.ip}:{conn.laddr.port}"
                raddr = f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "LISTENING"
                proto = "TCP" if conn.type == 1 else "UDP"
                
                # Filter for active or listening connections
                print(f"{proto:<6} {laddr:<25} {raddr:<25} {conn.status:<15}")
        except Exception as e:
            print(f"{Colors.FAIL}Error fetching connections: {e}{Colors.RESET}")