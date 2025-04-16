import os, re, json
from google import genai
from google.genai import types
import config

class GeminiAPI:
    def __init__(self, config):
        self.api_key            = config.GOOGLE_GEMINI_API_KEY
        os.environ["GEMINI_API_KEY"] = self.api_key
        self.client             = genai.Client(api_key=self.api_key)
        self.model              = "gemini-2.0-flash-lite"
        self.chat_history       = []
        self.custom_instruction = config.CUSTOM_INSTRUCTIONS

    def get_response(self, user_input):
        if not self.api_key:
            return {
                "chat_response": "Error: API key is missing.",
                "problem_title": "",
                "problem_description": ""
            }

        instr = (
            "You are a bank assistant. Analyze the entire conversation so far and identify the PRIMARY problem the user is facing (not just their last query). Then generate:\n"
            "1) A normal chat response to the user’s latest message;\n"
            "2) A problem_title (UPPERCASE, max 4 words) that clearly names the primary issue, e.g. \"LOST CREDIT CARD\";\n"
            "3) A problem_description with direct, imperative advice in second person (max 2 sentences) guiding them how to solve that PRIMARY problem, e.g. \"Upon losing your card, immediately block it and contact support to order a replacement.\";\n"
            "Return ONLY PLAIN JSON (no markdown, no backticks), EXACTLY in this format:\n"
            "{\"chat_response\":\"...\",\"problem_title\":\"...\",\"problem_description\":\"...\"}"
        )

        prompt = f"{user_input}\n{instr}"

        content = types.Content(
            role="user",
            parts=[types.Part.from_text(text=(
                f"{self.custom_instruction}, {prompt}" if not self.chat_history else prompt
            ))]
        )
        self.chat_history.append(content)

        cfg = types.GenerateContentConfig(response_mime_type="text/plain")
        try:
            stream = self.client.models.generate_content_stream(
                model=self.model, contents=self.chat_history, config=cfg
            )
            raw = "".join(chunk.text for chunk in stream).strip()
            cleaned = re.sub(r"```(?:json)?\s*", "", raw).replace("```", "").strip()

            self.chat_history.append(types.Content(
                role="model",
                parts=[types.Part.from_text(text=cleaned)]
            ))

            parsed = json.loads(cleaned)
            return {
                "chat_response":      parsed.get("chat_response", ""),
                "problem_title":      parsed.get("problem_title", ""),
                "problem_description":parsed.get("problem_description", "")
            }
        except Exception as e:
            return {
                "chat_response":       f"Error: {e}",
                "problem_title":       "",
                "problem_description": ""
            }

    def clear_history(self):
        self.chat_history = []
