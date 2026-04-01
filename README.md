# normalize-quotes

A zero-dependency CLI tool that replaces smart/curly quotes and ellipses with plain ASCII equivalents — in a single file or an entire directory of Markdown files.

## When Curly Quotes Break Everything

Smart quotes (`“` `”` `‘` `’`) and fancy ellipses (`…`) sneak into Markdown and text files from word processors, CMS exports, and copy-pasted content. They cause subtle bugs in parsers, static site generators, linters, and anywhere that expects plain ASCII punctuation. Hunting them down manually is tedious and easy to miss.

## Straight Quotes, Automatically

`normalize_quotes` scans a file or every `.md` file in a directory and replaces all curly/smart punctuation with their ASCII equivalents in place — no configuration, no dependencies beyond the Python standard library.

| Smart character | Replaced with |
|---|---|
| `‘` `’` (curly single quotes) | `'` |
| `“` `”` (curly double quotes) | `"` |
| `…` (ellipsis) | `...` |

Files that don't need changes are left untouched.

## Example

```
# Before
“It’s a ‘great’ day…” said the README.

# After
"It's a 'great' day..." said the README.
```

## Installation

```bash
git clone https://github.com/your-username/normalize-quotes.git
cd normalize-quotes
pip install -e .
```

After install, the `normalize_quotes` command is available system-wide (or within your active virtual environment).

## Usage

```bash
# Normalize a single file
normalize_quotes path/to/file.md

# Normalize all .md files in a directory
normalize_quotes path/to/docs/

# Adjust log verbosity
normalize_quotes path/to/docs/ --log-level DEBUG
```

### Options

```
positional arguments:
  path                  File or directory to process.

options:
  --log-level {DEBUG,INFO,WARNING,ERROR}
                        Logging verbosity (default: INFO).
  -h, --help            Show this help message and exit.
```

## Requirements

- Python 3.11+
- No third-party dependencies

<br>
