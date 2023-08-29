{% macro app() %}
@pytest.fixture(scope="session")
def app():
    """Session-wide test `Flask` application."""
    config_override = {
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": os.environ.get(
            "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/postgres"
        ),
    }
    app = create_app(config_override)

    with app.app_context():
        engines = db.engines
        db.create_all()
        seeder.seed_data(db, pathlib.Path(__file__).parent.parent / "seed_data.json")

    engine_cleanup = []

    for key, engine in engines.items():
        connection = engine.connect()
        transaction = connection.begin()
        engines[key] = connection
        engine_cleanup.append((key, engine, connection, transaction))

    yield app

    for key, engine, connection, transaction in engine_cleanup:
        transaction.rollback()
        connection.close()
        engines[key] = engine
{% endmacro %}