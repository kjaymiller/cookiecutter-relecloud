from jinja2.ext import Extension


def get_url_for_backend(route, framework):
    url_formulas = {
        "django": f"{{% url '{route}' %}}",
        "flask": f"{{{{ url_for('pages.{route}') }}}}",
        "fastapi": f"{{{{ url_for('{route}') }}}}",
    }

    return url_formulas[framework]


def get_detail_url_for_backend(route, framework): 
    """Return the url for the selected backend"""
    url_formulas = {
        "django": f"{{% url '{route}_detail' {route}.id %}}",
        "flask": f"{{{{ url_for('pages.{route}_detail', pk={route}.id) }}}}",
        "fastapi": f"{{{{ url_for('{route}_detail', pk={route}.id) }}}}",
    }

    return url_formulas[framework]


def get_static_url_for_backend(val, framework):
    """Return the url for the selected backend"""
    url_formulas = {
        "django": f"{{% static '{val}' %}}",
        "flask": f"{{{{ url_for('static', filename='{val}') }}}}",
        "fastapi": f"{{{{ url_for('static', path='{val}') }}}}",
    }
    return url_formulas[framework]


def get_model_url_for_backend(model, relation, framework):
    url_formulas = {
    "fastapi": f"{{% for {relation} in {model}.{relation}s %}}",
    "flask": f"{{% for {relation} in {model}.{relation}s %}}",
    "django": f"{{% for {relation} in {model}.{relation}s.all %}}",
    }

    return url_formulas[framework]


class GetUrlForBackend(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters['get_url_for_backend'] = get_url_for_backend
        environment.filters['get_detail_url_for_backend'] = get_detail_url_for_backend
        environment.filters['get_model_url_for_backend'] = get_model_url_for_backend
        environment.filters['get_static_url_for_backend'] = get_static_url_for_backend