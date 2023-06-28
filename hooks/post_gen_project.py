import logging
import pathlib
import shutil
import sys
import json


# Steps to finalize the cookiecutter build

# Move the root paths to the correct location
def move_root_files():
    try:
        root_folder = pathlib.Path("root")

        for file in root_folder.iterdir():
            shutil.move(file, pathlib.Path.cwd().parent)
        
        root_folder.rmdir()

    except Exception as e:
        # exit with status 1 to indicate failure
        logging.warning(e)
        sys.exit(1)

def rename_backend_files():
    """Rename the selected backend folder correspondint to the selected option"""
    # remove the project_backend folders that are not selected

    selected_backend = "{{cookiecutter.project_backend}}"

    project_backends = {{_cookiecutter.project_backend|jsonify}}
    project_backends.remove(selected_backend)

    for unused_backend in project_backends:
        shutil.rmtree(pathlib.Path(unused_backend))
        
    # rename the selected backend folder to backend
    for file in pathlib.Path(selected_backend).iterdir():
            shutil.move(file, pathlib.Path.cwd())

    pathlib.Path(selected_backend).rmdir()


# Run the steps
move_root_files()
rename_backend_files()