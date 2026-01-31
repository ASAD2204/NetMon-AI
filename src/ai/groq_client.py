from groq import Groq
import os
from dotenv import load_dotenv

# 1. Load Configuration (Dual-Mode: Local Dev vs Linux Prod)
if os.path.exists(".env"):
    load_dotenv(".env")
elif os.path.exists("/etc/netmon-ai/.env"):
    load_dotenv("/etc/netmon-ai/.env")

class GroqAIClient:
    """
    Handles communication with the Groq API.
    """
    def __init__(self):
        # Retrieve the API key from environment variables
        self.api_key = os.getenv("GROQ_API_KEY")
        
        if not self.api_key:
            self.client = None
            print("Error: GROQ_API_KEY not found. Please check your .env file or /etc/netmon-ai/.env")
        else:
            self.client = Groq(api_key=self.api_key)

    def get_completion(self, system_prompt, user_prompt, model="llama-3.3-70b-versatile"):
        """
        Sends a request to the Groq API and returns the text response.
        
        Args:
            system_prompt (str): Instructions defining the AI's behavior.
            user_prompt (str): The specific question or data from the user.
            model (str): Defaults to the powerful 70b model, but can be overridden.
        """
        if not self.client:
            return "Error: Groq client not initialized. Check API Key."
        
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