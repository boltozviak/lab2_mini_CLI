import logging
import json
from pathlib import Path


logger = logging.getLogger(__name__)

HISTORY_FILE = Path(__file__).parent.parent.parent / ".history"

def history_command() -> str:
    '''
    Выводит историю команд, сохраняется между сессиями
    '''
    if not HISTORY_FILE.exists():
        return "История пуста"

    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return "История пуста"

        history = json.loads(content)
        history = {int(k): v for k, v in history.items()}

        commands = []
        for num in sorted(history.keys()):
            commands.append(f"{num:5}  {history[num]}")

        return "\n".join(commands)
