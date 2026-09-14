from security_header_auditor.auditor import audit_headers


def test_complete_baseline_scores_100():
    headers = {
        "Content-Security-Policy": "default-src 'self'",
        "Strict-Transport-Security": "max-age=31536000",
        "X-Content-Type-Options": "nosniff",
        "Referrer-Policy": "strict-origin-when-cross-origin",
        "Permissions-Policy": "camera=(), microphone=()",
        "X-Frame-Options": "DENY",
    }

    result = audit_headers(headers)

    assert result["score"] == 100
    assert result["findings"] == []


def test_missing_headers_reduce_score():
    result = audit_headers({"X-Content-Type-Options": "nosniff"})

    assert result["score"] < 100
    assert len(result["findings"]) == 5


def test_invalid_nosniff_value_is_flagged():
    result = audit_headers({"X-Content-Type-Options": "text/html"})

    assert any(
        finding["header"] == "X-Content-Type-Options"
        and finding["severity"] == "high"
        for finding in result["findings"]
    )
