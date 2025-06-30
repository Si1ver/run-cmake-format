"""
This script transforms GitHub Actions job arguments into a format compatible with the run cmake tool script.

Argument conversion is handled in Python due to the limited conditional logic available in GitHub Actions workflow
files.
"""

__version__ = "0.1.0b1"

import argparse
import os
import shlex
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from typing import assert_never

# To avoid debugging issues with older Python versions, the script requires Python 3.12 or higher.
if sys.version_info < (3, 12):
    print("This script requires Python 3.12 or higher")
    sys.exit(1)

# The run cmake tool script name.
RUN_CMAKE_TOOL_SCRIPT_NAME: str = "run_cmake_tool.py"

# Environment variable name for the directory containing the run cmake tool script.
RUN_CMAKE_TOOL_DIR_ENV_VAR: str = "RUN_CMAKE_TOOL_DIR"


class ExitCodes(int, Enum):
    """Exit codes for the script."""

    TOOL_SCRIPT_NOT_FOUND = 101
    FAILED_TO_RUN_TOOL_SCRIPT = 102


class Command(str, Enum):
    """Commands for the run cmake tool script."""

    FORMAT = "format"
    LINT = "lint"


class LogLevel(str, Enum):
    """Log levels for the lint command of run cmake tool script."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class LoggingOptions:
    """A immutable class to hold parsed logging options."""

    verbose: bool
    quiet: bool

    @classmethod
    def create(
        cls: type,
        verbose: bool = False,
        quiet: bool = False,
    ):
        """A helper method to create an instance of LoggingOptions while handling argument collision."""

        return cls(verbose=verbose and not quiet, quiet=quiet)


def get_run_cmake_tool_script_path() -> str:
    """
    Composes the path to the run cmake tool script.

    Returns:
        str: The path to the script.
    """

    run_cmake_tool_dir: str = os.environ.get(RUN_CMAKE_TOOL_DIR_ENV_VAR, "")
    if not run_cmake_tool_dir:
        # If the environment variable is not set or empty, use the current directory.
        run_cmake_tool_dir = "."
    return os.path.join(run_cmake_tool_dir, RUN_CMAKE_TOOL_SCRIPT_NAME)


def run_cmake_tool_script(command_and_arguments: list[str], logging_options: LoggingOptions) -> int:
    """
    Runs the run cmake tool script with the provided command and arguments.

    Args:
        command_and_arguments (list[str]): The command and its arguments to run.
        logging_options (LoggingOptions): Options for logging output.

    Returns:
        int: Exit code from the executed tool, or a non-zero value for execution errors.
    """

    run_cmake_tool_path: str = get_run_cmake_tool_script_path()
    if not os.path.isfile(run_cmake_tool_path):
        if not logging_options.quiet:
            print(
                f"Error: The {RUN_CMAKE_TOOL_SCRIPT_NAME} script was not found at the expected path:"
                f" {run_cmake_tool_path}"
            )
        return ExitCodes.TOOL_SCRIPT_NOT_FOUND

    # Tool script intentionally called using sys.executable to make it run as if it were called directly.
    subprocess_arguments: list[str] = [sys.executable, run_cmake_tool_path]
    subprocess_arguments.extend(command_and_arguments)

    if not logging_options.quiet:
        print(f"Running command: {shlex.join(subprocess_arguments)}")

    try:
        result = subprocess.run(subprocess_arguments, check=False)
        return result.returncode

    except subprocess.SubprocessError as ex:
        if not logging_options.quiet:
            print(f"Error: An exception occurred while calling run_cmake_tool.py: {ex}")
        return ExitCodes.FAILED_TO_RUN_TOOL_SCRIPT


def convert_args_to_run_cmake_tool(args: argparse.Namespace, logging_options: LoggingOptions) -> list[str]:
    """
    Converts GitHub Actions job arguments into a format suitable for the run cmake tool script.

    Args:
        args (argparse.Namespace): The parsed command line arguments.
        logging_options (LoggingOptions): The logging options for the command.

    Returns:
        list[str]: A list of command and its arguments to be passed to the run cmake tool script.
    """

    if logging_options.verbose:
        print(f"Running entrypoint script for {RUN_CMAKE_TOOL_SCRIPT_NAME} v.{__version__}")

    command: Command = args.command
    path: str = args.path

    match command:
        case Command.FORMAT:
            apply: bool = args.apply

            if logging_options.verbose:
                print(f"Running format on path: {path} with apply: {apply}")

            format_subprocess_arguments: list[str] = ["format"]
            if apply:
                format_subprocess_arguments.append("--apply")
            format_subprocess_arguments.append(path)

            return format_subprocess_arguments

        case Command.LINT:
            log_level: LogLevel = args.log_level

            if logging_options.verbose:
                print(f"Running lint on path: {path} with log level: {log_level.value}")

            lint_subprocess_arguments: list[str] = ["lint", "--log-level", log_level.value, path]

            return lint_subprocess_arguments

        # This case is unreachable because all possible commands are handled.
        case _ as unreachable:
            assert_never(unreachable)


def execute_tool_command(args: argparse.Namespace) -> int:
    """
    Executes the run cmake tool script.

    Args:
        args (argparse.Namespace): The parsed command line arguments.

    Returns:
        int: Exit code from the executed tool, or a non-zero value for execution errors.
    """

    logging_options: LoggingOptions = LoggingOptions.create(args.verbose, args.quiet)

    # Convert the arguments to a format suitable for the run cmake tool script.
    command_and_arguments: list[str] = convert_args_to_run_cmake_tool(args, logging_options)

    return run_cmake_tool_script(command_and_arguments, logging_options)


def convert_bool_argument(arg: str) -> bool:
    """
    Converts a string argument to a boolean value.

    Args:
        arg (str): The string argument to convert.

    Returns:
        bool: The converted boolean value.
    """

    if arg.lower() in ("true", "yes", "1"):
        return True
    elif arg.lower() in ("false", "no", "0"):
        return False
    else:
        raise argparse.ArgumentTypeError(
            f"Invalid boolean argument: '{arg}' is not a valid boolean. Use 'true' or 'false'."
        )


def create_argument_parser() -> argparse.ArgumentParser:
    """
    Creates an argument parser for the script.

    Returns:
        argparse.ArgumentParser: The argument parser instance.
    """

    parser = argparse.ArgumentParser(
        prog="github_action_entrypoint",
        description=(
            "This script converts GitHub Actions job arguments into a format suitable for"
            f" {RUN_CMAKE_TOOL_SCRIPT_NAME}."
        ),
    )

    parser.add_argument(
        "command",
        type=Command,
        choices=list(Command),
        help="The command to run. Possible values: 'format', 'lint'.",
    )
    parser.add_argument(
        "path",
        type=str,
        help=(
            "The path to the project directory to format or lint. CMake files will be searched recursively in this"
            " directory."
        ),
    )
    parser.add_argument(
        "apply",
        type=convert_bool_argument,
        help=(
            "Whether to apply formatting changes. Values: 'true', 'false'. If 'true', changes will be written to files."
            " Only relevant for the 'format' command."
        ),
    )
    parser.add_argument(
        "log_level",
        type=LogLevel,
        choices=list(LogLevel),
        help=(
            "The log level for cmake-lint. Possible values are 'debug', 'info', 'warning', or 'error'. Only relevant"
            " for the 'lint' command."
        ),
    )

    parser.add_argument("--verbose", action="store_true", default=False, help="Enable additional logging output.")
    parser.add_argument(
        "--quiet",
        action="store_true",
        default=False,
        help="Disable all logging output. This option takes precedence over '--verbose'.",
    )

    parser.set_defaults(func=execute_tool_command)

    return parser


def main() -> int:
    """
    Main entry point for the script.

    Returns:
        int: Exit code from the executed tool, or a non-zero value for execution errors.
    """

    parser = create_argument_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
