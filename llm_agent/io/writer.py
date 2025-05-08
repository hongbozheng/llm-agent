from pathlib import Path

import json
from datetime import datetime


class Writer:
    def __init__(self, base_dir: str = "output"):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        self.path = Path(base_dir) / timestamp
        self.path.mkdir(parents=True, exist_ok=True)

    def save_json(self, obj: dict, name: str):
        file_path = self.path / f"{name}.json"
        with open(file=file_path, mode='w') as f:
            json.dump(obj, f, indent=2)

    def save_code(self, code: str, name: str = "backtest_code"):
        file_path = self.path / f"{name}.py"
        with open(file=file_path, mode='w') as f:
            f.write(code.strip() + "\n")

    def save_text(self, content: str, name: str = "summary", ext: str = "md"):
        file_path = self.path / f"{name}.{ext}"
        with open(file=file_path, mode='w') as f:
            f.write(content.strip() + "\n")

    def get_path(self) -> Path:
        return self.path
