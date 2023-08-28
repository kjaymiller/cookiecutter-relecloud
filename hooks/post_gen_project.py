import rich.progress
import rich
import importlib.util
import logging
import os
import pathlib
import shutil
import subprocess


# Steps to finalize the cookiecutter build
def error_msg(pkg):
    return f"`{pkg}` is not installed. Run `pip install {pkg}` to install it."

def remove_aca_files():
    """Removes the files that are not needed for app service"""
    file_names = ("infra/web.bicep")
    for file_name in file_names:
        os.remove(file_name)
    os.remove("src/Dockerfile")

def move_db_files():
    """
    Moves the correct db files to the correct location
    Delete the remaining files in the db folder and the db folder itself
    """
    if "postgres" in "{{ cookiecutter.db_resource}}":
        shutil.move(
            "src/db/postgres_models.py",
            "src/models.py"
        )
    elif "mongo" in "{{ cookiecutter.db_resource}}":
        shutil.move(
            "src/db/mongo_models.py",
            "src/models.py"
        )

    shutil.rmtree("src/db")

def remove_postgres_files():
    if "{{ cookiecutter.project_backend }}" == "flask":
        shutil.rmtree("src/flask/flaskapp/migrations")

def rename_backend_files():
    """
    Rename the selected backend folder corresponding to the selected option.
    remove the project_backend folders that are not selected
    """

    selected_backend = "{{cookiecutter.project_backend}}"

    project_backends = ["django", "fastapi", "flask"]
    project_backends.remove(selected_backend)

    src = pathlib.Path('src')
    
    for unused_backend in project_backends:
        shutil.rmtree(src / pathlib.Path(unused_backend))
        
    shutil.copytree(
        src / pathlib.Path(selected_backend),
        pathlib.Path.cwd() / src,
        dirs_exist_ok=True,
    )
    shutil.rmtree(src / pathlib.Path(selected_backend))

def run_ruff_fix_and_black():
    """checks if ruff and black are installed and runs them on the project"""

    if importlib.util.find_spec("ruff"):
        subprocess.run(["python3", "-m" "ruff", "--fix", "src"])
    else:
        logging.warning(error_msg("ruff"))

    if importlib.util.find_spec("black"):
        subprocess.run(["python3", "-m", "black", "-q", "src"])
    else:
        logging.warning(error_msg("black"))

def run_bicep_format():
    """formats your bicep files"""
    subprocess.run(["az", "bicep", "format", "--file", "infra/main.bicep"])

if __name__ == "__main__":
    # It's import to remove the unecessary files before moving the db files
    
    with rich.progress.Progress() as progress:
        removing_files = progress.add_task(
            "Removing unecessary files",
            total=len((remove_postgres_files, remove_aca_files)),
        )

        if "postgres" not in "{{ cookiecutter.db_resource }}":
            progress.update(removing_files, description="Removing [blue]postgres[/blue] files")
            remove_postgres_files()
        progress.update(removing_files, advance=1)
    
        
        if "{{ cookiecutter.project_host }}" != "aca":
            progress.update(
                removing_files,
                description="[yellow]{{cookiecutter.project_host}}[/yellow] selected. Removing [blue]aca[/blue] files"
            )
            remove_aca_files()
        progress.update(removing_files, advance=1)

        moving_files = progress.add_task(
            "Moving files",
            total=len((move_db_files, rename_backend_files)),
        )
        progress.update(moving_files, description="Moving [blue]{{cookiecutter.db_resource}}[/blue] files")
        move_db_files()
        progress.update(moving_files, advance=1)
        progress.update(moving_files, description="Moving [blue]{{cookiecutter.project_host}}[/blue] files")
        rename_backend_files()
        progress.update(moving_files, advance=1)

        formatting = progress.add_task(
            "Formatting files",
            total=len((run_ruff_fix_and_black, run_bicep_format)),
        )

        progress.update(formatting, description="[yellow]Linting Project[/yellow]")
        run_ruff_fix_and_black()
        progress.update(formatting, advance=1)

        progress.update(formatting, description="[yellow]Linting Deployment Files[/yellow]")
        run_bicep_format()
        progress.update(formatting, advance=1)
