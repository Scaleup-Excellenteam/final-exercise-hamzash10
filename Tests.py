import os
import pytest
from main import main
import sys

@pytest.mark.asyncio
async def test_system():
    # default command line arguments
    sys.argv = ['Tests.py', 'Corona.pptx']
    await main()
    assert os.path.exists("Corona.json"), "Output JSON file does not exist."


if __name__ == '__main__':
    pytest.main()
