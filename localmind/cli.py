#!/usr/bin/env python3
"""
LocalMind CLI entrypoint.

Responsibilities:
- Define the CLI interface (argparse)
- Validate arguments at the CLI boundary
- Dispatch to core runner functions using a stable, explicit API
"""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime
from .core import runner, config
from .core.config import get_default_model, get_outputs_dir

# --------------------------------------------------------------------------------------
# Command handlers
# --------------------------------------------------------------------------------------

def run_file(prompt_file: Path, source_file: Path, model: str = None, dry_run: bool = False):
    """
    Run a prompt file against a source file using Ollama.
    Prints output to terminal and writes to a timestamped file in outputs_dir.
    """

    print(f"[RUNNER] run_file called: {prompt_file} -> {source_file} (model={model})")

    # Resolve model from config if None
    if model is None:
        model = config.get_default_model()

    # Read files
    prompt_text = prompt_file.read_text()
    source_text = source_file.read_text()

    if dry_run:
        print("[DRY RUN]")
        print(f"Model: {model}")
        print(f"Prompt:\n{prompt_text}")
        print(f"Source file contents:\n{source_text}")
        return

    # Call Ollama
    output_text = _call_ollama(prompt_text, source_text, model)

    # Generate timestamped output filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    outputs_dir = config.get_outputs_dir()
    outputs_dir.mkdir(parents=True, exist_ok=True)
    output_file = outputs_dir / f"{source_file.stem}_{timestamp}{source_file.suffix}"

    # Write to file
    output_file.write_text(output_text, encoding="utf-8")
    print(f"[RUNNER] Output written to: {output_file}")

    return output_text

def cmd_file(args: argparse.Namespace) -> None:
    """
    CLI wrapper: Run a prompt file on a source file using runner.run_file.
    """
    model = args.model or config.get_default_model()
    runner.run_file(
        prompt_file=Path(args.prompt_file).expanduser().resolve(),
        source_file=Path(args.source_file).expanduser().resolve(),
        model=model,
        dry_run=args.dry_run,
    )


def cmd_text(args: argparse.Namespace) -> None:
    """
    Run inline prompt text against a single source file.
    """
    source_file = Path(args.source_file).expanduser().resolve()
    output = runner.run_text(
        prompt_text=args.prompt,
        source_text=source_file.read_text(),
        model=args.model or config.get_default_model(),
        dry_run=args.dry_run,
    )

    if output and not args.dry_run:
        outputs_dir = config.get_outputs_dir()
        outputs_dir.mkdir(parents=True, exist_ok=True)
        output_file = outputs_dir / f"{source_file.stem}_text_output.txt"
        output_file.write_text(output)
        print(f"[OUTPUT SAVED] {output_file}")


def cmd_dir(args: argparse.Namespace) -> None:
    """
    Run a prompt file against all supported files in a directory.
    """
    prompt_file = Path(args.prompt_file).expanduser().resolve()
    source_dir = Path(args.source_dir).expanduser().resolve()

    runner.run_dir(
        prompt_file=prompt_file,
        source_dir=source_dir,
        model=args.model or config.get_default_model(),
        dry_run=args.dry_run,
    )


def cmd_last(args: argparse.Namespace) -> None:
    """Re-run the last-used prompt/file combination."""
    runner.run_last(
        model=args.model or config.get_default_model(),
        dry_run=args.dry_run,
    )


def cmd_paths(_: argparse.Namespace) -> None:
    """Print LocalMind important paths."""
    runner.print_paths()


def cmd_outputs(_: argparse.Namespace) -> None:
    """Print information about LocalMind outputs."""
    runner.print_outputs()


def cmd_prompt(_: argparse.Namespace) -> None:
    """Interactively select a prompt file."""
    runner.select_prompt_interactive()


# --------------------------------------------------------------------------------------
# Argument parser
# --------------------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lcm",
        description="LocalMind – local-first prompt runner",
    )

    parser.add_argument(
        "--model",
        default=None,
        help="Model override (otherwise use config default)",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not execute inference; print what would run",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # file
    p_file = subparsers.add_parser("file", help="Run a prompt file on a file")
    p_file.add_argument("prompt_file")
    p_file.add_argument("source_file")
    p_file.set_defaults(func=cmd_file)

    # text
    p_text = subparsers.add_parser("text", help="Run inline prompt text on a file")
    p_text.add_argument("prompt")
    p_text.add_argument("source_file")
    p_text.set_defaults(func=cmd_text)

    # dir
    p_dir = subparsers.add_parser("dir", help="Run a prompt file on a directory")
    p_dir.add_argument("--prompt-file", required=True)
    p_dir.add_argument("source_dir")
    p_dir.set_defaults(func=cmd_dir)

    # last
    p_last = subparsers.add_parser("last", help="Re-run last invocation")
    p_last.set_defaults(func=cmd_last)

    # paths
    p_paths = subparsers.add_parser("paths", help="Show LocalMind paths")
    p_paths.set_defaults(func=cmd_paths)

    # outputs
    p_outputs = subparsers.add_parser("outputs", help="Show output folders")
    p_outputs.set_defaults(func=cmd_outputs)

    # prompt
    p_prompt = subparsers.add_parser("prompt", help="Select prompt interactively")
    p_prompt.set_defaults(func=cmd_prompt)

    return parser


# --------------------------------------------------------------------------------------
# Entry point
# --------------------------------------------------------------------------------------

def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)

    # Dispatch
    args.func(args)


if __name__ == "__main__":
    main()
