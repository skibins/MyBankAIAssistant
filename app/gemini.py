import os
import re
import json
from google import genai
from google.genai import types
import config

class GeminiAPI:
    """
    Class for communicating with the Google Gemini API, applying custom and additional prompts,
    and parsing responses into structured JSON for chat and sidebar updates.
    """

    # Regex to extract the largest JSON object in response text
    _JSON_PATTERN = re.compile(r'\{(?:[^{}]|"(?:\\.|[^"])*")*\}', re.DOTALL)

    def __init__(self, config: config.Config):
        """
        Initialize the GeminiAPI client and load configuration settings.
        """
        self.api_key = config.GOOGLE_GEMINI_API_KEY
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.0-flash-lite"
        self.chat_history = []
        self.custom_instruction = config.CUSTOM_INSTRUCTIONS
        self.additional_prompt = config.ADDITIONAL_PROMPT
        self._stream_config = types.GenerateContentConfig(response_mime_type="text/plain")
        self._max_history = 10

    def clear_history(self):
        """
        Clear the stored chat history to start a fresh conversation.
        """
        self.chat_history.clear()

    def _build_prompt(self, user_input: str) -> str:
        """
        Construct the full prompt by combining the custom instruction (once)
        and the additional JSON-specific prompt for sidebar generation.
        """
        body = f"{user_input}\n{self.additional_prompt}"
        if not self.chat_history:
            return f"{self.custom_instruction}, {body}"
        return body

    def _stream_response(self, prompt: str) -> str:
        """
        Send the prompt to the Gemini API and stream back the raw text response.
        """
        self.chat_history.append(
            types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
        )
        # Truncate history to avoid drift
        if len(self.chat_history) > self._max_history:
            self.chat_history = self.chat_history[-self._max_history:]

        stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=self.chat_history,
            config=self._stream_config
        )
        return ''.join(chunk.text for chunk in stream)

    def _clean_response(self, raw: str) -> str:
        """
        Remove markdown fences, unescape JSON strings, and isolate the JSON substring.
        """
        text = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "").strip()

        # Unwrap and unescape JSON if it's a quoted string
        if text.startswith('"') and text.endswith('"'):
            try:
                text = json.loads(text)
            except json.JSONDecodeError:
                text = text[1:-1]

        # Replace escaped quotes
        text = text.replace(r'\"', '"')

        # Extract the JSON object
        match = self._JSON_PATTERN.search(text)
        if match:
            return match.group(0)
        return text

    def get_response(self, user_input: str) -> dict:
        """
        Public method to send a user message and retrieve a structured response.
        """
        if not self.api_key:
            return {
                "chat_response": "Error: API key is missing.",
                "problem_title": "",
                "problem_description": ""
            }

        prompt = self._build_prompt(user_input)
        raw = self._stream_response(prompt)
        cleaned = self._clean_response(raw)

        # Record the cleaned model output in history
        self.chat_history.append(
            types.Content(role="model", parts=[types.Part.from_text(text=cleaned)])
        )

        try:
            data = json.loads(cleaned)
            return {
                "chat_response": data.get("chat_response", ""),
                "problem_title": data.get("problem_title", ""),
                "problem_description": data.get("problem_description", "")
            }
        except json.JSONDecodeError:
            return {
                "chat_response": cleaned,
                "problem_title": "",
                "problem_description": ""
            }
        except Exception as e:
            return {
                "chat_response": f"Error: {e}",
                "problem_title": "",
                "problem_description": ""
            }