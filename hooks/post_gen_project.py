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
    file_names = ["infra/web.bicep"]
    for file_name in file_names:
        os.remove(file_name)

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
    rename_backend_files()
    
    if "{{ cookiecutter.project_host }}" != "aca":
        remove_aca_files()

    run_ruff_fix_and_black()
    run_bicep_format()
