import os
import subprocess
import sys
from time import sleep
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client_package.Client import Client

SAMPLE_PPTX = "Corona.pptx"


@pytest.mark.asyncio
async def test_system():
    """
    verify end-to-end functionality of the system:
        1_ start the web api and the explainer
        2_ start the clinet and connect to the web api
        3_upload a file
        2_check the status of the file twice
    """
    web_api = subprocess.Popen([sys.executable, "client_package/Web_API.py"])
    explainer = subprocess.Popen([sys.executable, "client_package/Explainer.py"])

    # ensure that the web_api and the explainer are running
    sleep(1)

    try:
        client = Client("http://127.0.0.1:5000")
        uid = client.upload(SAMPLE_PPTX)
        data = client.status(uid)  # this will not return the explanation
        assert data.is_pending() is True
        sleep(20)  # ensure that the explainer found and processed the data
        data = client.status(uid)  # this will return the explanation
        assert data.is_done() is True
    except Exception as e:
        assert False, f"Error: {e}"
    finally:
        web_api.terminate()
        explainer.terminate()


if __name__ == '__main__':
    pytest.main()
