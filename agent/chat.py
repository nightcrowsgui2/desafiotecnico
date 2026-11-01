"""The agent: one Gemini chat session with the store tools and automatic function calling."""

import os

from google import genai
from google.genai import types

from agent import tools
from agent.prompt import build_system_prompt

DEFAULT_MODEL = "gemini-2.5-flash"


class StoreAgent:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        client = genai.Client(http_options=types.HttpOptions(
            # The free tier rate-limits often; retry 429/5xx with backoff instead of failing the turn.
            retry_options=types.HttpRetryOptions(attempts=4, initial_delay=2),
        ))
        self.chat = client.chats.create(model=self.model, config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(),
            tools=tools.ALL_TOOLS,
            temperature=0.3,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=6),
        ))

    def send(self, message: str) -> tuple[str, list[dict]]:
        """Send a customer message; return the reply and the tool calls made to produce it."""
        tools.call_log.clear()
        response = self.chat.send_message(message)
        return (response.text or "").strip(), list(tools.call_log)
