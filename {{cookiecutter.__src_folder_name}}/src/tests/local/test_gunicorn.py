import sys
from unittest import mock

import pytest
from gunicorn.app.wsgiapp import run


def test_config_imports():
    {% set app_arg = {"flask": "flaskapp:create_app()", "fastapi": "fastapi_app.app:app", "django": "project.wsgi:application"}[cookiecutter.project_backend] %}
    argv = ["gunicorn", "--check-config", {{ app_arg }}, "-c", "src/gunicorn.conf.py"]

    with mock.patch.object(sys, "argv", argv):
        with pytest.raises(SystemExit) as excinfo:
            run()

    assert excinfo.value.args[0] == 0
