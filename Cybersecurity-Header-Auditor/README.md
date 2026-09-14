# Cybersecurity Header Auditor

A lightweight, defensive security tool that checks a website's HTTP response headers against a practical baseline of security controls.

## Features

- Checks common security headers such as CSP, HSTS, X-Content-Type-Options, and Referrer-Policy
- Reports missing or weak configurations
- Supports JSON output for automation
- Includes unit tests
- Designed for authorized security assessments and defensive engineering

## Requirements

- Python 3.10+
- `requests`

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python -m security_header_auditor https://example.com
```

JSON output:

```bash
python -m security_header_auditor https://example.com --json
```

For a local module checkout:

```bash
PYTHONPATH=src python -m security_header_auditor https://example.com
```

## What it checks

| Header | Purpose |
|---|---|
| Content-Security-Policy | Helps reduce XSS and injection impact |
| Strict-Transport-Security | Enforces HTTPS in supporting browsers |
| X-Content-Type-Options | Reduces MIME-sniffing risks |
| Referrer-Policy | Controls referrer information leakage |
| Permissions-Policy | Restricts browser capabilities |
| X-Frame-Options | Helps reduce clickjacking risk |

A missing header is not automatically a vulnerability in every application. Review findings in the context of the application's architecture.

## Ethics

Use this tool only against systems you own or have explicit permission to assess. It is intended for defensive security testing, configuration review, and learning.

## Project structure

```text
Cybersecurity-Header-Auditor/
├── .github/workflows/tests.yml
├── src/security_header_auditor/
│   ├── __init__.py
│   ├── __main__.py
│   └── auditor.py
├── tests/
│   └── test_auditor.py
├── .gitignore
├── LICENSE
├── requirements.txt
└── README.md
```

## Roadmap

- Add configurable organization security baselines
- Add HTML reporting
- Add severity scoring
- Add support for security-header policy exceptions
