from datetime import datetime
from time import sleep

import requests
import Status


class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path):
        """
        this method uploads a file to the server and returns the UID.
        """
        upload_url = f"{self.base_url}/upload"
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(upload_url, files=files)
                response.raise_for_status()
                return response.json()['uid']
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP ERROR: {e}")
        except Exception as e:
            raise Exception(f"ERROR: {e}")

    def status(self, received_uid):
        """
        using the received uid get the processed data if it exists
        :param received_uid:
        :return: Status object that contains the received data
        """
        status_url = f"{self.base_url}/status"
        params = {'uid': received_uid}
        try:
            response = requests.get(status_url, params=params)
            response.raise_for_status()
            data = response.json()
            return Status.Status(
                status=data['status'],
                filename=data['filename'],
                timestamp=datetime.fromtimestamp(int(data['timestamp'])),
                explanation=data.get('explanation')
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP ERROR: {e}")
        except Exception as e:
            raise Exception(f"ERROR: {e}")

