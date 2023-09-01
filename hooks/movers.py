"""functions that move files around or delete them"""
import os
import shutil
from rich.progress import Task

def move_db_files(db_resource: str):
    """
    Moves the correct db files to the correct location
    Delete the remaining files in the db folder and the db folder itself
    """

    if "postgres" in db_resource:
        shutil.move(
            "src/db/postgres_models.py",
            "src/models.py"
        )
        shutil.move(
            "src/db/postgres_seeder.py",
            "src/flask/flaskapp/seeder.py",
        )
    if "mongo" in db_resource:
        shutil.move(
            "src/db/mongo_models.py",
            "src/models.py"
        )
        shutil.move(
            "src/db/mongo_seeder.py",
            "src/flask/flaskapp/seeder.py",
        )

def remove_aca_files() -> None:
    """Removes unneeded files if aca is not selected"""
    file_names = (
        "infra/web.bicep",
        "src/Dockerfile",
    )

    for file_name in file_names:
        os.remove(file_name)

def remove_flask_migration_files() -> None:
    """
    Removes the flask migration files if postgres is not selected
    This only applies to flask projects
    """
    if "{{ cookiecutter.project_backend }}" == "flask" and "mongo" in "{{cookiecutter.db_resource }}":
        shutil.rmtree("src/flask/flaskapp/migrations")
    else:
        pass

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


def choose_web_bicep():
    """Selects the correct web.bicep file"""
    bicep_files = {
        "aca": "infra/web_aca.bicep",
        "appservice": "infra/web_appservice.bicep",
    }

    shutil.move(
        bicep_files.pop("{{cookiecutter.project_host}}"),
        "infra/web.bicep",
    )

    for file_name in bicep_files.values():
        os.remove(file_name)

    


def check_for_files(task: Task) -> None:
    """
    Iterate through the cookiecutter options.
    remove the files corresponding to the results
    TODO: Add task progress
    """

    # DB Options
    # The chosen db option is stored in src.
    move_db_files({{cookiecutter.db_resource}})
    shutil.rmtree("src/db") # Clean up remaining db folder

    # Backend Options
    remove_flask_migration_files()

    # Azure Host Options
    choose_web_bicep()
    if "{{cookiecutter.project_host }}" != "aca":
        remove_aca_files()

    if "{{cookiecutter.project_host}}" == "appservice":
        pass


    rename_backend_files()
    