"""
LocalMind Test Helpers
---------------------
Utility functions for setting up temporary environments, files, prompts, 
and output directories for testing LocalMind CLI and runner functionality.

These helpers ensure tests are isolated, reproducible, and clean up after themselves.
"""

import tempfile
from pathlib import Path

def create_temp_dir():
    """Create and return a temporary directory context for tests."""
    return tempfile.TemporaryDirectory()

def create_dummy_file(tmp_dir: Path, name="hello.py", content="print('hello world')") -> Path:
    """
    Create a temporary source file for testing purposes.

    Args:
        tmp_dir (Path): Base directory for the file.
        name (str): Filename to create.
        content (str): Python source code or text content to write.

    Returns:
        Path: Full path to the created source file.
    """
    file_path = tmp_dir / name
    file_path.write_text(content)
    return file_path

def create_dummy_prompt(tmp_dir: Path, name="refactor.md", content="# Refactor prompt") -> Path:
    """
    Create a temporary prompt file for CLI tests.

    Args:
        tmp_dir (Path): Base directory for the prompt.
        name (str): Filename of the prompt.
        content (str): Markdown content describing the prompt.

    Returns:
        Path: Full path to the created prompt file.
    """
    prompt_path = tmp_dir / name
    prompt_path.write_text(content)
    return prompt_path

def create_dummy_outputs_dir(tmp_dir: Path, name="outputs") -> Path:
    """
    Create a dedicated outputs directory for testing runner output.

    Args:
        tmp_dir (Path): Base temporary directory.
        name (str): Name of the outputs folder.

    Returns:
        Path: Full path to the outputs directory.
    """
    outputs_path = tmp_dir / name
    outputs_path.mkdir(exist_ok=True)
    return outputs_path
