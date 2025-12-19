# UauthAPIX v2.0

```
██╗   ██╗ █████╗ ██╗   ██╗████████╗██╗  ██╗ █████╗ ██████╗ ██╗██╗  ██╗
██║   ██║██╔══██╗██║   ██║╚══██╔══╝██║  ██║██╔══██╗██╔══██╗██║╚██╗██╔╝
██║   ██║███████║██║   ██║   ██║   ███████║███████║██████╔╝██║ ╚███╔╝
██║   ██║██╔══██║██║   ██║   ██║   ██╔══██║██╔══██║██╔═══╝ ██║ ██╔██╗
╚██████╔╝██║  ██║╚██████╔╝   ██║   ██║  ██║██║  ██║██║     ██║██╔╝ ██╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
```

**Advanced API Security Testing Tool**

UauthAPIX is a powerful security testing tool for detecting unauthorized access vulnerabilities in REST APIs. It tests OpenAPI/Swagger specifications for endpoints that are accessible without proper authentication.

## Features

### Core Capabilities
- **OpenAPI/Swagger Support**: Parses OpenAPI 3.x and Swagger 2.0 specifications
- **Smart Detection**: Identifies truly vulnerable endpoints while avoiding false positives
- **Multiple Testing Techniques**: Tests various authentication bypass methods
- **Concurrent Testing**: Multi-threaded execution for faster scanning
- **Rich Reporting**: Colored console output with detailed statistics
- **Multiple Export Formats**: JSON, CSV, and HTML report generation

### Testing Techniques

1. **Direct Testing**: Standard requests to endpoints as defined in the spec
2. **Bypass Headers**: Tests common header-based authentication bypasses:
   - X-Forwarded-For, X-Real-IP, X-Client-IP
   - X-Original-URL, X-Rewrite-URL
   - X-Remote-IP, X-Remote-Addr
   - And more...

3. **Path Variations**: Tests path manipulation techniques:
   - Trailing slash variations (`/api/users` vs `/api/users/`)
   - Path normalization (`//api/users`, `/api/users/..`)
   - Double slashes and traversal attempts

4. **HTTP Method Testing**: Tests alternative HTTP methods (GET, POST, PUT, DELETE, PATCH, HEAD, OPTIONS, TRACE)

### Detection Logic

The tool uses intelligent detection to minimize false positives:
- Checks for success status codes (200, 201, 202, 204, 206)
- Identifies proper security responses (401, 403, 405, 407)
- Filters out HTML error pages
- Analyzes response content for error messages
- Validates response size and content

## Installation

### Requirements
- Python 3.7+
- Required packages:

```bash
pip install requests urllib3
```

### Setup

```bash
# Clone or download the tool
chmod +x unauth-api-tester.py
```

## Usage

### Basic Usage

```bash
# Basic test with base URL
python unauth-api-tester.py api-spec.json --base-url https://api.example.com

# Use base URL from spec (OpenAPI 3.x servers or Swagger 2.0 host)
python unauth-api-tester.py api-spec.json
```

### Advanced Testing

```bash
# Test with all techniques enabled
python unauth-api-tester.py api-spec.json --base-url https://api.example.com --test-all

# Test specific techniques
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --test-headers --test-paths --test-methods

# Use multiple threads for faster scanning
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --threads 10 --delay 0.1
```

### Output Options

```bash
# Increase verbosity
python unauth-api-tester.py api-spec.json --base-url https://api.example.com -v
python unauth-api-tester.py api-spec.json --base-url https://api.example.com -vv
python unauth-api-tester.py api-spec.json --base-url https://api.example.com -vvv

# Quiet mode (only show vulnerabilities)
python unauth-api-tester.py api-spec.json --base-url https://api.example.com -q

# Disable colored output
python unauth-api-tester.py api-spec.json --base-url https://api.example.com --no-color

# Export results
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --output results.json --format json

python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --output results.csv --format csv

python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --output report.html --format html
```

### Configuration Options

```bash
# Use custom headers (e.g., API keys for testing)
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --custom-headers headers.txt

# Use proxy (e.g., Burp Suite)
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --proxy http://127.0.0.1:8080

# Enable SSL verification (disabled by default)
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --verify-ssl

# Exclude specific paths
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --exclude "/health" --exclude "/metrics"

# Set custom timeout
python unauth-api-tester.py api-spec.json --base-url https://api.example.com \
  --timeout 30
```

## Command-Line Options

### Required Arguments
- `spec_file`: Path to OpenAPI/Swagger JSON file
- `--base-url`: Base URL for the API (optional if specified in spec)

### Testing Options
- `--test-headers`: Test with bypass headers
- `--test-paths`: Test path variations
- `--test-methods`: Test alternative HTTP methods
- `--test-all`: Enable all testing techniques

### Performance Options
- `--threads N`: Number of concurrent threads (default: 1)
- `--delay N`: Delay between requests in seconds (default: 0)
- `--timeout N`: Request timeout in seconds (default: 10)

### Output Options
- `-v, -vv, -vvv`: Increase verbosity level
- `-q, --quiet`: Quiet mode (only show vulnerabilities)
- `--no-color`: Disable colored output
- `--output FILE`: Output file path
- `--format {json,csv,html}`: Output format (default: json)

### Configuration Options
- `--custom-headers FILE`: File with custom headers
- `--proxy URL`: Proxy URL
- `--verify-ssl`: Enable SSL certificate verification
- `--exclude PATTERN`: Exclude paths matching regex pattern

## Custom Headers File Format

Create a text file with one header per line:

```
# Comments start with #
Authorization: Bearer test-token
X-API-Key: your-api-key
Custom-Header: custom-value
```

## Output Formats

### Console Output
- Colored output with symbols (✓ for secure, ✗ for vulnerable)
- Real-time progress updates
- Summary statistics at the end
- Configurable verbosity levels

### JSON Export
```json
{
  "summary": {
    "total_tests": 150,
    "vulnerabilities_found": 3,
    "secure_endpoints": 147,
    "errors": 0
  },
  "results": [
    {
      "method": "GET",
      "url": "https://api.example.com/users",
      "status_code": 200,
      "response_time": 0.234,
      "response_length": 1024,
      "content_type": "application/json",
      "is_vulnerable": true,
      "technique": "direct"
    }
  ]
}
```

### CSV Export
Spreadsheet-compatible format with columns:
- Method, URL, Status Code, Response Time, Response Length, Content Type, Vulnerable, Technique

### HTML Export
Professional HTML report with:
- Summary dashboard
- Color-coded results table
- Sortable columns
- Print-friendly layout

## Exit Codes

- `0`: No vulnerabilities found
- `1`: Vulnerabilities detected

Useful for CI/CD integration:

```bash
python unauth-api-tester.py api-spec.json --base-url https://api.example.com
if [ $? -eq 1 ]; then
    echo "Security vulnerabilities detected!"
    exit 1
fi
```

## Examples

### Example 1: Basic Security Scan

```bash
python unauth-api-tester.py swagger.json --base-url https://api.example.com
```

### Example 2: Comprehensive Security Audit

```bash
python unauth-api-tester.py openapi.json \
  --base-url https://api.example.com \
  --test-all \
  --threads 10 \
  --delay 0.2 \
  --output audit-report.html \
  --format html \
  -vv
```

### Example 3: Testing Through Burp Suite

```bash
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --proxy http://127.0.0.1:8080 \
  --test-all
```

### Example 4: CI/CD Integration

```bash
# In your CI/CD pipeline
python unauth-api-tester.py api-spec.json \
  --base-url https://staging-api.example.com \
  --test-all \
  --quiet \
  --output security-scan.json \
  --format json

# Parse results or fail build if vulnerabilities found
```

### Example 5: Testing with Authentication

Create `headers.txt`:
```
Authorization: Bearer valid-token-123
```

Run test:
```bash
# Test which endpoints are accessible even WITH authentication
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --custom-headers headers.txt \
  --test-headers
```

## Understanding Results

### Vulnerable Endpoint
```
✗ GET     https://api.example.com/admin/users -> 200 (VULNERABLE)
```
This endpoint returned a success code without authentication - potential security issue!

### Secure Endpoint
```
✓ GET     https://api.example.com/admin/users -> 401 (SECURE)
```
This endpoint properly rejected unauthenticated requests.

### Bypass Technique Detection
```
✗ GET     https://api.example.com/api/data -> 200 (VULNERABLE) [header:X-Forwarded-For]
```
This endpoint was bypassed using the X-Forwarded-For header.

## Best Practices

1. **Rate Limiting**: Use `--delay` to avoid overwhelming the target server
2. **Threading**: Start with low thread count and increase gradually
3. **Comprehensive Testing**: Use `--test-all` for thorough security assessment
4. **Proxy Usage**: Route through Burp Suite for deeper analysis
5. **Regular Scanning**: Integrate into CI/CD for continuous security monitoring
6. **False Positive Review**: Always manually verify reported vulnerabilities
7. **Exclude Health Checks**: Use `--exclude` to skip known public endpoints

## Limitations

- Does not test authentication logic (only tests for missing authentication)
- Path parameter substitution uses random values (may not match API requirements)
- Does not test request body payloads
- May generate false positives on misconfigured APIs
- Does not handle CAPTCHA or rate limiting

## Security Considerations

This tool is designed for authorized security testing only. Usage guidelines:

- ✅ Test your own APIs
- ✅ Authorized penetration testing with permission
- ✅ Bug bounty programs (within scope)
- ✅ Security research on test environments
- ❌ Unauthorized scanning of third-party APIs
- ❌ Malicious or illegal activities

## Troubleshooting

### No endpoints found in spec
- Verify JSON syntax is valid
- Ensure spec contains `paths` object
- Check OpenAPI/Swagger version compatibility

### SSL Certificate errors
- Use `--verify-ssl` flag if you have valid certificates
- SSL verification is disabled by default for testing environments

### Connection timeouts
- Increase timeout: `--timeout 30`
- Reduce thread count
- Add delay between requests

### Too many false positives
- Review response content with `-vvv`
- Adjust detection logic in `is_vulnerable_response()`
- Use `--exclude` for known public endpoints

## Contributing

Suggestions for improvements:
- Additional bypass techniques
- Enhanced detection logic
- Support for request body testing
- Integration with other security tools

## License

This tool is provided for educational and authorized security testing purposes only.

## Version History

### v2.0 (Current)
- Complete rewrite with enhanced features
- Multi-threading support
- Advanced bypass techniques
- Multiple output formats
- Improved detection logic
- Custom headers support
- Proxy support
- Comprehensive CLI options

### v1.0
- Basic endpoint testing
- Simple 200 OK detection
- Limited output options
