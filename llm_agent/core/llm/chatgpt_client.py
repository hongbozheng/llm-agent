import os
from openai import OpenAI


class ChatGPTClient:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI()

    def call(
            self,
            model: str,
            system_prompt: str,
            user_prompt: str,
            top_p: float = 0.8,
    ) -> str:
        response = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            top_p=top_p,
        )
        return response.choices[0].message.content.strip()
