# Contributing to touch-struct

Thank you for your interest in contributing to touch-struct! This document provides guidelines and instructions for development and releasing new versions.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/jadeglaze/touch-struct
cd touch-struct
```

2. Install in development mode with test dependencies:
```bash
pip install -e ".[test]"
```

3. Run tests to verify your setup:
```bash
python -m pytest tests/
```

## Making Changes

1. Create a new branch for your changes:
```bash
git checkout -b your-feature-name
```

2. Make your changes and ensure:
   - All tests pass
   - New features include tests
   - Code is properly formatted
   - Documentation is updated

3. Commit your changes with clear commit messages
4. Push to your fork and submit a pull request

## Publishing a New Release

1. Install the required publishing tools:
```bash
pip install build twine
```

2. Update version number in `pyproject.toml`

3. Build the distribution files:
```bash
python -m build
```

4. Test the package on TestPyPI first (recommended):
```bash
python -m twine upload --repository testpypi dist/*
```

5. Install and test the package from TestPyPI:
```bash
pip install --index-url https://test.pypi.org/simple/ touch-struct
```

6. If everything looks good, upload to PyPI:
```bash
python -m twine upload dist/*
```

7. Create a new release on GitHub:
   - Tag the version (e.g., v0.1.0)
   - Include release notes
   - Include any breaking changes or migration instructions

## Code Style

- Follow PEP 8 guidelines
- Include docstrings for public functions and classes
- Keep functions focused and single-purpose
- Write clear commit messages

## Questions?

If you have questions about contributing, please open an issue in the GitHub repository. 