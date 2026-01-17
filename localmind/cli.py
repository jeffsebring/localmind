#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from datetime import datetime
from .core import runner, config

"""
LocalMind - local-first prompt runner

This module provides a command-line interface (CLI) for running prompts on files and directories using the LocalMind system. It supports various commands to interact with the system, including file, text, directory, last invocation, listing paths, showing outputs, and interactive selection of prompts. The CLI is built using the argparse library and includes detailed documentation for each command and argument.
"""

def cmd_file(args: argparse.Namespace) -> None:
    """Run a prompt file on a specified source file using the provided model and dry run option.
    
    Args:
        args (argparse.Namespace): The parsed arguments from the CLI.
            - prompt_file (str): Path to the prompt file.
            - source_file (str): Path to the source file to be processed.
            - model (Optional[str]): Model to use for processing, defaults to the default model configured in the system.
            - dry_run (bool): If True, performs a dry run without executing inference.
    """
    runner.run_file(
        prompt_file=Path(args.prompt_file).expanduser().resolve(),
        source_file=Path(args.source_file).expanduser().resolve(),
        model=args.model or config.get_default_model(),
        dry_run=args.dry_run,
    )

def cmd_text(args: argparse.Namespace) -> None:
    """Run an inline prompt text on a provided source file.
    
    Args:
        args (argparse.Namespace): The parsed arguments from the CLI.
            - prompt (str): The inline prompt text to be executed.
            - source_file (str): Path to the source file containing the text to be processed by the prompt.
            - model (Optional[str]): Model to use for processing, defaults to the default model configured in the system.
            - dry_run (bool): If True, performs a dry run without executing inference.
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
    """Run a prompt file on all files within a specified directory.
    
    Args:
        args (argparse.Namespace): The parsed arguments from the CLI.
            - prompt_file (str): Path to the prompt file.
            - source_dir (str): Directory containing the files to be processed by the prompt.
            - ext (Optional[str]): Filter files by extension, e.g., .py, .md.
            - model (Optional[str]): Model to use for processing, defaults to the default model configured in the system.
            - dry_run (bool): If True, performs a dry run without executing inference.
    """
    runner.run_dir(
        prompt_file=Path(args.prompt_file).expanduser().resolve(),
        source_dir=Path(args.source_dir).expanduser().resolve(),
        model=args.model or config.get_default_model(),
        dry_run=args.dry_run,
        ext_filter=args.ext
    )

def cmd_last(args: argparse.Namespace) -> None:
    """Re-run the last executed prompt with an optional model override and dry run mode.
    
    Args:
        args (argparse.Namespace): The parsed arguments from the CLI.
            - model (Optional[str]): Model to use for processing, defaults to the default model configured in the system.
            - dry_run (bool): If True, performs a dry run without executing inference.
    """
    runner.run_last(model=args.model or config.get_default_model(), dry_run=args.dry_run)

def cmd_paths(_: argparse.Namespace) -> None:
    """Print all configured paths used by LocalMind.
    
    This function does not take any arguments as it simply prints the system configuration paths.
    """
    runner.print_paths()

def cmd_outputs(_: argparse.Namespace) -> None:
    """Print the directories where LocalMind outputs are saved.
    
    This function does not take any arguments as it simply prints the configured output directories.
    """
    runner.print_outputs()

def cmd_prompt(_: argparse.Namespace) -> None:
    """Interactively select and run a prompt from available options.
    
    This function does not take any arguments as it relies on user interaction to select a prompt.
    """
    runner.select_prompt_interactive()

def build_parser() -> argparse.ArgumentParser:
    """Create and configure an ArgumentParser for handling CLI commands.
    
    Returns:
        argparse.ArgumentParser: The configured argument parser ready to handle CLI inputs.
    """
    parser = argparse.ArgumentParser(
        prog="lcm",
        description="LocalMind – local-first prompt runner"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # Command to run a prompt on a single file
    p_file = subparsers.add_parser("file", help="Run a prompt file on a file")
    p_file.add_argument("prompt_file")
    p_file.add_argument("source_file")
    p_file.add_argument("--dry-run", action="store_true", help="Do not execute inference; print what would run")
    p_file.add_argument("--model", default=None, help="Model override (otherwise use config default)")
    p_file.set_defaults(func=cmd_file)

    # Command to run a prompt on inline text from a file
    p_text = subparsers.add_parser("text", help="Run inline prompt text on a file")
    p_text.add_argument("prompt")
    p_text.add_argument("source_file")
    p_text.add_argument("--dry-run", action="store_true", help="Do not execute inference; print what would run")
    p_text.add_argument("--model", default=None, help="Model override (otherwise use config default)")
    p_text.set_defaults(func=cmd_text)

    # Command to run a prompt on all files in a directory
    p_dir = subparsers.add_parser("dir", help="Run a prompt file on a directory")
    p_dir.add_argument("prompt_file")
    p_dir.add_argument("source_dir")
    p_dir.add_argument("--ext", default=None, help="Filter files by extension (e.g. .py, .md)")
    p_dir.add_argument("--dry-run", action="store_true", help="Do not execute inference; print what would run")
    p_dir.add_argument("--model", default=None, help="Model override (otherwise use config default)")
    p_dir.set_defaults(func=cmd_dir)

    # Command to re-run the last executed prompt
    p_last = subparsers.add_parser("last", help="Re-run last invocation")
    p_last.add_argument("--dry-run", action="store_true", help="Do not execute inference; print what would run")
    p_last.set_defaults(func=cmd_last)

    # Command to list all configured paths in the system
    p_paths = subparsers.add_parser("paths", help="List all configured paths")
    p_paths.set_defaults(func=cmd_paths)

    # Command to show output directories used by LocalMind
    p_outputs = subparsers.add_parser("outputs", help="Show output directories")
    p_outputs.set_defaults(func=cmd_outputs)

    # Command to interactively select and run a prompt
    p_prompt = subparsers.add_parser("prompt", help="Select prompt interactively")
    p_prompt.set_defaults(func=cmd_prompt)

    return parser

def main(argv: list[str] | None = None) -> None:
    """Main entry point for LocalMind CLI, parses command-line arguments and executes the appropriate command.
    
    Args:
        argv (Optional[List[str]]): List of command-line arguments to parse, defaults to sys.argv if not provided.
    """
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)

if __name__ == "__main__":
    main()