from __future__ import annotations

from typing import Any
from urllib.parse import urlparse

import requests


HEADER_RULES = {
    "Content-Security-Policy": {
        "weight": 25,
        "message": "Define a restrictive Content-Security-Policy appropriate for the application.",
    },
    "Strict-Transport-Security": {
        "weight": 20,
        "message": "Enable HSTS when the site is intended to be HTTPS-only.",
    },
    "X-Content-Type-Options": {
        "weight": 15,
        "message": "Set X-Content-Type-Options to nosniff.",
    },
    "Referrer-Policy": {
        "weight": 15,
        "message": "Define an explicit Referrer-Policy.",
    },
    "Permissions-Policy": {
        "weight": 15,
        "message": "Restrict browser features with an appropriate Permissions-Policy.",
    },
    "X-Frame-Options": {
        "weight": 10,
        "message": "Set X-Frame-Options unless framing is intentionally required.",
    },
}


def _validate_url(url: str) -> None:
    parsed = urlparse(url)
    if parsed.scheme != "https" or not parsed.netloc:
        raise ValueError("Only valid HTTPS URLs are accepted.")


def audit_headers(headers: dict[str, str]) -> dict[str, Any]:
    normalized = {k.lower(): v for k, v in headers.items()}
    findings = []
    score = 100

    for header, rule in HEADER_RULES.items():
        value = normalized.get(header.lower())

        if not value:
            score -= rule["weight"]
            findings.append(
                {
                    "header": header,
                    "severity": "medium",
                    "message": rule["message"],
                }
            )
            continue

        if header == "X-Content-Type-Options" and value.lower() != "nosniff":
            score -= rule["weight"]
            findings.append(
                {
                    "header": header,
                    "severity": "high",
                    "message": "The value should normally be 'nosniff'.",
                }
            )

        if header == "Strict-Transport-Security" and "max-age=" not in value.lower():
            score -= rule["weight"]
            findings.append(
                {
                    "header": header,
                    "severity": "high",
                    "message": "HSTS should include an explicit max-age directive.",
                }
            )

    return {"score": max(score, 0), "findings": findings}


def audit_url(url: str, timeout: float = 10.0) -> dict[str, Any]:
    _validate_url(url)

    response = requests.get(
        url,
        timeout=timeout,
        allow_redirects=True,
        headers={"User-Agent": "Cybersecurity-Header-Auditor/1.0"},
    )

    analysis = audit_headers(dict(response.headers))

    return {
        "url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        **analysis,
    }
