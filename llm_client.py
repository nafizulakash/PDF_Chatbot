import requests
import os
import streamlit as st

class NemotronClient:
    def __init__(self):
        # Try to get API key from Streamlit secrets first, then from environment
        try:
            self.api_key = st.secrets["NVIDIA_API_KEY"]
        except:
            self.api_key = os.getenv("NVIDIA_API_KEY")
        
        self.api_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        # Use the free model (262k context)
        self.model = "nvidia/nemotron-3-super-120b-a12b-free"
    
    def chat(self, messages):
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
            
            if response.status_code == 200:
                answer = response.json()["choices"][0]["message"]["content"]
                return answer
            else:
                return f"Error: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error: {str(e)}"