# My CLI App

A simple command-line interface Python project for generating documentation from Python code.

## Features

- Parses Python files to extract classes, functions, and methods.
- Generates Markdown documentation with summaries and code snippets.
- Supports configuration via `config.yaml`.
- Allows filtering for public methods and classes only.
- Opens the generated documentation file automatically (optional).

## Installation

Install the required dependencies:

```bash
pip install -r .
```

## Usage

The backend for the cli can be found in the following repo: [code_docgen_backend](https://github.com/RadwanAlfakseh/code_docgen)

Run the CLI to generate documentation:

```bash
mycli <path_to_python_project> --public-only --open-file
```

### Options

- `<path_to_python_project>`: Path to the Python project directory.
- `--public-only`: Only document public methods and classes (optional).
- `--open-file`: Open the generated documentation file after creation (optional).

## Configuration

You can customize the behavior of the CLI by editing the `config.yaml` file:

```yaml
generation_prefix: "🚀 Generating documentation for repository: "
type_prefix: "✅ Completed Generating documentation for type: "
function_prefix: "✅ Completed Generating documentation for function: "
generation_suffix: "✅ Documentation generation completed successfully."
API_KEY: "your-api-key"
BACKEND_URL: "http://your-backend-url/api"
TAGS: ["python", "documentation"]
```

## Example

To generate documentation for a project located in `./my_project`, run:

```bash
mycli ./my_project --public-only --open-file
```

This will create a `generated_docs.md` file in the specified directory.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
