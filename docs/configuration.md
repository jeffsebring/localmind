---
title: Configuration | LocalMind - Local AI Prompt Runner
---

# Configuration

This document describes how LocalMind is configured, where configuration files live, and how configuration values are used at runtime.

---

## Configuration File Location

LocalMind uses a single JSON configuration file located at:

```
~/.localmind/config.json
```

This file is read on startup for all CLI commands.

If the file does not exist, LocalMind will fall back to internal defaults, but creating this file is strongly recommended.

---

## Example Configuration

```json
{
  "default_model": "deepseek-coder-v2:latest",
  "outputs_dir": "/home/user/.localmind/outputs",
  "prompts_dir": "/home/user/.localmind/prompts"
}
```

---

## Configuration Fields

### default_model

- **Type:** string
- **Required:** No (but recommended)

The default AI model to use when no `--model` flag is provided on the command line.

Example:

```json
"default_model": "deepseek-coder-v2:latest"
```

This value is passed directly to the underlying model runner (for example, Ollama).

---

### outputs_dir

- **Type:** string (absolute path)
- **Required:** Yes

Directory where LocalMind writes all generated outputs.

Each run creates a timestamped subdirectory containing output files.

Example:

```json
"outputs_dir": "/home/user/.localmind/outputs"
```

Expected structure:

```
~/.localmind/outputs/
  20260116_104233/
    hello.py_deepseek-coder-v2.txt
```

---

### prompts_dir

- **Type:** string (absolute path)
- **Required:** Yes

Directory where prompt files are stored.

Prompt files are plain text or Markdown files that are passed verbatim to the model along with the target file contents.

Example:

```json
"prompts_dir": "/home/user/.localmind/prompts"
```

Expected structure:

```
~/.localmind/prompts/
  summarize.md
  refactor.md
  explain.md
```

---

## Environment Expansion

Paths in `config.json` must be absolute paths.

Shell expansions such as `~` are **not** automatically expanded. Use full paths:

Correct:
```
/home/user/.localmind/outputs
```

Incorrect:
```
~/.localmind/outputs
```

---

## Command-Line Overrides

Most configuration values can be overridden at runtime using CLI flags.

Example:

```bash
python -m localmind file prompt.md file.py --model qwen2.5-coder:latest
```

In this case:
- `default_model` is ignored
- The specified model is used only for this invocation

Directory paths (`outputs_dir`, `prompts_dir`) are not currently overrideable via CLI in v1.

---

## Validation Behavior

On startup, LocalMind will:

1. Load `config.json`
2. Validate required fields
3. Create missing directories if possible

If validation fails, LocalMind exits with a descriptive error message.

---

## Minimal Configuration

The smallest recommended configuration is:

```json
{
  "default_model": "deepseek-coder-v2:latest",
  "outputs_dir": "/home/user/.localmind/outputs",
  "prompts_dir": "/home/user/.localmind/prompts"
}
```

## Version Notes

- Configuration format is stable for v1
- Future versions may support:
  - Per-project configuration
  - Environment-variable overrides
  - Multiple model profiles

---

[Back to Top](#title)
