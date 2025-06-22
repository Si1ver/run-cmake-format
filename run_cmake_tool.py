# This script runs cmake tools like cmake-format and cmake-lint.

import argparse
import os
import shutil
import subprocess
import sys

def get_cmake_files(start_path):
    cmake_files = []
    for root, _, files in os.walk(start_path):
        if "CMakeLists.txt" in files:
            cmake_files.append(os.path.join(root, "CMakeLists.txt"))
    return cmake_files

def print_process_output(result):
    if result.stdout:
        print(f"Stdout:\n{result.stdout.strip()}")
    if result.stderr:
        print(f"Stderr:\n{result.stderr.strip()}")

def check_files_formatted(cmake_files):
    print(f"Found {len(cmake_files)} CMakeLists.txt files. Checking files are formatted...")
    print("No changes will be applied. Use --apply to write changes.")

    not_formatted = False

    for file_path in cmake_files:
        print(f"Processing: {file_path}")
        try:
            result = subprocess.run(
                ["cmake-format", "--check", file_path],
                check=False,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                not_formatted = True
                print(f"File {file_path} is not formatted correctly.")
            else:
                print(f"File {file_path} is formatted correctly.")
            print_process_output(result)
        except Exception as e:
            not_formatted = True
            print(f"An exception occurred while checking {file_path}: {e}")

    return not_formatted

def format_cmake_files(cmake_files):
    print(f"Found {len(cmake_files)} CMakeLists.txt files. Formatting files...")

    have_errors = False

    for file_path in cmake_files:
        print(f"Formatting: {file_path}")
        try:
            result = subprocess.run(
                ["cmake-format", file_path, "-o", file_path],
                check=False,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                have_errors = True
                print(f"Error: Command failed for {file_path}")
                print(f"Exit code: {result.returncode}")
            else:
                print(f"Success: {file_path}")
            print_process_output(result)
        except Exception as e:
            have_errors = True
            print(f"An exception occurred while formatting {file_path}: {e}")

    return have_errors

def lint_cmake_files(cmake_files, log_level):
    print(f"Found {len(cmake_files)} CMakeLists.txt files. Linting files with log level: {log_level}")

    have_errors = False

    for file_path in cmake_files:
        print(f"Linting: {file_path}")
        try:
            result = subprocess.run(
                ["cmake-lint", "--log-level", log_level, file_path],
                check=False,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                have_errors = True
                print(f"Error: Command failed for {file_path}")
                print(f"Exit code: {result.returncode}")
            else:
                print(f"Success: {file_path}")
            print_process_output(result)
        except Exception as e:
            have_errors = True
            print(f"An exception occurred while linting {file_path}: {e}")

    return have_errors

def run_cmake_format(args):
    start_path = args.path
    print(f"Starting cmake-format in directory: {start_path}")

    if not os.path.isdir(start_path):
        print(f"Error: The path '{start_path}' is not a valid directory.")
        return 1

    if not shutil.which("cmake-format"):
        print("Error: cmake-format is not installed or not found in PATH.")
        return 1

    cmake_files = get_cmake_files(start_path)
    if not cmake_files:
        print(f"Error: No CMakeLists.txt files found in {start_path}.")
        return 1

    result = subprocess.run(
        ["cmake-format", "--version"],
        check=False,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error: Failed to get cmake-format version: {result.stderr.strip()}")
        return 1
    else:
        print(f"cmake-format version: {result.stdout.strip()}")

    if (args.apply):
        have_errors = format_cmake_files(cmake_files)
        if have_errors:
            print("Error: Some files could not be formatted correctly.")
            return 1
        else:
            print("All files formatted successfully.")
    else:
        not_formatted = check_files_formatted(cmake_files)
        if not_formatted:
            print("Error: Some files are not formatted correctly. Use --apply to write changes.")
            return 1
        else:
            print("All files are formatted correctly.")

    return 0

def run_cmake_lint(args):
    start_path = args.path
    log_level = args.log_level
    print(f"Starting cmake-lint in directory: {start_path}")

    if not os.path.isdir(start_path):
        print(f"Error: The path '{start_path}' is not a valid directory.")
        return 1

    if not shutil.which("cmake-lint"):
        print("Error: cmake-lint is not installed or not found in PATH.")
        return 1

    cmake_files = get_cmake_files(start_path)
    if not cmake_files:
        print(f"Error: No CMakeLists.txt files found in {start_path}.")
        return 1

    result = subprocess.run(
        ["cmake-lint", "--version"],
        check=False,
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        print(f"Error: Failed to get cmake-lint version: {result.stderr.strip()}")
        return 1
    else:
        print(f"cmake-lint version: {result.stdout.strip()}")

    have_errors = lint_cmake_files(cmake_files, log_level)
    if have_errors:
        print("Error: Some files could not be linted correctly.")
        return 1
    else:
        print("All files are linted successfully.")

    return 0

def main():
    print("Run CMake Tool Script")

    parser = argparse.ArgumentParser(
                        prog='run_cmake_tool',
                        description='This script runs cmake tools like cmake-format and cmake-lint.')

    subparsers = parser.add_subparsers(title="subcommands", dest="command", required=True)

    format_parser = subparsers.add_parser('format', help="Format CMakeLists.txt files or check if they are formatted")
    format_parser.add_argument("path", help="Starting directory path")
    format_parser.add_argument('--apply', required=False, help="Write changes to files", action='store_true')
    format_parser.set_defaults(func=run_cmake_format)

    lint_parser = subparsers.add_parser('lint', help="Lint CMakeLists.txt files")
    lint_parser.add_argument("path", help="Starting directory path")
    lint_parser.add_argument('--log-level', required=False, help="Set the log level for cmake-lint", choices=['error', 'warning', 'info', 'debug'], default='warning')
    lint_parser.set_defaults(func=run_cmake_lint)

    args = parser.parse_args()
    exit_code = args.func(args)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
