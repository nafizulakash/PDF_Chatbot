import requests
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()

class NemotronClient:
    def __init__(self):
        self.api_key = os.getenv("NVIDIA_API_KEY")
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.model = "nvidia/nemotron-4-340b-instruct"
    
    def chat(self, messages):
        """
        Send messages to NVIDIA Nemotron API and get response
        
        Args:
            messages: List of message dictionaries
                     [{"role": "user", "content": "hello"}, ...]
        
        Returns:
            str: AI response
        """
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "application/json",
        }
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 1024,
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            
            # Check if successful
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                return answer
            else:
                return f"Error: {response.status_code}"
        
        except Exception as e:
            return f"Error: {str(e)}"