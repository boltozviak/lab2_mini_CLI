import logging
import json
from pathlib import Path


logger = logging.getLogger(__name__)

HISTORY_FILE = Path(__file__).parent.parent.parent / ".history"

def history_command() -> str:
    if not HISTORY_FILE.exists():
        logger.info("History file does not exist")
        return "History is empty"

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return "History is empty"

        history = json.loads(content)
        history = {int(k): v for k, v in history.items()}

        commands = []
        for num in sorted(history.keys()):
            commands.append(f"{num:5}  {history[num]}")

        return "\n".join(commands)
