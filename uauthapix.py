#!/usr/bin/env python3
"""
UauthAPIX - Advanced API Security Testing Tool
Test API endpoints for authentication bypass vulnerabilities
"""
import requests
import json
import urllib3
import argparse
import re
import random
import string
import time
import sys
from typing import Dict, List, Set, Optional, Any
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import csv

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ANSI Color codes
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

    @staticmethod
    def disable():
        Colors.RED = ''
        Colors.GREEN = ''
        Colors.YELLOW = ''
        Colors.BLUE = ''
        Colors.MAGENTA = ''
        Colors.CYAN = ''
        Colors.WHITE = ''
        Colors.BOLD = ''
        Colors.RESET = ''


@dataclass
class TestResult:
    method: str
    url: str
    status_code: int
    response_time: float
    response_length: int
    content_type: str
    is_vulnerable: bool
    technique: str = ""
    response_preview: str = ""
    headers: Dict[str, str] = field(default_factory=dict)


@dataclass
class TestStats:
    total_tests: int = 0
    vulnerabilities_found: int = 0
    errors: int = 0
    secure_endpoints: int = 0
    results: List[TestResult] = field(default_factory=list)


# Bypass headers to test
BYPASS_HEADERS = [
    {"X-Original-URL": "/"},
    {"X-Rewrite-URL": "/"},
    {"X-Forwarded-For": "127.0.0.1"},
    {"X-Forwarded-Host": "127.0.0.1"},
    {"X-Remote-IP": "127.0.0.1"},
    {"X-Remote-Addr": "127.0.0.1"},
    {"X-Originating-IP": "127.0.0.1"},
    {"X-Client-IP": "127.0.0.1"},
    {"X-Real-IP": "127.0.0.1"},
    {"X-Custom-IP-Authorization": "127.0.0.1"},
    {"X-ProxyUser-Ip": "127.0.0.1"},
    {"X-Host": "127.0.0.1"},
    {"Forwarded": "for=127.0.0.1;by=127.0.0.1;host=127.0.0.1"},
]

# Alternative HTTP methods to test
ALTERNATIVE_METHODS = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS', 'TRACE']


def random_string(length=8):
    """Generate a random alphanumeric string"""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


def substitute_params(path):
    """Replace path parameters with random values"""
    # Replace {param} style parameters
    path = re.sub(r"\{[^}]+\}", lambda match: random_string(), path)
    # Replace :param style parameters
    path = re.sub(r":([a-zA-Z_][a-zA-Z0-9_]*)", lambda match: random_string(), path)
    return path


def print_banner():
    """Print tool banner"""
    banner = f"""{Colors.CYAN}{Colors.BOLD}
██╗   ██╗ █████╗ ██╗   ██╗████████╗██╗  ██╗ █████╗ ██████╗ ██╗██╗  ██╗
██║   ██║██╔══██╗██║   ██║╚══██╔══╝██║  ██║██╔══██╗██╔══██╗██║╚██╗██╔╝
██║   ██║███████║██║   ██║   ██║   ███████║███████║██████╔╝██║ ╚███╔╝
██║   ██║██╔══██║██║   ██║   ██║   ██╔══██║██╔══██║██╔═══╝ ██║ ██╔██╗
╚██████╔╝██║  ██║╚██████╔╝   ██║   ██║  ██║██║  ██║██║     ██║██╔╝ ██╗
 ╚═════╝ ╚═╝  ╚═╝ ╚═════╝    ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝
{Colors.RESET}{Colors.WHITE}
        Advanced API Security Testing Tool v2.0
        Unauthorized Access Detection & Bypass Testing
{Colors.RESET}{Colors.CYAN}
══════════════════════════════════════════════════════════════════════
{Colors.RESET}
"""
    print(banner)


def is_vulnerable_response(status_code: int, content_type: str, response_text: str, response_length: int) -> bool:
    """
    Determine if a response indicates a vulnerability

    Returns True if the endpoint appears to be accessible without authentication
    """
    # Success status codes that indicate vulnerability
    SUCCESS_CODES = {200, 201, 202, 204, 206}

    # Status codes that indicate proper security
    SECURE_CODES = {401, 403, 405, 407}

    if status_code in SECURE_CODES:
        return False

    if status_code in SUCCESS_CODES:
        # Additional checks to avoid false positives

        # Ignore HTML responses (likely error pages)
        if 'text/html' in content_type.lower():
            return False

        # Check for common error messages in response
        error_indicators = [
            'unauthorized', 'not authorized', 'access denied',
            'forbidden', 'authentication required', 'login required',
            'invalid token', 'missing token', 'expired token',
            'permission denied', 'insufficient privileges'
        ]

        response_lower = response_text.lower()
        if any(indicator in response_lower for indicator in error_indicators):
            return False

        # Very small responses might be empty/error responses
        if response_length < 10 and status_code == 200:
            return False

        return True

    return False


def test_endpoint(method: str, url: str, headers: Dict[str, str],
                 timeout: int, verify_ssl: bool, proxy: Optional[Dict] = None,
                 technique: str = "direct") -> Optional[TestResult]:
    """Test a single endpoint and return results"""
    try:
        start_time = time.time()
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            verify=verify_ssl,
            timeout=timeout,
            proxies=proxy,
            allow_redirects=False
        )
        response_time = time.time() - start_time

        content_type = response.headers.get('Content-Type', '')
        response_length = len(response.content)
        response_preview = response.text[:200] if response.text else ""

        is_vuln = is_vulnerable_response(
            response.status_code,
            content_type,
            response.text,
            response_length
        )

        return TestResult(
            method=method,
            url=url,
            status_code=response.status_code,
            response_time=response_time,
            response_length=response_length,
            content_type=content_type,
            is_vulnerable=is_vuln,
            technique=technique,
            response_preview=response_preview,
            headers=dict(response.headers)
        )
    except requests.exceptions.Timeout:
        return None
    except requests.exceptions.RequestException as e:
        return None
    except Exception as e:
        return None


def print_result(result: TestResult, verbosity: int):
    """Print a test result with appropriate formatting"""
    if result.is_vulnerable:
        color = Colors.RED
        status = "VULNERABLE"
        symbol = "✗"
    else:
        color = Colors.GREEN
        status = "SECURE"
        symbol = "✓"

    if verbosity >= 1:
        technique_info = f" [{result.technique}]" if result.technique != "direct" else ""
        print(f"{color}{symbol} {result.method:7} {result.url} -> {result.status_code} ({status}){technique_info}{Colors.RESET}")

        if verbosity >= 2:
            print(f"  {Colors.CYAN}├─ Response Time: {result.response_time:.3f}s{Colors.RESET}")
            print(f"  {Colors.CYAN}├─ Content-Type: {result.content_type}{Colors.RESET}")
            print(f"  {Colors.CYAN}├─ Response Length: {result.response_length} bytes{Colors.RESET}")

            if verbosity >= 3 and result.response_preview:
                preview = result.response_preview.replace('\n', ' ')[:100]
                print(f"  {Colors.CYAN}└─ Preview: {preview}...{Colors.RESET}")
    elif result.is_vulnerable:
        # Always show vulnerabilities even in quiet mode
        technique_info = f" [{result.technique}]" if result.technique != "direct" else ""
        print(f"{color}{symbol} {result.method:7} {result.url} -> {result.status_code}{technique_info}{Colors.RESET}")


def test_with_variations(base_method: str, base_url: str, base_headers: Dict[str, str],
                        args, stats: TestStats) -> List[TestResult]:
    """Test an endpoint with various techniques"""
    results = []

    # 1. Direct test (original method)
    result = test_endpoint(base_method, base_url, base_headers, args.timeout,
                          args.verify_ssl, args.proxy, "direct")
    if result:
        stats.total_tests += 1
        results.append(result)
        if result.is_vulnerable:
            stats.vulnerabilities_found += 1
        else:
            stats.secure_endpoints += 1
        print_result(result, args.verbosity)

    # 2. Test with bypass headers
    if args.test_headers:
        for bypass_header in BYPASS_HEADERS:
            test_headers = {**base_headers, **bypass_header}
            header_name = list(bypass_header.keys())[0]
            result = test_endpoint(base_method, base_url, test_headers, args.timeout,
                                 args.verify_ssl, args.proxy, f"header:{header_name}")
            if result:
                stats.total_tests += 1
                results.append(result)
                if result.is_vulnerable:
                    stats.vulnerabilities_found += 1
                else:
                    stats.secure_endpoints += 1
                print_result(result, args.verbosity)

            if args.delay:
                time.sleep(args.delay)

    # 3. Test with trailing slash variations
    if args.test_paths:
        for path_variation in get_path_variations(base_url):
            result = test_endpoint(base_method, path_variation, base_headers, args.timeout,
                                 args.verify_ssl, args.proxy, "path-variation")
            if result:
                stats.total_tests += 1
                results.append(result)
                if result.is_vulnerable:
                    stats.vulnerabilities_found += 1
                else:
                    stats.secure_endpoints += 1
                print_result(result, args.verbosity)

            if args.delay:
                time.sleep(args.delay)

    # 4. Test alternative HTTP methods
    if args.test_methods:
        for alt_method in ALTERNATIVE_METHODS:
            if alt_method != base_method:
                result = test_endpoint(alt_method, base_url, base_headers, args.timeout,
                                     args.verify_ssl, args.proxy, f"method:{alt_method}")
                if result:
                    stats.total_tests += 1
                    results.append(result)
                    if result.is_vulnerable:
                        stats.vulnerabilities_found += 1
                    else:
                        stats.secure_endpoints += 1
                    print_result(result, args.verbosity)

                if args.delay:
                    time.sleep(args.delay)

    return results


def get_path_variations(url: str) -> List[str]:
    """Generate path variations for testing"""
    variations = []

    # Parse URL to get base and path
    if '://' in url:
        protocol, rest = url.split('://', 1)
        if '/' in rest:
            base, path = rest.split('/', 1)
            path = '/' + path
        else:
            return variations
    else:
        return variations

    base_url = f"{protocol}://{base}"

    # Trailing slash variations
    if path.endswith('/'):
        variations.append(f"{base_url}{path[:-1]}")  # Remove trailing slash
    else:
        variations.append(f"{base_url}{path}/")  # Add trailing slash

    # Path normalization tricks
    variations.append(f"{base_url}/{path}")  # Double slash
    variations.append(f"{base_url}{path}/..")  # Path traversal
    variations.append(f"{base_url}//{path.lstrip('/')}")  # Double slash at start

    return variations[:3]  # Limit variations to avoid too many requests


def print_summary(stats: TestStats, start_time: float):
    """Print test summary statistics"""
    duration = time.time() - start_time

    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.CYAN}Test Summary{Colors.RESET}")
    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")

    print(f"{Colors.WHITE}Total Tests:          {Colors.BOLD}{stats.total_tests}{Colors.RESET}")
    print(f"{Colors.RED}Vulnerabilities:      {Colors.BOLD}{stats.vulnerabilities_found}{Colors.RESET}")
    print(f"{Colors.GREEN}Secure Endpoints:     {Colors.BOLD}{stats.secure_endpoints}{Colors.RESET}")
    print(f"{Colors.YELLOW}Errors:               {Colors.BOLD}{stats.errors}{Colors.RESET}")
    print(f"{Colors.WHITE}Duration:             {Colors.BOLD}{duration:.2f}s{Colors.RESET}")

    if stats.vulnerabilities_found > 0:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠ WARNING: Found {stats.vulnerabilities_found} potentially vulnerable endpoint(s)!{Colors.RESET}")

        # Show vulnerable endpoints
        print(f"\n{Colors.RED}{Colors.BOLD}Vulnerable Endpoints:{Colors.RESET}")
        print(f"{Colors.RED}{'─'*70}{Colors.RESET}")

        vulnerable_results = [r for r in stats.results if r.is_vulnerable]
        for idx, result in enumerate(vulnerable_results, 1):
            technique_info = f" [{result.technique}]" if result.technique != "direct" else ""
            print(f"{Colors.RED}{idx:3}. {result.method:7} {result.url} -> {result.status_code}{technique_info}{Colors.RESET}")

        print(f"{Colors.RED}{'─'*70}{Colors.RESET}")
    else:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ No unauthorized access vulnerabilities detected{Colors.RESET}")

    print(f"{Colors.CYAN}{'='*70}{Colors.RESET}\n")


def export_results(stats: TestStats, output_file: str, output_format: str):
    """Export results to file"""
    if output_format == 'json':
        export_json(stats, output_file)
    elif output_format == 'csv':
        export_csv(stats, output_file)
    elif output_format == 'html':
        export_html(stats, output_file)


def export_json(stats: TestStats, output_file: str):
    """Export results to JSON"""
    data = {
        'summary': {
            'total_tests': stats.total_tests,
            'vulnerabilities_found': stats.vulnerabilities_found,
            'secure_endpoints': stats.secure_endpoints,
            'errors': stats.errors
        },
        'results': []
    }

    for result in stats.results:
        data['results'].append({
            'method': result.method,
            'url': result.url,
            'status_code': result.status_code,
            'response_time': result.response_time,
            'response_length': result.response_length,
            'content_type': result.content_type,
            'is_vulnerable': result.is_vulnerable,
            'technique': result.technique
        })

    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

    print(f"{Colors.GREEN}✓ Results exported to {output_file}{Colors.RESET}")


def export_csv(stats: TestStats, output_file: str):
    """Export results to CSV"""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Method', 'URL', 'Status Code', 'Response Time', 'Response Length',
                        'Content Type', 'Vulnerable', 'Technique'])

        for result in stats.results:
            writer.writerow([
                result.method,
                result.url,
                result.status_code,
                f"{result.response_time:.3f}",
                result.response_length,
                result.content_type,
                'Yes' if result.is_vulnerable else 'No',
                result.technique
            ])

    print(f"{Colors.GREEN}✓ Results exported to {output_file}{Colors.RESET}")


def export_html(stats: TestStats, output_file: str):
    """Export results to HTML"""
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>API Security Test Results</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        h1 {{ color: #333; }}
        .summary {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary-item {{ margin: 10px 0; }}
        table {{ width: 100%; border-collapse: collapse; background: white; }}
        th {{ background-color: #4CAF50; color: white; padding: 12px; text-align: left; }}
        td {{ padding: 12px; border-bottom: 1px solid #ddd; }}
        .vulnerable {{ background-color: #ffebee; }}
        .secure {{ background-color: #e8f5e9; }}
        .vuln-badge {{ background-color: #f44336; color: white; padding: 4px 8px; border-radius: 4px; }}
        .secure-badge {{ background-color: #4CAF50; color: white; padding: 4px 8px; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>API Security Test Results</h1>

    <div class="summary">
        <h2>Summary</h2>
        <div class="summary-item"><strong>Total Tests:</strong> {stats.total_tests}</div>
        <div class="summary-item"><strong>Vulnerabilities Found:</strong> {stats.vulnerabilities_found}</div>
        <div class="summary-item"><strong>Secure Endpoints:</strong> {stats.secure_endpoints}</div>
        <div class="summary-item"><strong>Errors:</strong> {stats.errors}</div>
    </div>

    <h2>Detailed Results</h2>
    <table>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Status</th>
            <th>Response Time</th>
            <th>Length</th>
            <th>Status</th>
            <th>Technique</th>
        </tr>
"""

    for result in stats.results:
        row_class = 'vulnerable' if result.is_vulnerable else 'secure'
        badge = f'<span class="vuln-badge">VULNERABLE</span>' if result.is_vulnerable else f'<span class="secure-badge">SECURE</span>'

        html += f"""        <tr class="{row_class}">
            <td>{result.method}</td>
            <td>{result.url}</td>
            <td>{result.status_code}</td>
            <td>{result.response_time:.3f}s</td>
            <td>{result.response_length} bytes</td>
            <td>{badge}</td>
            <td>{result.technique}</td>
        </tr>
"""

    html += """    </table>
</body>
</html>
"""

    with open(output_file, 'w') as f:
        f.write(html)

    print(f"{Colors.GREEN}✓ Results exported to {output_file}{Colors.RESET}")


def load_custom_headers(headers_file: str) -> Dict[str, str]:
    """Load custom headers from file"""
    headers = {}
    try:
        with open(headers_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if ':' in line:
                        key, value = line.split(':', 1)
                        headers[key.strip()] = value.strip()
    except Exception as e:
        print(f"{Colors.YELLOW}Warning: Could not load headers file: {e}{Colors.RESET}")

    return headers


def parse_openapi_spec(spec: Dict) -> Dict[str, List[str]]:
    """Parse OpenAPI specification and extract endpoints"""
    endpoints = {}

    # Handle OpenAPI 3.x and Swagger 2.0
    if 'paths' not in spec:
        print(f"{Colors.RED}Error: Invalid OpenAPI spec - missing 'paths' key{Colors.RESET}")
        sys.exit(1)

    paths = spec.get('paths', {})

    for path, methods in paths.items():
        if isinstance(methods, dict):
            endpoint_methods = []
            for method in methods.keys():
                if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                    endpoint_methods.append(method.upper())

            if endpoint_methods:
                endpoints[path] = endpoint_methods

    return endpoints


def get_base_url_from_spec(spec: Dict, provided_base_url: Optional[str]) -> str:
    """Extract base URL from OpenAPI spec or use provided URL"""
    if provided_base_url:
        return provided_base_url.rstrip('/')

    # OpenAPI 3.x
    if 'servers' in spec and spec['servers']:
        return spec['servers'][0]['url'].rstrip('/')

    # Swagger 2.0
    if 'host' in spec:
        scheme = spec.get('schemes', ['https'])[0]
        base_path = spec.get('basePath', '')
        return f"{scheme}://{spec['host']}{base_path}".rstrip('/')

    print(f"{Colors.RED}Error: Could not determine base URL from spec. Please provide --base-url{Colors.RESET}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Advanced API Security Testing Tool - Test for unauthorized access vulnerabilities",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s api-spec.json --base-url https://api.example.com
  %(prog)s api-spec.json --base-url https://api.example.com -v --test-all
  %(prog)s api-spec.json --base-url https://api.example.com --output results.json --format json
  %(prog)s api-spec.json --custom-headers headers.txt --threads 10 --delay 0.5
        """
    )

    # Required arguments
    parser.add_argument("spec_file", help="Path to OpenAPI/Swagger JSON file")
    parser.add_argument("--base-url", help="Base URL for the API (overrides spec)")

    # Testing options
    parser.add_argument("--test-headers", action="store_true",
                       help="Test with bypass headers (X-Forwarded-For, etc.)")
    parser.add_argument("--test-paths", action="store_true",
                       help="Test path variations (trailing slashes, normalization)")
    parser.add_argument("--test-methods", action="store_true",
                       help="Test alternative HTTP methods")
    parser.add_argument("--test-all", action="store_true",
                       help="Enable all testing techniques")

    # Performance options
    parser.add_argument("--threads", type=int, default=1,
                       help="Number of concurrent threads (default: 1)")
    parser.add_argument("--delay", type=float, default=0,
                       help="Delay between requests in seconds (default: 0)")
    parser.add_argument("--timeout", type=int, default=10,
                       help="Request timeout in seconds (default: 10)")

    # Output options
    parser.add_argument("-v", "--verbosity", action="count", default=1,
                       help="Increase output verbosity (-v, -vv, -vvv)")
    parser.add_argument("-q", "--quiet", action="store_true",
                       help="Quiet mode - only show vulnerabilities")
    parser.add_argument("--no-color", action="store_true",
                       help="Disable colored output")
    parser.add_argument("--output", "-o", help="Output file path")
    parser.add_argument("--format", choices=['json', 'csv', 'html'], default='json',
                       help="Output format (default: json)")

    # Configuration options
    parser.add_argument("--custom-headers", help="File containing custom headers (one per line: Header: Value)")
    parser.add_argument("--proxy", help="Proxy URL (e.g., http://127.0.0.1:8080)")
    parser.add_argument("--verify-ssl", action="store_true",
                       help="Verify SSL certificates (default: disabled)")
    parser.add_argument("--exclude", action="append", default=[],
                       help="Exclude paths matching pattern (can be used multiple times)")

    args = parser.parse_args()

    # Handle quiet mode
    if args.quiet:
        args.verbosity = 0

    # Handle test-all flag
    if args.test_all:
        args.test_headers = True
        args.test_paths = True
        args.test_methods = True

    # Disable colors if requested
    if args.no_color:
        Colors.disable()

    # Print banner
    print_banner()

    # Validate spec file
    if not Path(args.spec_file).exists():
        print(f"{Colors.RED}Error: Spec file '{args.spec_file}' not found{Colors.RESET}")
        sys.exit(1)

    # Load OpenAPI spec
    try:
        with open(args.spec_file, 'r') as f:
            spec = json.load(f)
    except json.JSONDecodeError as e:
        print(f"{Colors.RED}Error: Invalid JSON in spec file: {e}{Colors.RESET}")
        sys.exit(1)
    except Exception as e:
        print(f"{Colors.RED}Error loading spec file: {e}{Colors.RESET}")
        sys.exit(1)

    # Get base URL
    base_url = get_base_url_from_spec(spec, args.base_url)

    # Parse endpoints from spec
    endpoints = parse_openapi_spec(spec)

    if not endpoints:
        print(f"{Colors.YELLOW}Warning: No endpoints found in spec{Colors.RESET}")
        sys.exit(0)

    # Setup headers
    base_headers = {"Content-Type": "application/json"}
    if args.custom_headers:
        custom_headers = load_custom_headers(args.custom_headers)
        base_headers.update(custom_headers)

    # Setup proxy
    proxy = None
    if args.proxy:
        proxy = {
            'http': args.proxy,
            'https': args.proxy
        }
        print(f"{Colors.CYAN}Using proxy: {args.proxy}{Colors.RESET}")

    # Warn about SSL verification
    if not args.verify_ssl:
        print(f"{Colors.YELLOW}⚠ SSL verification is disabled{Colors.RESET}")

    # Print test configuration
    print(f"{Colors.CYAN}Base URL: {base_url}{Colors.RESET}")
    print(f"{Colors.CYAN}Endpoints: {len(endpoints)}{Colors.RESET}")
    print(f"{Colors.CYAN}Threads: {args.threads}{Colors.RESET}")

    techniques = []
    if args.test_headers:
        techniques.append("bypass headers")
    if args.test_paths:
        techniques.append("path variations")
    if args.test_methods:
        techniques.append("alternative methods")

    if techniques:
        print(f"{Colors.CYAN}Techniques: {', '.join(techniques)}{Colors.RESET}")

    print(f"\n{Colors.BOLD}Starting tests...{Colors.RESET}\n")

    # Initialize statistics
    stats = TestStats()
    start_time = time.time()

    # Process endpoints
    tasks = []
    for path, methods in endpoints.items():
        # Check exclusions
        if any(re.search(pattern, path) for pattern in args.exclude):
            if args.verbosity >= 2:
                print(f"{Colors.YELLOW}Skipping excluded path: {path}{Colors.RESET}")
            continue

        for method in methods:
            full_path = substitute_params(path)
            full_url = f"{base_url}{full_path}"
            tasks.append((method, full_url, base_headers.copy()))

    # Execute tests
    if args.threads > 1:
        # Concurrent execution
        with ThreadPoolExecutor(max_workers=args.threads) as executor:
            futures = []
            for method, url, headers in tasks:
                future = executor.submit(test_with_variations, method, url, headers, args, stats)
                futures.append(future)

                # Add delay between submissions if specified
                if args.delay:
                    time.sleep(args.delay)

            # Wait for completion
            for future in as_completed(futures):
                try:
                    results = future.result()
                    stats.results.extend(results)
                except Exception as e:
                    stats.errors += 1
    else:
        # Sequential execution
        for method, url, headers in tasks:
            try:
                results = test_with_variations(method, url, headers, args, stats)
                stats.results.extend(results)
            except Exception as e:
                stats.errors += 1

            if args.delay:
                time.sleep(args.delay)

    # Print summary
    print_summary(stats, start_time)

    # Export results if requested
    if args.output:
        export_results(stats, args.output, args.format)

    # Exit with error code if vulnerabilities found
    sys.exit(1 if stats.vulnerabilities_found > 0 else 0)


if __name__ == "__main__":
    main()
