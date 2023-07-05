"""
This module tests the cookiecutter generation of the project.
This DOES NOT TEST AZURE DEPLOYMENT
"""
import pytest
import itertools
# import subprocess
# import pathlib

# @pytest.mark.parametrize("context_override", SUPPORTED_COMBINATIONS, ids=_fixture_id)
# def test_project_generation(cookies, context, context_override):
#     """Test that project is generated and fully rendered."""

#     result = cookies.bake(extra_context={**context, **context_override})
#     assert result.exit_code == 0
#     assert result.exception is None
#     assert result.project_path.name == context["project_slug"]
#     assert result.project_path.is_dir()

#     paths = build_files_list(str(result.project_path))
#     assert paths
#     check_paths(paths)

# # @pytest.fixture()
# def context_override():
#     """Return a list of all combinations of the supported options."""
web_frameworks =  ["django", "flask", "fastapi"]
db_resources = ["postgres-flexible"]

combinations = itertools.product(web_frameworks, db_resources)
CONTEXT_OVERRIDE = [{"project_backend":x, "db_resource":y} for x,y in combinations]
    
    
@pytest.fixture()
def context():
    return {
        "project_name": "Relecloud",
        "project_slug": "demo-code",
        "version": "0.0.1",
        "project_backend": ["django", "fastapi", "flask"],
        "use_vnet": "n",
        "db_resource": ["postgres-flexible"],
        "web_port": "8000",
    }


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
