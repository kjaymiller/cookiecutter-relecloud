import os
from .app import app  # noqa
from azure.monitor.opentelemetry import configure_azure_monitor

if os.getenv("APPLICATIONINSIGHTS_CONNECTION_STRING"):
    configure_azure_monitor()
__all__ = ["app"]