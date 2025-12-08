# tests/__init__.py - test helpers
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    return TestClient(app)


# tests/factories.py - For test data factories
# tests/conftest.py - existing fixtures
