# Contributing to JetObsMC

Thank you for contributing.

## Development Setup

```bash
python3.13 -m venv .venv
source .venv/bin/activate
pip install -U pip
pip install -r requirements.txt
pip install .
```

## Quality Checks

Run tests before opening a pull request:

```bash
pytest -q
```

If you edit notebooks, ensure they run end-to-end from a clean kernel.

## Pull Request Guidelines

- Keep changes focused and atomic.
- Add or update tests for behavior changes.
- Update documentation (`README.md`, `docs/`, or notebook text) when APIs or outputs change.
- Use clear commit messages and PR descriptions.

## Reporting Issues

- Use GitHub Issues.
- Include reproduction steps, expected behavior, and actual behavior.
