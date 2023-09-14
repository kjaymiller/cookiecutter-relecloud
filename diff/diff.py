"""
1. Create a random cookiecutter instance
2. Look at your given filepath
3. Diff the two
"""
import difflib
import filecmp
import json
import os 
import pathlib
import random
import sys
import webbrowser

import rich
from cookiecutter.main import cookiecutter
import typer
from typing_extensions import Annotated


app = typer.Typer(
    rich_help_panel = True
)
def print_diff_files(dcmp):
    for name in dcmp.diff_files:
        from_lines = pathlib.Path(dcmp.left).joinpath(name).read_text().splitlines()
        to_lines = pathlib.Path(dcmp.right).joinpath(name).read_text().splitlines()

        htmldiff = difflib.HtmlDiff()
        html= htmldiff.make_file(from_lines, to_lines)
        html = f"<h1>{dcmp.left}/{name}</h1><hr />\n" + html
        report_file = f"report/{dcmp.left[1:].replace('/', '_')}--{name}.html"
        pathlib.Path(report_file).write_text(html)
        webbrowser.open_new_tab(report_file)
        short_file = pathlib.Path(f"{dcmp.left}/{name}")
        rich.print(f"- [green]{short_file}[/green]")


    for sub_dcmp in dcmp.subdirs.values():
        print_diff_files(sub_dcmp)

@app.command()
def diff_build(
        diff_path: Annotated[pathlib.Path,  typer.Option("-d", "--dir", help="Path to the project that you wish to diff")] = pathlib.Path.cwd(),
        path_to_cookiecutter_build: Annotated[str, typer.Option('--cc', '--cookiecutter_path', help="Path to the cookiecutter template. This can be a local path or url")] = ...,
        output_dir: Annotated[pathlib.Path, typer.Option("-o", "--output", help="Path to build the temp_folder")] = pathlib.Path("."),
        replay: Annotated[bool, typer.Option("--replay")]=False,
        ) -> str:
    random_cc_folder_prefix = ''.join([str(chr(random.randint(65, 90))) for _ in range(20)])

    # Create project from the cookiecutter-pypackage.git repo template
    

    if replay:
        generated_path = cookiecutter(
                path_to_cookiecutter_build,
                replay=replay,
                overwrite_if_exists=True,
        )
    else:
        generated_path = cookiecutter(
                path_to_cookiecutter_build,
                extra_context={"project_name": random_cc_folder_prefix},
        )

    dcmp = filecmp.dircmp(generated_path, diff_path)

    if not pathlib.Path("report").is_dir():
        os.mkdir("report")

    rich.print("Diffs\n-----------")
    rich.print("The following files have diffs")
    print_diff_files(dcmp)


if __name__ == "__main__":
    app()
    
