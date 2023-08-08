import pathlib
import shutil


# Steps to finalize the cookiecutter build

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

rename_backend_files()

