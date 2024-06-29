import os
import re
import subprocess
import sys
from time import sleep
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from client_package.Client import Client

SAMPLE_PPTX = "Corona.pptx"


@pytest.fixture(scope="module")
def start_services():
    """
    starting the web api and the explainer processes and terminate them after the tests
    """
    web_api = subprocess.Popen([sys.executable, "client_package/Web_API.py"])
    explainer = subprocess.Popen([sys.executable, "client_package/Explainer.py"])
    # make sure that processes are up and running
    sleep(2)
    yield
    # continue after the testes
    web_api.terminate()
    explainer.terminate()


@pytest.mark.asyncio
async def test_explainer_processes_new_files(start_services):
    """
    checks if the explainer process only newly uploaded files
    :param start_services:
    """
    client = Client("http://127.0.0.1:5000")
    # the number of files should be equal
    uploaded_files = os.listdir("uploads")
    output_files = os.listdir("outputs")
    assert len(uploaded_files) == len(output_files)

    # after uploading a file the number of files in the uploads folder should be bigger by 1 than the outputs folder
    uid = client.upload(SAMPLE_PPTX)
    uploaded_files = os.listdir("uploads")
    output_files = os.listdir("outputs")
    assert len(uploaded_files) - 1 == len(output_files)

    # the file that is just uploaded shouldn't be in the outputs folder yet
    files = os.listdir("outputs")
    matching_files = [f for f in files if re.search(f"{uid}", f)]
    assert len(matching_files) == 0

    # give time for the explainer to do it's work
    sleep(20)

    # after the explainer had time to work the number of files should be equal thus the explainer processed the new file
    uploaded_files = os.listdir("uploads")
    output_files = os.listdir("outputs")
    assert len(uploaded_files) == len(output_files)

    # check if the file that has benn processed is the correct one
    files = os.listdir("outputs")
    matching_files = [f for f in files if re.search(f"{uid}", f)]
    assert len(matching_files) == 1


@pytest.mark.asyncio
async def test_upload_returns_uid(start_services):
    """
    tests if the upload process returns uid
    :param start_services:
    """
    client = Client("http://127.0.0.1:5000")
    uid = client.upload(SAMPLE_PPTX)
    assert uid is not None


@pytest.mark.asyncio
async def test_upload_creates_file_with_uid(start_services):
    """
    tests if the upload process creates a file with the correct uid in uploads folder
    :param start_services:
    """
    client = Client("http://127.0.0.1:5000")
    uid = client.upload(SAMPLE_PPTX)
    # find a file that contains the uid in the uploads
    files = os.listdir("uploads")
    # checks if there is a file that contains uid
    matching_files = [f for f in files if re.search(f"{uid}", f)]
    assert len(matching_files) == 1


@pytest.mark.asyncio
async def test_client_raises_error_for_invalid_uid(start_services):
    """
    test if the client raises an error when uid is invalid
    :param start_services:
    :return:
    """
    client = Client("http://127.0.0.1:5000")
    invalid_uid = "this will raise an exception"
    with pytest.raises(Exception):
        client.status(invalid_uid)


@pytest.mark.asyncio
async def test_status_returns_pending_after_upload(start_services):
    """
    tests if the status returns pending immediately after upload
    :param start_services:
    :return:
    """
    client = Client("http://127.0.0.1:5000")
    uid = client.upload(SAMPLE_PPTX)
    data = client.status(uid)
    assert data.is_pending() is True


@pytest.mark.asyncio
async def test_end_to_end_system():
    """
    verify end-to-end functionality of the system
    """

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


if __name__ == '__main__':
    # Run pytest with arguments as if running from command line
    exit_code = pytest.main(["-v", "--tb=short"])  # Adjust arguments as needed

    # Check the exit code to determine success or failure
    if exit_code == 0:
        print("All tests passed!")
    else:
        print(f"Tests failed with exit code: {exit_code}")
