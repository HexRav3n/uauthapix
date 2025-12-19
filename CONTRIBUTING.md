# Contributing to UauthAPIX

Thank you for considering contributing to UauthAPIX! We welcome contributions from the security community.

## How to Contribute

### Reporting Bugs

If you find a bug, please create an issue with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior vs actual behavior
- Your environment (OS, Python version)
- Sample API spec if applicable (sanitized)

### Suggesting Enhancements

We love new ideas! Please create an issue with:
- A clear description of the enhancement
- Use cases and benefits
- Example usage if applicable

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Follow the existing code style
   - Add type hints
   - Include docstrings
   - Keep functions focused and modular

4. **Test your changes**
   - Test with various API specs
   - Verify all output formats work
   - Check edge cases
   - Ensure no regressions

5. **Update documentation**
   - Update README.md if needed
   - Add examples if applicable
   - Update CHANGELOG.md

6. **Commit your changes**
   ```bash
   git commit -m "Add: brief description of changes"
   ```
   Use commit prefixes:
   - `Add:` for new features
   - `Fix:` for bug fixes
   - `Update:` for enhancements
   - `Docs:` for documentation
   - `Refactor:` for code improvements

7. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**
   - Provide a clear description
   - Reference any related issues
   - Explain the changes and why they're needed

## Code Style

- Follow PEP 8
- Use type hints
- Maximum line length: 100 characters
- Use meaningful variable names
- Add docstrings to all functions
- Keep functions under 50 lines when possible

### Example

```python
def test_endpoint(method: str, url: str, headers: Dict[str, str],
                 timeout: int, verify_ssl: bool) -> Optional[TestResult]:
    """
    Test a single endpoint and return results

    Args:
        method: HTTP method to use
        url: Full URL to test
        headers: Request headers
        timeout: Request timeout in seconds
        verify_ssl: Whether to verify SSL certificates

    Returns:
        TestResult object or None if request failed
    """
    # Implementation
```

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/uauthapix.git
cd uauthapix

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install requests urllib3

# Run tests
python unauth-api-tester.py example-api-spec.json --base-url https://httpbin.org
```

## Testing Guidelines

- Test with both OpenAPI 3.x and Swagger 2.0 specs
- Test with various API configurations
- Verify all output formats (console, JSON, CSV, HTML)
- Test edge cases (empty specs, invalid JSON, timeouts)
- Test all bypass techniques
- Test multi-threading

## Ideas for Contributions

### High Priority
- [ ] Add request body testing from spec schemas
- [ ] Implement response similarity detection
- [ ] Add more bypass techniques
- [ ] Support for GraphQL APIs
- [ ] Better false positive detection

### Medium Priority
- [ ] Support for authentication schemes (OAuth, JWT)
- [ ] Webhook testing
- [ ] Rate limit detection and handling
- [ ] Response caching
- [ ] Progress bar for long scans

### Low Priority
- [ ] Web UI
- [ ] Database result storage
- [ ] Scheduled scanning
- [ ] Integration with security platforms
- [ ] Docker container

### Documentation
- [ ] Video tutorials
- [ ] More examples
- [ ] Use case guides
- [ ] Integration guides (Jenkins, GitHub Actions, etc.)

## Security Considerations

When contributing:
- **Never** include real credentials or tokens
- **Never** include real company API specs (use sanitized examples)
- Ensure new features can't be easily misused
- Add appropriate warnings for dangerous operations
- Consider rate limiting and ethical use

## Code Review Process

1. Maintainers will review your PR
2. Feedback will be provided if changes are needed
3. Once approved, your PR will be merged
4. Your contribution will be credited in the changelog

## Recognition

Contributors will be:
- Listed in the README
- Credited in CHANGELOG.md
- Acknowledged in release notes

## Questions?

Feel free to:
- Open an issue for discussion
- Ask questions in pull requests
- Suggest improvements to this guide

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for making UauthAPIX better! 🔒🛡️
