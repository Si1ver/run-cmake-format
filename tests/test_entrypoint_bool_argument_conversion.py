"""
A set of tests for the github_action_entrypoint script.

This module contains tests for the conversion of boolean arguments.
"""

import argparse
from dataclasses import dataclass
import pytest
from test_entrypoint_constants import Consts
from github_action_entrypoint import convert_bool_argument


@dataclass(frozen=True)
class BoolArgumentValidTestCase:
    """A class to hold test data for boolean argument conversion."""

    input_value: str
    expected_output: bool


convert_bool_argument_valid_cases = [
    BoolArgumentValidTestCase(input_value="true", expected_output=True),
    BoolArgumentValidTestCase(input_value="True", expected_output=True),
    BoolArgumentValidTestCase(input_value="TRUE", expected_output=True),
    BoolArgumentValidTestCase(input_value="yes", expected_output=True),
    BoolArgumentValidTestCase(input_value="1", expected_output=True),
    BoolArgumentValidTestCase(input_value="false", expected_output=False),
    BoolArgumentValidTestCase(input_value="False", expected_output=False),
    BoolArgumentValidTestCase(input_value="FALSE", expected_output=False),
    BoolArgumentValidTestCase(input_value="no", expected_output=False),
    BoolArgumentValidTestCase(input_value="0", expected_output=False),
]


@pytest.mark.parametrize(
    "input_value, expected_output",
    [(case.input_value, case.expected_output) for case in convert_bool_argument_valid_cases],
    ids=[case.input_value for case in convert_bool_argument_valid_cases],
)
def test_convert_bool_argument_valid_cases(input_value: str, expected_output: bool) -> None:
    """Test the convert_bool_argument function with various valid inputs."""

    assert convert_bool_argument(input_value) is expected_output


convert_bool_argument_invalid_cases = [Consts.INVALID_BOOL, "not_a_bool", "maybe", "11", "00", "2", ""]


@pytest.mark.parametrize("input_value", convert_bool_argument_invalid_cases)
def test_convert_bool_argument_invalid_cases(input_value: str) -> None:
    """Test that convert_bool_argument raises ArgumentTypeError for invalid inputs."""

    with pytest.raises(argparse.ArgumentTypeError):
        convert_bool_argument(input_value)
