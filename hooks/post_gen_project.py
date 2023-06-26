import logging
import pathlib
import shutil
import sys

# Steps to finalize the cookiecutter build

# Move the root paths to the correct location
try:
    root_folder = pathlib.Path("root")

    for file in root_folder.iterdir():
        shutil.move(file, pathlib.Path.cwd().parent)
    
    root_folder.rmdir()

except Exception as e:
    # exit with status 1 to indicate failure
    logging.warning(e)
    sys.exit(1)