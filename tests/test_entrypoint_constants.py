"""
A set of tests for the github_action_entrypoint script.

This module contains common constants used across tests.
"""

from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Consts:
    """A class to hold string constants for testing."""

    # Valid string constants.
    COMMAND_FORMAT = "format"
    COMMAND_LINT = "lint"
    LOG_LEVEL_DEBUG = "debug"
    LOG_LEVEL_INFO = "info"
    LOG_LEVEL_WARNING = "warning"
    LOG_LEVEL_ERROR = "error"
    BOOL_TRUE = "true"
    BOOL_FALSE = "false"
    PATH = "some" + os.path.sep + "directory" + os.path.sep + "path"
    FLAG_VERBOSE = "--verbose"
    FLAG_QUIET = "--quiet"

    # Intentionally invalid string constants.
    INVALID_COMMAND = "unknowncommand"
    INVALID_LOG_LEVEL = "unknownlevel"
    INVALID_BOOL = "notabool"

    # Internal constants.
    MODULE_NAME_ENTRYPOINT = "github_action_entrypoint"
    FILE_NAME_TOOL_SCRIPT = "run_cmake_tool.py"
    FILE_NAME_ENTRYPOINT_SCRIPT = "github_action_entrypoint.py"
    ENV_VAR_TOOL_DIR = "RUN_CMAKE_TOOL_DIR"
    ENV_VAR_TOOL_SCRIPT_NAME = "RUN_CMAKE_TOOL_SCRIPT_NAME"
