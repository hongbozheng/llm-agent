import google.generativeai as genai
import openai
import os
from logger import log
from openai import OpenAI


def call_llm(llm: str, sys_prompt: str, usr_prompt: str, temp: float) -> str:
    """Send a system and user prompt to the specified LLM and return the
    response content."""

    try:
        if llm == "gpt-4o":
            openai.api_key = os.getenv("OPENAI_API_KEY")
            response = openai.chat.completions.create(
                model=llm,
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": usr_prompt},
                ],
                temperature=temp,
            )
            return response.choices[0].message.content.strip()

        elif llm == "deepseek":
            api_key = os.getenv("DEEPSEEK_API_KEY")
            client = OpenAI(
                api_key=api_key, base_url="https://api.deepseek.com"
            )
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": sys_prompt},
                    {"role": "user", "content": usr_prompt},
                ],
                temperature=temp,
            )
            return response.choices[0].message.content.strip()

        elif llm.startswith("gemini"):
            api_key = os.getenv("GOOGLE_API_KEY")
            genai.configure(api_key=api_key)

            full_prompt = sys_prompt + "\n\n" + usr_prompt
            model = genai.GenerativeModel(llm)
            response = model.generate_content(
                full_prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=temp,
                )
            )

            if not response.candidates:
                raise ValueError(
                    f"Gemini response was blocked. Prompt feedback: {response.prompt_feedback}")
            return response.text.strip()

        else:
            log(f"❌ [ERROR] Unsupported LLM {llm}")
            exit(1)

    except Exception as e:
        log(f"❌ [ERROR] Failed to get response from LLM {llm} {e}")
        exit(1)
