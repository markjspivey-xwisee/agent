from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class FileTraceSink:
    def __init__(self, directory: Path) -> None:
        self._directory = directory
        self._directory.mkdir(parents=True, exist_ok=True)

    def write(self, trace_record: dict[str, Any]) -> Path:
        trace_id = trace_record["id"].replace(":", "_")
        path = self._directory / f"{trace_id}.json"
        path.write_text(json.dumps(trace_record, indent=2))
        return path
