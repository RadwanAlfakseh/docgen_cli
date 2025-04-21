from rich import print
from my_cli_app.config import get_config
from my_cli_app import parser
import typer
import os

def generate(path: str = typer.Argument(..., help="Path to the Python project directory."),
    public_only: bool = typer.Option(False, help="Only document public methods and classes."),
    open_file: bool = typer.Option(False, help="Open the generated documentation file after creation.")):
    
    config = get_config()
    generation_prefix = config.get("generation_prefix", "parsing repository")
    generation_suffix = config.get("generation_suffix", "✅ Documentation generation completed successfully.")
    if not os.path.exists(path):
        print(f"[bold red]Error: The specified path '{path}' does not exist.[/bold red]")
        raise typer.Exit(code=1)
    
    parser.PUBLIC_ONLY = public_only
    parser.TARGET_DIR = path
    parser.TAGS = config.get("TAGS", ["python"])
    parser.SOURCE = config.get("SOURCE", "GitHub")
    parser.API_KEY = config.get("API_KEY","demo-secret-token")
    parser.BACKEND_URL = config.get("BACKEND_URL", "http://localhost:5000/api")
        
    print(f"[bold green]{generation_prefix} [underline magenta]{path}[/underline magenta]![/bold green]")
    docs = parser.parse_directory(parser.TARGET_DIR)
    markdown = parser.export_markdown(docs)

    # Ensure the generated_docs.md file is created in parser.TARGET_DIR
    output_file_path = os.path.join(parser.TARGET_DIR, "generated_docs.md")
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write(markdown)

    print(f"{generation_suffix}: {output_file_path}")
    # based on the os type, open the file in the appropriate way
    if open_file:
            if os.name == 'nt':  # For Windows
                os.startfile(output_file_path)
            elif os.name == 'posix':  # For macOS
                os.system(f'open "{output_file_path}"')  # macOS
            else:  # For Linux
                os.system(f'xdg-open "{output_file_path}"')  # Linux
            raise typer.Exit(code=0)
