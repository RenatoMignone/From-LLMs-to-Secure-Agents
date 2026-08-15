"""Fetch and convert remote URLs or local documents to clean, token-efficient Markdown."""

from __future__ import annotations

import argparse
import sys
import tempfile
import urllib.request
from pathlib import Path
from typing import Sequence


def fetch_url(url: str, user_agent: str = "Mozilla/5.0") -> bytes:
    request = urllib.request.Request(
        url,
        headers={"User-Agent": user_agent, "Accept": "text/html,application/xhtml+xml,application/xml,text/plain,*/*"},
    )
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read()


def convert_to_markdown(data: bytes, suffix: str = ".html") -> str:
    try:
        from markitdown import MarkItDown  # type: ignore

        md = MarkItDown()
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as temporary:
            temporary.write(data)
            temp_path = temporary.name

        try:
            result = md.convert(temp_path)
            return result.text_content or ""
        finally:
            Path(temp_path).unlink(missing_ok=True)
    except ImportError:
        import re

        text = data.decode("utf-8", errors="replace")
        text = re.sub(r"<style[\s\S]*?</style>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"<script[\s\S]*?</script>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"<head[\s\S]*?</head>", "", text, flags=re.IGNORECASE)
        text = re.sub(r"<[^>]+>", "\n", text)
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return "\n\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python3 scripts/main.py fetch",
        description="Fetch and convert web pages or documents to clean Markdown for token-efficient agent ingestion.",
    )
    parser.add_argument("source", help="URL or path to local document (HTML, PDF, etc.)")
    parser.add_argument("-o", "--output", help="Output file path (e.g. /tmp/source.md). If omitted, prints to stdout.")
    parser.add_argument("--grep", help="Optional regex filter to extract only matching lines or paragraphs.")
    args = parser.parse_args(argv)

    if args.source.startswith("http://") or args.source.startswith("https://"):
        try:
            data = fetch_url(args.source)
        except Exception as error:
            sys.stderr.write(f"Error fetching URL {args.source}: {error}\n")
            return 1
        suffix = ".html"
        if args.source.lower().endswith(".pdf"):
            suffix = ".pdf"
    else:
        path = Path(args.source)
        if not path.is_file():
            sys.stderr.write(f"Error: file not found: {args.source}\n")
            return 1
        data = path.read_bytes()
        suffix = path.suffix or ".html"

    markdown_text = convert_to_markdown(data, suffix=suffix)

    if args.grep:
        import re

        pattern = re.compile(args.grep, re.IGNORECASE)
        paragraphs = markdown_text.split("\n\n")
        matched = [p for p in paragraphs if pattern.search(p)]
        markdown_text = "\n\n".join(matched) if matched else "No matching sections found."

    if args.output:
        out_path = Path(args.output)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown_text, encoding="utf-8")
        print(f"Saved {len(markdown_text.split())} words ({len(markdown_text)} bytes) to {args.output}")
    else:
        print(markdown_text)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
