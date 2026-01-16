---
title: Usage | LocalMind - Local AI Prompt Runner
---

# LocalMind Documentation: CLI Usage

## Overview

This document describes how to use LocalMind from the command line to run prompts on files, directories, or inline text. All commands can be run via the `lcm` CLI or with `python -m localmind`.

---

## Command Reference

### 1. File Command

Run a prompt file on a single source file.

```bash
python -m localmind file <prompt_file> <source_file> [--model MODEL] [--dry-run]
```

**Parameters**

* `prompt_file`: Path to the Markdown prompt file.
* `source_file`: Path to the source file you want to process.
* `--model MODEL`: Optional. Override default AI model.
* `--dry-run`: Optional. Print what would run without generating output.

**Example**

```bash
python -m localmind file ~/.localmind/prompts/uppercase.md ~/projects/hello.py --dry-run
```

---

### 2. Text Command

Run an inline prompt string against a source file.

```bash
python -m localmind text "<prompt_text>" <source_file> [--model MODEL] [--dry-run]
```

**Parameters**

* `<prompt_text>`: Inline prompt string.
* `source_file`: Path to the source file.
* `--model MODEL`: Optional model override.
* `--dry-run`: Optional preview.

**Example**

```bash
python -m localmind text "uppercase this file" ~/projects/hello.py --dry-run
```

---

### 3. Directory Command

Run a prompt file against all supported files in a directory.

```bash
python -m localmind dir <prompt_file> <source_dir> [--model MODEL] [--dry-run] [--ext EXTENSION]
```

**Parameters**

* `prompt_file`: Path to prompt file.
* `source_dir`: Directory containing source files.
* `--model MODEL`: Optional AI model override.
* `--dry-run`: Optional preview.
* `--ext EXTENSION`: Optional filter to only process files with this extension (e.g., `.py`, `.md`).

**Example**

```bash
python -m localmind dir ~/.localmind/prompts/uppercase.md ~/projects/myrepo --ext .py
```

---

### 4. Last Command

Re-run the last-used prompt/file combination.

```bash
python -m localmind last [--model MODEL] [--dry-run]
```

---

### 5. Paths Command

Print LocalMind's important paths.

```bash
python -m localmind paths
```

---

### 6. Outputs Command

Show information about generated output files.

```bash
python -m localmind outputs
```

---

### 7. Prompt Command

Interactively select a prompt file to run.

```bash
python -m localmind prompt
```

---

## Notes

* All outputs are timestamped in your configured `outputs_dir`.
* Use `--dry-run` to preview commands without writing files.
* Use `--ext` in directory mode to target specific file types.

---

End of usage.md