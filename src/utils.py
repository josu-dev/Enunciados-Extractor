import json
import os

from typing import Any


join_path = os.path.join


def ensure_dirs(path: str) -> None:
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def save_json(path: str, value: Any, is_custom_class: bool = False, prettify: bool = False, write_mode: str = 'w') -> None:
    ensure_dirs(os.path.dirname(path))

    with open(path, mode=write_mode, encoding='utf-8') as file:
        def default(o: Any): return o.__dict__ if is_custom_class else None
        json.dump(value, file, default=default, indent=2 if prettify else None)


def scan_dir(path: str, file_extension: str) -> list[tuple[str, str]]:
    if not os.path.exists(path):
        return []

    return [
        (entry.name, entry.path)
        for entry in os.scandir(path) if entry.is_file() and entry.name.endswith(file_extension)
    ]


def normalize_file_name(name: str) -> str:
    return '_'.join(name.lower().split())
