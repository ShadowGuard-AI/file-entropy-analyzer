![Banner](banner.png)

# file-entropy-analyzer
Calculates and displays the entropy of a file, highlighting potentially compressed or encrypted data. - Focused on File operations and analysis

## Install
`git clone https://github.com/ShadowStrikeHQ/file-entropy-analyzer`

## Usage
`python3 main.py <file_path>`

A missing path, a path that is not a regular file, and an empty file are errors: the tool logs an error and exits 1 with no entropy verdict. A completed analysis of a non-empty regular file exits 0.

## Parameters
- `file_path`: The path to the file to analyze (required, positional)
- `-h`: Show help message and exit

## License
Copyright (c) ShadowStrikeHQ
