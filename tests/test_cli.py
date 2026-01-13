import subprocess
import sys
import tempfile
from pathlib import Path

def run_cli(args):
    return subprocess.run(
        [sys.executable, "-m", "localmind.cli.main", *args],
        capture_output=True,
        text=True,
    )


def create_dummy_file(tmp_dir: Path) -> Path:
    p = tmp_dir / "hello.py"
    p.write_text("print('hello')")
    return p


def create_dummy_prompt(tmp_dir: Path) -> Path:
    p = tmp_dir / "refactor.md"
    p.write_text("Refactor this code")
    return p


def test_file_command():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        source = create_dummy_file(tmp_dir)
        prompt = create_dummy_prompt(tmp_dir)

        result = run_cli(["file", str(prompt), str(source), "--dry-run"])

        assert "[DRY RUN]" in result.stdout
        assert str(source) in result.stdout


def test_text_command():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        source = create_dummy_file(tmp_dir)

        result = run_cli(["text", "Summarize this", str(source), "--dry-run"])

        assert "[DRY RUN]" in result.stdout
        assert str(source) in result.stdout


def test_dir_command_with_prompt_file():
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        source = create_dummy_file(tmp_dir)
        prompt = create_dummy_prompt(tmp_dir)

        result = run_cli(
            ["dir", "--prompt-file", str(prompt), str(tmp_dir), "--dry-run"]
        )

        assert "[DRY RUN]" in result.stdout
        assert str(source) in result.stdout


def test_paths_command():
    result = run_cli(["paths"])

    assert "LocalMind home:" in result.stdout
    assert "Prompts dir:" in result.stdout
    assert "Outputs dir:" in result.stdout


def test_outputs_command():
    result = run_cli(["outputs"])

    assert (
        "Last output folder:" in result.stdout
        or "No output folder exists yet." in result.stdout
    )


def test_interactive_prompt(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        prompt = create_dummy_prompt(tmp_dir)
        source = create_dummy_file(tmp_dir)

        def mock_run(*args, **kwargs):
            class MockResult:
                stdout = str(prompt) + "\n"
            return MockResult()

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = run_cli(["prompt", str(source), "--dry-run"])

        # stdout comes from mocked fzf, NOT the CLI
        assert result.stdout.strip() == str(prompt)


def test_last_file(monkeypatch):
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        prompt = create_dummy_prompt(tmp_dir)
        source = create_dummy_file(tmp_dir)

        # seed last file
        run_cli(["file", str(prompt), str(source), "--dry-run"])

        def mock_run(*args, **kwargs):
            class MockResult:
                stdout = str(prompt) + "\n"
            return MockResult()

        monkeypatch.setattr(subprocess, "run", mock_run)

        result = run_cli(["last", "--dry-run"])

        # stdout comes from mocked fzf
        assert result.stdout.strip() == str(prompt)
