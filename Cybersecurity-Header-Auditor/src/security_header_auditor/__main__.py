import argparse
import json

from .auditor import audit_url


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit HTTP security headers on an authorized website."
    )
    parser.add_argument("url", help="HTTPS URL to audit")
    parser.add_argument("--timeout", type=float, default=10.0)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()

    result = audit_url(args.url, timeout=args.timeout)

    if args.as_json:
        print(json.dumps(result, indent=2))
        return

    print(f"URL: {result['url']}")
    print(f"Status: {result['status_code']}")
    print(f"Final URL: {result['final_url']}")
    print(f"Score: {result['score']}/100")
    print("\nFindings:")
    for finding in result["findings"]:
        print(
            f"- [{finding['severity'].upper()}] "
            f"{finding['header']}: {finding['message']}"
        )


if __name__ == "__main__":
    main()
