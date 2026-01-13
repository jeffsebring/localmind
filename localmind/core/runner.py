# localmind/core/runner.py
import subprocess
from pathlib import Path
from .config import get_default_model  # Config helper for default model

def run_file(prompt_file: Path, source_file: Path, model: str = "local", dry_run: bool = False):
    """
    Run a prompt file against a source file using Ollama.

    Parameters:
        prompt_file: Path to the prompt template (.md)
        source_file: Path to the source code or text file
        model: Ollama model name
        dry_run: If True, only prints what would be run
    """
    print(f"[RUNNER] run_file called: {prompt_file} -> {source_file} (model={model})")
    
    # Read the prompt template
    prompt_text = prompt_file.read_text()
    source_text = source_file.read_text()
    
    if dry_run:
        print("[DRY RUN]")
        print(f"Prompt:\n{prompt_text}")
        print(f"Source file contents:\n{source_text}")
        return

    # Call Ollama
    output = _call_ollama(prompt_text, source_text, model)

    # Save output to file
    outputs_dir = Path.home() / ".localmind" / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    output_file = outputs_dir / f"{source_file.stem}_output.txt"
    output_file.write_text(output)
    
    print(f"[OUTPUT SAVED] {output_file}")
    return output


def run_text(prompt_text: str, source_text: str = "", model: str | None = None, dry_run: bool = False):
    """
    Run a literal prompt string against optional source text.

    Parameters:
        prompt_text: The prompt string
        source_text: Optional source text
        model: Ollama model name. Uses default from config if None
        dry_run: If True, prints instead of executing
    """
    model = model or get_default_model()
    print(f"[RUNNER] run_text called (model={model})")
    
    if dry_run:
        print("[DRY RUN]")
        print(f"Prompt:\n{prompt_text}")
        if source_text:
            print(f"Source text:\n{source_text}")
        return
    
    return _call_ollama(prompt_text, source_text, model)


def run_dir(prompt_file: Path, source_dir: Path, model: str | None = None, dry_run: bool = False):
    """
    Run a prompt file against all files in a directory.

    Parameters:
        prompt_file: Path to the prompt template
        source_dir: Directory containing source files
        model: Ollama model name. Uses default from config if None
        dry_run: If True, prints instead of executing
    """
    model = model or get_default_model()
    print(f"[RUNNER] run_dir called: {prompt_file} -> {source_dir} (model={model})")
    prompt_text = prompt_file.read_text()
    
    for file_path in sorted(source_dir.iterdir()):
        if file_path.is_file():
            print(f"[RUNNER] Processing file: {file_path.name}")
            run_file(prompt_file, file_path, model=model, dry_run=dry_run)


def _call_ollama(prompt_text: str, source_text: str, model: str):
    """
    Internal helper to invoke Ollama via subprocess.
    Combines prompt and source text and sends to Ollama CLI.

    Raises RuntimeError if Ollama fails.
    """
    cmd = ["ollama", "run", model]
    full_input = f"{prompt_text}\n{source_text}"

    try:
        result = subprocess.run(
            cmd,
            input=full_input.encode("utf-8"),
            capture_output=True,
            check=True
        )
        output = result.stdout.decode("utf-8")
        print("[OLLAMA OUTPUT]")
        print(output)
        return output
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode("utf-8") if e.stderr else str(e)
        raise RuntimeError(f"Ollama call failed: {err}")
