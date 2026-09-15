from pathlib import Path
from uuid import uuid4

import pytest


@pytest.fixture
def tmp_path(request):
    safe_name = "".join(
        character if character.isalnum() else "_"
        for character in request.node.name
    )
    path = Path(".test-tmp") / f"{safe_name}-{uuid4().hex}"
    path.mkdir(parents=True, exist_ok=False)
    return path
