from groq import Groq
import os
import base64
from dotenv import load_dotenv
from pathlib import Path

class GroqAIClient:
    """
    Handles communication with the Groq API.
    """
    def __init__(self):
        api_key = None
        
        # Try to load from base64-encoded file first (production)
        if os.path.exists("/etc/netmon-ai/.env.b64"):
            try:
                with open("/etc/netmon-ai/.env.b64", 'r') as f:
                    encoded = f.read().strip()
                    api_key = base64.b64decode(encoded).decode('utf-8')
            except Exception as e:
                print(f"Warning: Error reading encrypted API key: {e}")
        
        # Fall back to plaintext .env files (development)
        # NOTE: automatic .env loading is disabled by default before pushing code.
        # To enable locally for testing, set LOAD_ENV = True or uncomment the block below.
        LOAD_ENV = False

        if not api_key and LOAD_ENV:
            # Search for .env in current dir and parent directories up to repo root
            def find_env(start_path, name='.env', max_levels=4):
                p = Path(start_path).resolve()
                for _ in range(max_levels + 1):
                    candidate = p / name
                    if candidate.exists():
                        return str(candidate)
                    if p.parent == p:
                        break
                    p = p.parent
                return None

            # Try current working directory first (where script was invoked)
            env_path = find_env(os.getcwd(), '.env', max_levels=6)
            # Also try repository root relative to this file
            if not env_path:
                repo_root = Path(__file__).resolve().parents[2] if len(Path(__file__).resolve().parents) >= 3 else Path(__file__).resolve().parent
                env_path = find_env(repo_root, '.env', max_levels=2)

            if env_path:
                try:
                    load_dotenv(env_path)
                    print(f"[GroqAIClient] Loaded .env from: {env_path}")
                except Exception as e:
                    print(f"[GroqAIClient] Warning: failed to load .env at {env_path}: {e}")
            else:
                # Also try the packaged /etc location
                if os.path.exists("/etc/netmon-ai/.env"):
                    load_dotenv("/etc/netmon-ai/.env")

            api_key = os.getenv("GROQ_API_KEY")
        
        self.api_key = api_key
        
        if not self.api_key:
            self.client = None
            print("=" * 60)
            print("ERROR: GROQ_API_KEY not found!")
            print("=" * 60)
            print("For Development:")
            print("  Create a .env file in the project root with:")
            print("  GROQ_API_KEY=your_actual_api_key_here")
            print()
            print("For Production:")
            print("  Reinstall the package or check /etc/netmon-ai/.env.b64")
            print("=" * 60)
        else:
            try:
                self.client = Groq(api_key=self.api_key)
            except Exception as e:
                self.client = None
                print(f"Error initializing Groq client: {e}")

    def get_completion(self, system_prompt, user_prompt, model="llama-3.3-70b-versatile"):
        """
        Sends a request to the Groq API and returns the text response.
        
        Args:
            system_prompt (str): Instructions defining the AI's behavior.
            user_prompt (str): The specific question or data from the user.
            model (str): Defaults to the powerful 70b model, but can be overridden.
        """
        if not self.client:
            return "Error: Groq client not initialized. Check API Key configuration."
        
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model=model,
                temperature=0.2,  # Low temperature for deterministic/safe commands
                max_tokens=1024
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"API Error: {str(e)}"
