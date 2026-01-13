"""
Thin launcher for LocalMind.
Allows running the CLI using:
    python -m localmind [subcommand] [args]
"""

from .cli import main

if __name__ == "__main__":
    main()
