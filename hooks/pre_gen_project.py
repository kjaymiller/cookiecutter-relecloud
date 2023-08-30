import subprocess
import re

import rich
from rich.traceback import install
from packaging.version import Version, parse

install()

def check_version(current_version: str, supported_version: str) -> bool:
    """Checks if the current version is supported"""
    return current_version < supported_version


def check_not_implemented() -> None:
    if 'mongodb' in "{{cookiecutter.db_resource}}"  and "{{cookiecutter.project_backend}}" in ('fastAPI', 'django'):
        raise NotImplementedError(
            "MongoDB is not yet supported for FastAPI or Django projects"
        )

    if "{{cookiecutter.project_host}}" == "appservice" and "{{cookiecutter.db_resource}}" == "mongodb":
        raise NotImplementedError(
            "MongoDB is not yet supported for App Service projects"
        )


def tests_bicep_is_installed():
    """Tests that bicep is installed"""

    supported_bicep_version = Version("0.20.4")
    bicep_check = subprocess.run(["az", "bicep", "version"], capture_output=True)
    bicep_version = parse(
        re.search(r"\d+\.\d+\.\d+", bicep_check.stdout.decode("utf-8")).group(0),
    )

    if bicep_check.stderr:
        rich.print("""[bold yellow][WARNING]:[/bold yellow] An error occured with your bicep setup!
Please check that [yellow]`az bicep install`[/yellow] was successful before deploying your project.""")

    # check if version is lower than 0.20.4
    if check_version(bicep_version, supported_bicep_version):
        rich.print(f"""[bold yellow][WARNING]: Non-Supported Bicep Version:[/bold yellow] {bicep_version}.
Please update your bicep version using [yellow]`az bicep upgrade`[/yellow] before deploying your project."""
        )


if __name__ == "__main__":
    check_not_implemented()
    tests_bicep_is_installed()

