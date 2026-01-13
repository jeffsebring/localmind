#!/usr/bin/env python3
"""
LocalMind CLI entrypoint.

This file is intentionally boring.
It contains *no* business logic, *no* inference logic, and *no* filesystem policy.

Responsibilities:
- Define the CLI interface (argparse)
- Validate arguments at the CLI boundary
- Dispatch to core runner functions using a *stable, explicit API*

If something breaks at runtime, this file should make it obvious *where* and *why*.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

from localmind.core import runner

# --------------------------------------------------------------------------------------
# Command handlers
# --------------------------------------------------------------------------------------


def cmd_file(args: argparse.Namespace) -> None:
    """Run a prompt file against a single source file."""
    runner.run_file(
        prompt_file=Path(args.prompt_file).expanduser().resolve(),
        source_file=Path(args.source_file).expanduser().resolve(),
        model=args.model,
        dry_run=args.dry_run,
    )


def cmd_text(args: argparse.Namespace) -> None:
    """Run an inline prompt against a single source file."""
    runner.run_text(
        prompt=args.prompt,
        source_file=Path(args.source_file).expanduser().resolve(),
        model=args.model,
        dry_run=args.dry_run,
    )


def cmd_dir(args: argparse.Namespace) -> None:
    """Run a prompt file against all supported files in a directory."""
    runner.run_dir(
        prompt_file=Path(args.prompt_file).expanduser().resolve(),
        source_dir=Path(args.source_dir).expanduser().resolve(),
        model=args.model,
        dry_run=args.dry_run,
    )


def cmd_last(args: argparse.Namespace) -> None:
    """Re-run the last-used prompt/file combination."""
    runner.run_last(
        model=args.model,
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
