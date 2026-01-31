import logging
import os
from datetime import datetime

class AuditLogger:
    def __init__(self, log_file="data/ai_audit.log"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        
        self.logger = logging.getLogger("AI_Audit")
        self.logger.setLevel(logging.INFO)
        
        if not self.logger.handlers:
            handler = logging.FileHandler(self.log_file)
            formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

    def log_intent(self, query, intent, authorized):
        """Records the AI's proposal and the human's final decision."""
        status = "AUTHORIZED" if authorized else "REJECTED"
        risk = intent.get('risk_level', 'UNKNOWN')
        action = intent.get('action', 'NONE')
        
        msg = (
            f"\n[QUERY]: {query}\n"
            f"[ACTION]: {action} | [RISK]: {risk}\n"
            f"[STATUS]: {status}\n"
            f"{'-'*50}"
        )
        if authorized:
            self.logger.info(msg)
        else:
            self.logger.warning(msg)