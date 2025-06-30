"""
A set of tests for the github_action_entrypoint script.

This module contains integration tests that verify the behavior of the github_action_entrypoint script.
"""

import sys
import json
from dataclasses import dataclass
import pytest
from test_entrypoint_constants import Consts
from github_action_entrypoint import main


@dataclass(frozen=True)
class ModuleConsts:
    """A class to hold string constants for tests in this module."""

    FILE_NAME_ARGS_TEST_HELPER = "args_test_helper.py"
    FILE_NAME_ARGS_OUTPUT = "args.txt"


@dataclass(frozen=True)
class TestEntrypointIntegrationTestCase:
    """A class to hold test data for integration testing."""

    case_name: str
    arguments: list[str]
    expected_arguments: list[str]
    exit_code: int


entrypoint_integration_cases = [
    TestEntrypointIntegrationTestCase(
        case_name="Format command with apply true",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_TRUE, Consts.LOG_LEVEL_INFO],
        expected_arguments=["format", "--apply", Consts.PATH],
        exit_code=0,
    ),
    TestEntrypointIntegrationTestCase(
        case_name="Format command with apply false and verbose flag",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO, Consts.FLAG_VERBOSE],
        expected_arguments=["format", Consts.PATH],
        exit_code=0,
    ),
    TestEntrypointIntegrationTestCase(
        case_name="Format command with apply true and log level debug",
        arguments=[Consts.COMMAND_FORMAT, Consts.PATH, Consts.BOOL_TRUE, Consts.LOG_LEVEL_DEBUG],
        expected_arguments=["format", "--apply", Consts.PATH],
        exit_code=0,
    ),
    TestEntrypointIntegrationTestCase(
        case_name="Lint command with apply true and log level warning",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_TRUE, Consts.LOG_LEVEL_WARNING],
        expected_arguments=["lint", "--log-level", "warning", Consts.PATH],
        exit_code=0,
    ),
    TestEntrypointIntegrationTestCase(
        case_name="Lint command with verbose flag",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_ERROR, Consts.FLAG_VERBOSE],
        expected_arguments=["lint", "--log-level", "error", Consts.PATH],
        exit_code=1,
    ),
    TestEntrypointIntegrationTestCase(
        case_name="Lint command with quiet flag",
        arguments=[Consts.COMMAND_LINT, Consts.PATH, Consts.BOOL_FALSE, Consts.LOG_LEVEL_INFO, Consts.FLAG_QUIET],
        expected_arguments=["lint", "--log-level", "info", Consts.PATH],
        exit_code=1,
    ),
]


@pytest.mark.parametrize(
    "arguments, expected_arguments, exit_code",
    [(case.arguments, case.expected_arguments, case.exit_code) for case in entrypoint_integration_cases],
    ids=[case.case_name for case in entrypoint_integration_cases],
)
def test_entrypoint_integration(
    arguments: list[str], expected_arguments: list[str], exit_code: int, monkeypatch, tmp_path
):
    """Test the integration of the entrypoint script with a helper script that simulates the run cmake tool script."""

    helper_script = tmp_path.joinpath(ModuleConsts.FILE_NAME_ARGS_TEST_HELPER)
    output_file = tmp_path.joinpath(ModuleConsts.FILE_NAME_ARGS_OUTPUT)

    # Write the helper script
    with open(helper_script, "w", encoding="utf-8") as f:
        f.write(f"""\
import sys
import json
with open(r"{output_file}", "w", encoding="utf-8") as f:
    json.dump(sys.argv[1:], f)
sys.exit({exit_code})
""")

    monkeypatch.setattr(f"{Consts.MODULE_NAME_ENTRYPOINT}.{Consts.ENV_VAR_TOOL_SCRIPT_NAME}", str(helper_script))

    test_argument: list[str] = [Consts.FILE_NAME_ENTRYPOINT_SCRIPT]
    test_argument.extend(arguments)
    monkeypatch.setattr(sys, "argv", test_argument)

    # Run the main function of the entrypoint script
    actual_exit_code: int = main()

    assert actual_exit_code == exit_code

    with open(output_file, "r", encoding="utf-8") as f:
        result = json.load(f)
        assert result == expected_arguments
