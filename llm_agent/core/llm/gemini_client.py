import os
import google.generativeai as genai
from llm_agent.core.llm.base_client import LLMBaseClient


class GeminiClient(LLMBaseClient):
    def __init__(self):
        api_key = os.getenv("GOOGLE_API_KEY")
        genai.configure(api_key=api_key)

    def call(
            self,
            model: str,
            system_prompt: str,
            user_prompt: str,
            max_tokens: int = 1024,
            temperature: float = 0.5,
            top_p: float = 0.8,
    ) -> str:
        full_prompt = f"{system_prompt}\n\n{user_prompt}"

        model_obj = genai.GenerativeModel(model)
        response = model_obj.generate_content(
            contents=full_prompt,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
            )
        )

        if not response.candidates:
            raise ValueError(
                f"Gemini response blocked. Feedback: {response.prompt_feedback}"
            )

        return response.text.strip()
