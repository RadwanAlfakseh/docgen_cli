import typer
from my_cli_app.commands import doc_generater
from my_cli_app.logger import setup_logging

app = typer.Typer()

app.command()(doc_generater.generate)

def main():
    setup_logging()
    app()