import os
import pytest
from main import main


@pytest.mark.asyncio
async def test_system():
    await main()
    assert os.path.exists("Corona.json"), "Output JSON file does not exist."


if __name__ == '__main__':
    pytest.main()
