import multiprocessing

max_requests = 1000
max_requests_jitter = 50
log_file = "-"
bind = f"0.0.0.0:{{cookiecutter.web_port}}"
workers = (multiprocessing.cpu_count() * 2) + 1

{% if cookiecutter.project_backend == "fastapi" %}
worker_class = "uvicorn.workers.UvicornWorker"
{% else %}
threads = workers
{% endif %}

timeout = 600