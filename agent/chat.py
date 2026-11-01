"""The agent: one Gemini chat session with the store tools and automatic function calling."""

import os

from google import genai
from google.genai import types

from agent import tools
from agent.prompt import build_system_prompt

DEFAULT_MODEL = "gemini-3.5-flash-lite"


class StoreAgent:
    def __init__(self, model: str | None = None):
        self.model = model or os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
        self.client = genai.Client(http_options=types.HttpOptions(
            # The free tier rate-limits often; retry 429/5xx with backoff instead of failing the turn.
            retry_options=types.HttpRetryOptions(attempts=5, initial_delay=10, max_delay=60),
        ))
        self.chat = self.client.chats.create(model=self.model, config=types.GenerateContentConfig(
            system_instruction=build_system_prompt(),
            tools=tools.ALL_TOOLS,
            temperature=0.3,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=8),
        ))

    def send(self, message: str) -> tuple[str, list[dict]]:
        """Send a customer message; return the reply and the tool calls made to produce it."""
        tools.call_log.clear()
        response = self.chat.send_message(message)
        reply = (response.text or "").strip()
        if not reply:
            # Happens when the model hits the tool-call limit without writing an answer.
            reply = "Desculpe, não consegui concluir essa consulta agora. Pode reformular a pergunta?"
        return reply, list(tools.call_log)
