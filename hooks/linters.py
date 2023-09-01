import importlib.util
import logging
import subprocess

def error_msg(pkg: str) -> str:
    return f"`{pkg}` is not installed. Run `pip install {pkg}` to install it."

def run_ruff_fix_and_black() -> None:
    """checks if ruff and black are installed and runs them on the project"""
    if importlib.util.find_spec("ruff"):
        subprocess.run(["python3", "-m" "ruff", "--fix", "src"])
    else:
        logging.warning(error_msg("ruff"))

    if importlib.util.find_spec("black"):
        subprocess.run(["python3", "-m", "black", "-q", "src"])
    else:
        logging.warning(error_msg("black"))

def run_bicep_format() -> None:
    """formats your bicep files"""
    subprocess.run(["az", "bicep", "format", "--file", "infra/main.bicep"])


def lint() -> None:
    """Runs all linters"""
    run_ruff_fix_and_black()
    run_bicep_format()