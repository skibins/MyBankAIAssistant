import os
import json

class Config:
    """
    Configuration class to manage application settings.
    """

    SECRET_KEY = 'supersecretkey' # super extra safe user session secret key
    DATA_FILE = 'data/users.json'
    CUSTOM_INSTRUCTIONS_FILE = 'data/custom_instructions.txt'
    ADDITIONAL_PROMPT_FILE = 'data/additional_prompt.txt'

    def __init__(self, api_key_file='apiKey.txt'):
        """
        Initializes the Config object.

        Args:
            api_key_file (str): Path to the file containing the API key.
        """
        self.api_key_file = api_key_file
        self.GOOGLE_GEMINI_API_KEY = self._load_api_key()
        self.CUSTOM_INSTRUCTIONS = self._load_custom_instructions() # Load custom instructions
        self.ADDITIONAL_PROMPT = self._load_additional_promppt() # Load additional prompt

    def _load_api_key(self):
        """
        Loads the API key from the specified file.

        Returns:
            str: The API key, or None if the file is not found.
        """
        try:
            with open(self.api_key_file, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{self.api_key_file}' not found.")
            return None

    def _load_custom_instructions(self):
        """
        Loads custom instructions from the specified file.

        Returns:
            str: The custom instructions, or an empty string if the file is not found.
        """
        try:
            with open(self.CUSTOM_INSTRUCTIONS_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{self.CUSTOM_INSTRUCTIONS_FILE}' not found.")
            return ""

    def _load_additional_promppt(self):
        """
            Loads additional prompt from the specified file.

            Returns:
                str: Additional prompt, or an empty string if the file is not found.
        """
        try:
            with open(self.ADDITIONAL_PROMPT_FILE, 'r', encoding='utf-8') as f:
                return f.read().strip()
        except FileNotFoundError:
            print(f"Error: File '{self.ADDITIONAL_PROMPT_FILE}' not found.")
            return ""