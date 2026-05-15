import requests
import os
import streamlit as st

class NemotronClient:
    def __init__(self):
        # Get API key from Streamlit secrets
        try:
            self.api_key = st.secrets["NVIDIA_API_KEY"]
        except:
            self.api_key = os.getenv("NVIDIA_API_KEY")
        
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        # Correct free model name from your screenshot
        self.model = "nvidia/nemotron-3-nano-omni-30b-a3b-reasoning"
    
    def chat(self, messages):
        if not self.api_key:
            return "Error: NVIDIA_API_KEY not found in secrets."
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
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
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                return answer
            else:
                return f"API Error ({response.status_code}): {response.text[:200]}"
        except Exception as e:
            return f"Request Error: {str(e)}"