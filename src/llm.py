import google.generativeai as genai
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class GeminiLLM:
    def __init__(self):
        # Initialize the model
        self.model = genai.GenerativeModel('gemini-pro')
        
    def get_response(self, prompt: str, context: List[str]) -> str:
        """
        Get response from Gemini using prompt and context
        """
        # Combine context and prompt
        full_prompt = f"""Context information is below.
        ---------------------
        {' '.join(context)}
        ---------------------
        Given the context information and not prior knowledge, answer the question: {prompt}
        """
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            print(f"Error getting response from Gemini: {e}")
            return "I encountered an error processing your request." 