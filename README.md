# LocalMind

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE) [![Documentation](https://img.shields.io/badge/docs-github_pages-blue)](https://jeffsebring.github.io/localmind/)

LocalMind is a local-first prompt runner designed to automate running prompts and scripts against source files and directories. It provides a consistent CLI interface for running prompt files, inline prompts, and directory-wide processing with outputs logged to timestamped files.

## Features

* Run prompt files or inline prompts against single files or directories
* Recursive directory processing with file type filtering
* Dry-run mode for safe testing
* Timestamped output logging
* Configurable defaults via `~/.localmind/config.json`

## Installation

```bash
git clone https://github.com/jeffsebring/localmind.git
cd localmind
pip install -r requirements.txt
```

## Usage

```bash
# Run a prompt file on a file
python -m localmind file ~/.localmind/prompts/refactor.md ~/localmind_test/hello.py

# Run inline text
python -m localmind text "uppercase this file" ~/localmind_test/hello.py

# Run a prompt file on a directory
python -m localmind dir ~/.localmind/prompts/uppercase.md ~/localmind_test/ --ext .py

# Dry-run example
python -m localmind --dry-run text "uppercase this file" ~/localmind_test/hello.py
```

## Configuration

LocalMind looks for configuration in `~/.localmind/config.json`. Example:

```json
{
  "default_model": "deepseek-coder-v2:latest",
  "outputs_dir": "~/.localmind/outputs",
  "prompts_dir": "~/.localmind/prompts"
}
```

## Philosophy

LocalMind is designed to be **local-first, extensible, and modular**. It encourages reproducible automation workflows while giving developers complete control over prompts, source files, and output management.

