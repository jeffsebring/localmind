"""
LocalMind is a local-first AI orchestration system designed to emphasize deterministic behavior, explicit file I/O, minimal magic, and auditability. This thin launcher enables the execution of the CLI using the command:
    python -m localmind [subcommand] [args]
"""

from .cli import main

if __name__ == "__main__":
    main()

