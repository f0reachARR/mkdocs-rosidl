# Contributing to mkdocs-rosidl

Thank you for your interest in contributing to mkdocs-rosidl! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Issues

If you find a bug or have a feature request, please create an issue on GitHub with:

- A clear description of the problem or feature
- Steps to reproduce (for bugs)
- Expected vs. actual behavior (for bugs)
- Your environment details (OS, Python version, ROS2 version, MkDocs version)

### Submitting Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the coding standards below
3. **Test your changes** thoroughly
4. **Update documentation** if necessary
5. **Submit a pull request** with a clear description of your changes

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/f0reachARR/mkdocs-rosidl.git
cd mkdocs-rosidl
```

2. Install in development mode:
```bash
pip install -e .
```

3. Install development dependencies:
```bash
pip install mkdocs jinja2 rosidl-runtime-py rosidl-parser ament-index-python
```

## Coding Standards

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions focused and modular
- Add type hints where appropriate

## Testing

Before submitting a pull request:

1. Test the plugin with various ROS2 packages
2. Verify that generated documentation is correct
3. Check that the plugin integrates properly with MkDocs

## License

By contributing to mkdocs-rosidl, you agree that your contributions will be licensed under the Apache License 2.0.

## Questions?

If you have questions about contributing, feel free to open an issue for discussion.
