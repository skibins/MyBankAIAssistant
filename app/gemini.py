import os
from google import genai
from google.genai import types
import config
import re

class GeminiAPI:
    """
    Class for communicating with the Google Gemini API with chat history and custom instructions from config.
    """

    def __init__(self, config):
        """
        Initializes the API object, sets the authentication key, and initializes chat history.
        """
        self.api_key = config.GOOGLE_GEMINI_API_KEY
        os.environ["GEMINI_API_KEY"] = self.api_key
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash-lite"
        self.chat_history = []
        self.custom_instruction = config.CUSTOM_INSTRUCTIONS # Get from config

    def get_response(self, user_input):
        """
        Sends a request to the Google Gemini API, including chat history and custom instructions, and returns a response.
        """
        if not self.api_key:
            return "Error: API key is missing."

        if not self.chat_history:
            self.chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=f"{self.custom_instruction}, {user_input}")]))
        else:
            self.chat_history.append(types.Content(role="user", parts=[types.Part.from_text(text=user_input)]))

        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )

        try:
            response = self.client.models.generate_content_stream(
                model=self.model,
                contents=self.chat_history,
                config=generate_content_config,
            )

            output_text = ""
            for chunk in response:
                output_text += chunk.text

            output_text = output_text.strip()
            if output_text:
                output_text = re.sub(r'\*', '', output_text)
                self.chat_history.append(types.Content(role="model", parts=[types.Part.from_text(text=output_text)]))
                return output_text
            else:
                return "Error: No response from AI."
        except Exception as e:
            return f"Error: {str(e)}"

    def clear_history(self):
        """
        Clears the chat history.
        """
        self.chat_history = []