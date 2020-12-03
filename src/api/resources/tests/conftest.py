import pytest
from falcon import testing

from api import app


@pytest.fixture()
def client():
    return testing.TestClient(app.app)
