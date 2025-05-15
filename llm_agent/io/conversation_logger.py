from pathlib import Path
from typing import Union


class ConversationLogger:
    def __init__(self, path: Path):
        self.path = path
        self.path.mkdir(parents=True, exist_ok=True)
        self.filepath = self.path / "conversation.md"
        self.file = open(file=self.filepath, mode='a', encoding="utf-8")

    def log(self, label: str, content: str):
        content = content.replace("```", "\"\"\"")
        self.file.write(f"### {label}\n")
        self.file.write(f"```\n{content.strip()}\n```\n\n")

    def log_system(self, prompt: str):
        self.log("⚙️ System Prompt", prompt)

    def log_user(self, prompt: str):
        self.log("🧑 User Prompt", prompt)

    def log_llm(self, response: Union[dict, str]):
        self.log("🤖 LLM Response", response)

    def close(self):
        self.file.close()

    def get_log_path(self) -> Path:
        return self.filepath
