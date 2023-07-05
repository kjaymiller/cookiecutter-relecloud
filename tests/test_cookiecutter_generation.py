"""
This module tests the cookiecutter generation of the project.
This DOES NOT TEST AZURE DEPLOYMENT
"""
import json
import pytest
import itertools
# import subprocess
# import pathlib


web_frameworks =  ["django", "flask", "fastapi"]
db_resources = ["postgres-flexible"]

combinations = itertools.product(web_frameworks, db_resources)
# Creates the context override for the parametrized test
CONTEXT_OVERRIDE = [{"project_backend":x, "db_resource":y} for x,y in combinations]
    
    
@pytest.fixture(scope="session")
def context():
    with open("cookiecutter.json", "r") as f:
        context = json.load(f)

        # remove all the non-prompted values
        for key in list(context.keys()):
            if key.startswith("_"):
                del context[key]

    return context


@pytest.mark.parametrize("context_override", CONTEXT_OVERRIDE)  
def tests_project_generation(cookies, context, context_override):
    """Test that project is generated and fully rendered."""

    extra_context = {**context, **context_override}

    print(context_override)
    result = cookies.bake(extra_context=extra_context) # TODO: parametrize and add context override
    assert result.exit_code == 0
    assert result.exception is None
    


# FUTURE TESTS
    # assert result.project_path.name == "demo_code"
    # assert result.project_path.is_dir()

    # paths = build_files_list(str(result.project_path))
    # assert paths
    # check_paths(paths) 


# def test_all_cookiecutter_paths_generated(cookies):
# result = cookies.bake()
# pathlib.rglob("**/*cookiecutter*")
# for path in pathlib.Path(result.project_path).rglob("*"):
    # if path.relative_to(result.project_path) == "/static/res/img"
    #     continue
    # re.findall(r"{{\s*cookiecutter\.\w+\s*}}", path.read_text())

# def test_src_folder_name_slugifies(cookies):
    
    
# def files_moved_one_level_above():
"""There are files that are moved outside of the source folder. Test those files are moved"""
# Tests Files exist one level above the source folder
# Tests Files do not exist in the source folder

# _and_ruff_isnt_upset():
