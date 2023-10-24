import cruft
import pathlib
import subprocess
import random
from typing import Generator
import typer
import re
import json
import itertools
from collections import defaultdict

with open('cookiecutter.json') as f:
    data = json.load(f)

db_resources = data['__prompts__']['db_resource'].items()
web_frameworks = data['__prompts__']['project_backend'].items()
deployment_hosts = data['__prompts__']['project_host'].items()


combos = list(itertools.product(web_frameworks, db_resources, deployment_hosts))
random_cc_folder_prefix = ''.join([str(chr(random.randint(65, 90))) for _ in range(20)])

def get_azure_combinations() -> Generator[tuple[str, str], None, None]:
    """Returns the base_keys and base_values for the combinations"""
    for framework, db_resource, host in combos:
        base_keys= (f"azure-{framework[0]}/{db_resource[0]}/{host[0]}").lower().replace('/','-')

        if re.findall('__prompt', base_keys):
            continue
        base_values = f"azure-{framework[0]}-{db_resource[0]}-{host[0]}" 
        yield base_keys, base_values


app = typer.Typer()

@app.command()
def metadata_list():
    metadata_dict = defaultdict(list)

    for framework, db_resource, host in combos:
        base_keys= (f"azure-{framework[0]}/{db_resource[0]}/{host[0]}").lower().replace('/','-')
        if re.findall('__prompt', base_keys):
            continue
        base_values = f"azure-{framework[0]}-{db_resource[0]}-{host[0]}"
        metadata_dict[framework[0]].append(base_values)
    
    with open("metadata.json", "w") as outfile:
        json.dump(metadata_dict, outfile, indent=4)

@app.command()
def update_all_repos():
    """
    Iterates through combinations:

    - Creates a Placeholder Folder
    - Attempts to pull the combination url
    - Runs Cruft to update based on the path's cruft.json
    - Creates pull request for the updates
    """

    logging.debug("Creating Placeholder Folder")
    pathlib.Path(random_cc_folder_prefix).mkdir()

    logging.debug("Cloning Repos and Running Cruft")
    for base_key, base_values in get_azure_combinations():
        cmd = ["git", "clone", "url", pathlib.Path(base_key)]
        url = (f"https://github.com/Azure-Samples/{base_key}")
        path = pathlib.Path(random_cc_folder_prefix).joinpath(base_key)

        try:
            subprocess.check_output(
                cmd, stderr=subprocess.STDOUT, text=True, cwd=random_cc_folder_prefix
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to clone {url}: {e}")
            continue

        cruft.update(path, skip_apply_ask=True)


@app.command()
def update_readme():
    web_framework_values = defaultdict(list)

    for framework, db_resource, host in combos:
        base_keys= (f"azure-{framework[0]}/{db_resource[0]}/{host[0]}").lower().replace('/','-')
        if re.findall('__prompt', base_keys):
            continue
        base_values = (f"{framework[1]} {db_resource[1]} {host[1]}")
        url = (f"https://github.com/Azure-Samples/{base_keys}")
        md_link = (re.sub(r"\[\w+\].*\[\/\w+\]", "", f"- [{base_values}]({url})"))
        web_framework_values[framework[0]].append(md_link)

    for key, value in web_framework_values.items():
        print(f"### {key.title()}")
        print("----------")
        for item in value:
            print(item)
        print("\n")


    print(f"{len(list(combos))}: Total Combinations")

if __name__ == "__main__":
    app()