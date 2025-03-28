# Contributing to Muscle5 Sequence Alignment Tool

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR-USERNAME/bioinformatic-python-alignment-muscle5.git`
3. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Environment Setup

1. Install Python 3.8 or higher
2. Install dependencies: `pip install -r requirements.txt`
3. Download MUSCLE5 executable from https://drive5.com/muscle/
4. Set the MUSCLE5_PATH environment variable to point to your executable:
   - Windows: `set MUSCLE5_PATH=path\to\muscle.exe`
   - Mac/Linux: `export MUSCLE5_PATH=/path/to/muscle`

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines for Python code
- Use docstrings for functions and classes
- Keep lines under 100 characters when possible

### Testing

Run tests before submitting changes:

```bash
python test_app.py
```

### Pull Request Process

1. Update the README.md with details of any interface changes
2. Update the requirements.txt if you add dependencies
3. Create a Pull Request with a clear description of the changes
4. Ensure all tests pass

## Feature Suggestions

If you have ideas for new features, please open an issue to discuss before implementing.

## License

By contributing, you agree that your contributions will be licensed under the project's MIT license.
