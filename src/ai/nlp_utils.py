import nltk
from nltk.corpus import wordnet

# Download necessary NLTK data (only runs once)
nltk.download('wordnet', quiet=True)

class SynonymResolver:
    def __init__(self):
        # Map specific sysadmin keywords to standard intents
        self.keyword_map = {
            "terminate": "kill",
            "nuke": "kill",
            "stop": "stop",
            "halt": "stop",
            "check": "monitor",
            "usage": "monitor",
            "stats": "monitor",
            "lookup": "search",
            "find": "search",
            "directory": "dir",
            "folder": "dir",
            "move": "cd",
            "change": "cd"
        }

    def normalize_text(self, text):
        """Replaces synonyms with standard command words for better AI parsing."""
        words = text.lower().split()
        normalized = []
        for word in words:
            # Check manual map first
            if word in self.keyword_map:
                normalized.append(self.keyword_map[word])
            else:
                normalized.append(word)
        return " ".join(normalized)