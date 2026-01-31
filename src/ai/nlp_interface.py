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

        # Define allowed actions (whitelist)
        self.ALLOWED_ACTIONS = {
            "MONITOR_CPU",
            "MONITOR_MEM",
            "MONITOR_DISK",
            "MONITOR_SUMMARY",
            "MONITOR_DASHBOARD",
            "LIST_FILES",
            "MOVE_DIR",
            "MOVE_AND_LIST",
            "SERVICE_OP",
            "KILL_PROC",
            "PORT_SCAN",
            "PING",
            "BANDWIDTH",
            "CONNECTIONS",
            "UNKNOWN",
        }

        self.ALLOWED_RISK_LEVELS = {"GREEN", "YELLOW", "RED"}

    def _get_system_prompt(self, current_dir):
        """Generates a prompt injected with real-time system context."""
        return f"""
        You are the NetMon-AI Lead Architect. Output ONLY valid JSON.

        ### CURRENT CONTEXT:
        - Operating System: {os.name}
        - Current Directory: {current_dir}

        ### PROTOCOL:
        1. Assign a RISK_LEVEL: GREEN (Read-only/Safe), YELLOW (Non-destructive changes), RED (Critical/Destructive).
        2. Handle multi-step commands: "Go to X and list files" -> action: "MOVE_AND_LIST".
        3. Sanitization: Do not include extra quotes or backslashes in paths.
        4. ONLY use actions from this list: {', '.join(self.ALLOWED_ACTIONS)}

        ### REQUIRED JSON FORMAT:
        {{"action": "ACTION_NAME", "target": "target_path_or_name", "value": "value_or_none", "risk_level": "GREEN|YELLOW|RED"}}

        ### EXAMPLES:
        User: "Show me CPU usage"
        Response: {{"action": "MONITOR_CPU", "target": "none", "value": "none", "risk_level": "GREEN"}}

        User: "List files in /tmp"
        Response: {{"action": "LIST_FILES", "target": "/tmp", "value": "none", "risk_level": "GREEN"}}

        User: "Kill process 1234"
        Response: {{"action": "KILL_PROC", "target": "1234", "value": "none", "risk_level": "RED"}}
        """

    def _validate_intent(self, intent):
        """
        Validates the structure and content of AI-generated intent.
        Returns (is_valid, error_message)
        """
        # Check required fields
        required_fields = ["action", "risk_level"]
        for field in required_fields:
            if field not in intent:
                return False, f"Missing required field: {field}"

        # Validate action is in whitelist
        action = intent.get("action")
        if action not in self.ALLOWED_ACTIONS:
            return False, f"Invalid action: {action} (not in whitelist)"

        # Validate risk level
        risk = intent.get("risk_level")
        if risk not in self.ALLOWED_RISK_LEVELS:
            return False, f"Invalid risk level: {risk}"

        # Validate target if present
        target = intent.get("target")
        if target and not isinstance(target, str):
            return False, "Target must be a string"

        # Additional validation: check for suspicious patterns in target
        if target and target.lower() != "none":
            suspicious_patterns = [
                r';\s*rm\s',
                r'\|\s*rm\s',
                r'&&\s*rm\s',
                r'`.*`',
                r'\$\(',
                r'>\s*/dev/',
                r'\.\./\.\./\.',
            ]
            for pattern in suspicious_patterns:
                if re.search(pattern, target):
                    return False, f"Suspicious pattern detected in target: {pattern}"

        return True, None

    def process_query(self, user_query):
        # 1. Normalize query
        normalized = self.resolver.normalize_text(user_query)

        # 2. Inject Context
        cwd = os.getcwd()
        system_prompt = self._get_system_prompt(cwd)

        print(f"{Colors.CYAN}Analyzing intent at {cwd}...{Colors.RESET}")

        # 3. Get AI Completion
        raw_response = self.ai.get_completion(system_prompt, normalized, model="llama-3.3-70b-versatile")

        # 4. JSON Extraction & Cleaning
        try:
            # Helper to extract the first balanced JSON object
            def extract_first_json(s):
                if not isinstance(s, str):
                    s = str(s or "")
                start = s.find('{')
                if start == -1:
                    return None
                depth = 0
                in_string = False
                esc = False
                for i in range(start, len(s)):
                    ch = s[i]
                    if ch == '"' and not esc:
                        in_string = not in_string
                    if in_string:
                        if ch == '\\' and not esc:
                            esc = True
                        else:
                            esc = False
                        continue
                    if ch == '{':
                        depth += 1
                    elif ch == '}':
                        depth -= 1
                        if depth == 0:
                            return s[start:i+1]
                return None

            json_text = extract_first_json(raw_response)
            
            if json_text:
                intent = json.loads(json_text)

                # VALIDATE INTENT
                is_valid, error = self._validate_intent(intent)
                if not is_valid:
                    print(f"{Colors.FAIL}AI output validation failed: {error}{Colors.RESET}")
                    return {
                        "action": "UNKNOWN",
                        "target": "none",
                        "value": "none",
                        "message": f"Invalid AI response: {error}",
                        "risk_level": "RED",
                    }

                return intent

            # --- FALLBACK: If no JSON found, use heuristics ---
            
            if not isinstance(raw_response, str):
                raw_response = str(raw_response or "")

            if raw_response.strip().lower().startswith("error") or "api error" in raw_response.lower():
                return {
                    "action": "UNKNOWN",
                    "target": "none",
                    "value": "none",
                    "message": raw_response.strip(),
                    "risk_level": "GREEN",
                }

            # Heuristic fallback for common queries
            q = normalized.lower()
            metrics = 0
            if any(k in q for k in ["ram", "memory", "mem"]):
                metrics += 1
            if "cpu" in q:
                metrics += 1
            if any(k in q for k in ["disk", "storage"]):
                metrics += 1

            if metrics >= 2:
                # Multi-metric summary
                return {"action": "MONITOR_SUMMARY", "target": "none", "value": "none", "risk_level": "GREEN"}

            # Explicit dashboard requests
            if "dashboard" in q or any(phrase in q for phrase in ["open dashboard", "show dashboard", "live dashboard", "full dashboard", "open live dashboard", "show live dashboard"]):
                return {"action": "MONITOR_DASHBOARD", "target": "none", "value": "none", "risk_level": "GREEN"}

            if any(k in q for k in ["ram", "memory", "mem"]):
                return {"action": "MONITOR_MEM", "target": "none", "value": "none", "risk_level": "GREEN"}
            if "cpu" in q:
                return {"action": "MONITOR_CPU", "target": "none", "value": "none", "risk_level": "GREEN"}
            if any(k in q for k in ["disk", "storage"]):
                return {"action": "MONITOR_DISK", "target": "none", "value": "none", "risk_level": "GREEN"}
            if any(k in q for k in ["list", "ls", "dir", "files"]):
                # try to extract a path after 'in' or 'at'
                m = re.search(r'(?:in|at)\s+([\w\./\\:-]+)', normalized, re.IGNORECASE)
                tgt = m.group(1) if m else "none"
                return {"action": "LIST_FILES", "target": tgt, "value": "none", "risk_level": "GREEN"}

            # Last resort: return UNKNOWN with the raw AI text
            return {
                "action": "UNKNOWN",
                "target": "none",
                "value": "none",
                "message": "No JSON found in AI response.",
                "raw": raw_response,
                "risk_level": "GREEN",
            }

        except json.JSONDecodeError as e:
            return {
                "action": "UNKNOWN",
                "target": "none",
                "value": "none",
                "message": f"JSON parsing error: {str(e)}",
                "risk_level": "GREEN",
            }
        except Exception as e:
            return {
                "action": "UNKNOWN",
                "target": "none",
                "value": "none",
                "message": f"Unexpected error: {str(e)}",
                "risk_level": "GREEN",
            }