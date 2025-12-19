# UauthAPIX - Quick Start Guide

## Installation

```bash
# Install required dependencies
pip install requests urllib3
```

## Quick Start

### 1. Basic Test
Test an API using an OpenAPI spec:
```bash
python unauth-api-tester.py example-api-spec.json --base-url https://api.example.com
```

### 2. Comprehensive Scan
Run all tests with increased verbosity:
```bash
python unauth-api-tester.py api-spec.json --base-url https://api.example.com --test-all -vv
```

### 3. Export Results
Generate an HTML report:
```bash
python unauth-api-tester.py api-spec.json --base-url https://api.example.com --test-all --output report.html --format html
```

## Common Use Cases

### Testing with Burp Suite
```bash
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --proxy http://127.0.0.1:8080 \
  --test-all
```

### Fast Scan (Multiple Threads)
```bash
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --threads 10 \
  --delay 0.1 \
  --test-all
```

### Quiet Mode (Only Show Vulnerabilities)
```bash
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --test-all \
  -q
```

### Testing with Custom Headers
Create a `headers.txt` file:
```
Authorization: Bearer your-token-here
X-API-Key: your-api-key
```

Then run:
```bash
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --custom-headers headers.txt \
  --test-headers
```

### Exclude Certain Endpoints
```bash
python unauth-api-tester.py api-spec.json \
  --base-url https://api.example.com \
  --exclude "/health" \
  --exclude "/metrics" \
  --test-all
```

## Understanding Output

### Color Coding
- 🟢 **Green (✓)**: Endpoint is properly secured (401, 403 response)
- 🔴 **Red (✗)**: Potential vulnerability detected (200, 201, etc. without auth)

### Verbosity Levels
- Default: Shows all tests with basic info
- `-v`: Adds response time, content type, length
- `-vv`: Adds response preview
- `-q`: Only shows vulnerabilities

### Summary Section
At the end, you'll see:
```
Total Tests:          45
Vulnerabilities:      3
Secure Endpoints:     42
Errors:               0
Duration:             2.34s
```

## Exit Codes
- `0`: No vulnerabilities found
- `1`: Vulnerabilities detected (useful for CI/CD)

## Example: Testing the Included Sample

```bash
# Test the example API spec (will fail since the URL is not real)
python unauth-api-tester.py example-api-spec.json

# The spec includes a server URL, so --base-url is optional
# To test against a real API, override with --base-url:
python unauth-api-tester.py example-api-spec.json --base-url https://your-real-api.com
```

## Tips

1. **Start Simple**: Begin with basic test, then add `--test-all`
2. **Use Proxy**: Route through Burp Suite for deeper analysis
3. **Increase Verbosity**: Use `-vv` to understand false positives
4. **Export Reports**: Generate HTML reports for documentation
5. **Rate Limit**: Use `--delay` to avoid overwhelming the server
6. **CI/CD**: Check exit code for automated security testing

## Getting Help

```bash
python unauth-api-tester.py --help
```

For full documentation, see [README.md](README.md)
