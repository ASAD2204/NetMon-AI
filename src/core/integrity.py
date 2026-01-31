import hashlib
import json
import os
from utils.colors import Colors

class IntegrityMonitor:
    def __init__(self, db_path="data/integrity_db.json"):
        self.db_path = db_path
        self.hashes = self._load_db()

    def _load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r') as f:
                return json.load(f)
        return {}

    def _save_db(self):
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        with open(self.db_path, 'w') as f:
            json.dump(self.hashes, f, indent=4)

    def calculate_hash(self, filepath):
        """Generates a SHA-256 hash for a file."""
        sha256_hash = hashlib.sha256()
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            return None

    def register_file(self, filepath):
        """Saves the current state of a file to the database."""
        h = self.calculate_hash(filepath)
        if h:
            self.hashes[filepath] = h
            self._save_db()
            print(f"{Colors.GREEN}Successfully registered {filepath}{Colors.RESET}")
        else:
            print(f"{Colors.FAIL}Failed to read file.{Colors.RESET}")

    def check_integrity(self):
        """Compares current files against the saved database."""
        print(f"{Colors.HEADER}--- Integrity Audit ---{Colors.RESET}")
        for filepath, stored_hash in self.hashes.items():
            current_hash = self.calculate_hash(filepath)
            if current_hash is None:
                print(f"{Colors.FAIL}MISSING:[/] {filepath}")
            elif current_hash != stored_hash:
                print(f"{Colors.FAIL}⚠️ TAMPERED:[/] {filepath}")
            else:
                print(f"{Colors.GREEN}SAFE:[/] {filepath}")