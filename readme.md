# Run `cmake-format` GitHub Action

This repository provides a GitHub Action for running `cmake-format` and `cmake-lint` on your project workspace.

> **Note:** This action is in early development. Features and usage may change, and documentation is not yet complete.

## Usage

> **Note:** Usage examples and action input documentation may be incomplete or inaccurate at this stage, as this
> action is not intended for public use during early development.

Following inputs are available for this action:

| Input Name | Description | Default Value |
|------------|-------------|---------------|
| `command` | The command to run. Possible values are `format` or `lint`. `format` will run `cmake-format`, `lint` will run `cmake-lint`. | This input is required. |
| `path` | The path to the project directory to format or lint. CMake files will be searched recursively in this directory. | This input is required. |
| `apply-formatting` | Whether to apply formatting changes. Possible values are `true` or `false`. Only relevant for the `format` command. | `false` |
| `lint-log-level` | The log level for cmake-lint. Possible values are `debug`, `info`, `warning`, or `error`. Only relevant for the `lint` command. | `warning` |

## License

This project is licensed under the MIT License.

See the [LICENSE.md](LICENSE.md) file for details.
