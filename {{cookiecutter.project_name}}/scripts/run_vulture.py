#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


def main():
    # Files that are part of this commit (passed by pre-commit)
    # We resolve them to absolute paths for comparison
    try:
        staged_files = {Path(f).resolve() for f in sys.argv[1:]}
    except OSError:
        # Handle cases where files might be deleted or paths are invalid
        staged_files = {Path(f).absolute() for f in sys.argv[1:]}

    if not staged_files:
        return 0

    # Run vulture on the whole project
    # We rely on pyproject.toml to configure paths/excludes for vulture.
    # We ignore the exit code because we will parse the output ourselves.
    try:
        result = subprocess.run(
            [sys.executable, "-m", "vulture"], capture_output=True, text=True
        )  # noqa: S603
    except FileNotFoundError:
        print("Error: 'vulture' command not found. Ensure it is installed.")
        return 1

    output_lines = result.stdout.splitlines()
    exit_code = 0
    project_root = Path.cwd().resolve()

    for line in output_lines:
        # Vulture output format usually is: src/file.py:10: unused function 'foo'
        parts = line.split(":", 1)
        if len(parts) < 2:
            continue

        rel_path = parts[0]
        try:
            # Resolve the path reported by vulture to absolute path
            abs_path = (project_root / rel_path).resolve()

            # Only print and fail if the reported file is in our staged files
            if abs_path in staged_files:
                print(line)
                exit_code = 1
        except Exception:  # noqa: S112
            # If path resolution fails, we ignore the line (safe default)
            continue

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
