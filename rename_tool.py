#!/usr/bin/env python3

import os
import argparse
import re
import sys
import platform

def convert_windows_path_to_wsl(path):
    """Convert Windows path to WSL path."""
    if platform.system() == "Linux" and ':' in path:
        # Remove any quotes
        path = path.strip('"')
        # Split drive letter and rest of the path
        drive, rest = path.split(':', 1)
        # Convert backslashes to forward slashes
        rest = rest.replace('\\', '/')
        # Ensure path starts with /
        if not rest.startswith('/'):
            rest = '/' + rest
        # Construct WSL path
        return f"/mnt/{drive.lower()}{rest}"
    return path

def rename_files(directory, operation, files_filter=None, dry_run=False):
    """Rename files in the specified directory based on the selected operation."""
    try:
        # Convert Windows path to WSL path if necessary
        directory = convert_windows_path_to_wsl(directory)
        print(f"Processing directory: {directory}")  # Debug print
        
        files = os.listdir(directory)
        if not files:
            print("No files found.")
            return

        # Filter files if a filter is provided
        if files_filter:
            pattern = files_filter.replace('*', '.*')
            files = [f for f in files if re.match(pattern, f)]

        for filename in files:
            old_path = os.path.join(directory, filename)

            if os.path.isfile(old_path):
                new_filename = filename
                # Apply the selected operation
                if operation == 'replace_spaces':
                    new_filename = filename.replace(' ', '_')
                elif operation == 'lowercase':
                    new_filename = filename.lower()
                elif operation == 'uppercase':
                    new_filename = filename.upper()
                elif operation == 'add_prefix':
                    prefix = input("Enter the prefix to add: ").strip()
                    new_filename = prefix + filename
                elif operation == 'add_suffix':
                    suffix = input("Enter the suffix to add: ").strip()
                    name, ext = os.path.splitext(filename)
                    new_filename = name + suffix + ext
                elif operation == 'change_extension':
                    new_ext = input("Enter the new extension (include the dot): ").strip()
                    if not new_ext.startswith('.'):
                        new_ext = '.' + new_ext
                    name, _ = os.path.splitext(filename)
                    new_filename = name + new_ext
                elif operation == 'remove_text':
                    text_to_remove = input("Enter the text to remove: ").strip()
                    new_filename = filename.replace(text_to_remove, '')
                else:
                    print(f"Unknown operation: {operation}")
                    sys.exit(1)

                new_path = os.path.join(directory, new_filename)

                if new_filename != filename:
                    if dry_run:
                        print(f"Will rename: {filename} -> {new_filename}")
                    else:
                        os.rename(old_path, new_path)
                        print(f"Renamed: {filename} -> {new_filename}")
                else:
                    print(f"Skipped (no change): {filename}")
        print("Renaming completed.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_operations():
    """List available operations."""
    print("Available operations:")
    print("  replace_spaces   - Replace spaces in filenames with underscores")
    print("  lowercase        - Convert filenames to lowercase")
    print("  uppercase        - Convert filenames to uppercase")
    print("  add_prefix       - Add a prefix to filenames")
    print("  add_suffix       - Add a suffix to filenames")
    print("  change_extension - Change the file extension")
    print("  remove_text      - Remove specific text from filenames")

def main():
    parser = argparse.ArgumentParser(
        description="Bulk rename files using preset operations.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-d', '--directory', required=True, help='Directory containing files to rename.')
    parser.add_argument('-o', '--operation', required=False, help='Rename operation to perform.')
    parser.add_argument('--filter', required=False, help='Only rename files matching this pattern (e.g., "*.txt").')
    parser.add_argument('--list', action='store_true', help='List available operations.')
    parser.add_argument('--dry-run', action='store_true', help="Show what would be renamed without making changes.")

    args = parser.parse_args()

    if args.list:
        list_operations()
        sys.exit(0)

    if not args.operation:
        print("Please specify an operation. Use --list to see available operations.")
        sys.exit(1)

    rename_files(args.directory, args.operation, args.filter, args.dry_run)

if __name__ == "__main__":
    main()

