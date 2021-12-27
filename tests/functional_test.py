# Third party modules
import pytest
import sys
# First party modules
sys.path.append("../api")

#flask app
from app import app

@pytest.fixture
def client():
    """Generic Flask application fixture"""

    app.testing = True
    return app.test_client()



def test_notlocked(client):
    rv = client.post("/islocked", json={"service": "test"})
    assert rv.status_code == 200
    assert rv.data == b"Not Locked"

def test_locked(client):
    rv = client.post("/islocked", json={"service": "iris"})
    assert rv.status_code == 200
    assert rv.data == b"Locked"