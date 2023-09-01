import linters
import movers

import rich
# Steps to finalize the cookiecutter build

if __name__ == "__main__":
    # It's import to remove the unecessary files before moving the db files
    
    rich.print("Removing unecessary files")
    movers.check_for_files()
    rich.print("Linting files")
    linters.lint()
