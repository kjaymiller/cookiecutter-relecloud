import pytest 
import itertools

postgres_db_resources = ["postgres-flexible", "cosmos-postgres", "postgres-service"]
mongo_db_resources = ["cosmos-mongodb"]

web_frameworks = [
    "django",
    "flask",
    "fastapi",
]
db_resources = postgres_db_resources # + mongo_db_resources


# Creates the context override for the parametrized test
def CONTEXT_OVERRIDE(web_frameworks, db_resource):
    return [{"project_backend": x, "db_resource": y} for x, y in itertools.product(web_frameworks, db_resources)]

@pytest.fixture(scope="session")
def default_context():
    return {
        "project_name": "Long_MIXED_CASE-demo name",
        "azd_template_version": "0.0.1",
        "project_backend": ["django", "fastapi", "flask"],
        "use_vnet": "n",
        "db_resource": [
            "postgres-flexible",
            "cosmos-postgres", 
            "postgres-service", 
            "cosmos-mongodb",
        ],
        "web_port": "8000",
    }

@pytest.fixture(
        scope="module",
        params=[*CONTEXT_OVERRIDE(web_frameworks, db_resources)],
)
def bakery(request, default_context, cookies_session):
    extra_context = {**default_context, **request.param}
    result = cookies_session.bake(extra_context=extra_context)
    yield result


@pytest.fixture(
        scope="module",
        params=[*CONTEXT_OVERRIDE(["flask"], db_resources)],
)
def flask_bakery(request, default_context, cookies_session):
    """Validates settings and options for Flask Deployments"""
    extra_context = {**default_context, **request.param}
    result = cookies_session.bake(extra_context=extra_context)
    yield result


@pytest.fixture(
        scope="module",
        params=[*CONTEXT_OVERRIDE(["flask", "fastapi"], mongo_db_resources)],
)
def mongo_bakery(request, default_context, cookies_session):
    """Validates settings and options for Flask Deployments"""
    extra_context = {**default_context, **request.param}
    result = cookies_session.bake(extra_context=extra_context)
    yield result