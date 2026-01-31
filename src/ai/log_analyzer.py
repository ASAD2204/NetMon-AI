from ai.groq_client import GroqAIClient
from utils.colors import Colors

class LogAnalyzer:
    def __init__(self):
        self.ai = GroqAIClient()
        self.security_prompt = """
        You are a Cybersecurity Expert. Analyze the following log lines for:
        1. Brute force attempts (repeated failures)
        2. Unusual login times
        3. Suspicious IP addresses
        Provide a concise summary with 'CRITICAL', 'WARNING', or 'INFO' levels.
        """

    def analyze_file(self, file_path, lines=50):
        """Reads a log file and sends the tail to the AI for analysis."""
        try:
            with open(file_path, 'r') as f:
                content = f.readlines()[-lines:]
                log_text = "".join(content)
            
            print(f"{Colors.CYAN}AI is analyzing {file_path} for threats...{Colors.RESET}")
            analysis = self.ai.get_completion(self.security_prompt, log_text)
            
            print(f"\n{Colors.BOLD}🛡️ AI SECURITY ANALYSIS{Colors.RESET}")
            print(f"{Colors.BLUE}Target:{Colors.RESET} {file_path}")
            print("-" * 30)
            print(analysis)
        except FileNotFoundError:
            print(f"{Colors.FAIL}Error: Log file not found at {file_path}{Colors.RESET}")