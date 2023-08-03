import logging
import os
import pathlib
import shutil
import sys


# Steps to finalize the cookiecutter build

# Move the root paths to the correct location
def move_root_files():
    try:
        root_folder = pathlib.Path("root")
        shutil.copytree(root_folder, pathlib.Path.cwd().parent, dirs_exist_ok=True)
        shutil.rmtree(root_folder)

    except Exception as e:
        # exit with status 1 to indicate failure
        logging.warning(e)
        sys.exit(1)

def rename_backend_files():
    """
    Rename the selected backend folder corresponding to the selected option.
    remove the project_backend folders that are not selected
    """

    selected_backend = "{{cookiecutter.project_backend}}"

    project_backends = ["django", "fastapi", "flask"]
    project_backends.remove(selected_backend)

    for unused_backend in project_backends:
        shutil.rmtree(pathlib.Path(unused_backend))
        
    shutil.copytree(pathlib.Path(selected_backend), pathlib.Path.cwd(), dirs_exist_ok=True)
    shutil.rmtree(pathlib.Path(selected_backend))

move_root_files()
rename_backend_files()
