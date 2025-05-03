import os
from llm_agent.core.llm.base_client import LLMBaseClient
from openai import OpenAI


class ChatGPTClient(LLMBaseClient):
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()

    def call(
            self,
            model: str,
            system_prompt: str,
            user_prompt: str,
            max_tokens: int = 1024,
            temperature: float = 0.5,
            top_p: float = 0.8,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
        )
        return response.choices[0].message.content.strip()
