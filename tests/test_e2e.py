import tempfile
from pathlib import Path
import pytest

from localmind.core import runner, paths

# ----------------------------
# Helper to create dummy files
# ----------------------------
def create_dummy_env(tmp_dir: Path):
    """Create a dummy prompt file, source file, and outputs dir for testing."""
    prompts_dir = tmp_dir / "prompts"
    prompts_dir.mkdir()
    prompt_file = prompts_dir / "dummy_prompt.md"
    prompt_file.write_text("This is a dummy prompt.")

    source_file = tmp_dir / "hello.py"
    source_file.write_text("print('Hello world')")

    outputs_dir = tmp_dir / "outputs"
    outputs_dir.mkdir()

    return prompt_file, source_file, outputs_dir

# ----------------------------
# Test: run_prompt_file (dry-run)
# ----------------------------
def test_file_prompt():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        prompt_file, source_file, outputs_dir = create_dummy_env(tmp_dir)
        output_file = outputs_dir / "hello.out.md"

        # Dry run, should not fail
        runner.run_prompt_file(
            prompt_file,
            source_file,
            output_file,
            model="deepseek-coder-v2:latest",
            dry_run=True
        )

        # Output file should not exist in dry run
        assert not output_file.exists()

# ----------------------------
# Test: run_literal_prompt (dry-run)
# ----------------------------
def test_literal_prompt():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        _, source_file, outputs_dir = create_dummy_env(tmp_dir)
        output_file = outputs_dir / "hello_literal.out.md"

        runner.run_literal_prompt(
            "Summarize this code",
            source_file,
            output_file,
            model="deepseek-coder-v2:latest",
            dry_run=True
        )

        assert not output_file.exists()

# ----------------------------
# Test: run_interactive (mocked)
# ----------------------------
def test_interactive_prompt(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        prompt_file, source_file, outputs_dir = create_dummy_env(tmp_dir)

        # Mock interactive selection to return our dummy prompt
        monkeypatch.setattr(runner, "select_prompt_interactive", lambda: prompt_file)

        runner.run_interactive(source_file, model="deepseek-coder-v2:latest", dry_run=True)

# ----------------------------
# Test: last file tracking
# ----------------------------
def test_last_file():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        prompt_file, source_file, outputs_dir = create_dummy_env(tmp_dir)

        # Set last file
        paths.set_last_file(source_file)
        last_file = paths.get_last_file()
        assert last_file == source_file

        # Mock interactive selection
        import types
        runner.select_prompt_interactive = lambda: prompt_file

        # Dry-run should succeed
        runner.run_last_file_with_prompt(model="deepseek-coder-v2:latest", dry_run=True)
