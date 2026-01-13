#!/usr/bin/env python3
"""
LocalMind Paths & State Management
----------------------------------
Handles folder locations, recent files tracking, timestamps, and configuration.
"""

from pathlib import Path
import json
import os
from datetime import datetime

# ----------------------------
# Default Paths
# ----------------------------

def get_localmind_home() -> Path:
    """Return the LocalMind home directory (~/.localmind)."""
    home = Path(os.getenv("HOME", "~")).expanduser()
    return home / ".localmind"

def get_outputs_dir() -> Path:
    """Return the outputs directory (~/.localmind/outputs)."""
    out_dir = get_localmind_home() / "outputs"
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir

def get_prompts_dir() -> Path:
    """Return the prompts directory (~/.localmind/prompts)."""
    prompts_dir = get_localmind_home() / "prompts"
    prompts_dir.mkdir(parents=True, exist_ok=True)
    return prompts_dir

def get_state_dir() -> Path:
    """Return the state directory (~/.localmind/state)."""
    state_dir = get_localmind_home() / "state"
    state_dir.mkdir(parents=True, exist_ok=True)
    return state_dir

def get_config_file() -> Path:
    """Return the config file (~/.localmind/config.json)."""
    cfg_file = get_localmind_home() / "config.json"
    if not cfg_file.exists():
        # default config
        cfg_file.write_text(json.dumps({"recent_files_limit": 10}, indent=2))
    return cfg_file

# ----------------------------
# Timestamps
# ----------------------------

def current_timestamp() -> str:
    """Return current timestamp as YYYY-MM-DD HH:MM:SS"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ----------------------------
# Recent Files Management
# ----------------------------

def _get_recent_files_file() -> Path:
    """Path to recent files JSON state."""
    f = get_state_dir() / "recent_files.json"
    if not f.exists():
        f.write_text(json.dumps([]))
    return f

def _load_recent_files() -> list[str]:
    try:
        with _get_recent_files_file().open() as f:
            return json.load(f)
    except Exception:
        return []

def _save_recent_files(files: list[str]):
    with _get_recent_files_file().open("w") as f:
        json.dump(files, f, indent=2)

def get_recent_files() -> list[str]:
    """Return the list of recent files, most recent first."""
    return _load_recent_files()

def record_recent_file(file_path: Path):
    """Add a file to the recent files list, respecting config limit."""
    files = _load_recent_files()
    file_str = str(file_path.resolve())
    if file_str in files:
        files.remove(file_str)
    files.insert(0, file_str)

    # enforce limit
    limit = 10
    cfg_file = get_config_file()
    try:
        cfg = json.load(cfg_file.open())
        limit = cfg.get("recent_files_limit", 10)
    except Exception:
        pass

    files = files[:limit]
    _save_recent_files(files)

def set_last_file(file_path: Path):
    """Alias to record the last file (for backwards compatibility)."""
    record_recent_file(file_path)
