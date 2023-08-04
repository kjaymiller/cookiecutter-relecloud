{% if cookiecutter.project_backend == "fastapi" %}
# Deploy a FastAPI Application via Azure Container Apps

This project deploy a [FastAPI](https://fastapi.tiangolo.com) application to [Azure Container Apps](https://aka.ms/aca). The FastAPI application is a simple web application for a space travel agency. The application is built using the FastAPI framework and uses a PostgreSQL database with SQLModel as an ORM. The application can be deployed to Azure using the [Azure Developer CLI](https://learn.microsoft.com/azure/developer/azure-developer-cli/overview).

{% endif %}

## Opening the project

This project has [Dev Container support](https://code.visualstudio.com/docs/devcontainers/containers), so it will be be setup automatically if you open it in Github Codespaces or in local VS Code with the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers).

If you're not using one of those options for opening the project, then you'll need to:

1. Create a [Python virtual environment](https://docs.python.org/3/tutorial/venv.html#creating-virtual-environments) and activate it.

1. Install production requirements:

    ```sh
    python -m pip install -r {{cookiecutter.__src_folder_name}}/requirements.txt
    ```

{% if cookiecutter.project_backend in ("flask", "fastapi") %}
1. Install the app as an editable package:

    ```sh
    python -m pip install -e {{cookiecutter.__src_folder_name}}
    ```
{% endif %}

1. Apply database migrations and seed initial data:

{% if cookiecutter.project_backend == "django" %}
    ```sh
    python {{cookiecutter.__src_folder_name}}/manage.py migrate
    python {{cookiecutter.__src_folder_name}}/manage.py loaddata {{cookiecutter.__src_folder_name}}/seed_data.json
    ```
{% endif %}
{% if cookiecutter.project_backend == "flask" %}
    ```sh
    python3 -m flask --app flaskapp db upgrade --directory {{cookiecutter.__src_folder_name}}/flaskapp/migrations
    python3 -m flask --app flaskapp seed --filename {{cookiecutter.__src_folder_name}}/seed_data.json
    ```
{% endif %}
{% if cookiecutter.project_backend == "fastapi" %}
    ```sh
    python3 demo_code/fastapi_app/seed_data.py
    ```
{% endif %}

## Running locally

Run gunicorn on the app:

```sh
{% if cookiecutter.project_backend == "flask" %}
python3 -m gunicorn 'flaskapp:create_app()' -c demo_code/gunicorn.conf.py
{% endif %}
{% if cookiecutter.project_backend == "fastapi" %}
python3 -m gunicorn fastapi_app:app -c demo_code/gunicorn.conf.py
{% endif %}
{% if cookiecutter.project_backend == "django" %}
python3 manage.py collectstatic
python3 -m gunicorn project.wsgi:application --name relecloud
{% endif %}
```

## Running tests

2. Install the development requirements:

    ```sh
    python3 -m pip install -r requirements-dev.in
    playwright install --with-deps
    ```

3. Run the tests:

    ```sh
    python3 -m pytest
    ```