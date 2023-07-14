## Running tests

1. Create a virtual environment (if not already in a Dev Container or virtual env).

```
python3 -m venv .venv
source .venv/bin/activate
```

2. Install the development requirements:

```
python3 -m pip install -r requirements-dev.in
playwright install --with-deps
```

3. Run the tests:

```
python3 -m pytest
```