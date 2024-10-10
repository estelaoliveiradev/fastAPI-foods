from fast_zero.app import app

import pytest

from fastapi.testclient import TestClient

@pytest.fixture
def client():
    return TestClient(app)