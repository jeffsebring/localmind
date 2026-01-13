# localmind/core/runner.py
import subprocess
from pathlib import Path
from datetime import datetime

from .config import get_default_model, get_outputs_dir


def _write_output(
    *,
    output_text: str,
    source_file: Path | None,
    model: str,
) -> Path:
    """
    Write Ollama output to a timestamped file in the configured outputs directory.
    """
    outputs_dir = get_outputs_dir()
    outputs_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    source_name = source_file.stem if source_file else "text"
    safe_model = model.replace(":", "_")

    filename = f"{timestamp}_{source_name}_{safe_model}.txt"
    output_path = outputs_dir / filename

    output_path.write_text(output_text, encoding="utf-8")
    return output_path


def run_file(
    prompt_file: Path,
    source_file: Path,
    model: str | None = None,
    dry_run: bool = False,
):
    """
    Run a prompt file against a source file using Ollama.
    """
    model = model or get_default_model()
    print(f"[RUNNER] run_file called: {prompt_file} -> {source_file} (model={model})")

    prompt_text = prompt_file.read_text()
    source_text = source_file.read_text()

    if dry_run:
        print("[DRY RUN]")
        print(f"Prompt:\n{prompt_text}")
        print(f"Source file contents:\n{source_text}")
        return

    output = _call_ollama(prompt_text, source_text, model)

    output_path = _write_output(
        output_text=output,
        source_file=source_file,
        model=model,
    )

    print(f"[OUTPUT SAVED] {output_path}")
    return output


def run_text(
    prompt_text: str,
    source_text: str = "",
    model: str | None = None,
    dry_run: bool = False,
):
    """
    Run a literal prompt string against optional source text.
    """
    model = model or get_default_model()
    print(f"[RUNNER] run_text called (model={model})")

    if dry_run:
        print("[DRY RUN]")
        print(f"Prompt:\n{prompt_text}")
        if source_text:
            print(f"Source text:\n{source_text}")
        return

    output = _call_ollama(prompt_text, source_text, model)

    output_path = _write_output(
        output_text=output,
        source_file=None,
        model=model,
    )

    print(f"[OUTPUT SAVED] {output_path}")
    return output


def run_dir(prompt_file: Path, source_dir: Path, model: str | None = None, dry_run: bool = False):
    """
    Run a prompt file against all files in a directory tree (recursively).

    Parameters:
        prompt_file: Path to the prompt template
        source_dir: Directory containing source files
        model: Ollama model name. Uses default from config if None
        dry_run: If True, prints instead of executing
    """
    model = model or get_default_model()
    print(f"[RUNNER] run_dir called: {prompt_file} -> {source_dir} (model={model})")
    prompt_text = prompt_file.read_text()
    
    for file_path in sorted(source_dir.rglob("*")):  # recursively find all files
        if file_path.is_file():
            print(f"[RUNNER] Processing file: {file_path}")
            run_file(prompt_file, file_path, model=model, dry_run=dry_run)


def _call_ollama(prompt_text: str, source_text: str, model: str) -> str:
    """
    Invoke Ollama via subprocess and return stdout.
    """
    cmd = ["ollama", "run", model]
    full_input = f"{prompt_text}\n{source_text}"

    try:
        result = subprocess.run(
            cmd,
            input=full_input.encode("utf-8"),
            capture_output=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8") if e.stderr else str(e)
        raise RuntimeError(f"Ollama call failed: {err}")

    output = result.stdout.decode("utf-8")

    print("[OLLAMA OUTPUT]")
    print(output)

    return output
