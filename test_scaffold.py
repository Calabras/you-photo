import ast
import importlib
from pathlib import Path

import pytest

MODULES = (
    "backend_core_module",
    "file_storage_module",
    "notification_module",
    "web_client_module",
    "desktop_client_module",
    "camera_integration_module",
    "printer_integration_module",
)


@pytest.mark.parametrize("name", MODULES)
def test_module_imports_without_infrastructure(name: str) -> None:
    assert importlib.import_module(name).__name__ == name


def test_web_has_no_storage_service_dependency() -> None:
    path = Path(__file__).with_name("web_client_module.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            assert node.module != "file_storage_module"
        elif isinstance(node, ast.Import):
            assert all(alias.name != "file_storage_module" for alias in node.names)


def test_backend_api_adapters_expose_the_same_signatures() -> None:
    from inspect import isabstract, signature

    from backend_contracts import IBackendApi
    from backend_core_module import BackendApi
    from desktop_client_module import RestApiClient

    for adapter in (BackendApi, RestApiClient):
        assert not isabstract(adapter)
        for name in IBackendApi.__abstractmethods__:
            assert signature(getattr(adapter, name)) == signature(
                getattr(IBackendApi, name)
            )
