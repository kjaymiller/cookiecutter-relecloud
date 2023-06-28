from jinja2.ext import Extension


class GetUrlForBackend(Extension):
    def __init__(self, environment):
        super().__init__(environment)
        environment.filters['get_url_for_backend'] = lambda val, framework: get_url_for_backend(val, framework)
        environment.filters['get_static_url_for_backend'] = lambda val, framework: get_static_url_for_backend(val, framework)


def get_url_for_backend(v, framework):
    """Return the url for the selected backend"""
    url_formulas = {
        "django": f"{{% url '{v}' %}}",
        "flask": f"{{% url_for('{v}') %}}",
        "fastapi": f"{{% url_for('{v}') %}}"
    }
    return url_formulas[framework]

def get_static_url_for_backend(v, framework):
    """Return the url for the selected backend"""
    url_formulas = {
        "django": f"{{% static '{v}' %}}",
        "flask": f"{{% url_for(static, path='{v}') %}}",
        "fastapi": f"{{% url_for(static, path='{v}') %}}",
    }
    return url_formulas[framework]
