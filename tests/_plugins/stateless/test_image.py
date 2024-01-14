# Copyright 2023 Marimo. All rights reserved.
from marimo._plugins.stateless.image import image
from marimo._runtime.context import get_context
from marimo._runtime.runtime import Kernel
from tests.conftest import ExecReqProvider
import tempfile


def test_image() -> None:
    result = image(
        "https://marimo.io/logo.png",
    )
    assert result.text == "<img src='https://marimo.io/logo.png' />"


def test_image_bytes_io(k: Kernel, exec_req: ExecReqProvider) -> None:
    k.run(
        [
            exec_req.get(
                """
                import io
                import marimo as mo
                bytestream = io.BytesIO(b"hello")
                image = mo.image(bytestream)
                """
            ),
        ]
    )
    assert len(get_context().virtual_file_registry.registry) == 1
    for fname, _ in get_context().virtual_file_registry.registry.items():
        assert fname.endswith(".png")


def test_image_bytes(k: Kernel, exec_req: ExecReqProvider) -> None:
    k.run(
        [
            exec_req.get(
                """
                import io
                import marimo as mo
                bytestream = io.BytesIO(b"hello")
                image = mo.image(bytestream)
                """
            ),
        ]
    )
    assert len(get_context().virtual_file_registry.registry) == 1
    for fname, _ in get_context().virtual_file_registry.registry.items():
        assert fname.endswith(".png")


def test_image_str(k: Kernel, exec_req: ExecReqProvider) -> None:
    k.run(
        [
            exec_req.get(
                """
                import marimo as mo
                image = mo.image("https://marimo.io/logo.png")
                """
            ),
        ]
    )
    assert len(get_context().virtual_file_registry.registry) == 0


def test_image_local_file(k: Kernel, exec_req: ExecReqProvider) -> None:
    with tempfile.NamedTemporaryFile(suffix=".jpg") as tmp:
        tmp.write(b"hello")
        tmp.seek(0)
        k.run(
            [
                exec_req.get(
                    f"""
                    import marimo as mo
                    image = mo.image('{tmp.name}')
                    """
                ),
            ]
        )
        assert len(get_context().virtual_file_registry.registry) == 1
