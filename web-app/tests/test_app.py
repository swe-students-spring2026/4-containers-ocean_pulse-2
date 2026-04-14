import os
import sys
from unittest.mock import MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app import app  

def test_app_exists():
    assert app is not None

def test_home_route():
    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = []

    app.config["TESTING"] = True

    import app as app_module
    app_module.get_collection = lambda: mock_collection

    client = app.test_client()
    response = client.get("/")

    assert response.status_code == 200