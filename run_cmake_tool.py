# This script runs cmake tools like cmake-format and cmake-lint.

import argparse
import os
import shutil
import subprocess
import sys
from enum import Enum
from typing import Optional

# To avoid debugging issues with older Python versions, the script requires Python 3.12 or higher.
if sys.version_info < (3, 12):
    print("This script requires Python 3.12 or higher")
    sys.exit(1)

# The CMakeLists file name.
CMAKE_LIST_FILE_NAME: str = "CMakeLists.txt"


class ExitCodes(int, Enum):
    """
    Exit codes for the script.
    """

    SUCCESS = 0
    TOOL_NOT_FOUND = 11
    INVALID_ARGUMENTS = 12
    NO_CMAKE_FILES_FOUND = 13


def get_cmake_files(start_path: str) -> list[str]:
    """
    Recursively searches for all CMakeLists files starting from the given directory.

    Args:
        start_path (str): The root directory to begin the search.

    Returns:
        list[str]: A list of full file paths to each found CMakeLists file.
    """

    cmake_files: list[str] = []
    for root, _, files in os.walk(start_path):
        if CMAKE_LIST_FILE_NAME in files:
            cmake_files.append(os.path.join(root, CMAKE_LIST_FILE_NAME))
    return cmake_files


def print_process_output(result: subprocess.CompletedProcess[str]) -> None:
    """
    Prints the standard output and error from a subprocess run.
    Args:
        result (subprocess.CompletedProcess[str]): The result of the subprocess run.
    """

    stdout: Optional[str] = result.stdout
    if stdout:
        stdout = stdout.strip()
        if stdout:
            print(f"Stdout:\n{stdout}")

    stderr: Optional[str] = result.stderr
    if stderr:
        stderr = stderr.strip()
        if stderr:
            print(f"Stderr:\n{stderr}")


def check_cmake_files_formatted(cmake_files: list[str]) -> bool:
    print(f"Found {len(cmake_files)} {CMAKE_LIST_FILE_NAME} files. Checking files are formatted...")
    print("No changes will be applied. Use --apply to write changes.")

    has_unformatted_files: bool = False

    for file_path in cmake_files:
        print(f"Processing: {file_path}")
        try:
            result = subprocess.run(["cmake-format", "--check", file_path], check=False, capture_output=True, text=True)
            if result.returncode != 0:
                has_unformatted_files = True
                print(f"File {file_path} is not formatted correctly.")
            else:
                print(f"File {file_path} is formatted correctly.")
            print_process_output(result)
        except subprocess.SubprocessError as ex:
            has_unformatted_files = True
            print(f"An exception occurred while checking {file_path}: {ex}")

    return has_unformatted_files


def format_cmake_files(cmake_files: list[str]) -> bool:
    print(f"Found {len(cmake_files)} {CMAKE_LIST_FILE_NAME} files. Formatting files...")

    has_errors: bool = False

    for file_path in cmake_files:
        print(f"Formatting: {file_path}")
        try:
            result = subprocess.run(
                ["cmake-format", file_path, "-o", file_path], check=False, capture_output=True, text=True
            )
            if result.returncode != 0:
                has_errors = True
                print(f"Error: Command failed for {file_path}")
                print(f"Exit code: {result.returncode}")
            else:
                print(f"Success: {file_path}")
            print_process_output(result)
        except subprocess.SubprocessError as ex:
            has_errors = True
            print(f"An exception occurred while formatting {file_path}: {ex}")

    return has_errors


def lint_cmake_files(cmake_files: list[str], log_level: str) -> bool:
    print(f"Found {len(cmake_files)} {CMAKE_LIST_FILE_NAME} files. Linting files with log level: {log_level}")

    has_errors: bool = False

    for file_path in cmake_files:
        print(f"Linting: {file_path}")
        try:
            result = subprocess.run(
                ["cmake-lint", "--log-level", log_level, file_path], check=False, capture_output=True, text=True
            )
            if result.returncode != 0:
                has_errors = True
                print(f"Error: Command failed for {file_path}")
                print(f"Exit code: {result.returncode}")
            else:
                print(f"Success: {file_path}")
            print_process_output(result)
        except subprocess.SubprocessError as ex:
            has_errors = True
            print(f"An exception occurred while linting {file_path}: {ex}")

    return has_errors


def run_cmake_format(args) -> int:
    start_path = args.path
    print(f"Starting cmake-format in directory: {start_path}")

    if not os.path.isdir(start_path):
        print(f"Error: The path '{start_path}' is not a valid directory.")
        return ExitCodes.INVALID_ARGUMENTS

    if not shutil.which("cmake-format"):
        print("Error: cmake-format is not installed or not found in PATH.")
        return ExitCodes.TOOL_NOT_FOUND

    cmake_files = get_cmake_files(start_path)
    if not cmake_files:
        print(f"Error: No {CMAKE_LIST_FILE_NAME} files found in {start_path}.")
        return ExitCodes.NO_CMAKE_FILES_FOUND

    result = subprocess.run(["cmake-format", "--version"], check=False, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: Failed to get cmake-format version: {result.stderr.strip()}")
        return 1
    else:
        print(f"cmake-format version: {result.stdout.strip()}")

    if args.apply:
        have_errors = format_cmake_files(cmake_files)
        if have_errors:
            print("Error: Some files could not be formatted correctly.")
            return 1
        else:
            print("All files formatted successfully.")
    else:
        not_formatted = check_cmake_files_formatted(cmake_files)
        if not_formatted:
            print("Error: Some files are not formatted correctly. Use --apply to write changes.")
            return 1
        else:
            print("All files are formatted correctly.")

    return ExitCodes.SUCCESS


def run_cmake_lint(args) -> int:
    start_path = args.path
    log_level = args.log_level
    print(f"Starting cmake-lint in directory: {start_path}")

    if not os.path.isdir(start_path):
        print(f"Error: The path '{start_path}' is not a valid directory.")
        return ExitCodes.INVALID_ARGUMENTS

    if not shutil.which("cmake-lint"):
        print("Error: cmake-lint is not installed or not found in PATH.")
        return ExitCodes.TOOL_NOT_FOUND

    cmake_files = get_cmake_files(start_path)
    if not cmake_files:
        print(f"Error: No {CMAKE_LIST_FILE_NAME} files found in {start_path}.")
        return ExitCodes.NO_CMAKE_FILES_FOUND

    result = subprocess.run(["cmake-lint", "--version"], check=False, capture_output=True, text=True)
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

    return ExitCodes.SUCCESS


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates an argument parser for the script.

    Returns:
        argparse.ArgumentParser: The argument parser instance.
    """

    parser = argparse.ArgumentParser(
        prog="run_cmake_tool", description="This script runs cmake tools like cmake-format and cmake-lint."
    )

    subparsers = parser.add_subparsers(title="subcommands", dest="command", required=True)

    format_parser = subparsers.add_parser("format", help="Format CMakeLists files or check if they are formatted")
    format_parser.add_argument("path", help="Starting directory path")
    format_parser.add_argument("--apply", required=False, help="Write changes to files", action="store_true")
    format_parser.set_defaults(func=run_cmake_format)

    lint_parser = subparsers.add_parser("lint", help="Lint CMakeLists files")
    lint_parser.add_argument("path", help="Starting directory path")
    lint_parser.add_argument(
        "--log-level",
        required=False,
        help="Set the log level for cmake-lint",
        choices=["error", "warning", "info", "debug"],
        default="warning",
    )
    lint_parser.set_defaults(func=run_cmake_lint)

    return parser


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        int: Exit code from the executed tool, or a non-zero value for execution errors.
    """

    print("Run CMake Tool Script")

    parser = create_argument_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
