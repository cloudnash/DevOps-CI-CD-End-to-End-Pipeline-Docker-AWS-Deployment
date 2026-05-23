"""
health_check.py — Application Health Checker (Python)
Usage: python scripts/health_check.py --url http://localhost:5000 --verbose
"""

import argparse
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime


def check_endpoint(url: str, timeout: int = 5) -> dict:
    """Check a single endpoint and return status info."""
    result = {
        "url": url,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "status": "unknown",
        "http_code": None,
        "response_time_ms": None,
        "body": None,
        "error": None
    }

    start = datetime.now()
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "DevOps-HealthChecker/1.0"})
        with urllib.request.urlopen(req, timeout=timeout) as response:
            end = datetime.now()
            result["http_code"] = response.status
            result["response_time_ms"] = round((end - start).total_seconds() * 1000, 2)
            result["body"] = json.loads(response.read().decode())
            result["status"] = "healthy" if response.status == 200 else "degraded"
    except urllib.error.HTTPError as e:
        result["http_code"] = e.code
        result["status"] = "unhealthy"
        result["error"] = str(e)
    except Exception as e:
        result["status"] = "unreachable"
        result["error"] = str(e)

    return result


def run_checks(base_url: str, verbose: bool = False) -> bool:
    """Run health checks on all key endpoints."""
    endpoints = ["/health", "/", "/info"]
    all_healthy = True

    print(f"\n{'='*55}")
    print(f"  🔍 Health Check Report — {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
    print(f"  Base URL: {base_url}")
    print(f"{'='*55}\n")

    for path in endpoints:
        url = base_url.rstrip("/") + path
        result = check_endpoint(url)

        icon = "✅" if result["status"] == "healthy" else "❌"
        print(f"  {icon} {path:<12} → {result['status'].upper():<12} "
              f"[HTTP {result['http_code'] or 'N/A'}] "
              f"{result['response_time_ms'] or '--'}ms")

        if verbose and result["body"]:
            print(f"      Response: {json.dumps(result['body'], indent=6)}\n")

        if result["status"] not in ("healthy",):
            all_healthy = False
            if result["error"]:
                print(f"      Error: {result['error']}")

    print(f"\n{'='*55}")
    if all_healthy:
        print("  ✅ All checks passed. Application is healthy.")
    else:
        print("  ❌ Some checks failed. Review the results above.")
    print(f"{'='*55}\n")

    return all_healthy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DevOps Showcase — Health Checker")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of the application")
    parser.add_argument("--verbose", action="store_true", help="Print full response bodies")
    args = parser.parse_args()

    success = run_checks(args.url, verbose=args.verbose)
    sys.exit(0 if success else 1)
