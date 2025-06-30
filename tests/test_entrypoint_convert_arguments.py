"""
A set of tests for the github_action_entrypoint script.

This module contains tests for argument conversion from the GitHub Actions workflow step to the run cmake tool script
format.
"""

import argparse
from dataclasses import dataclass
import pytest
from test_entrypoint_constants import Consts
from github_action_entrypoint import Command, LogLevel, LoggingOptions, convert_args_to_run_cmake_tool


def create_args_helper(command: Command, path: str, apply: bool, log_level: LogLevel) -> argparse.Namespace:
    """Helper function to create a Namespace object with the given arguments."""
    return argparse.Namespace(command=command, path=path, apply=apply, log_level=log_level)


@dataclass(frozen=True)
class ConvertArgsToRunCMakeToolTestCase:
    """A class to hold test data for argument conversion."""

    case_name: str
    arguments: argparse.Namespace
    expected_args: list[str]


valid_argument_cases = [
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Format command with apply and log level info (log level is ignored)",
        arguments=create_args_helper(Command.FORMAT, Consts.PATH, True, LogLevel.INFO),
        expected_args=["format", "--apply", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Format command with log level info (log level is ignored)",
        arguments=create_args_helper(Command.FORMAT, Consts.PATH, False, LogLevel.INFO),
        expected_args=["format", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Format command with log level debug (log level is ignored)",
        arguments=create_args_helper(Command.FORMAT, Consts.PATH, True, LogLevel.DEBUG),
        expected_args=["format", "--apply", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Format command with log level warning (log level is ignored)",
        arguments=create_args_helper(Command.FORMAT, Consts.PATH, True, LogLevel.WARNING),
        expected_args=["format", "--apply", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Format command with log level error (log level is ignored)",
        arguments=create_args_helper(Command.FORMAT, Consts.PATH, True, LogLevel.ERROR),
        expected_args=["format", "--apply", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Lint command with log level info and apply (apply is ignored)",
        arguments=create_args_helper(Command.LINT, Consts.PATH, True, LogLevel.INFO),
        expected_args=["lint", "--log-level", "info", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Lint command with log level debug",
        arguments=create_args_helper(Command.LINT, Consts.PATH, False, LogLevel.DEBUG),
        expected_args=["lint", "--log-level", "debug", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Lint command with log level warning",
        arguments=create_args_helper(Command.LINT, Consts.PATH, False, LogLevel.WARNING),
        expected_args=["lint", "--log-level", "warning", Consts.PATH],
    ),
    ConvertArgsToRunCMakeToolTestCase(
        case_name="Lint command with log level error",
        arguments=create_args_helper(Command.LINT, Consts.PATH, False, LogLevel.ERROR),
        expected_args=["lint", "--log-level", "error", Consts.PATH],
    ),
]


@pytest.mark.parametrize(
    "arguments, expected_args",
    [(case.arguments, case.expected_args) for case in valid_argument_cases],
    ids=[case.case_name for case in valid_argument_cases],
)
def test_convert_args_to_run_cmake_tool(arguments: argparse.Namespace, expected_args: list[str]) -> None:
    """Test the conversion of arguments to the run cmake tool script format."""

    # Default logging options for testing
    logging_options = LoggingOptions.create(False, False)

    command_and_arguments = convert_args_to_run_cmake_tool(arguments, logging_options)

    assert command_and_arguments == expected_args
