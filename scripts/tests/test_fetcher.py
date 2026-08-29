try:
    from fetch.fetcher import fallback_html_to_text
except ImportError:
    from scripts.fetch.fetcher import fallback_html_to_text


def test_fallback_ignores_non_content_elements_and_irregular_end_tags() -> None:
    html = b"""
    <html>
      <head><title>Hidden title</title></head>
      <body>
        <h1>Readable heading</h1>
        <script>alert('not content')</script >
        <style>.hidden { display: none; }</style >
        <p>Readable &amp; decoded text.</p>
      </body>
    </html>
    """

    result = fallback_html_to_text(html)

    assert "Readable heading" in result
    assert "Readable & decoded text." in result
    assert "Hidden title" not in result
    assert "alert" not in result
    assert "display: none" not in result
