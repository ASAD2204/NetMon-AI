import json
import re
import os
from ai.groq_client import GroqAIClient
from ai.nlp_utils import SynonymResolver
from utils.colors import Colors

class NLPInterface:
    def __init__(self):
        self.ai = GroqAIClient()
        self.resolver = SynonymResolver()
        
    def _get_system_prompt(self, current_dir):
        """Generates a prompt injected with real-time system context."""
        # Use single braces for the string, but explain JSON format clearly
        return f"""
        You are the NetMon-AI Lead Architect. Output ONLY valid JSON.
        
        ### CURRENT CONTEXT:
        - Operating System: {os.name}
        - Current Directory: {current_dir}

        ### PROTOCOL:
        1. Assign a RISK_LEVEL: GREEN (Read), YELLOW (Non-destructive), RED (Critical).
        2. Handle multi-step commands: "Go to X and list files" -> action: "MOVE_AND_LIST".
        3. Sanitization: Do not include extra quotes or backslashes in paths.

        ### REQUIRED JSON FORMAT:
        {{"action": "ACTION_NAME", "target": "target_path_or_name", "value": "value_or_none", "risk_level": "GREEN|YELLOW|RED"}}
        """

    def process_query(self, user_query):
        # 1. Normalize query
        normalized = self.resolver.normalize_text(user_query)
        
        # 2. Inject Context
        cwd = os.getcwd()
        system_prompt = self._get_system_prompt(cwd)
        
        print(f"{Colors.CYAN}Analyzing impact at {cwd}...{Colors.RESET}")
        
        # 3. Get AI Completion
        raw_response = self.ai.get_completion(system_prompt, normalized, model="llama-3.3-70b-versatile")
        
        # 4. JSON Extraction & Cleaning
        try:
            # Locate the JSON block using regex
            json_match = re.search(r'\{.*\}', raw_response, re.DOTALL)
            if json_match:
                # Clean and parse
                return json.loads(json_match.group(0))
            else:
                # Return standard dict format (no double braces)
                return {"action": "UNKNOWN", "message": "No JSON found in AI response."}
        except Exception as e:
            # Return standard dict format
            return {"action": "UNKNOWN", "message": str(e)}