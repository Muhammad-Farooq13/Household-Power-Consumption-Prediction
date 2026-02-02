# Contributing to Household Power Consumption Prediction

Thank you for your interest in contributing! Here are the guidelines to help you get started.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/household-power-consumption.git
   cd household-power-consumption
   ```

3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Before you start coding:

1. Check existing issues and pull requests
2. Create an issue to discuss your proposed change
3. Get feedback before implementing

### While coding:

1. **Follow PEP 8** style guide
2. **Add type hints** to functions
3. **Write docstrings** for all functions and classes
4. **Add tests** for new functionality

### Code Style

Run these tools to ensure code quality:

```bash
# Format code with black
black src/

# Check linting with pylint
pylint src/

# Check type hints with mypy
mypy src/
```

### Testing

Write tests in the `tests/` directory:

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=src/

# Run specific test
pytest tests/test_models.py::TestModelTrainer::test_train_test_split -v
```

**Minimum coverage requirement: 80%**

## Commit Guidelines

- Use clear, descriptive commit messages
- Reference issues when relevant: `Fixes #123`
- Format: `[TYPE] Brief description`

Examples:
- `[FEATURE] Add LSTM model support`
- `[FIX] Handle missing values in preprocessor`
- `[DOCS] Update API documentation`
- `[TEST] Add tests for feature engineering`

## Pull Request Process

1. **Update documentation** if needed
2. **Run tests**: `pytest tests/ -v`
3. **Update README** if you've added new features
4. **Create a pull request** with a clear title and description
5. **Link related issues**: `Closes #123`
6. **Wait for review** and address feedback

## Reporting Issues

When reporting bugs, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages/tracebacks
- Code example (if applicable)

## Questions?

- Open an issue with label `question`
- Contact: mfarooqshafee333@gmail.com

## Code of Conduct

- Be respectful and inclusive
- No harassment or discrimination
- Focus on the code, not the person
- Welcome feedback and constructive criticism

Thank you for contributing! 🎉
