# Changelog

All notable changes to UauthAPIX will be documented in this file.

## [2.0.0] - 2025-12-19

### Added - Major Rewrite
- **New Name**: Rebranded as UauthAPIX with cool ASCII art logo
- **Enhanced Detection**: Smart vulnerability detection with false positive filtering
  - Checks multiple success status codes (200, 201, 202, 204, 206)
  - Identifies proper security responses (401, 403, 405, 407)
  - Filters HTML error pages
  - Analyzes response content for error indicators
  - Validates response size

- **Advanced Testing Techniques**:
  - 13 different bypass headers (X-Forwarded-For, X-Real-IP, etc.)
  - Path manipulation (trailing slashes, normalization, traversal)
  - Alternative HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE)
  - Request variations testing

- **Performance Features**:
  - Multi-threaded execution with configurable thread count
  - Configurable delay between requests for rate limiting
  - Request timeout configuration
  - Concurrent test execution

- **Output & Reporting**:
  - Colored console output with ANSI codes
  - Multiple verbosity levels (-v, -vv, -vvv)
  - Quiet mode for CI/CD integration
  - Export to JSON, CSV, and HTML formats
  - Beautiful summary statistics
  - Real-time progress updates

- **Configuration Options**:
  - Custom headers file support
  - Proxy support (Burp Suite integration)
  - SSL verification toggle
  - Path exclusion patterns
  - Custom timeout settings

- **OpenAPI/Swagger Support**:
  - OpenAPI 3.x support
  - Swagger 2.0 support
  - Automatic base URL extraction from spec
  - Support for both {param} and :param path parameters
  - Proper endpoint parsing

- **Error Handling**:
  - Comprehensive exception handling
  - Graceful timeout handling
  - Connection error management
  - JSON validation
  - File existence checks

- **Documentation**:
  - Comprehensive README with examples
  - Quick start guide
  - Example files included
  - Detailed help text

### Changed
- Complete rewrite of core functionality
- Improved code structure with dataclasses
- Type hints throughout codebase
- Better function organization
- Enhanced CLI argument parsing

### Technical Improvements
- Used dataclasses for result and stats management
- Implemented proper request/response handling
- Added thread pooling for concurrent execution
- Structured logging and output
- Modular function design

### Security
- Added warnings for SSL verification being disabled
- Proper handling of sensitive headers
- Safe file operations
- Input validation

## [1.0.0] - Original Version

### Features
- Basic endpoint testing
- Simple 200 OK detection
- OpenAPI spec parsing
- Path parameter substitution
- Basic error handling

### Limitations
- Only checked for 200 status code
- No false positive filtering
- Silent error handling
- Limited output options
- No advanced bypass techniques
- No concurrent execution
- No export capabilities

---

## Upgrade Guide

### From 1.0 to 2.0

The 2.0 version is a complete rewrite with many new features. Key differences:

**Command Line Changes**:
- Added many new flags: `--test-headers`, `--test-paths`, `--test-methods`, `--test-all`
- Added output options: `--output`, `--format`, `--verbosity`
- Added configuration: `--custom-headers`, `--proxy`, `--exclude`
- Added performance: `--threads`, `--delay`, `--timeout`

**Behavior Changes**:
- Now shows colored output by default (use `--no-color` to disable)
- Provides detailed summary at the end
- Exits with code 1 if vulnerabilities found (good for CI/CD)
- More intelligent vulnerability detection (fewer false positives)

**Usage**:
```bash
# Old v1.0 usage
python unauth-api-tester.py spec.json https://api.example.com

# New v2.0 usage
python unauth-api-tester.py spec.json --base-url https://api.example.com

# With advanced features
python unauth-api-tester.py spec.json --base-url https://api.example.com --test-all -vv
```

**Migration**: Simply update your command line to use `--base-url` flag instead of positional argument.

---

## Future Enhancements (Planned)

- [ ] Support for request body testing
- [ ] Integration with authentication providers
- [ ] More bypass techniques
- [ ] Response similarity analysis
- [ ] Machine learning for false positive detection
- [ ] Support for GraphQL APIs
- [ ] Support for gRPC APIs
- [ ] WebSocket testing
- [ ] Automatic retry with exponential backoff
- [ ] Response caching
- [ ] Diff mode (compare two scans)
- [ ] Integration with CI/CD platforms
- [ ] Docker container
- [ ] Web UI
- [ ] Database storage for results
- [ ] Scheduled scanning
- [ ] Alert notifications

---

## Contributing

To contribute to UauthAPIX:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Update documentation
6. Submit a pull request

Please follow the existing code style and add appropriate documentation.
