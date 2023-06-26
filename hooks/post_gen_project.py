import logging
import pathlib
import shutil
import sys
import subprocess


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

def install_required_packages(install_deps:bool):
    subprocess.run(['pip', 'install', 'pip-tools'])
    subprocess.run(['python', '-m', 'piptools', 'compile', '-o', '../requirements-dev.txt', '../requirements-dev.in'])

    if install_deps:
        subprocess.run(['python', '-m', 'pip', 'install', '../requirements.txt'])


# Run the steps
move_root_files()
install_required_packages(install_deps={{cookiecutter.install_deps}})