import asyncio
from time import sleep

import Client

def main():
    # client
    client = Client.Client("http://127.0.0.1:5000")
    uid = client.upload("Corona.pptx", "hamzash@gmail.com")
    print(client.status(email="hamzash@gmail.com",filename="Corona.pptx"))


if __name__ == '__main__':
    main()
