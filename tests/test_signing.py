from xiaohongshu_ecommerce.signing import build_signature


def test_build_signature_matches_java_algorithm():
    signature = build_signature(
        method="oauth.getAccessToken",
        app_id="test-app",
        timestamp="1700000000",
        version="1.0",
        app_secret="secret-key",
    )

    # Expected value computed with the Java algorithm: md5(method?sortedParams+secret)
    assert signature == "15dd91e56a77df52c8a652a43a7c131e"
