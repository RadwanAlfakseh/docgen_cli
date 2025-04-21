import os
import ast
import requests
from my_cli_app.config import get_config
from rich import print

TARGET_DIR = "."
PUBLIC_ONLY = False
BACKEND_URL = "."
API_KEY = "."
SOURCE = "."
TAGS = []


def summarize_code(code: str, type_: str, name: str) -> str:
    try:
        TAGS.append(os.name)
        response = requests.post(
            BACKEND_URL+"/summarize",
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "x-api-key": API_KEY,
            },
            json={
                "code": code,
                "type": type_,
                "name": name,
                "metadata": {
                    "source": SOURCE,
                    "tags": TAGS
                }
            },
        )
        if response.status_code == 200:
            summary = response.json().get("content", "")
        else:
            summary = f"⚠️ Error summarizing: {response.text}"

    except requests.RequestException as e:
        summary = f"⚠️ Error during request: {e}"
    
    config = get_config()
    function_prefix = config.get("function_prefix", f"📚 Generating documentation for {type_}: ")
    print(f"[bold green]{function_prefix} [underline magenta]{name}[/underline magenta]![/bold green]")
    return summary

def extract_definitions(filepath: str) -> list:
    with open(filepath, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=filepath)
    results = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if PUBLIC_ONLY and node.name.startswith("_"):
                continue
            parent = getattr(node, "parent", None)
            if PUBLIC_ONLY and (not parent or not isinstance(parent, ast.ClassDef)):
                continue
            type_ = "method" if parent and isinstance(parent, ast.ClassDef) else "function"
        elif isinstance(node, ast.ClassDef):
            if PUBLIC_ONLY and node.name.startswith("_"):
                continue
            type_ = "class"
        else:
            continue

        start_line = node.lineno - 1
        end_line = getattr(node, 'end_lineno', None) or start_line + 1
        snippet = source.splitlines()[start_line:end_line]
        code = '\\n'.join(snippet)
        name = node.name
        summary = summarize_code(code, type_, name)
        results.append({
            "name": name,
            "type": type_,
            "summary": summary,
            "code": code,
        })

    return results

def parse_directory(directory: str) -> list:
    all_summaries = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                summaries = extract_definitions(path)
                for summary in summaries:
                    summary["file"] = os.path.relpath(path, directory)
                    all_summaries.append(summary)
    return all_summaries

def export_markdown(docs: list) -> str:
    md = "# 📄 Code Documentation\n\n"
    for item in docs:
        md += f"## `{item['name']}` ({item['type']})\n"
        md += f"**File**: `{item['file']}`\n\n"
        md += f"{item['summary']}\n\n"
        md += "```python\n"
        md += f"{item['code']}\n"
        md += "```\n\n"
    return md