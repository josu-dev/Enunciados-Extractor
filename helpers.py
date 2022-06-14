import json
import os
from typing import Any


def save_json(path: str, value: Any, is_custom_class: bool = False, write_mode: str = 'w', ensure_path: bool = True) -> None:
    if ensure_path:
        parent_path = os.path.dirname(path)
        if not os.path.exists(parent_path):
            os.makedirs(parent_path, exist_ok=True)

    with open(path, mode=write_mode, encoding='utf-8') as file:
        def default(o: Any): return o.__dict__ if is_custom_class else None
        json.dump(value, file, default=default, indent=2)


def scan_dir(path: str, file_extension: str) -> list[tuple[str, str]]:
    if not os.path.exists(path):
        return []

    return [
        (entry.name, entry.path)
        for entry in os.scandir(path) if entry.is_file() and entry.name.endswith(file_extension)
    ]


dirname = os.path.dirname


def join_path(*names: str) -> str:
    return os.path.join(*names)