import json
import logging

import requests

logger = logging.getLogger(__name__)


class Client:
    def __init__(self, base_url):
        self.base_url = base_url

    def send_message(self, message):
        r = requests.post(f'http://{self.base_url}/message', data=json.dumps({'message': message}))
        logger.info(r.text)


if __name__ == '__main__':
    client = Client('localhost:9000')
    client.send_message('test')
