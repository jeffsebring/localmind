---
title: Development | LocalMind - Local AI Prompt Runner
---

# LocalMind Documentation: Development

## Overview

This document provides guidelines for contributing to LocalMind, including development setup, testing, and coding standards.

LocalMind is a Python project designed to be modular, maintainable, and open-source. The development workflow assumes familiarity with Python 3.13+, virtual environments, and basic Git usage.

---

## Development Setup

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

3. Install development dependencies:

```bash
pip install -r requirements.txt
```

4. Ensure the `lcm` CLI is available:

```bash
export PATH="$PATH:$(pwd)/localmind"
```

---

## Project Structure

```
localmind/
├── core/         # Core modules and CLI runner
├── tests/        # Unit and integration tests
├── prompts/      # Sample prompt files
├── README.md
├── pyproject.toml
└── requirements.txt
```

---

## Coding Standards

* Use **PEP8** style conventions.
* Docstrings are required for all public functions and classes.
* Type hints are encouraged for all function signatures.
* Avoid breaking changes in the public API.

---

## Running Tests

Unit tests are located in the `tests/` directory. To run tests:

```bash
pytest tests/ --maxfail=1 --disable-warnings -q
```

---

## CLI Testing

Use the `--dry-run` flag for safe testing of CLI commands without executing prompts:

```bash
python -m localmind file ~/.localmind/prompts/example.md ~/localmind_test/hello.py --dry-run
```

---

## Contributing

1. Fork the repository.
2. Create a feature branch:

```bash
git checkout -b feature/my-feature
```

3. Make your changes and ensure all tests pass.
4. Submit a pull request against the `master` branch.

---

## Version Control Guidelines

* Use meaningful commit messages.
* Rebase before merging to maintain a clean history.

---
* Tag releases using semantic versioning (e.g., v1.0.0).

## Notes

* This project aims to be **open, modular, and easily extensible**.
* All development should prioritize stability and backward compatibility for the CLI interface.

--- End of development.md
