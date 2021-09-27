import pytest
from src.macrozero import MacroZero


@pytest.fixture
def app():
    app = MacroZero(test_env=True, run_webserver=False)

    yield app


@pytest.fixture
def client(app):
    return app.webend.server.test_client()


@pytest.fixture
def runner(app):
    return app.webend.server.test_cli_runner()
