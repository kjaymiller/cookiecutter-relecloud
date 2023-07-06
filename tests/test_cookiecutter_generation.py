"""
This module tests the cookiecutter generation of the project.
This DOES NOT TEST AZURE DEPLOYMENT
"""
import re
import pytest
import itertools
import pathlib
import subprocess


web_frameworks =  ["django", "flask", "fastapi"]
db_resources = ["postgres-flexible"]

combinations = itertools.product(web_frameworks, db_resources)
# Creates the context override for the parametrized test
CONTEXT_OVERRIDE = [{"project_backend":x, "db_resource":y} for x,y in combinations]
    
    
@pytest.fixture(scope="session")
def context():
    return {
    "project_name": "Relecloud",
    "project_slug": "Long_MIXED_CASE-demo name",
    "version": "0.0.1",
    "project_backend": ["django", "fastapi", "flask"],
    "use_vnet": "n",
    "db_resource": ["postgres-flexible"],
    "web_port": "8000",
    }

@pytest.fixture(scope="module", params=[*CONTEXT_OVERRIDE])
def bakery(request, context, cookies_session):
    extra_context = {**context, **request.param}
    result = cookies_session.bake(extra_context=extra_context)
    yield result

def test_project_generation(bakery):
    """Test that project is generated and fully rendered."""
    assert bakery.exit_code == 0
    assert bakery.exception is None


def test_bicep_assertion_working_path_referenced_in_bicep(bakery):
    """Ensures that the generated path name is same as referenced path in azure.yaml"""
    assert bakery.project_path.name == "long_mixed_case_demo_name"
    assert bakery.project_path.is_dir()

# FUTURE TESTS
    # paths = build_files_list(str(result.project_path))
    # assert paths
    # check_paths(paths) 

def test_all_cookiecutter_paths_generated(bakery):
    """Check for any cookiecutter variables that were not replaced"""
    for path in pathlib.Path(bakery.project_path).rglob("*_"):
        
        # This path is the only one that should have files
        if path.relative_to(bakery.project_path) == "/static/res/img": 
            matches = re.findall(r"\{\{\s*cookiecutter\.\w+\s*\}\}", path.read_text())
            if matches:
                pytest.fail(f"Found cookiecutter variable in {path.relative_to(result.project_path)}")

def test_build_folders_are_deleted(bakery, context):
    backend_names = context.get("project_backend")
    for path in bakery.project_path.iterdir():
        if path.is_dir():
            if path.name in backend_names:
                pytest.fail(f"Found build folder {path.name} - {path.relative_to(bakery.project_path)}")
    

def test_files_moved_one_level_above(bakery, context):
    """There are files that are moved outside of the source folder. Test those files are moved"""
    # Tests files exist one level above the source folder
    assert (bakery.project_path.parent / "infra").exists()
    assert (bakery.project_path.parent / "infra").is_dir()

    # Tests Files do not exist in the source folder
    assert not (bakery.project_path / "root").exists()


def tests_valid_bicep(bakery, context):
    commands = f"az bicep build --file {bakery.project_path.parent}/infra/main.bicep".split(" ")
    result = subprocess.run(commands, capture_output=True, text=True)
    assert result.returncode == 0 

