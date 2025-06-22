# This script converts arguments from a GitHub Actions workflow into a format suitable for the run_cmake_tool.py script.
# GitHub Actions does not support conditional logic in the workflow file,
# so argument transformation must be handled manually.
# This conversion is separated from the main script to allow its reuse outside of GitHub Actions.
#
# Argument list:
# This script accepts exactly four required arguments:
# 1. 'command': The command to run. Possible values are 'format' or 'lint'.
# 2. 'path': The starting directory path for the command.
# 3. 'apply': A flag for the 'format' command to apply changes. Possible values are 'true' or 'false'.
# 4. 'log-level': An argument for the 'lint' command to set the log level. Possible values are 'debug', 'info', 'warning', or 'error'.

import argparse
import subprocess
import sys

def convert_args_to_run_cmake_tool(args):
    command = args.command
    path = args.path
    apply = args.apply.lower() == 'true'
    log_level = args.log_level

    subprocess_arguments = [sys.executable, "run_cmake_tool.py"]

    if command == 'format':
        print(f"Running format on path: {path} with apply: {apply}")

        subprocess_arguments.append("format")
        if apply:
            subprocess_arguments.append("--apply")

        subprocess_arguments.append(path)

        print(f"Subprocess arguments: {subprocess_arguments}")
        print("===========================")

        try:
            result = subprocess.run(subprocess_arguments, check=False)
            return result.returncode

        except Exception as e:
            print(f"Error: An exception occurred while calling run_cmake_tool.py: {e}")
            return 1

    elif command == 'lint':
        print(f"Running lint on path: {path} with log level: {log_level}")

        subprocess_arguments.extend(["lint", "--log-level", log_level, path])

        print(f"Subprocess arguments: {subprocess_arguments}")
        print("===========================")

        try:
            result = subprocess.run(subprocess_arguments, check=False)
            return result.returncode

        except Exception as e:
            print(f"Error: An exception occurred while calling run_cmake_tool.py: {e}")
            return 1

    else:
        print(f"Error: Unknown command: {command}")
        return 1

def main():
    print("Processing GitHub Actions inputs for run_cmake_tool.py")

    parser = argparse.ArgumentParser(
                        prog='github_action_entrypoint',
                        description='This script converts GitHub Actions arguments into a format suitable for run_cmake_tool.py.')

    parser.add_argument("command", help="The command to run. Possible values are 'format' or 'lint'.", choices=['format', 'lint'])
    parser.add_argument("path", help="The path to the project directory to format or lint. CMake files will be searched recursively in this directory.")
    parser.add_argument("apply", help="Whether to apply formatting changes. Possible values are 'true' or 'false'.", choices=['true', 'false'])
    parser.add_argument("log_level", help="The log level for cmake-lint. Possible values are 'debug', 'info', 'warning', or 'error'.", choices=['debug', 'info', 'warning', 'error'])

    parser.set_defaults(func=convert_args_to_run_cmake_tool)

    args = parser.parse_args()
    exit_code = args.func(args)

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
