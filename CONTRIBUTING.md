# Contributing to AI Incident Commander

Thank you for your interest in contributing to AI Incident Commander!

## Development Setup

1. Fork the repository
2. Clone your fork:
```bash
git clone https://github.com/YOUR_USERNAME/ai-incident-commander.git
cd ai-incident-commander
```

3. Set up the development environment:
```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

4. Create a feature branch:
```bash
git checkout -b feature/your-feature-name
```

## Code Style

### Python (Backend)
- Follow PEP 8 guidelines
- Use type hints for function signatures
- Write docstrings for classes and functions
- Format code with `black`:
```bash
pip install black
black app/
```

### JavaScript/React (Frontend)
- Use functional components and hooks
- Follow React best practices
- Use meaningful variable and component names
- Format code with Prettier:
```bash
npm run format
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md with your changes
5. Submit a pull request with a clear description

### PR Title Format
```
[Type] Brief description

Types: feat, fix, docs, style, refactor, test, chore
```

Examples:
- `[feat] Add incident postmortem generation`
- `[fix] Resolve WebSocket connection issue`
- `[docs] Update API documentation`

## Commit Message Guidelines

Follow conventional commits:
```
type(scope): description

[optional body]
[optional footer]
```

Examples:
```
feat(api): add endpoint for incident bulk export
fix(websocket): handle reconnection on network failure
docs(readme): update installation instructions
```

## Feature Requests

Open an issue with the label `enhancement` and include:
- Clear use case description
- Proposed solution or approach
- Any relevant examples or mockups

## Bug Reports

Open an issue with the label `bug` and include:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Screenshots if applicable
- Environment details (OS, Python version, etc.)

## Areas for Contribution

### High Priority
- Add authentication and authorization
- Implement database persistence (PostgreSQL)
- Add more AI analysis capabilities
- Improve test coverage
- Performance optimizations

### Good First Issues
- Add more seed data scenarios
- Improve error messages
- Add loading states to UI
- Write additional documentation
- Create example integrations

## Questions?

Feel free to open a discussion or reach out to the maintainers.

Thank you for contributing!
