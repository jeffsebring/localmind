# localmind/core/config.py
import json
from pathlib import Path

CONFIG_PATH = Path.home() / ".localmind/config.json"

def load_config() -> dict:
    """
    Load the LocalMind configuration from ~/.localmind/config.json.
    Returns an empty dict if the file does not exist or is invalid.
    """
    if not CONFIG_PATH.exists():
        print(f"[CONFIG] Config file not found at {CONFIG_PATH}")
        return {}
    try:
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"[CONFIG] Error parsing config file: {e}")
        return {}

def get_default_model() -> str:
    """
    Get the default Ollama model from config.
    Falls back to 'local' if not set.
    """
    config = load_config()
    return config.get("default_model", "local")

def get_outputs_dir() -> Path:
    """
    Get the outputs directory from config, defaulting to ~/.localmind/outputs.
    """
    config = load_config()
    return Path(config.get("outputs_dir", str(Path.home() / ".localmind/outputs"))).expanduser()

def get_prompts_dir() -> Path:
    """
    Get the prompts directory from config, defaulting to ~/.localmind/prompts.
    """
    config = load_config()
    return Path(config.get("prompts_dir", str(Path.home() / ".localmind/prompts"))).expanduser()