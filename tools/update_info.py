from typing_extensions import Annotated
import cruft
import logging
import pathlib
import subprocess
import random
from typing import Generator
import typer
import re
import json
import itertools
from collections import defaultdict
# from rich import console

# Typer CLI Info
app = typer.Typer()
info_app = typer.Typer()
app.add_typer(info_app, name="info")
repos_app = typer.Typer()
app.add_typer(repos_app, name="repos")

# Configure Logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("update_info.log")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
# Add the file handler to the logger
logger.addHandler(file_handler)

with open("cookiecutter.json") as f:
    data = json.load(f)

db_resources = data["__prompts__"]["db_resource"].items()
web_frameworks = data["__prompts__"]["project_backend"].items()
deployment_hosts = data["__prompts__"]["project_host"].items()


combos = list(itertools.product(web_frameworks, db_resources, deployment_hosts))
random_cc_folder_prefix = "".join([str(chr(random.randint(65, 90))) for _ in range(20)])


def get_azure_combinations() -> Generator[tuple[str, str], None, None]:
    """
    Returns the base_keys and base_values for the combinations
    
    Yields:
        tuple[str, str]: The base_keys and base_values for the combinations
        Example: ("azure-flask-postgresql-azure-app-service", "Flask PostgreSQL Azure App Service")
    """
    for framework, db_resource, host in combos:
        base_keys = (
            (f"azure-{framework[0]}/{db_resource[0]}/{host[0]}")
            .lower()
            .replace("/", "-")
        )

        if re.findall("__prompt", base_keys):
            continue
        base_values = f"azure-{framework[0]}-{db_resource[0]}-{host[0]}"
        yield base_keys, base_values


@info_app.command(name='list_repos')
def metadata_list():
    """
    Creates a json file with the metadata for the combinations

    TODO: #302 Allow passing in a file to update_repos to iterate
    TODO: #303 Add a pattern that will allow for updating a subset of repos
    TODO: #304 Create a list of patterns to exclude
    """
    metadata_dict = defaultdict(list)

    for framework, db_resource, host in combos:
        base_keys = (
            (f"azure-{framework[0]}/{db_resource[0]}/{host[0]}")
            .lower()
            .replace("/", "-")
        )
        if re.findall("__prompt", base_keys):
            continue
        base_values = f"azure-{framework[0]}-{db_resource[0]}-{host[0]}"
        metadata_dict[framework[0]].append(base_values)

    with open("metadata.json", "w") as outfile:
        json.dump(metadata_dict, outfile, indent=4)

@info_app.command()
def update_readme():
    """Updates the README of cookiecutter-relecloud with the list of combinations"""
    web_framework_values = defaultdict(list)

    for framework, db_resource, host in combos:
        base_keys = (
            (f"azure-{framework[0]}/{db_resource[0]}/{host[0]}")
            .lower()
            .replace("/", "-")
        )
        if re.findall("__prompt", base_keys):
            continue
        base_values = f"{framework[1]} {db_resource[1]} {host[1]}"
        url = f"https://github.com/Azure-Samples/{base_keys}"
        md_link = re.sub(r"\[\w+\].*\[\/\w+\]", "", f"- [{base_values}]({url})")
        web_framework_values[framework[0]].append(md_link)

    for key, value in web_framework_values.items():
        print(f"### {key.title()}")
        print("----------")
        for item in value:
            print(item)
        print("\n")

    print(f"{len(list(combos))}: Total Combinations")

def create_base_folder():
    """Creates the base folder for the repo"""
    base_path = pathlib.Path(f"update_repos/{random_cc_folder_prefix}")
    base_path.mkdir(parents=True, exist_ok=True)
    return base_path
    # TODO: Get repos by pattern
    

def get_repos_by_pattern(pattern:str, repos: list[str]=list(get_azure_combinations())) -> list[str]:
    """
    Returns a list of repos that match the provided pattern.
    TODO: #305 Add Test
    """
    pattern = re.compile(pattern)
    matching_repos = [repo for repo in repos if pattern.match(repo)]
    return matching_repos
    
def update_repo(
        repo:str,
        path: pathlib.Path,
        branch:str="cruft/update",
        checkout_branch:str|None=None,
        **kwargs) -> None:
    """
    Updates the repo with the provided name
    
    Parameters:
        repo (str): The name of the repo to update.
            It should be the same as seen on GitHub.
        path (pathlib.Path): The parent folder where the will be saved.
        branch (str): The name of the branch to create and push to.
            Defaults to cruft/update.
        **kwargs: Additional keyword arguments to pass to cruft.update as 
    """
    # console = console.Console()
    logger.debug("Creating Placeholder Folder")
    url = f"git@github.com:Azure-Samples/{repo}.git"
    path = path.joinpath(repo)

    try:
        subprocess.check_output(
            ["git", "clone", url],
            cwd=path.parent,
        )

    except subprocess.CalledProcessError as e:
        raise ValueError(f"Could not to clone {url}: {e}.\nThis is likely a non-existent repo.")

    subprocess.check_output(
        ["git", "checkout", "-b", branch],
        text=True,
        cwd=path,
    )

    cruft.update(
        path,
        skip_apply_ask=True,
        extra_context=kwargs,
        checkout=checkout_branch if checkout_branch else None,
    )

    if not subprocess.check_output(
        ["git", "status", "--porcelain"],
        text=True,
        cwd=path,
    ):
        logger.info(f"No changes for {path}, skipping.")
        return

    if rejection_files:=list(pathlib.Path(path).rglob("*.rej")):
        logger.error(f"Rejection files found for {path}!\nFiles: {'\n- '.join(rejection_files)}")
        exit(1)

    # Add the Changes and Create a PR
    subprocess.check_output(
        ["git", "add", "."],
        text=True,
        cwd=path,
    )
    subprocess.check_output(
        ["git", "commit", "-m", "Cruft Update"],
        text=True,
        cwd=path,
    )
    subprocess.check_output(
        ["git", "push", "--set-upstream", "origin", branch],
        text=True,
        cwd=path,
    )
    subprocess.check_output(
        ["gh", "pr", "create", "--fill", "--reviewer", "kjaymiller,pamelafox"],
        text=True,
        cwd=path,
    )

@repos_app.command(name="update-one")
def update_single_repo(
    repo: Annotated[str, typer.Argument(
        help="The name of the repo to update.",
        show_default=False,
    )],
    branch: Annotated[str, typer.Option(
        "--branch",
        "-b",
        help="The branch to create and push to.",
    )]="cruft/update",
    checkout: Annotated[str, typer.Option(
        "--checkout",
        "-c",
        help="The branch to use for cruft updates `checkout` parameter.",
    )] = None,
    ) -> None:
    """
    Clones a single repo and updates it using `cruft update`
    
    TODO: #307 Add dict pattern to pass in kwargs to cruft.update
    """
    logger.info(f)
    return update_repo(
        repo=repo,
        path=create_base_folder(),
        branch=branch,
        checkout=checkout,
        )

@repos_app.command(name="update-many")
def update_repos(pattern:str, branch:str="cruft/update") -> None:
    """Updates all repos that match the provided pattern"""
    path = create_base_folder()
    repos = get_repos_by_pattern(pattern)
    for repo in repos:
        update_repo(repo=repo, path=path, branch=branch)


@repos_app.command(name="update-all")
def update_all_repos(branch:str="cruft/update"):
    """
    Iterates through combinations:

    - Creates a Placeholder Folder
    - Attempts to pull the combination url
    - Runs Cruft to update based on the path's cruft.json
    - Creates pull request for the updates
    """

    path = create_base_folder()
    for base_key,_ in get_azure_combinations():
        update_repo(base_key, path, branch=branch)



if __name__ == "__main__":
    app()
