# Namemate

## Task
A CLI tool for bulk renaming files with preset operations. Supports various renaming patterns like replacing spaces, changing case, adding prefixes/suffixes, and changing extensions.

## Spec
- Replace spaces with underscores
- Convert filenames to lowercase/uppercase
- Add prefix/suffix to filenames
- Change file extensions
- Remove specific text from filenames
- Cross-platform (Windows/Linux/WSL)
- Handles duplicates
- Dry-run mode for previewing changes
- File filtering support

## Plan

1. Install Dependencies
```bash
pip install argparse
```

2. Usage
```bash
# List available operations
python rename_tool.py --list

# Replace spaces with underscores
python rename_tool.py -d "/path/to/files" -o replace_spaces

# Convert to lowercase
python rename_tool.py -d "/path/to/files" -o lowercase

# Add prefix (will prompt for prefix)
python rename_tool.py -d "/path/to/files" -o add_prefix

# Change extension (will prompt for new extension)
python rename_tool.py -d "/path/to/files" -o change_extension

# Filter specific files
python rename_tool.py -d "/path/to/files" -o lowercase --filter "*.txt"

# Preview changes without renaming
python rename_tool.py -d "/path/to/files" -o lowercase --dry-run
```

## Code

Key Components:
- Path conversion for cross-platform compatibility
- Preset renaming operations
- File filtering
- Interactive prompts for customization
- Dry-run mode for safety

Operations:
- replace_spaces: Replace spaces with underscores
- lowercase: Convert filenames to lowercase
- uppercase: Convert filenames to uppercase
- add_prefix: Add a prefix to filenames
- add_suffix: Add a suffix to filenames
- change_extension: Change the file extension
- remove_text: Remove specific text from filenames

Dependencies:
- argparse: Command-line argument parsing
- os: File operations
- re: Regular expressions
- platform: System detection for path handling

---

Feel free to contribute to the project or suggest improvements!
