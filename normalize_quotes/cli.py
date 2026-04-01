"""
CLI entry point for normalize-quotes.

Usage:
    normalize_quotes <file>
    normalize_quotes <directory>
"""

import argparse
import logging
import sys
from pathlib import Path

logger = logging.getLogger(__name__)

# Smart/curly quote replacements
REPLACEMENTS = [
    ("\u2018", "'"),   # left single quotation mark
    ("\u2019", "'"),   # right single quotation mark
    ("\u201c", '"'),   # left double quotation mark
    ("\u201d", '"'),   # right double quotation mark
    ("\u2026", "..."), # horizontal ellipsis
]


def normalize_file(file_path: Path) -> bool:
    """Normalize smart quotes in a single file. Returns True on success."""
    try:
        content = file_path.read_text(encoding="utf-8")
        updated = content
        for original, replacement in REPLACEMENTS:
            updated = updated.replace(original, replacement)

        if updated != content:
            file_path.write_text(updated, encoding="utf-8")
            logger.info("Normalized: %s", file_path)
        else:
            logger.info("No changes needed: %s", file_path)

        return True

    except OSError as exc:
        logger.error("Error reading/writing %s: %s", file_path, exc)
        return False
    except UnicodeDecodeError as exc:
        logger.error("Encoding error in %s: %s", file_path, exc)
        return False


def normalize_directory(directory_path: Path) -> None:
    """Normalize smart quotes in all .md and .txt files in a directory (non-recursive)."""
    target_files = list(directory_path.glob("*.md")) + list(directory_path.glob("*.txt"))

    if not target_files:
        logger.warning("No .md or .txt files found in '%s'.", directory_path)
        return

    logger.info("Found %d file(s). Processing...", len(target_files))

    success_count = sum(normalize_file(target_file) for target_file in target_files)
    logger.info(
        "Done: %d/%d file(s) processed successfully.",
        success_count,
        len(target_files),
    )


def build_arg_parser() -> argparse.ArgumentParser:
    """Return the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="normalize_quotes",
        description="Replace smart/curly quotes with straight ASCII equivalents.",
    )
    parser.add_argument(
        "path",
        help="File or directory to process. Directories scan for *.md and *.txt files.",
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        help="Logging verbosity (default: INFO).",
    )
    return parser


def main() -> None:
    """CLI entry point."""
    parser = build_arg_parser()
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level,
        format="%(levelname)s: %(message)s",
        stream=sys.stderr,
    )

    target = Path(args.path)

    if not target.exists():
        logger.error("'%s' does not exist.", target)
        sys.exit(1)

    if target.is_dir():
        normalize_directory(target)
    elif target.is_file():
        if not normalize_file(target):
            sys.exit(1)
    else:
        logger.error("'%s' is neither a file nor a directory.", target)
        sys.exit(1)
