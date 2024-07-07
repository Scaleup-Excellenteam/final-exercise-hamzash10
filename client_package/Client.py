from asyncio import sleep
from datetime import datetime

import requests
import Status


class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def upload(self, file_path, email=None):
        """
        this method uploads a file to the server and returns the UID.
        """
        upload_url = f"{self.base_url}/upload"
        try:
            with open(file_path, 'rb') as f:
                files = {'file': f}
                response = requests.post(upload_url, files=files, params={'email': email})
                response.raise_for_status()
                return response.json()['uid']
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP ERROR: {e}")
        except Exception as e:
            raise Exception(f"ERROR: {e}")

    def status(self, received_uid=None, email=None, filename=None):
        """
        using the received uid get the processed data if it exists
        :param received_uid:
        :return: Status object that contains the received data
        """
        status_url = f"{self.base_url}/status"
        params = {}
        if received_uid:
            params['uid'] = received_uid
        elif email and filename:
            params['email'] = email
            params['filename'] = filename
        else:
            raise ValueError("Either 'received_uid' or both 'email' and 'filename' must be provided.")
        try:
            response = requests.get(status_url, params=params)
            response.raise_for_status()
            data = response.json()
            return Status.Status(
                status=data['status'],
                filename=data['filename'],
                upload_time=data['upload_time'],
                finish_time=data['finish_time'],
                explanation=data.get('explanation')
            )
        except requests.exceptions.HTTPError as e:
            raise Exception(f"HTTP ERROR: {e}")
        except Exception as e:
            raise Exception(f"ERROR: {e}")