from pathlib import Path

def get_denied_paths(current_dir: Path | str) -> set[Path]:
    current_dir = Path(current_dir)
    return {Path.home().resolve(), Path("/").resolve(), current_dir.resolve()}
