"""
A set of tests for the github_action_entrypoint script.

This module contains tests for argument parsing functions.
"""

from dataclasses import dataclass
import pytest
from tests.entrypoint_constants import Consts
from github_action_entrypoint import Command, LogLevel, create_argument_parser


@dataclass(frozen=True)
class ArgumentParserInvalidArgumentsTestCase:
    """A class to hold test data for invalid argument parsing."""

    case_name: str
    arguments: list[str]


invalid_argument_cases = [
    ArgumentParserInvalidArgumentsTestCase(
        case_name="Invalid command",
        arguments=[Consts.INVALID_COMMAND, Consts.PATH, Consts.BOOL_TRUE, Consts.LOG_LEVEL_INFO],
    ),
    ArgumentParserInvalidArgumentsTestCase(
        case_name="Invalid log level in format command",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_TRUE, Consts.INVALID_LOG_LEVEL],
    ),
    ArgumentParserInvalidArgumentsTestCase(
        case_name="Invalid log level in lint command",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.INVALID_LOG_LEVEL],
    ),
    ArgumentParserInvalidArgumentsTestCase(
        case_name="Invalid bool in format command",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.INVALID_BOOL, Consts.LOG_LEVEL_INFO],
    ),
    ArgumentParserInvalidArgumentsTestCase(
        case_name="Invalid bool in lint command",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.INVALID_BOOL, Consts.LOG_LEVEL_INFO],
    ),
]


@pytest.mark.parametrize(
    "arguments",
    [case.arguments for case in invalid_argument_cases],
    ids=[case.case_name for case in invalid_argument_cases],
)
def test_argument_parser_invalid_arguments(arguments: list[str]) -> None:
    """Test that invalid arguments raise SystemExit on parsing."""

    parser = create_argument_parser()

    with pytest.raises(SystemExit):
        _ = parser.parse_args(arguments)


@dataclass(frozen=True)
class ParsedArgs:
    """A class to hold parsed arguments to compare against."""

    command: Command
    path: str
    apply: bool
    log_level: LogLevel
    verbose: bool
    quiet: bool

    @classmethod
    def create(
        cls: type,
        command: Command,
        path: str,
        apply: bool,
        log_level: LogLevel,
        verbose: bool = False,
        quiet: bool = False,
    ):
        """A helper method to create an instance of ParsedArgs to make test more compact."""

        return cls(command, path, apply, log_level, verbose, quiet)


@dataclass(frozen=True)
class ArgumentParserValidArgumentsTestCase:
    """A class to hold test data for valid argument parsing."""

    case_name: str
    arguments: list[str]
    expected_args: ParsedArgs


valid_argument_cases = [
    ArgumentParserValidArgumentsTestCase(
        case_name="Format command without apply",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO],
        expected_args=ParsedArgs.create(Command.FORMAT, Consts.PATH, False, LogLevel.INFO),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Format command with apply",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_TRUE, Consts.LOG_LEVEL_DEBUG],
        expected_args=ParsedArgs.create(Command.FORMAT, Consts.PATH, True, LogLevel.DEBUG),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Format command with verbose flag",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO, Consts.FLAG_VERBOSE],
        expected_args=ParsedArgs.create(Command.FORMAT, Consts.PATH, False, LogLevel.INFO, verbose=True),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Format command with quiet flag",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO, Consts.FLAG_QUIET],
        expected_args=ParsedArgs.create(Command.FORMAT, Consts.PATH, False, LogLevel.INFO, quiet=True),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Format command with verbose and quiet flags",
        arguments=[
            Consts.COMMAND_FORMAT,
            Consts.PATH,
            Consts.BOOL_FALSE,
            Consts.LOG_LEVEL_INFO,
            Consts.FLAG_VERBOSE,
            Consts.FLAG_QUIET,
        ],
        expected_args=ParsedArgs.create(Command.FORMAT, Consts.PATH, False, LogLevel.INFO, verbose=True, quiet=True),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with debug log level",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_DEBUG],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.DEBUG),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with info log level",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.INFO),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with warning log level",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_WARNING],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.WARNING),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with error log level",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_ERROR],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.ERROR),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with verbose flag",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO, Consts.FLAG_VERBOSE],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.INFO, verbose=True),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with quiet flag",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO, Consts.FLAG_QUIET],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.INFO, quiet=True),
    ),
    ArgumentParserValidArgumentsTestCase(
        case_name="Lint command with verbose and quiet flags",
        arguments=[
            Consts.COMMAND_LINT,
            Consts.PATH,
            Consts.BOOL_FALSE,
            Consts.LOG_LEVEL_INFO,
            Consts.FLAG_VERBOSE,
            Consts.FLAG_QUIET,
        ],
        expected_args=ParsedArgs.create(Command.LINT, Consts.PATH, False, LogLevel.INFO, verbose=True, quiet=True),
    ),
]


@pytest.mark.parametrize(
    "arguments, expected_args",
    [(case.arguments, case.expected_args) for case in valid_argument_cases],
    ids=[case.case_name for case in valid_argument_cases],
)
def test_argument_parser_valid_arguments(arguments: list[str], expected_args: ParsedArgs) -> None:
    """Test parsing of valid arguments."""

    parser = create_argument_parser()

    args = parser.parse_args(arguments)

    assert args.command == expected_args.command
    assert args.path == expected_args.path
    assert args.apply is expected_args.apply
    assert args.log_level == expected_args.log_level
    assert args.verbose is expected_args.verbose
    assert args.quiet is expected_args.quiet
