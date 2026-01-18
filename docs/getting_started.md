---
title: Gettings Started | LocalMind - Local AI Prompt Runner
---

# LocalMind Documentation: Getting Started

## Introduction

LocalMind is a local-first prompt runner designed to simplify running AI-driven prompts against code or text. It supports running prompt files against single files, directories, or inline text, and provides timestamped outputs for easy tracking. LocalMind is designed to be modular, extensible, and open-source, making it suitable for developers and AI enthusiasts.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jeffsebring/localmind.git
cd localmind
```

2. Create a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate     # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) Add LocalMind to your PATH for easy CLI access:

```bash
export PATH="$PATH:$(pwd)/localmind"
```

## Configuration

LocalMind uses a JSON configuration file located at:

```
~/.localmind/config.json
```

Example configuration:

```json
{
  "default_model": "deepseek-coder-v2:latest",
  "outputs_dir": "/home/user/.localmind/outputs",
  "prompts_dir": "/home/user/.localmind/prompts"
}
```

- **default_model**: The AI model to use by default.
- **outputs_dir**: Directory to store timestamped output files.
- **prompts_dir**: Directory containing your prompt files.

## CLI Usage

LocalMind provides a command-line interface `lcm` (or via `python -m localmind`).

### Commands

1. **File Command**

Run a prompt file on a single source file:

```bash
python -m localmind file <prompt_file> <source_file> [--model MODEL] [--dry-run]
```

Example:

```bash
python -m localmind file ~/.localmind/prompts/uppercase.md ~/projects/hello.py --dry-run
```

2. **Text Command**

Run an inline prompt string against a file:

```bash
python -m localmind text "uppercase this file" <source_file> [--model MODEL] [--dry-run]
```

Example:

```bash
python -m localmind text "uppercase this file" ~/projects/hello.py --dry-run
```

3. **Directory Command**

Run a prompt file against all files in a directory:

```bash
python -m localmind dir <prompt_file> <source_dir> [--model MODEL] [--dry-run] [--ext EXTENSION]
```

Example:

```bash
python -m localmind dir ~/.localmind/prompts/uppercase.md ~/projects/myrepo --ext .py
```

4. **Paths Command**

Print LocalMind important paths:

```bash
python -m localmind paths
```

5. **Outputs Command**

Show information about output folders:

```bash
python -m localmind outputs
```

6. **Prompt Command**

Interactively select a prompt file:

```bash
python -m localmind prompt
```

## Output Files

All outputs are timestamped and stored in your `outputs_dir`. Filename format:

```
YYYYMMDD_HHMMSS_<source_filename>_<model>.txt
```

## Example Workflow

1. Place your prompt files in `~/.localmind/prompts/`.
2. Run a prompt against a single file:

```bash
python -m localmind file ~/.localmind/prompts/uppercase.md ~/projects/hello.py
```

3. Run a prompt against all `.py` files in a directory:

```bash
python -m localmind dir ~/.localmind/prompts/uppercase.md ~/projects/myrepo --ext .py
```

4. View output files:

```bash
python -m localmind outputs
```

## Tips

- Use `--dry-run` to preview prompt execution without generating output files.
- Keep your prompts modular and reusable by storing them in `~/.localmind/prompts/`.
- Timestamped outputs allow you to easily track progress across multiple runs.

## Next Steps

- Explore inline prompt usage for quick testing (`text` command).
- Organize prompt files by project for easier management.
- Combine LocalMind with version control for reproducible AI-assisted workflows.

---

End of getting_started.md

