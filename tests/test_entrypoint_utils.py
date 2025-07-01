"""
A set of tests for the github_action_entrypoint script.

This module contains tests for utility functions.
"""

from dataclasses import dataclass
import os
import pytest
from tests.entrypoint_constants import Consts
from github_action_entrypoint import get_run_cmake_tool_script_path


@dataclass(frozen=True)
class GetRunCmakeToolScriptPathTestCase:
    """A class to hold test data for getting the CMake tool script path."""

    case_name: str
    env_var_value: str | None
    expected_path: str


get_run_cmake_tool_script_path_cases = [
    GetRunCmakeToolScriptPathTestCase(
        case_name="Some valid path",
        env_var_value=Consts.PATH,
        expected_path=Consts.PATH + os.path.sep + Consts.FILE_NAME_TOOL_SCRIPT,
    ),
    GetRunCmakeToolScriptPathTestCase(
        case_name="Empty environment variable",
        env_var_value="",
        expected_path="." + os.path.sep + Consts.FILE_NAME_TOOL_SCRIPT,
    ),
    GetRunCmakeToolScriptPathTestCase(
        case_name="Current directory",
        env_var_value=".",
        expected_path="." + os.path.sep + Consts.FILE_NAME_TOOL_SCRIPT,
    ),
    GetRunCmakeToolScriptPathTestCase(
        case_name="No environment variable set",
        env_var_value=None,
        expected_path="." + os.path.sep + Consts.FILE_NAME_TOOL_SCRIPT,
    ),
]


@pytest.mark.parametrize(
    "env_var_value, expected_path",
    [(case.env_var_value, case.expected_path) for case in get_run_cmake_tool_script_path_cases],
    ids=[case.case_name for case in get_run_cmake_tool_script_path_cases],
)
def test_get_run_cmake_tool_script_path(env_var_value: str, expected_path: str, monkeypatch) -> None:
    """Test the get_run_cmake_tool_script_path function with various environment variable values."""

    if env_var_value is not None:
        monkeypatch.setenv(Consts.ENV_VAR_TOOL_DIR, env_var_value)
    else:
        monkeypatch.delenv(Consts.ENV_VAR_TOOL_DIR, raising=False)

    assert get_run_cmake_tool_script_path() == expected_path
