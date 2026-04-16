"""Tests for the Flask web application."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from unittest.mock import MagicMock


APP_PATH = Path(__file__).resolve().parents[1] / "app.py"
APP_SPEC = spec_from_file_location("web_app_module", APP_PATH)
app_module = module_from_spec(APP_SPEC)
assert APP_SPEC is not None
assert APP_SPEC.loader is not None
APP_SPEC.loader.exec_module(app_module)


def test_app_exists():
    """Test that the Flask app object exists."""
    assert app_module.app is not None


def test_home_route():
    """Test that the home route returns a successful response."""
    mock_collection = MagicMock()
    mock_collection.find.return_value.sort.return_value = []

    app_module.app.config["TESTING"] = True

    original_get_collection = app_module.get_collection
    app_module.get_collection = lambda: mock_collection
    try:
        client = app_module.app.test_client()
        response = client.get("/")
        assert response.status_code == 200
    finally:
        app_module.get_collection = original_get_collection
