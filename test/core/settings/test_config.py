import importlib
import os

import pytest

from core.settings.config import settings


@pytest.mark.unittest
async def test_application_path():
    app_directory = settings.app_dir.__str__()
    assert app_directory.endswith("app")
    assert os.path.exists(os.path.join(app_directory, "__init__.py"))
    module = importlib.import_module("app")
    app_class = getattr(module, "App")
    assert app_class is not None
    assert app_class.__name__ == "App"
    assert app_class.app_name == "todo_application"
