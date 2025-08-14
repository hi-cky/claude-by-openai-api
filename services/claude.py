import anthropic
from typing import List, Dict, Iterable, Optional
from config import settings

class ClaudeService:
    def __init__(self):
        self.client = anthropic.AsyncClient(
            api_key=settings.ANTHROPIC_API_KEY,
            auth_token=settings.ANTHROPIC_AUTH_TOKEN,
            base_url=settings.ANTHROPIC_BASE_URL
        )
        self.available_models = [
            "claude-sonnet-4-20250514",
            "claude-opus-4-20250514"
        ]


    async def complete(self, model: str, messages: List[Dict], max_tokens=1000, temperature=0.7) -> str:
        """发送请求到 Claude API"""
        if model not in self.available_models:
            model = settings.DEFAULT_MODEL

        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages, # type: ignore
            stream=False
        )

        return response.content[0].text # type: ignore


    async def stream_complete(self, model: str, messages: List[Dict], max_tokens=1000, temperature=0.7, tools: Optional[Iterable] = None):
        """流式调用Claude API"""
        if model not in self.available_models:
            model = settings.DEFAULT_MODEL


        stream = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=messages, # type: ignore
            stream=True,
            tools=tools # type: ignore
        )
        return stream

claude_service = ClaudeService()
